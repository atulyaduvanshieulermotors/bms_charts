"""
This module will receive data from CAN
"""
from .can_exceptions import CANInternalConnectionError


def read_can_data(can_bus, msg_count=1):
    """
    If you come to this function that means CAN has already been successfully powered up.
    This function will receive msg from CAN.

    Args:
        can_bus (_type_): CAN connection object
        msg_count(int): count of messages you want to take

    Exceptions:
        CANInternalConnectionError
    """

    msg_list = []
    for count in range(msg_count):
        msg_list.append(can_bus.recv(timeout=1.5))
    if msg_count != 0 and len(msg_list) == 0:
        raise CANInternalConnectionError
    return msg_list
