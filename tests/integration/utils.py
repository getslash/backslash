from slash import plugins
from slash import Session
from backslash.contrib.slash_plugin import BackslashPlugin

from urlobject import URLObject as URL

from contextlib import ExitStack

def run_suite(backslash_url, name='simple'):
    with ExitStack() as stack:

        plugin = BackslashPlugin(backslash_url, keepalive_interval=10)
        plugin.fetch_token(username='vmalloc@gmail.com', password='password')

        with Session() as session, session.get_started_context():
            pass
