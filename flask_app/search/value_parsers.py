import dateparser
import datetime
from .exceptions import SearchSyntaxError


def parse_date(value):
    parsed = dateparser.parse(value, settings={'RETURN_AS_TIMEZONE_AWARE': True})

    if parsed is None:
        raise SearchSyntaxError('Unknown date/time format')

    min_parsed = max_parsed = parsed

    if (parsed.hour, parsed.minute, parsed.second) == (0, 0, 0):
        if '0:0' not in value:
            max_parsed += datetime.timedelta(days=1)


    return min_parsed, max_parsed
