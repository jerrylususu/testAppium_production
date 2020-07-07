from func_timeout import FunctionTimedOut

import functools

def timeout_exception_wrapper(func):
    @functools.wraps(func)
    def f_wrapper(*args, **kwargs): 
        try:
            return func(*args, **kwargs)
        except FunctionTimedOut as e:
            return Exception("[exp] timeout happened! " + str(e).strip())
    return f_wrapper