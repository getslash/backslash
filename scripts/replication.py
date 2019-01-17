import time
from contextlib import contextmanager
import click
from pathlib import Path
import sys

sys.path.insert(0, "")

from flask_app.tasks import replications
from flask_app.app import create_app
from flask_app import models


@click.group()
def cli():
    pass


@cli.command()
def status():
    app = create_app()
    with app.app_context():
        replica = models.Replication.query.first()
        print("Found replica", replica)
        with _timing(f"Fetching tests to replicate..."):
            tests = list(
                models.db.session.execute(
                    replications._get_tests_to_replicate_query(replica)
                )
            )
            print(f"Found {len(tests)} to replicate. First one is {tests[0]}")


@contextmanager
def _timing(msg):
    print(msg, "...")
    start_time = time.time()
    yield
    print(f"... took {time.time() - start_time}s")


if __name__ == "__main__":
    cli()
