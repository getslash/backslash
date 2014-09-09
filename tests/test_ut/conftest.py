import flux

import pytest


@pytest.fixture(autouse=True, scope='session')
def freeze_timeline(request):

    original_factor = flux.current_timeline.get_time_factor()

    @request.addfinalizer
    def finalizer():
        flux.current_timeline.set_time_factor(original_factor)

    flux.current_timeline.set_time_factor(0)
