import threading
from time import sleep

def wait_until_number_of_threads_is(threads: int, polling_frequency: float):
    while (threading.active_count()) > threads:
        sleep(polling_frequency)