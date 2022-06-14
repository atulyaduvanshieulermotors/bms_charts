"""
This module will verify whether we are currently connected to can or not.
"""

from typing import Any
from .can_exceptions import CANInternalConnectionError


def check_can_connection(can_bus: Any) -> str:
    """
        This module will take a can_bus connection as input and will verify it whether it is working fine or not.
        We are receiving output from CAN here basically. If we are not receiving it, then sth is not OK.

    Returns:
        str: Whether CAN connection is a success or will raise an exception.

    Exceptions:
        CANInternalConnectionError
    """

    msg_counter = 2
    flag = False
    for count in range(msg_counter):
        msg = can_bus.recv(timeout=1.5)
        if msg != None:
            flag = True
    if flag == False:
        raise CANInternalConnectionError
