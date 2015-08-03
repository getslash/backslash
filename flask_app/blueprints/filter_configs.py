import operator

from .. import models
from ..utils.filtering import ConstFilter, FilterConfig
from ..utils import statuses

SESSION_FILTERS = FilterConfig({
    'status': ConstFilter(models.Session.status, {
        'unsuccessful': (operator.ne, statuses.SUCCESS),
        'successful': statuses.SUCCESS,
    })})
