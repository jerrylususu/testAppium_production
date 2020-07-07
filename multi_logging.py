import multiprocessing
import logging
from logging.handlers import QueueHandler, QueueListener

# ∂‡ worker »’÷æ

def worker_init(q):
    # all records from worker processes go to qh and then into q
    qh = QueueHandler(q)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # logger.addHandler(qh)


def logger_init(file_location="multi.log"):
    q = multiprocessing.Queue()
    # this is the handler for all log records
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(asctime)s - %(process)s - [%(filename)s:%(lineno)s] - %(message)s")
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(file_location, encoding="utf8")
    file_handler.setFormatter(formatter)

    # ql gets records from the queue and sends them to the handler
    ql = QueueListener(q, stream_handler, file_handler, respect_handler_level=True)
    ql.start()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # add the handler to the logger so records from this process are handled
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return ql, q

