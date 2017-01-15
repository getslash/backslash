import threading
import operator

from sqlalchemy import func
from ..models import Test, TestInformation, User, Session, db, session_label, Label, session_subject, SubjectInstance, Subject, Entity, session_entity, ProductVersion, ProductRevision
from . import value_parsers
from .exceptions import UnknownField
from .helpers import only_ops

_current = threading.local()


def get_current_logic():
    return _current.logic


class SearchContext(object):

    SEARCHABLE_FIELDS = {
    }
    MODEL = None

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

    def search__start_time(self, op, value):
        return self._search_time_field(self.MODEL.start_time, op, value)

    def search__end_time(self, op, value):
        return self._search_time_field(self.MODEL.end_time, op, value)

    @only_ops(['='])
    def search__at(self, op, value): # pylint: disable=unused-argument
        value = value_parsers.parse_date(value)
        return (self.MODEL.end_time >= value) & (self.MODEL.start_time <= value)

    def _search_time_field(self, field, op, value):
        return op.func(field, value_parsers.parse_date(value))

    @only_ops(['=', '!=', '~'])
    def search__user(self, op, value): # pylint: disable=unused-argument
        search_func = op.func if op.op != '!=' else operator.eq
        user_ids = db.session.query(User.id).filter(search_func(func.lower(User.first_name), value) | search_func(func.lower(User.last_name), value) | search_func(User.email, value)).all()
        if not user_ids:
            return op.op == '!='
        returned = Session.user_id.in_(user_ids)
        if op.op == '!=':
            returned = ~returned
        return returned

    def resolve_search_clause(self, lhs, op, rhs):
        field = self.SEARCHABLE_FIELDS.get(lhs)
        if field is True:
            field = getattr(self.MODEL, lhs)

        if field is not None:
            return op.func(field, rhs)

        method = getattr(self, 'search__{}'.format(lhs), None)
        if method is not None:
            return method(op, rhs)

        raise UnknownField(lhs)


class TestSearchContext(SearchContext):

    MODEL = Test

    SEARCHABLE_FIELDS = {
        'id': True,
        'name': TestInformation.name,
        'file': TestInformation.file_name,
        'class': TestInformation.class_name,
        'status': func.lower(Test.status),
    }


    def get_base_query(self):
        return (Test.query
                .join(Session)
                .join(TestInformation)
                .join(User, User.id == Session.user_id))

    def get_fallback_filter(self, term):
        return TestInformation.name.contains(term)

    @only_ops(['=', '!='])
    def search__subject(self, op, value): # pylint: disable=unused-argument
        subject_id = db.session.query(Subject.id).filter(Subject.name == value).first()
        if subject_id is None:
            return op.op == '!='
        query = Session.id.in_(db.session.query(session_subject.c.session_id).distinct(session_subject.c.session_id).join(SubjectInstance).filter(SubjectInstance.subject_id == subject_id))
        if op.op == '!=':
            query = ~query
        return query


    @only_ops(['=', '!='])
    def search__related(self, op, value): # pylint: disable=unused-argument
        entity = Entity.query.filter(Entity.name == value).first()
        if not entity:
            return op.op == '!='
        subquery = db.session.query(session_entity).filter_by(entity_id=entity.id, session_id=Test.session_id).exists().correlate(Test)
        if op.op == '!=':
            subquery = ~subquery
        return subquery

    @only_ops(['=', '!='])
    def search__product_version(self, op, value):
        subquery = db.session.query(session_subject).join(SubjectInstance).join(ProductRevision).join(ProductVersion).filter(ProductVersion.version == value, session_subject.c.session_id == Test.session_id).exists().correlate(Test)
        if op.op == '!=':
            subquery = ~subquery
        return subquery



class SessionSearchContext(SearchContext):

    SEARCHABLE_FIELDS = {
        'id': True,
    }

    MODEL = Session

    @only_ops(['='])
    def search__label(self, op, value): # pylint: disable=unused-argument
        return db.session.query(session_label).join(Label).filter((session_label.c.session_id == Session.id) & (Label.name == value)).exists().correlate(Session)


    def get_base_query(self):
        return Session.query.join(User, Session.user_id == User.id)

    def get_fallback_filter(self, term):
        return TestInformation.name.contains(term)

    @only_ops(['=', '!='])
    def search__subject(self, op, value): # pylint: disable=unused-argument
        subquery = db.session.query(session_subject).join(SubjectInstance).join(Subject).filter(
            Subject.name == value, session_subject.c.session_id == Session.id).exists().correlate(Session)
        if op.op == '!=':
            subquery = ~subquery
        return subquery

    @only_ops(['=', '!='])
    def search__related(self, op, value): # pylint: disable=unused-argument
        entity = Entity.query.filter(Entity.name == value).first()
        if not entity:
            return op.op == '!='
        subquery = db.session.query(session_entity).filter_by(entity_id=entity.id, session_id=Session.id).exists().correlate(Session)
        if op.op == '!=':
            subquery = ~subquery
        return subquery

    @only_ops(['=', '!='])
    def search__product_version(self, op, value):
        subquery = db.session.query(session_subject).join(SubjectInstance).join(ProductRevision).join(ProductVersion).filter(ProductVersion.version == value, session_subject.c.session_id == Session.id).exists().correlate(Session)
        if op.op == '!=':
            subquery = ~subquery
        return subquery
