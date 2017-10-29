import flux
from ...models import Timing, db
from ...utils.db_utils import json_object_agg
from .blueprint import API

from sqlalchemy import case

NoneType = type(None)


@API
def report_timing_start(name: str, session_id: int, test_id: (int, NoneType)=None):  # pylint: disable=bad-whitespace
    db.session.execute(
        '''
        INSERT INTO timing(session_id, test_id, name, total)
        VALUES (:session_id, :test_id, :name, :interval)
        ON CONFLICT(id) DO UPDATE SET total = timing.total + EXCLUDED.total''',
        {'session_id': session_id, 'test_id': test_id, 'name': name, 'interval': -flux.current_timeline.time()})
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
            (Timing.total < 0, now - Timing.total)
        ], else_=Timing.total)
    kwargs = {'test_id': test_id}
    if session_id is not None:
        kwargs['session_id'] = session_id
    query = db.session.query(json_object_agg(Timing.name, total_clause)).\
            filter_by(**kwargs)
    return query.scalar() or {}
