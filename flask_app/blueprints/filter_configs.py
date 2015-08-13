import operator

from .. import models
from ..utils.filtering import ConstFilter, FilterConfig
from ..utils import statuses

SESSION_FILTERS = FilterConfig({
    'investigated': ConstFilter(models.Session.investigated, {
        'not investigated': False,
        'investigated': True,
    }),
    'status': ConstFilter(models.Session.status, {
        'unsuccessful': (operator.ne, statuses.SUCCESS),
        'successful': statuses.SUCCESS,
    }),
})

TEST_FILTERS = FilterConfig({
    'status': ConstFilter(models.Test.status, {
        'unsuccessful': (operator.ne, statuses.SUCCESS),
        'successful': statuses.SUCCESS,
    }),
})
