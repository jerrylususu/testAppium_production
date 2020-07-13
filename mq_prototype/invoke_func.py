import logging

def some_method(i: int,
 j: int = 1) -> str:
    logging.info("input is %d", i)
    return str(i)