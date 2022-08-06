# -*- coding: utf-8 -*-
"""
Mathics timing method(s) and timing context manager.
"""

import os
import time

MIN_ELAPSE_REPORT = int(os.environ.get("MIN_ELAPSE_REPORT", "0"))


# A small, simple timing tool
def timeit(method):
    """Add this as a decorator to time parts of the code.

    For example:
        @timeit
        def long_running_function():
            ...
    """

    def timed(*args, **kw):
        method_name = method.__name__
        # print(f"{date.today()}	{method_name} starts")
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        elapsed = (te - ts) * 1000
        if elapsed > MIN_ELAPSE_REPORT:
            if "log_time" in kw:
                name = kw.get("log_name", method.__name__.upper())
                kw["log_time"][name] = elapsed
            else:
                print("%r  %2.2f ms" % (method_name, elapsed))
        # print(f"{date.today()}	{method_name} ends")
        return result

    return timed


class TimeitContextManager:
    """Add this as a context manager to time parts of the code.

    For example:
        with TimeitContextManager("testing my loop"):
           for x in collection:
               ...
    """

    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        # print(f"{date.today()}	{method_name} starts")
        self.ts = time.time()

    def __exit__(self, exc_type, exc_value, exc_tb):
        te = time.time()
        elapsed = (te - self.ts) * 1000
        if elapsed > MIN_ELAPSE_REPORT:
            print("%r  %2.2f ms" % (self.name, elapsed))
