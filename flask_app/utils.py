import datetime

import flux


def get_current_time():
    return datetime.datetime.utcfromtimestamp(flux.current_timeline.time())
