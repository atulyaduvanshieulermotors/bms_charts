"""
This module will contain all the can exceptions it can raise.
"""


class CANConnectionError(Exception):
    """This exception will be raised when we are unable to connect to CAN."""

    def __init__(self):
        self.message = "Please check your CAN connection."


class CANPowerUpError(Exception):
    """This exception will be raised when we are unable to power up CAN."""

    def __init__(self):
        self.message = "We are unable to power up CAN."


class CANInternalConnectionError(Exception):
    """This exception will be raised when we have powered up CAN but because of some internal wiring issue in CAN
    we are unable to successfully connect to it."""

    def __init__(self):
        self.message = "CAN has been powered up but because of some internal wiring issue we are unable to connect to it."


class CANGeneralisedError(Exception):
    """This exception will be raised when we are unable to identify issue with CAN."""

    def __init__(self):
        self.message = "Issue with CAN."

class CANDataLoggingError(Exception):
    """This exception will be raised when we are unable to log CAN data because of some issue."""

    def __init__(self):
        self.message = "Because of some issue we could not log CAN data. Please log CAN data again."
