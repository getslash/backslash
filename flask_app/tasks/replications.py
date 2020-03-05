from elasticsearch import helpers as es_helpers
from elasticsearch import Elasticsearch
from flask import current_app
import flux
import logbook
from .main import needs_app_context
from .. import models
import sqlalchemy
from sqlalchemy import select, or_, and_, func, text
from sqlalchemy.sql.expression import label, cast
import traceback
from ..utils import statuses, get_current_time
from .maintenance import reliable_task



_logger = logbook.Logger(__name__)
_ES_MAX_STRING_LENGTH = 10000

class ElasticsearchIndex(object):
    def __init__(self, replica):
        self._replica = replica
        self._client = Elasticsearch([self._replica.url])

    def get_model(self):
        raise NotImplementedError()

    def get_filter(self):
        raise NotImplementedError()

    def _get_properties_definitions(self):
        raise NotImplementedError()

    def get_client(self):
        return self._client

    def estimate_time_left(self):
        if self._replica.backlog_remaining is None:
            self._replica.backlog_remaining = self.get_model().query.filter(self.get_filter()).count()

    def reconfigure(self):
        client = self.get_client()
        client.indices.create(index=self._replica.index_name, ignore=400)
        client.indices.put_settings(
            index=self._replica.index_name,
            body={
                "index.mapping.total_fields.limit": 5000,
                })
        client.indices.put_mapping(
            index=self._replica.index_name,
            doc_type=self._doc_type,
            body={
                'properties': self._get_properties_definitions()
            })

        client.indices.put_mapping(
            index=self._replica.index_name,
            doc_type=self._doc_type,
            body={
                "dynamic_templates": [
                    {
                        "strings": {
                            "match_mapping_type": "string",
                            "mapping": {
                                "type": "text",
                                "ignore_above": str(_ES_MAX_STRING_LENGTH),
                                }}}]})


    def get_fields_to_stringify(self):
        return []

    def _stringify_fields(self, result):
        for field_name in self.get_fields_to_stringify():
            field = result.get(field_name)
            if isinstance(field, dict):
                for key in list(field):
                    field[key] = str(field[key])

    def _truncate(self, result_dict, max_length=_ES_MAX_STRING_LENGTH):
        for key, value in result_dict.items():
            if isinstance(value, dict):
                self._truncate(value)
            elif isinstance(value, str) and len(value) > max_length:
                result_dict[key] = value[:max_length-3] + '...'

    def handle_result(self, result):
        result = dict(result.items())
        self._stringify_fields(result)
        self._truncate(result)
        result['_index'] = self._replica.index_name
        self.enrich_result(result)
        return result

    def enrich_result(self, result):
        pass


