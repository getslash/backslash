import random
import sys
import time
import re
import os
from contextlib import contextmanager
from uuid import uuid4

import logbook

import click

from .bootstrapping import requires_env

_DATABASE_URI_RE = re.compile(r"(?P<driver>(?P<db_type>sqlite|postgresql)(\+.*)?):\/\/(?P<host>[^/]*)\/(?P<db>.+)")


@click.group()
def db():
    pass


def _create_sqlite(path):
    pass

def _create_postgres(match):
    import sqlalchemy
    from flask_app.models import db

    uri = match.group(0)
    db_name = match.group('db')
    try:
        sqlalchemy.create_engine(uri).connect()
    except sqlalchemy.exc.OperationalError:
        engine = sqlalchemy.create_engine('{}://{}/postgres'.format(match.group('driver'), match.group('host')))
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("create database {} with encoding = 'UTF8'".format(db_name))
        conn.close()
        logbook.info("Database {} successfully created on {}.", db_name, uri)
    else:
        logbook.info("Database {} exists.", db_name)


@db.command()
@requires_env("app")
def ensure():
    from flask_app.app import create_app
    from flask_app.models import db
    app = create_app()

    uri = app.config['SQLALCHEMY_DATABASE_URI']
    match = _DATABASE_URI_RE.match(uri)
    if not match:
        logbook.error("Don't know how to create a database of type {}", uri)
        sys.exit(-1)

    if match.group('db_type') == 'sqlite':
        _create_sqlite(match.group('db'))
    elif match.group('db_type') == 'postgresql':
        _create_postgres(match)

    with app.app_context():
        db.create_all()
    logbook.info("DB successfully created")




@db.command()
def wait(num_retries=60, retry_sleep_seconds=1):
    import sqlalchemy

    from flask_app.app import create_app
    app = create_app()

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
    from flask_app.app import create_app
    from flask_app.models import db
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.engine.execute('DROP TABLE IF EXISTS alembic_version')


@db.command()
@requires_env("app")
@click.option('-m', '--message', default=None)
def revision(message):
    with _migrate_context() as migrate:
        migrate.upgrade()
        migrate.revision(autogenerate=True, message=message)


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


@db.command()
@requires_env("app")
def downgrade():
    with _migrate_context() as migrate:
        migrate.downgrade()


@contextmanager
def _migrate_context(app):
    from flask_app.app import create_app
    from flask_app.models import db
    from flask.ext import migrate
    if app is None:
        app = create_app()

    migrate.Migrate(app, db)

    with app.app_context():
        yield migrate


@db.command()
@requires_env("app", "develop")
def populate():
    drop.callback()
    upgrade.callback()
    _populate_db()


def _populate_db(num_sessions=10, delay_between_sessions=(5, 60), tests_per_session=(1, 20), test_duration=(10, 60), fail_percent=(0, 20)):
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
                test = session.report_test_start(file_name='filename.py', function_name='func_name')
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
    from flask_app.app import create_app

    from flask.ext.loopback import FlaskLoopback
    from backslash import Backslash as BackslashClient

    app = create_app({'DEBUG': True, 'TESTING': True, 'SECRET_KEY': 'dummy', 'SECURITY_PASSWORD_SALT': 'dummy'})
    with app.app_context():
        address = str(uuid4())
        loopback = FlaskLoopback(app)
        loopback.activate_address((address, 80))
        try:
            yield BackslashClient('http://{0}'.format(address))
        finally:
            loopback.deactivate_address((address, 80))
