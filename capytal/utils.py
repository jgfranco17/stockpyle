import math
import datetime as dt


def get_pause():
    now = dt.datetime.now()
    next_min = now.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
    pause = math.ceil((next_min - now).seconds)
    print(f"Sleep for {pause}")
    return pause