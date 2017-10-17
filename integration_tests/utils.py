import os

import slash
from slash import plugins
from slash import Session
from backslash.contrib.slash_plugin import BackslashPlugin

from contextlib import ExitStack

from slash.frontend.slash_run import slash_run


def run_suite(backslash_url, name='simple', interrupt=False):

    session_id = None

    with ExitStack() as stack:

        plugin = BackslashPlugin(backslash_url, keepalive_interval=10)
        plugin.fetch_token(username='vmalloc@gmail.com', password='password')

        @slash.hooks.register
        def session_start():
            nonlocal session_id
            session_id = slash.context.session.id

        plugins.manager.install(plugin, activate=True)
        stack.callback(plugins.manager.uninstall, plugin)
        try:
            slash_run([os.path.join('_sample_suites', name), '--session-label', 'testing'])
        except KeyboardInterrupt:
            if not interrupt:
                raise

    return session_id
