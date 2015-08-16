import sys
import time
import re
import os
from contextlib import contextmanager

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
        logbook.info("Testing database connection... (retry {0}/{1})", retry+1, num_retries)
        if retry > 0:
            time.sleep(retry_sleep_seconds)
        try:
            sqlalchemy.create_engine(uri).connect()
        except sqlalchemy.exc.OperationalError as e:
            if 'does not exist' in str(e):
                break
            logbook.error("Ignoring OperationError {0} (db still not availalbe?)", e)
        except Exception as e:
            logbook.error("Could not connect to database ({0.__class__}: {0}. Going to retry...", e, exc_info=True)
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
    from flask_app.app import create_app
    from flask_app.models import db
    from flask.ext import migrate
    app = create_app()

    migrate.Migrate(app, db)

    with app.app_context():
        yield migrate
