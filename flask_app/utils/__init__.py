import datetime

import flux


def get_current_datetime():
    return datetime.datetime.utcfromtimestamp(flux.current_timeline.time())

def get_current_time():
    return flux.current_timeline.time()

