import threading

from sqlalchemy import func, exists
from ..models import Test, TestInformation, User, Session, Subject, Entity, session_subject, db, SubjectInstance, session_label, Label, session_entity
from .computed_search_field import Either, FunctionComputedField
from . import value_parsers

_current = threading.local()


def get_current_logic():
    return _current.logic


class SearchContext(object):

    CUSTOM_FIELDS = {}
    VALUE_PARSERS = {}
    MODEL = None

    def resolve_model_field(self, field_name):
        returned = self.CUSTOM_FIELDS.get(field_name)
        if returned is not None:
            return returned

        return getattr(self.MODEL, field_name, None)

    def resolve_value(self, field_name, value): # pylint: disable=unused-argument
        parser = self.VALUE_PARSERS.get(field_name)
        if parser is not None:
            return parser(value)
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
        if objtype is Session or (isinstance(objtype, str) and objtype.lower() == 'session'):
            return SessionSearchContext()
        raise NotImplementedError() # pragma: no cover

_COMMON_FIELDS = {
    'user': Either([User.email, func.lower(User.first_name), func.lower(User.last_name)]),
}


class TestSearchContext(SearchContext):

    MODEL = Test

    VALUE_PARSERS = {
        'start_time': value_parsers.parse_date,
        'end_time': value_parsers.parse_date,
    }

    CUSTOM_FIELDS = {
        'name': TestInformation.name,
        'file': TestInformation.file_name,
        'class': TestInformation.class_name,
        'status': func.lower(Test.status),
        **_COMMON_FIELDS,
    }


    def get_base_query(self):
        return Test.query\
                   .join(Session, Session.id == Test.session_id)\
                   .join(User, Session.user_id == User.id)\
                   .join(TestInformation)

    def get_fallback_filter(self, term):
        return TestInformation.name.contains(term)

def has_label(_, label):
    return db.session.query(session_label).join(Label).filter((session_label.c.session_id == Session.id) & (Label.name == label)).exists().correlate(Session)


class SessionSearchContext(SearchContext):

    VALUE_PARSERS = {
        'start_time': value_parsers.parse_date,
        'end_time': value_parsers.parse_date,
    }

    CUSTOM_FIELDS = {
        'label': FunctionComputedField(has_label),
        **_COMMON_FIELDS,
    }

    MODEL = Session


    def get_base_query(self):
        return Session.query\
                   .join(User, Session.user_id == User.id)

    def get_fallback_filter(self, term):
        return TestInformation.name.contains(term)



def with_(entity_name):
    returned = db.session.query(session_entity).join(Entity).filter(
        (session_entity.c.session_id == Test.session_id) & (Entity.name == entity_name)).exists().correlate(Test)
    returned |= db.session.query(session_subject).join(SubjectInstance).join(Subject).filter(
        (session_subject.c.session_id == Test.session_id) &
        (Subject.name == entity_name)).exists().correlate(Test)

    return returned
