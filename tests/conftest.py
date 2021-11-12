from functools import wraps


def stub_sleep(func):
    """Decorator to speed up time.sleep function used in any methods under test."""
    import time
    from time import sleep

    def newsleep(seconds):
        sleep_speed_factor = 10.0
        sleep(seconds / sleep_speed_factor)

    time.sleep = newsleep

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
