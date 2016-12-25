import requests

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from flask import abort

from flask_simple_api import error_abort

from ...models import Session, Test, db, SessionMetadata, TestMetadata
from .blueprint import API


@API
def set_metadata(entity_type: str, entity_id: int, key: str, value: object):
    _set_metadata_dict(entity_type=entity_type,
                       entity_id=entity_id, metadata={key: value})


@API
def set_metadata_dict(entity_type: str, entity_id: int, metadata: dict):
    _set_metadata_dict(entity_type=entity_type,
                       entity_id=entity_id, metadata=metadata)


def _set_metadata_dict(*, entity_type, entity_id, metadata, commit=True):
    model = _get_metadata_model(entity_type)
    for key, value in metadata.items():
        db.session.add(model(key=key, metadata_item=value, **
                             {'{}_id'.format(entity_type): entity_id}))

    if commit:
        try:
            db.session.commit()
        except IntegrityError:
            abort(requests.codes.not_found)


@API(require_login=False)
def get_metadata(entity_type: str, entity_id: (int, str)):
    if entity_type not in {'session', 'test'}:
        error_abort('Invalid entity type', requests.codes.bad_request)
    query = text(('select json_object_agg(key, metadata_item)'
                  ' from {0}_metadata'
                  ' where {0}_id = :entity_id group by {0}_id').format(entity_type))
    return db.session.execute(query, {'entity_id': entity_id}).scalar()


def _get_metadata_model(entity_type):
    if entity_type == 'session':
        return SessionMetadata

    if entity_type == 'test':
        return TestMetadata

    error_abort('Unknown entity type')


@API
def add_test_metadata(id: int, metadata: dict):
    try:
        test = Test.query.filter(Test.id == id).one()
        test.metadata_objects.append(TestMetadata(metadata_item=metadata))
    except NoResultFound:
        abort(requests.codes.not_found)
    db.session.commit()


@API
def add_session_metadata(id: int, metadata: dict):
    try:
        session = Session.query.filter(Session.id == id).one()
        session.metadata_objects.append(
            SessionMetadata(metadata_item=metadata))
    except NoResultFound:
        abort(requests.codes.not_found)
    db.session.commit()
