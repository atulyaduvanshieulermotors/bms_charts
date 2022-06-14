"""
This module will get a new CAN connection and also will get that connection verified.
"""
from .can_exceptions import (
    CANConnectionError,
    CANInternalConnectionError,
    CANPowerUpError,
)
from .can_conn_create import connect_to_can
from .can_conn_check import check_can_connection
from ..shared import can_error_logger, exception_logger


@exception_logger(can_error_logger)
def get_can_connection():
    """
    This function will get a new CAN connection and also will get that connection verified.
    It checks CAN connection by reading CAN Data. If it receives CAN data then connection is fine.
    Exceptions:
        CANPowerUpError
        CANConnectionError
        CANInternalConnectionError
    """
    try:
        can_bus = connect_to_can()
        check_can_connection(can_bus)
        return can_bus
    except CANPowerUpError as e:
        raise e
    except CANConnectionError as e:
        raise e
    except CANInternalConnectionError as e:
        raise e
