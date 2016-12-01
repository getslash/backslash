import threading

from sqlalchemy import func, exists
from ..models import Test, TestInformation, User, Session, Subject, RelatedEntity, session_subject, db, SubjectInstance
from .computed_search_field import Either
from . import value_parsers

_current = threading.local()


def get_current_logic():
    return _current.logic


class SearchContext(object):

    def resolve_model_field(self, field_name):
        raise NotImplementedError()  # pragma: no cover

    def resolve_value(self, field_name, value): # pylint: disable=unused-argument
        return value

    def get_base_query(self):
        raise NotImplementedError() # pragma: no cover

    def get_fallback_filter(self, search_term):
        raise NotImplementedError() # pragma: no cover

    def __enter__(self):
        _current.logic = self
        return self

    def __exit__(self, *_):
        _current.logic = None

    @classmethod
    def get_for_type(cls, objtype):
        if objtype is Test or (isinstance(objtype, str) and objtype.lower() == 'test'):
            return TestSearchContext()
        raise NotImplementedError() # pragma: no cover


_TEST_SPECIAL_SEARCH_FIELDS = {
    'name': TestInformation.name,
    'file': TestInformation.file_name,
    'class': TestInformation.class_name,
    'user': Either([User.email, User.first_name, User.last_name]),
    'status': func.lower(Test.status),
}

_TEST_VALUE_PARSERS = {
    'start_time': value_parsers.parse_date,
    'end_time': value_parsers.parse_date,
}

class TestSearchContext(SearchContext):

    def resolve_model_field(self, field_name):

        returned = _TEST_SPECIAL_SEARCH_FIELDS.get(field_name)
        if returned is not None:
            return returned

        return getattr(Test, field_name, None)

    def resolve_value(self, field_name, value):
        parser = _TEST_VALUE_PARSERS.get(field_name)
        if parser is not None:
            return parser(value)
        return super(TestSearchContext, self).resolve_value(field_name, value)

    def get_base_query(self):
        return Test.query\
                   .join(Session, Session.id == Test.session_id)\
                   .join(User, Session.user_id == User.id)\
                   .join(TestInformation)

    def get_fallback_filter(self, term):
        return TestInformation.name.contains(term)


def with_(entity_name):
    return _get_related_entity_query(entity_name) | _get_subject_query(entity_name)


def without_(entity_name):
    return (~_get_related_entity_query(entity_name)) & (~_get_subject_query(entity_name))


def _get_related_entity_query(entity_name):
    return Session.related_entities.any(RelatedEntity.name == entity_name)

def _get_subject_query(entity_name):
    return db.session.query(session_subject).join(SubjectInstance).join(Subject).filter(session_subject.c.session_id == Test.session_id, Subject.name == entity_name).correlate(Test).exists()
