import click

import logbook

from .bootstrapping import requires_env, from_project_root

_logger = logbook.Logger(__name__)

@click.command()
@click.option('--interactive', default=False, is_flag=True)
@click.option('--debug', default=False, is_flag=True)
@click.option('use_subjects', '--use-subjects', default=False, is_flag=True)
@click.option('use_related', '--use-related', default=False, is_flag=True)
@click.argument('name')
@click.argument('args', nargs=-1)
@requires_env('app', 'develop')
def suite(name, args, interactive=False, debug=False, use_subjects=False, use_related=False):
    import slash
    import gossip

    from slash.frontend.slash_run import slash_run
    from backslash.contrib.slash_plugin import BackslashPlugin


    class _Plugin(BackslashPlugin):

        def _get_initial_session_metadata(self):
            returned = super()._get_initial_session_metadata()
            returned.update({"users": {
                "some_data": [
                    {'bla': '2', 'j': 3},
                ]
            }})
            return returned

        def _get_extra_session_start_kwargs(self):
            returned = {}
            if use_subjects:
                returned['subjects'] = [
                    {
                        'name': 'microwave1',
                        'product': 'Microwave',
                        'version': 'v1',
                        'revision': '123456',
                    }
                ]
            return returned

        def session_start(self):
            super().session_start()
            if use_related:
                self.session.add_related_entity(entity_type='toaster', entity_name='toaster01')


    plugin = _Plugin('http://127.0.0.1:8000', keepalive_interval=10, propagate_exceptions=True)

    @gossip.register('backslash.session_start')
    def configure(session):
        session.add_subject('system1', product='Microwave', version='1.0', revision='100')

    slash.plugins.manager.install(plugin, activate=True)

    args = list(args)
    if interactive:
        args.append('-i')
    if debug:
        args.append('--pdb')
    slash_run([from_project_root('_sample_suites', name)] + args)
