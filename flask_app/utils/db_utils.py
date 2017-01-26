from .. import models
import sqlalchemy.types
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.functions import GenericFunction

from contextlib import contextmanager


def get_or_create(model, **kwargs):
    try:
        returned = model.query.filter_by(**kwargs).one()
    except NoResultFound:
        returned = model(**kwargs)
        models.db.session.add(returned)
        models.db.session.flush()
        models.db.session.commit()
    return returned


@contextmanager
def statement_timeout_context(timeout_seconds=20):
    prev = models.db.session.execute('show statement_timeout').scalar()
    assert prev
    models.db.session.execute('SET statement_timeout={}'.format(timeout_seconds * 1000))
    yield
    models.db.session.execute('SET statement_timeout={}'.format(prev))


class json_object_agg(GenericFunction):
    type = sqlalchemy.types.JSON

    name = identifier = 'json_object_agg'
