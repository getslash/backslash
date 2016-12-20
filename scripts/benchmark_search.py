#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
from uuid import uuid4

import click
import logbook
import requests
from flask_app.app import create_app
from flask_loopback import FlaskLoopback
from urlobject import URLObject as URL

_root_address = str(uuid4())
_root_url = URL('http://{}'.format(_root_address))


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet", count=True)
def main(verbose, quiet):

    from _benchmark_queries import queries

    with logbook.NullHandler(), logbook.StreamHandler(sys.stderr, level=logbook.CRITICAL-verbose+quiet, bubble=False):

        loopback = FlaskLoopback(create_app())
        loopback.activate_address((_root_address, 80))


        num_attempts = 5
        for obj, query in queries:
            times = []
            has_error = False
            print(obj, '|', click.style(query, fg='cyan'), '--')
            for i in range(num_attempts):
                start_time = time.time()
                resp = requests.get(_root_url.add_path('/rest').add_path(obj).add_query_param('search', query).add_query_param('page_size', 25))
                end_time = time.time()
                if resp.status_code == requests.codes.internal_server_error:
                    print('\t', click.style('Timeout', fg='red'))
                    has_error=True
                    break
                else:
                    resp.raise_for_status()
                    times.append(end_time - start_time)
            if not has_error:
                print('\t', len(resp.json()[obj]), 'results --', '(Out of {}) Best: {:.03}s Avg: {:.03}s Worst: {:.03}s'.format(num_attempts, min(times), sum(times) / len(times), max(times)))


if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter
