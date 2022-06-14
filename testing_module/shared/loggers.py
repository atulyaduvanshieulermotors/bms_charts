"""
    This file will define all the loggers
"""
from .logging_config import setup_logger

# this logger will log all the genereal logs for main.py files
general_logger = setup_logger("general_logger", "testing_module/general.log")

# this logger will log all the error logs for main.py
error_logger = setup_logger("error_logger", "testing_module/error.log")

# this logger will log all the genereal logs for testing_module/can_module/logs
can_general_logger = setup_logger(
    "can_general_logger",
    "testing_module/can_module/logs/can_general.log",
)

# this logger will log all data for testing_module/can_module/logs
can_data_logger = setup_logger(
    "can_data_logger", "testing_module/can_module/logs/can_data.log"
)

# this logger will log all the error logs for testing_module/can_module/logs
can_error_logger = setup_logger(
    "can_error_logger",
    "testing_module/can_module/logs/can_error.log",
)


# this logger will log all data for testing_module/shared/logs
shared_data_logger = setup_logger(
    "shared_data_logger", "testing_module/shared/logs/shared_data.log"
)

# this logger will log all the error logs for testing_module/shared/logs
shared_error_logger = setup_logger(
    "shared_error_logger",
    "testing_module/shared/logs/shared_error.log",
)

# this logger will log all the genereal logs for testing_module/can_data_logging_and_parsing/logs
can_logging_parsing_general_logger = setup_logger(
    "can_logging_parsing_general_logger",
    "testing_module/can_data_logging_and_parsing/logs/can_logging_parsing_general.log",
)

# this logger will log all data for testing_module/can_data_logging_and_parsing/logs
can_logging_parsing_data_logger = setup_logger(
    "can_logging_parsing_data_logger",
    "testing_module/can_data_logging_and_parsing/logs/can_logging_parsing_data.log",
)

# this logger will log all the error logs for testing_module/can_data_logging_and_parsing/logs
can_logging_parsing_error_logger = setup_logger(
    "can_logging_parsing_error_logger",
    "testing_module/can_data_logging_and_parsing/logs/can_logging_parsing_error.log",
)
