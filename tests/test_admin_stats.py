# pylint: disable=unused-argument,protected-access
import pytest
import flux
from flask_app import stats, models


def test_admin_dbsize(chart):
    assert chart[-1]['db_size'] > 0


def test_admin_num_new_sessions(chart, client, active_db_context):
    assert chart[-1]['num_new_sessions'] >= 0


def test_admin_num_redis_keys(chart, client, active_db_context):
    assert chart[-1]['num_redis_keys'] >= 0


def test_admin_redis_memory_usage(chart, client, active_db_context):
    assert chart[-1]['redis_memory_usage'] >= 0


def test_admin_num_new_sessions_no_previous(real_login, admin_role, active_db_context, client):
    models.Stat.query.delete()
    assert models.Stat.query.count() == 0
    stats.collect_stats()
    chart = client.api.call_function('get_admin_stats')['history']
    assert chart[-1]['num_new_sessions'] == 0


def test_collect_stats(active_db_context):
    stats.collect_stats()


def test_max_num_stats(active_db_context, request):
    for _ in range(stats.NUM_SAMPLES + 1):
        stats.collect_stats()
        flux.current_timeline.sleep(60 * 60)
    assert models.Stat.query.count() == stats.NUM_SAMPLES  # pylint: disable=no-member


@pytest.yield_fixture
def active_db_context(db_context):
    with db_context():
        yield


@pytest.fixture
def chart(client, real_login, admin_role, active_db_context):  # pylint: disable=unused-argumen
    stats.collect_stats()
    return client.api.call_function('get_admin_stats')['history']
