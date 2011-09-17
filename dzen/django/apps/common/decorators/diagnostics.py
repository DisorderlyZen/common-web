import time, logging

def simple_decorator(decorator):
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g

    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator

@simple_decorator
def log_performance(func):
    def timing(*args, **kwargs):
        logger = logging.getLogger('diagnostics.performance')

        start = time.time()
        res = func(*args, **kwargs)
        stop = time.time()
        elapsed = (stop-start)*1000.0

        logger.info("{0} took {1:0.3f} ms".format(func.__name__, elapsed))
        return res
    return timing
