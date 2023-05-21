import math
import datetime as dt


def get_pause() -> int:
    """
    Calculate number of seconds till next minute.

    Returns:
        int: Pause duration in seconds
    """
    now = dt.datetime.now()
    next_min = now.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
    return math.ceil((next_min - now).seconds)
