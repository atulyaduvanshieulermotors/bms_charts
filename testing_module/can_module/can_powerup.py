"""
This module is used to power up can.
"""
import subprocess, shlex
from ..shared.constants import SUCCESS, CAN_POWER_UP_COMMAND
from .can_exceptions import CANPowerUpError


def power_up_can():
    """
        This function will power up can using subprocess library and using following command
        'sudo ip link set can0 up type can bitrate 250000'

    Exceptions:
        CANPowerUpError
    """
    command = CAN_POWER_UP_COMMAND
    cmd = shlex.split(command)
    result = subprocess.run(cmd, capture_output=True, text=True)
    res_err = result.stderr

    # res_out = result.stdout to catch command output
    # If there is no error then it means can is already connected or successfully connected now.
    # RTNETLINK will shown if CAN connection is already alive
    

    if res_err == "" or res_err[:9] == "RTNETLINK":
        return SUCCESS
    else:
        print(res_err)
        #raise CANPowerUpError
