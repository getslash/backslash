import sys
import time
from contextlib import contextmanager

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
        conn.execute("create database {}".format(db_name))
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
    from flask_app.models import db
    db.drop_all()


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


@contextmanager
def _migrate_context():
    from flask_app.app import app
    from flask_app.models import db
    from flask.ext import migrate

    migrate.Migrate(app, db)

    with app.app_context():
        yield migrate
