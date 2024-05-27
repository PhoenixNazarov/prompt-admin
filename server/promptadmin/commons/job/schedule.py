import logging
import time
import traceback
import datetime
import threading

logger = logging.getLogger(__name__)


def _call_func(func, name: str):
    try:
        func()
    except Exception as e:
        logger.error(f'Scheduling function {name} throw error: ' + str(e))
        traceback.print_exception(e)


def sleep_schedule(func, delay: float):
    """
    func: Call every delay
    delay: seconds for delay
    """

    name = func.__name__

    while True:
        _call_func(func, name)
        time.sleep(delay)


def no_blocking_sleep_schedule(func, delay: float):
    threading.Thread(target=sleep_schedule, args=(func, delay,)).start()


def hour_schedule(func, hour: float, start_first=False):
    """
    func: Call every delay
    hour: once in that hour call func
    """

    name = func.__name__

    if hour < 0.5:
        raise Exception('Hours for schedule {name} lower 0.5')

    upper_time = 24 * 60
    delay_time = upper_time / (hour * 60)

    calc_times = []
    for i in range(0, upper_time, round(upper_time / delay_time)):
        calc_times.append(i)

    calc_times = list(set(calc_times))

    logger.info(f'Hours for schedule {name}: {[round(i / 60, 2) for i in calc_times]}')

    block_time = -1
    if start_first:
        _call_func(func, name)

    while True:
        current_time = datetime.datetime.now()
        current_minutes = current_time.minute + current_time.hour * 60

        if current_minutes == block_time:
            time.sleep(60)
            block_time = -1

        if current_minutes in calc_times:
            _call_func(func, name)
            block_time = current_time

        time.sleep(40)
