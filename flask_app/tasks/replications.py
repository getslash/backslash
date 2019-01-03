from elasticsearch import helpers as es_helpers
from flask import current_app
import flux
import logbook
from .main import queue, needs_app_context
from .. import models
import sqlalchemy
from sqlalchemy import select, or_, and_, func, text
from sqlalchemy.sql.expression import label, cast
import traceback
from ..utils import statuses
from .maintenance import reliable_task



_logger = logbook.Logger(__name__)

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
        if reconfigure:
            _reconfigure_replica(replica)
        _estimate_replication(replica)
        start_time = replica.last_chunk_finished or flux.current_timeline.time()

        query = _get_tests_to_replicate_query(replica)
        results = [_serialize_test(test, replica) for test in models.db.session.execute(query)]
        client = replica.get_client()


        num_replicated, _ = es_helpers.bulk(client, results)
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


_REPLICATION_TEST_FILTER = func.lower(models.Test.status).notin_([
    statuses.PLANNED.lower(),
    statuses.DISTRIBUTED.lower()
])


def _estimate_replication(replica):
    if replica.backlog_remaining is None:
        replica.backlog_remaining = models.Test.query.filter(_REPLICATION_TEST_FILTER).count()


def _get_tests_to_replicate_query(replica, bulk_size=200):

    session_entities_query = select([
       models.session_entity.c.session_id, models.session_entity.c.entity_id
    ]).where(models.session_entity.c.session_id == models.Test.session_id).distinct().correlate(models.Test).alias()

    test_entities_query = select([
       models.test_entity.c.test_id, models.test_entity.c.entity_id
    ]).where(models.test_entity.c.test_id == models.Test.id).distinct().correlate(models.Test).alias()

    query = select([
        label("_type", text("'test'")),
        label("_index", text("'backslash'")),
        label("_id", models.Test.id),

        *[getattr(models.Test, column_name)
         for column_name in models.Test.__table__.columns.keys()
         if column_name not in {'timespan', 'parameters'}],

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
    ).where(_REPLICATION_TEST_FILTER)

    if replica.untimed_done:
        if replica.last_replicated_timestamp is not None:
            query = query.where(or_(
                models.Test.updated_at > replica.last_replicated_timestamp,
                and_(
                    models.Test.updated_at == replica.last_replicated_timestamp,
                    models.Test.id > replica.last_replicated_id,
                )))
        query = query.order_by(models.Test.updated_at.asc(), models.Test.id.asc())
    else:
        query = query.where(models.Test.updated_at == None)
        if replica.last_replicated_id is not None:
            query = query.where(
                models.Test.id > replica.last_replicated_id)
        query = query.order_by(models.Test.id.asc())
    return query.limit(bulk_size)

_ES_MAX_STRING_LENGTH = 10000

def _reconfigure_replica(replica):
    client = replica.get_client()
    client.indices.create(index=replica.index_name, ignore=400)
    client.indices.put_settings(
        index=replica.index_name,
        body={
            "index.mapping.total_fields.limit": 5000,
            })
    client.indices.put_mapping(
        index=replica.index_name,
        doc_type='test',
        body={
            'properties': _get_properties_definitions()
        })

    client.indices.put_mapping(
        index=replica.index_name,
        doc_type='test',
        body={
            "dynamic_templates": [
                {
                    "strings": {
                        "match_mapping_type": "string",
                        "mapping": {
                            "type": "text",
                            "ignore_above": str(_ES_MAX_STRING_LENGTH),
                            }}}]})



def _get_properties_definitions():
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


def _serialize_test(test, replication):
    test = dict(test.items())
    _stringify_fields(test)
    _truncate(test)
    test['_index'] = replication.index_name
    return test


def _truncate(test_dict, max_length=_ES_MAX_STRING_LENGTH):
    for key, value in test_dict.items():
        if isinstance(value, dict):
            _truncate(value)
        elif isinstance(value, str) and len(value) > max_length:
            test_dict[key] = value[:max_length-3] + '...'


def _stringify_fields(test):
    for field_name in ("test_metadata", "session_metadata"):
        field = test.get(field_name)
        if isinstance(field, dict):
            for key in list(field):
                field[key] = str(field[key])
