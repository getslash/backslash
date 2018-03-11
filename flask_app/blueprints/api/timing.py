import flux
import requests
from ...models import Timing, db
from ...utils.db_utils import json_object_agg
from .blueprint import API
from flask_simple_api import error_abort
from sqlalchemy import and_, case, func
from sqlalchemy.exc import IntegrityError

NoneType = type(None)


@API
def report_timing_start(name: str, session_id: int, test_id: (int, NoneType)=None):  # pylint: disable=bad-whitespace
    interval = -flux.current_timeline.time()
    try:
        db.session.execute(
            Timing.__table__.insert().values(
                session_id=session_id, test_id=test_id, name=name, total=interval))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        res = db.session.execute(
            Timing.__table__.update()
            .values(total=Timing.total+interval)
            .where(and_(Timing.session_id==session_id, Timing.test_id==test_id, Timing.name==name, Timing.total >= 0)))
        if res.rowcount != 1:
            error_abort('Attempted to start measurement on an already started metric', code=requests.codes.conflict) # pylint: disable=no-member, line-too-long
        db.session.commit()


@API
def report_timing_end(name: str, session_id: int, test_id: (int, NoneType)=None):  # pylint: disable=bad-whitespace
    timing = Timing.query.filter_by(session_id=session_id, test_id=test_id, name=name).first_or_404()
    timing.total = Timing.total + flux.current_timeline.time()
    db.session.commit()


@API
def get_timings(session_id: (int, NoneType)=None, test_id: (int, NoneType)=None):
    now = flux.current_timeline.time()
    total_clause = case(
        [
            (Timing.total < 0, now + Timing.total)
        ], else_=Timing.total)
    if session_id is None and test_id is None:
        return {}
    if session_id is not None:
        total_sum_subquery = db.session.query(Timing.name, func.sum(total_clause).label('total_time')).\
                             group_by(Timing.session_id, Timing.name).filter_by(session_id=session_id).subquery()
        query = db.session.query(json_object_agg(total_sum_subquery.c.name, total_sum_subquery.c.total_time))
    else:
        query = db.session.query(json_object_agg(Timing.name, total_clause)).\
                filter_by(test_id=test_id)
    return query.scalar() or {}
