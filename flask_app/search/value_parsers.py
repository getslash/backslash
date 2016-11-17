import re

import datetime
import dateparser

from .exceptions import SearchSyntaxError

units = {
    'd': datetime.timedelta(days=1),
    'h': datetime.timedelta(hours=1),
}

def parse_date(value):
    match = re.match(r"^([\-\+])(\d+)([{}])".format(''.join(units)), value)
    if not match:
        returned = dateparser.parse(value)
        if returned is None:
            raise SearchSyntaxError('Invalid date provided: {!r}'.format(value))
        return returned.timestamp()

    returned = datetime.datetime.now()

    sign, num, unit = match.groups()
    num = int(num)

    diff = num * units[unit]

    if sign == '-':
        returned -= diff
    else:
        returned += diff
    return returned.timestamp()
