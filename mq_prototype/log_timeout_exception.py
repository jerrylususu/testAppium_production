# example showing func_timeout can not exit gracefully

import multiprocessing
import logging
from logging.handlers import QueueHandler, QueueListener
import time
import random
import signal

from func_timeout import func_timeout, FunctionTimedOut, func_set_timeout

import traceback, functools, multiprocessing

# from pebble import ProcessPool
from concurrent.futures import TimeoutError

def trace_unhandled_exceptions(func):
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            logging.exception()
    return wrapped_func

def timeout_exception_wrapper(func):
    @functools.wraps(func)
    def f_wrapper(*args, **kwargs): 
        try:
            return func(*args, **kwargs)
        except FunctionTimedOut as e:
            return Exception("timeout happened! " + str(e).strip())
    return f_wrapper

@timeout_exception_wrapper
@func_set_timeout(1)
def f(i):
    # time.sleep(1)
    logging.info('function called with {} in worker thread.'.format(i))
    time.sleep(2)
    return i

def worker_init(q):
    # all records from worker processes go to qh and then into q
    qh = QueueHandler(q)
    logger = logging.getLogger()


def logger_init(file_location="multi.log"):
    q = multiprocessing.Queue()
    # this is the handler for all log records
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(asctime)s - %(process)s - [%(filename)s:%(lineno)s] - %(message)s")
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler("multi.log", encoding="utf8")
    file_handler.setFormatter(formatter)

    # ql gets records from the queue and sends them to the handler
    ql = QueueListener(q, stream_handler, file_handler, respect_handler_level=True)
    ql.start()

    logger = logging.getLogger()
    print(logger.handlers)
    # logger.propagate = False
    logger.setLevel(logging.DEBUG)
    # add the handler to the 'logger so records from this process are handled
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    print("init",logger.handlers)

    return ql, q


def main():

    q_listener, q = logger_init()

    logging.info('hello from main thread')
    pool = multiprocessing.Pool(4, worker_init, [q])

    task_list = []
    for i in range(10):
        task = pool.apply_async(f, (i,))
        task_list.append(task)

    for t in task_list:
        logging.info("in loop!")
        try:
            logging.info(t.get())
            a = t.get()
            if isinstance(a, Exception):
                print("ex")
        except:
            print("this is exception")
            logging.exception("wow")

    q_listener.stop()

if __name__ == '__main__':
    main()