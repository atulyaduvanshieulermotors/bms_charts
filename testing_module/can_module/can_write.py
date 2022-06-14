"""
This module will send data to CAN
"""
from .can_exceptions import CANInternalConnectionError
from ..shared.constants import SUCCESS
from ..shared import can_error_logger


def write_to_can(can_bus, can_msg):
    """
    This function assumes CAN has already been powered up.
    This function will take a can_bus connection and will send can_msg to it.

    Args:
        can_bus (_type_): CAN bus connection object
        can_msg (_type_): CAN message object

    Exceptions:
        CANInternalConnectionError
    """
    try:
        can_bus.send(can_msg)
        return SUCCESS
    except Exception as e:
        can_error_logger.exception(e)
        raise CANInternalConnectionError