class TestIndex(ElasticsearchIndex):
    def __init__(self, replica):
        super(TestIndex, self).__init__(replica)
        self._doc_type = 'test'

    def get_model(self):
        return models.Test

    def get_filter(self):
        return func.lower(models.Test.status).notin_([
            statuses.PLANNED.lower(),
            statuses.DISTRIBUTED.lower()
        ])

    def _get_properties_definitions(self):
        returned = {}

        for datetime_field in ['start_time', 'end_time']:
            returned[datetime_field] = {
                "type":   "date",
                "format": "epoch_second"
            }

        for keyword_field in [
                'file_hash',
                'logical_id',
                'scm_revision',
                'status',
                'status',
                'subjects.name',
                'test.class_name',
                'test.file_name',
                'test.name',
                'user_email',
        ]:
            returned[keyword_field] = {
                "type": "keyword",
            }

        return returned

    def get_fields_query(self):
        session_entities_query = select([
           models.session_entity.c.session_id, models.session_entity.c.entity_id
        ]).where(models.session_entity.c.session_id == models.Test.session_id).distinct().correlate(models.Test).alias()

        test_entities_query = select([
           models.test_entity.c.test_id, models.test_entity.c.entity_id
        ]).where(models.test_entity.c.test_id == models.Test.id).distinct().correlate(models.Test).alias()

        return select([
            label("_type", text("'test'")),
            label("_index", text("'test'")),
            label("_id", models.Test.id),

            *[getattr(models.Test, column_name)
             for column_name in models.Test.__table__.columns.keys()
             if column_name not in {'timespan', 'parameters'}],
            models.Session.logical_id.label('session_logical_id'),
            models.User.email.label('user_email'),
            cast(models.Test.parameters, sqlalchemy.Text).label('parameters'),
            func.json_build_object(
                "file_name",
                models.TestInformation.file_name,
                "class_name",
                models.TestInformation.class_name,
                "name",
                models.TestInformation.name,
                "variation",
                cast(models.TestVariation.variation, sqlalchemy.Text),
            ).label('test'),
            select([func.array_agg(
                func.json_build_object(
                    'timestamp', models.Error.timestamp,
                    'message', models.Error.message)
            )]).where(models.Error.test_id == models.Test.id).label('errors'),
            select([func.array_agg(
                func.json_build_object(
                    'timestamp', models.Warning.timestamp,
                    'message', models.Warning.message)
            )]).where(models.Warning.test_id == models.Test.id).label('warnings'),
            select([
                func.json_object_agg(models.SessionMetadata.key,
                                     models.SessionMetadata.metadata_item).label('session_metadata')
            ]).where(models.SessionMetadata.session_id == models.Test.session_id).label('session_metadata'),
            select([
                func.json_object_agg(models.TestMetadata.key,
                                     models.TestMetadata.metadata_item)
            ]).where(models.TestMetadata.test_id == models.Test.id).label('test_metadata'),
            select([
                func.array_agg(
                    func.json_build_object(
                        "name",
                        models.Entity.name,
                        "type",
                        models.Entity.type,
                    )
                )
            ]).select_from(session_entities_query.join(models.Entity, models.Entity.id == session_entities_query.c.entity_id)).label('session_entities'),
            select([
                func.array_agg(
                    func.json_build_object(
                        "name",
                        models.Entity.name,
                        "type",
                        models.Entity.type,
                    )
                )
            ]).select_from(test_entities_query.join(models.Entity, models.Entity.id == test_entities_query.c.entity_id)).label('test_entities'),
            select([
                func.array_agg(
                    func.json_build_object(
                        "name", models.Subject.name,
                        "product", models.Product.name,
                        "version", models.ProductVersion.version,
                        "revision", models.ProductRevision.revision,
                    )
                )
            ]).select_from(
                models.session_subject
                .join(models.SubjectInstance)
                .join(models.Subject)
                .join(models.ProductRevision)
                .join(models.ProductVersion)
                .join(models.Product)
            ).where(models.session_subject.c.session_id == models.Test.session_id).label('subjects'),
        ]).select_from(
            models.Test.__table__.join(models.Session.__table__)
            .outerjoin(models.User.__table__, models.Session.user_id == models.User.id)
            .outerjoin(models.TestInformation)
            .outerjoin(models.TestVariation)
        )

    def get_fields_to_stringify(self):
        return ("test_metadata", "session_metadata")

class SessionIndex(ElasticsearchIndex):
    def __init__(self, replica):
        super(SessionIndex, self).__init__(replica)
        self._doc_type = 'session'

    def get_model(self):
        return models.Session

    def get_filter(self):
        return True

    def get_fields_query(self):
        labels_query = select([
           models.session_label.c.session_id, models.session_label.c.label_id
        ]).where(models.session_label.c.session_id == models.Session.id).distinct().correlate(models.Session).alias()
        return select([
            label("_type", text("'session'")),
            label("_index", text("'session'")),
            label("_id", models.Session.id),

            *[getattr(models.Session, column_name)
             for column_name in models.Session.__table__.columns.keys()
             if column_name not in {'timespan', 'parameters'}],
             models.User.email.label('user_email'),
             select([func.array_agg(
                 func.json_build_object(
                     'timestamp', models.Error.timestamp,
                     'message', models.Error.message)
             )]).where(models.Error.session_id == models.Session.id).label('session_errors'),
            select([
                func.array_agg(
                    func.json_build_object(
                        "name", models.Subject.name,
                        "product", models.Product.name,
                        "version", models.ProductVersion.version,
                        "revision", models.ProductRevision.revision,
                    )
                )
            ]).select_from(
                models.session_subject
                    .join(models.SubjectInstance)
                    .join(models.Subject)
                    .join(models.ProductRevision)
                    .join(models.ProductVersion)
                    .join(models.Product)
            ).where(models.session_subject.c.session_id == models.Session.id).label('subjects'),
            select([func.array_agg(
                func.json_build_object(
                    'timestamp', models.Warning.timestamp,
                    'message', models.Warning.message)
            )]).where(models.Warning.session_id == models.Session.id).label('session_warnings'),
            select([
                func.array_agg(
                    func.json_build_object(
                        "name",
                        models.Label.name
                    )
                )
            ]).select_from(labels_query.join(models.Label, models.Label.id == labels_query.c.label_id)).label('session_labels'),
            select([
                func.json_object_agg(models.SessionMetadata.key,
                                     models.SessionMetadata.metadata_item)
            ]).where(models.SessionMetadata.session_id == models.Session.id).label('session_metadata'),
        ]).select_from(models.Session.__table__.outerjoin(models.User.__table__, models.Session.user_id == models.User.id))

    def _get_properties_definitions(self):
        returned = {}

        for datetime_field in ['start_time', 'end_time']:
            returned[datetime_field] = {
                "type":   "date",
                "format": "epoch_second"
            }

        for keyword_field in [
                'logical_id',
                'status',
                'user_email',
        ]:
            returned[keyword_field] = {
                "type": "keyword",
            }

        return returned

    def enrich_result(self, result):
        next_keepalive = result.get('next_keepalive')
        result['is_abandoned'] = not (result.get('end_time') or next_keepalive is None or next_keepalive > get_current_time())

    def get_fields_to_stringify(self):
        return ("session_metadata",)

