import operator

from .. import models
from ..utils import statuses
from ..utils.filtering import ConstFilter, ToggleFilter, FilterConfig, in_, notin_

_STATUS_FILTERS = {
        'unsuccessful': (notin_, (statuses.SUCCESS, statuses.SKIPPED, statuses.RUNNING)),
        'successful': (in_, (statuses.SUCCESS, statuses.SKIPPED)),
        'skipped': (operator.eq, statuses.SKIPPED),
}


SESSION_FILTERS = FilterConfig({
    'investigated': ConstFilter(models.Session.investigated, {
        'not investigated': False,
        'investigated': True,
    }),
    'status': ConstFilter(models.Session.status, _STATUS_FILTERS),
    'archived': ToggleFilter(models.Session.archived, default=False),
})

TEST_FILTERS = FilterConfig({
    'status': ConstFilter(models.Test.status, _STATUS_FILTERS),
})
