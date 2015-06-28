from .. import models
from sqlalchemy.orm.exc import NoResultFound


def get_or_create(model, **kwargs):
    try:
        returned = model.query.filter_by(**kwargs).one()
    except NoResultFound:
        returned = model(**kwargs)
        models.db.session.add(returned)
        models.db.session.commit()
    return returned
