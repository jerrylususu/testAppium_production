import logging
import sys

sys.path.insert(0,'..')

from mq_prototype.invoke_func import some_method

if __name__ == "__main__":

    logging.basicConfig(filename="invoke.log", level=logging.INFO, format="%(levelname)s: %(asctime)s - %(process)s - [%(filename)s:%(lineno)s] - %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    some_method(1)

    pass