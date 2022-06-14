"""
This module will log can data
"""
import time
from ..can_module import (
    read_can_data,
    get_can_connection,
    CANPowerUpError,
    CANInternalConnectionError,
    CANConnectionError,
    CANDataLoggingError
)
from ..shared import can_logging_parsing_error_logger, exception_logger
from ..shared.constants import CAN_DATA_LOGGING_TIME, SUCCESS


@exception_logger(can_logging_parsing_error_logger)
def log_can_data() -> str:
    """
    This function will log can data
    Exceptions:
        CANPowerUpError
        CANConnectionError
        CANInternalConnectionError
        CANDataLoggingError
    """
    try:
        can_bus = get_can_connection()

        curr_time = time.time()

        # We can also take time as an input from the user.
        with open(
            "testing_module/can_data_logging_and_parsing/"
            +"recent_can_log"
            + ".txt",
            "w",
        ) as can_log_file:
            while True:

                try:
                    msg_list = read_can_data(can_bus)
                    print(msg_list)
                except Exception as e:
                    raise e

                msg = msg_list[0]
                print(msg)

                can_log_file.write(str(msg) + str("\n"))
                if time.time() > curr_time + 1:
                    break

        can_bus.shutdown()
        return SUCCESS

    except CANPowerUpError as e:
        raise e
    except CANConnectionError as e:
        raise e
    except CANInternalConnectionError as e:
        raise e
    except CANDataLoggingError as e:
        can_bus.shutdown()
        raise e
