import flux

from . import models
from .models import db

SAMPLE_FREQENCY_SECONDS = 60 * 60
SAMPLE_DAYS_BACK = 4
NUM_SAMPLES = (SAMPLE_DAYS_BACK * 24 * 60 * 60) // SAMPLE_FREQENCY_SECONDS

class StatCollectors(object):

    @classmethod
    def db_size(cls):
        return db.session.execute("select pg_database_size('backslash')").scalar()

    @classmethod
    def num_new_sessions(cls):
        latest = models.Stat.query.order_by(models.Stat.timestamp.desc()).first()
        if latest is None:
            return 0
        return models.Session.query.filter(models.Session.start_time > latest.timestamp).count()


def iter_stat_names():
    for name in dir(StatCollectors):
        if name.startswith('_'):
            continue
        yield name

################################################################################

def collect_stats():
    stat_dict = _get_stats_dict()
    db.session.add(models.Stat(**stat_dict))
    db.session.flush()
    _cleanup_oldest_samples()
    db.session.commit()

def _get_stats_dict():
    returned = {}
    for stat_name in iter_stat_names():
        if stat_name.startswith('_'):
            continue
        returned['stat_' + stat_name] = getattr(StatCollectors, stat_name)()
    return returned


def _cleanup_oldest_samples():
    db.session.execute('delete from stat where id not in (select id from stat order by timestamp desc limit {})'.format(NUM_SAMPLES))
