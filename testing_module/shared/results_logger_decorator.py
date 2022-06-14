"""
This module will provide a decorator for 
logging all the results before sending response.
"""
from typing import Dict

def log_results(logger):
    """
    This is a decorator. It will store the test results at the end of the  test completion.
    """

    def inner(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            logger.info(
                "Test Status - %s Test Errors - %s"
                % (str(res["test_status"]), " ".join(map(str, res["test_errors"])))
            )
            return res

        return wrapper

    return inner
