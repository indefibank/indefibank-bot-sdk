import time
import logging
import asyncio
import threading
from functools import wraps
from typing import Tuple


def benchmark(func):
    logger = logging.getLogger("benchmark")

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        finish = time.time()
        executed_time = finish - start
        extra_info = {
            "start_time": start,
            "finished_time": finish,
            "executed_time": executed_time,
            "func": func.__name__,
            "position_arguments": args,
            "keywords_arguments": kwargs
        }
        logger.debug(f"function {func.__name__} was executed in {executed_time} seconds", extra=extra_info)
        return return_value

    return wrapper


def create_and_start_event_loop() -> Tuple[asyncio.AbstractEventLoop,
                                           asyncio.Future,
                                           threading.Thread]:

    loop = asyncio.get_event_loop()
    # loop.set_debug(1)
    stopping_fut = asyncio.Future()
    loop_thread = threading.Thread(target=loop.run_until_complete,
                                   args=(stopping_fut,),
                                   name='EventLoop')
    loop_thread.start()
    loop._mythread = loop_thread
    return loop, stopping_fut, loop_thread
