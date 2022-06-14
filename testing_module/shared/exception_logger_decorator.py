"""
This module will provide a decorator for 
logging all the exceptions for a particular function.
"""


def exception_logger(logger):
    """
    This is a decorator. It will log exceptions in case there is an exception.
    """

    def inner(func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                if len(args) == 0:
                    logger.exception(e)
                else:
                    logger.exception(f"UUID is - {args[0]} Exception is - {e}")
                raise e
            return res

        return wrapper

    return inner
