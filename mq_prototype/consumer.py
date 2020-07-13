import os
import sys
import time
from datetime import datetime
import logging

# 运行单个 task

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("err: incorrect number of arguments")
        print("usage: consumer.py [input]")
        sys.exit()

    req = int(sys.argv[1])

    logging.basicConfig(filename=f"log2/{req}.log",level=logging.DEBUG)

    logging.info(f"requested: {req}")

    start = datetime.now()
    logging.info(f"started task @ {start}")

    sum = 0
    for i in range(req+1):
        sum += i
    logging.info(f"sum: {sum}")

    end = datetime.now()
    logging.info(f"finished task @ {end}")
    logging.info(f"took {end-start}")



