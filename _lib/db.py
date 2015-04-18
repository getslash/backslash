import random
import sys
import time
from contextlib import contextmanager
from uuid import uuid4

import logbook

import click

from .bootstrapping import requires_env


@click.group()
def db():
    pass


@db.command()
@requires_env("app")
def ensure():
    import sqlalchemy
    from flask_app.app import app

    uri = app.config['SQLALCHEMY_DATABASE_URI']
    if 'postgres' not in uri and 'psycopg2' not in uri:
        logbook.error(
            "Don't know how to create database - unrecognized connection type: {!r}", uri)
        sys.exit(-1)

    try:
        sqlalchemy.create_engine(uri).connect()
    except sqlalchemy.exc.OperationalError:
        uri, db_name = uri.rsplit('/', 1)
        engine = sqlalchemy.create_engine(uri + '/postgres')
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("create database {} with encoding = 'UTF8'".format(db_name))
        conn.close()
        logbook.info("Database {} successfully created on {}.", db_name, uri)
    else:
        logbook.info("Database exists. Not doing anything.")


@db.command()
def wait(num_retries=60, retry_sleep_seconds=1):
    import sqlalchemy

    from flask_app.app import app

    uri = app.config['SQLALCHEMY_DATABASE_URI']
    for retry in xrange(num_retries):
        logbook.info(
            "Testing database connection... (retry {0}/{1})", retry + 1, num_retries)
        if retry > 0:
            time.sleep(retry_sleep_seconds)
        try:
            sqlalchemy.create_engine(uri).connect()
        except sqlalchemy.exc.OperationalError as e:
            if 'does not exist' in str(e):
                break
            logbook.error(
                "Ignoring OperationError {0} (db still not availalbe?)", e)
        except Exception as e:
            logbook.error(
                "Could not connect to database ({0.__class__}: {0}. Going to retry...", e, exc_info=True)
        else:
            break
    else:
        raise RuntimeError("Could not connect to database")
    logbook.info("Database connection successful")


@db.command()
@requires_env("app")
def drop():
    from flask_app.app import app
    from flask_app.models import db
    db.drop_all()
    db.engine.execute('DROP TABLE IF EXISTS alembic_version')


@db.command()
@requires_env("app")
def revision():
    with _migrate_context() as migrate:
        migrate.upgrade()
        migrate.revision(autogenerate=True)


@db.command()
@requires_env("app")
def upgrade():
    with _migrate_context() as migrate:
        migrate.upgrade()

@db.command()
@requires_env("app")
def downgrade():
    with _migrate_context() as migrate:
        migrate.downgrade()


@contextmanager
def _migrate_context():
    from flask_app.app import app
    from flask_app.models import db
    from flask.ext import migrate

    migrate.Migrate(app, db)

    with app.app_context():
        yield migrate


@db.command()
@requires_env("app", "develop")
def populate():
    drop.callback()
    upgrade.callback()
    _populate_db()


def _populate_db(num_sessions=50, delay_between_sessions=(5, 60), tests_per_session=(1, 50), test_duration=(10, 60), fail_percent=(0, 20)):
    import flux

    flux.current_timeline.set_time(
        flux.current_timeline.time() - (24 * 60 * 60), allow_backwards=True)
    flux.current_timeline.set_time_factor(0)

    with _get_client_context() as client:
        for session_index in range(_pick(num_sessions)):
            session_fail_percent = _pick(fail_percent)
            logbook.info('Populating session #{}', session_index + 1)
            if session_index > 0:
                flux.current_timeline.sleep(_pick(delay_between_sessions))
            session = client.report_session_start()

            for test_index in range(_pick(tests_per_session)):
                logbook.info('Populating test #{}:#{}', session_index + 1, test_index + 1)
                test = session.report_test_start()
                flux.current_timeline.sleep(_pick(test_duration))
                if session_fail_percent == 100 or random.randint(0, 100) < session_fail_percent:
                    test.add_error()

                test.report_end()

            session.report_end()


def _pick(number_or_range):
    if isinstance(number_or_range, tuple):
        return random.randint(*number_or_range)
    return number_or_range


@contextmanager
def _get_client_context():
    from flask_app.app import app

    from flask.ext.loopback import FlaskLoopback
    from backslash import Backslash as BackslashClient

    app.config['PROPAGATE_EXCEPTIONS'] = True

    address = str(uuid4())
    loopback = FlaskLoopback(app)
    loopback.activate_address((address, 80))
    try:
        yield BackslashClient('http://{0}'.format(address))
    finally:
        loopback.deactivate_address((address, 80))