def get_next_bulk_query(query, replica, es_index):
    query = query.where(es_index.get_filter())

    if replica.untimed_done:
        if replica.last_replicated_timestamp is not None:
            query = query.where(or_(
                es_index.get_model().updated_at > replica.last_replicated_timestamp,
                and_(
                    es_index.get_model().updated_at == replica.last_replicated_timestamp,
                    es_index.get_model().id > replica.last_replicated_id,
                )))
        query = query.order_by(es_index.get_model().updated_at.asc(), es_index.get_model().id.asc())
    else:
        query = query.where(es_index.get_model().updated_at == None)
        if replica.last_replicated_id is not None:
            query = query.where(
                es_index.get_model().id > replica.last_replicated_id)
        query = query.order_by(es_index.get_model().id.asc())
    return query.limit(200)

def index_from_replica(replica):
    if replica.index_name == "test":
        return TestIndex(replica)
    elif replica.index_name == "session":
        return SessionIndex(replica)

@reliable_task
@needs_app_context
def do_elasticsearch_replication(replica_id=None, reconfigure=True):
    if replica_id is None:
        for replica in models.Replication.query.all():
            do_elasticsearch_replication.apply_async((replica.id,))
        return

    replica = models.Replication.query.get(replica_id)
    if replica is None:
        _logger.debug(f'Replica {replica_id} already deleted. Not doing anything')
        return
    if replica.paused:
        _logger.debug(f'Replica {replica_id} is paused')
        return
    sleep_time = 60
    results = None
    try:
        es_index = index_from_replica(replica)
        if not es_index:
            return
        if reconfigure:
            es_index.reconfigure()
        es_index.estimate_time_left()
        start_time = replica.last_chunk_finished or flux.current_timeline.time()

        results = [es_index.handle_result(result) \
                   for result in models.db.session.execute(get_next_bulk_query(es_index.get_fields_query(), replica, es_index))]
        num_replicated, _ = es_helpers.bulk(es_index.get_client(), results)
        end_time = flux.current_timeline.time()
        replica.avg_per_second = num_replicated / (end_time - start_time)

        if not replica.untimed_done and num_replicated == 0:
            replica.untimed_done = True

        if results:
            replica.last_replicated_id = results[-1]['id']
            if results[-1]['updated_at'] is not None:
                replica.last_replicated_timestamp = results[-1]['updated_at']
            replica.backlog_remaining = max(0, replica.backlog_remaining - num_replicated)
        else:
            replica.backlog_remaining = 0

    except Exception: # pylint: disable=broad-except
        _logger.error('Error during migration', exc_info=True)
        replica.last_error = traceback.format_exc()
        if 'sentry' in current_app.extensions:
            current_app.extensions['sentry'].captureException()
    else:
        replica.last_error = None
        replica.last_chunk_finished = flux.current_timeline.time()
        if results:
            sleep_time = 1

    models.db.session.commit()
    if replica.last_error is None:
        do_elasticsearch_replication.apply_async((replica_id,), {'reconfigure': False},
                                                 countdown=sleep_time)
