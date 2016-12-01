from sqlalchemy.dialects.postgresql import insert
from flask_simple_api import error_abort
from ...models import Label, Session, Test, db, session_label

from .blueprint import API

NoneType = type(None)


@API
def add_label(label: str, session_id: int):
    session = Session.query.get_or_404(session_id)

    db.session.execute(insert(Label).values(name=label).on_conflict_do_nothing())
    db.session.commit()

    session.labels.append(Label.query.filter_by(name=label).one())
    db.session.add(session)
    db.session.commit()


@API
def remove_label(label: str, session_id: int):

    db.session.execute(
        session_label.delete().where(
            (session_label.c.session_id == session_id) &
            session_label.c.label_id.in_(
                db.session.query(Label.id).filter(Label.name == label))))
    db.session.commit()
