import click

import logbook

from .bootstrapping import requires_env, from_project_root

_logger = logbook.Logger(__name__)

@click.command()
@click.argument('name')
@click.argument('args', nargs=-1)
@requires_env('app', 'develop')
def suite(name, args):
    import slash
    from slash.frontend.slash_run import slash_run
    from backslash.contrib.slash_plugin import BackslashPlugin

    slash.plugins.manager.install(BackslashPlugin('http://127.0.0.1:8000'), activate=True)
    slash_run([from_project_root('_sample_suites', name)] + list(args))


