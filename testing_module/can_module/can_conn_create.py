"""
This module will make a fresh connection to CAN.
"""
import can
from .can_exceptions import CANConnectionError, CANPowerUpError
from .can_powerup import power_up_can
from ..shared.constants import CAN_BUSTYPE, CAN_BITRATE, CAN_CHANNEL


def connect_to_can():
    """This module will make fresh connection to can when the server starts

    Exceptions:
        CANPowerUpError
        CANConnectionError
    """

    try:
        power_up_can()
    except CANPowerUpError as e:
        raise e

    try:
        can_bus = can.interface.Bus(
            bustype=CAN_BUSTYPE, channel=CAN_CHANNEL, bitrate=CAN_BITRATE
        )
        return can_bus
    except Exception as e:
        raise CANConnectionError
