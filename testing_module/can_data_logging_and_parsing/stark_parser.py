"""
This module is for parsing can data.
This module will take can_id and can_data as input(both in str format)
and will output a response dict object
Also another thing to keep in mind is that in can output, lower 2 bits comes first and upper 2 bits come later.
So for converting a hex string in decimal format you have to reverse them in pairs.
"""

from typing import Dict, List
from ..shared import can_logging_parsing_error_logger

reverse_string_in_pair = lambda string: "".join(
    reversed([string[idx : idx + 2] for idx in range(0, len(string), 2)])
)

check_is_battery_latched = lambda string: convert_and_get_desired_value(string) == 1


hex_to_bin = lambda string: bin(int(string, 16))


def convert_and_get_temperature(string: str, roundabout: float = None) -> float:
    """
        This function will take temperature string in hex format and will convert it into decimal format and will
        roundabout value from it

    Args:
        string (str): temperature string in hex format
        roundabout (float, optional): _Value we have to delete from temperature_. Defaults to None.

    Returns:
        float: returns temperature after converting string in decimal format and subtracting roundabout from it
    """
    if not roundabout:
        roundabout = 0
    assert isinstance(roundabout, int), "`roundabout` value should be integer"
    temperature = int(string, 16) - roundabout
    return float(format(temperature, ".1f"))


def convert_and_get_temperatures(string: str) -> List:
    """This function will take temperature string in hex format and will get it converted it into decimal format

    Args:
        string (str): this string is in hex format and has multiple temp.

    Returns:
        List: it will be list of temperatures in decimal format
    """
    temp = ""
    temperatures = []
    for idx, _str in enumerate(string):
        temp += _str
        if idx % 2:
            temperatures.append(convert_and_get_temperature(temp))
            temp = ""
    return temperatures


def convert_and_get_current_val(string: str) -> float:
    """This function will take string in hex format as input and will return it in decimal format.

    Args:
        string (str): this string is in hex format

    Returns:
        float: This is the decimal format of input.
    """
    new_string = reverse_string_in_pair(string)

    # this is to check if value is negative or not; if it is -ve it will have "FF" in the starting
    if new_string[0:2] == "FF":
        current = (
            int(hex(int("100000000", 16) - int(new_string, 16)), 16) / 1000
        ) * 0.01
        current *= -1
    else:
        current = (int(new_string, 16) / 1000) * 0.01
    return float(format(current, ".1f"))


def convert_and_get_desired_value(string: str, multiplier: int = None) -> float:
    """This function will take string in hex format and will convert it in decimal format and also will multiply it
       by scaling factor(multiplier)

    Args:
        string (str): This is string in hex format.
        multiplier (int, optional): This is scaling factor Defaults to None.

    Returns:
        float: Desired output after converting it in decimal format and multiplying it by scaling factor
    """
    string = reverse_string_in_pair(string)
    if not multiplier:
        multiplier = 1.0
    req = int(string, 16) * multiplier
    return float(format(req, ".1f"))


def convert_and_handle_negative_values(string: str, multiplier: int = None) -> float:
    """This function will take string in hex format and will convert it in decimal format and also will multiply it
       by scaling factor(multiplier). Speciality of this function is this can also handle negative values

    Args:
        string (str): This is string in hex format.
        multiplier (int, optional): This is scaling factor. Defaults to None.

    Returns:
        float: Desired output after converting it in decimal format and multiplying it by scaling factor
    """
    new_string = reverse_string_in_pair(string)
    if new_string[0:2] == "FF":
        val = int("FFFF", 16) - int(new_string, 16)
        if multiplier:
            val *= multiplier
    else:
        val = convert_and_get_desired_value(string, multiplier=multiplier)

    return float(format(val, ".2f"))


def stark_parser_function(can_id: str, can_data: str) -> Dict:
    """This is the main parser function. It will return a response dict object with key as
       the relevant name of the value

    Args:
        can_id (str): It is the can id
        can_data (str): It is a hex formatted string with 16 character. e.g.8000A00348010600

    Returns:
        Dict: It is a map with key as the relevant name of the value
    """
    bms_data = {}

    controller_data = {}
    response = {}
    if can_data:

        can_data = can_data.rjust(16, "0")

        if can_id == "110":
            try:
                bms_data["balancingLimit"] = convert_and_get_desired_value(
                    string=can_data[:4], multiplier=0.1
                )

                bms_data["prechargeActive"] = convert_and_get_desired_value(
                    string=can_data[4:6]
                )

                bms_data["balancingActive"] = convert_and_get_desired_value(
                    string=can_data[6:8]
                )

                bms_data["Pack_I_Master"] = convert_and_get_desired_value(
                    string=can_data[8:], multiplier=0.01
                )
                response["BMS Balancing Limit"] = bms_data["balancingLimit"]
                response["BMS Pre charge Active"] = bms_data["prechargeActive"]
                response["BMS Balancing active"] = bms_data["balancingActive"]
                response["BMS Pack I Master"] = bms_data["Pack_I_Master"]

            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["balancingLimit"] = bms_data["prechargeActive"] = bms_data[
                    "balancingActive"
                ] = bms_data["Pack_I_Master"] = 0

        elif can_id == "111":
            try:
                bms_data["Pack_Q_SOC_Trimmed"] = convert_and_get_desired_value(
                    string=can_data[0:4], multiplier=0.01
                )
                bms_data["SOH"] = convert_and_get_desired_value(
                    string=can_data[4:8], multiplier=0.01
                )
                bms_data["BMSStatus"] = convert_and_get_desired_value(
                    string=can_data[8:10]
                )
                bms_data["FullyChargeFlag"] = check_is_battery_latched(
                    string=can_data[10:12]
                )
                bms_data["Pack_V_Sum_of_Cells"] = convert_and_get_desired_value(
                    string=can_data[12:], multiplier=0.1
                )

                response["BMS Pack_Q_SOC_Trimmed"] = bms_data["Pack_Q_SOC_Trimmed"]
                response["BMS SOH"] = bms_data["SOH"]
                response["BMS BMSStatus"] = bms_data["BMSStatus"]
                response["BMS FullyChargeFlag"] = bms_data["FullyChargeFlag"]
                response["BMS Pack_V_Sum_of_Cells"] = bms_data["Pack_V_Sum_of_Cells"]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["Pack_Q_SOC_Trimmed"] = bms_data["SOH"] = bms_data[
                    "BMSStatus"
                ] = bms_data["FullyChargeFlag"] = bms_data["Pack_V_Sum_of_Cells"] = 0
        elif can_id == "112":
            try:
                bms_data["Aux_T"] = convert_and_get_temperatures(string=can_data[0:12])

                bms_data["BatteryCapacity"] = convert_and_get_desired_value(
                    string=can_data[12:], multiplier=0.1
                )
                response["BMS Aux_T"] = ",".join(bms_data["Aux_T"])
                response["BMS BatteryCapacity"] = bms_data["BatteryCapacity"]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["Aux_T"] = ""
                bms_data["BatteryCapacity"] = 0
        elif can_id == "113":
            try:
                bms_data["CMU1_Cell_Vtgs"] = []

                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU1_Cell_Vtgs cell_1"] = bms_data["CMU1_Cell_Vtgs"][0]
                response["BMS CMU1_Cell_Vtgs cell_2"] = bms_data["CMU1_Cell_Vtgs"][1]
                response["BMS CMU1_Cell_Vtgs cell_3"] = bms_data["CMU1_Cell_Vtgs"][2]
                response["BMS CMU1_Cell_Vtgs cell_4"] = bms_data["CMU1_Cell_Vtgs"][3]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["CMU1_Cell_Vtgs"] = list()
        elif can_id == "114":
            try:
                bms_data["CMU1_Cell_Vtgs"] = []

                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU1_Cell_Vtgs cell_5"] = bms_data["CMU1_Cell_Vtgs"][0]
                response["BMS CMU1_Cell_Vtgs cell_6"] = bms_data["CMU1_Cell_Vtgs"][1]
                response["BMS CMU1_Cell_Vtgs cell_7"] = bms_data["CMU1_Cell_Vtgs"][2]
                response["BMS CMU1_Cell_Vtgs cell_8"] = bms_data["CMU1_Cell_Vtgs"][3]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["CMU1_Cell_Vtgs"] = list()
        elif can_id == "115":
            try:
                bms_data["CMU1_Cell_Vtgs"] = []

                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bms_data["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU1_Cell_Vtgs cell_9"] = bms_data["CMU1_Cell_Vtgs"][0]
                response["BMS CMU1_Cell_Vtgs cell_10"] = bms_data["CMU1_Cell_Vtgs"][1]
                response["BMS CMU1_Cell_Vtgs cell_11"] = bms_data["CMU1_Cell_Vtgs"][2]
                response["BMS CMU1_Cell_Vtgs cell_12"] = bms_data["CMU1_Cell_Vtgs"][3]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["CMU1_Cell_Vtgs"] = list()

        elif can_id == "116":
            try:
                bms_data["CMU2_Cell_Vtgs"] = []
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU2_Cell_Vtgs Cell 1"] = bms_data["CMU2_Cell_Vtgs"][0]
                response["BMS CMU2_Cell_Vtgs Cell 2"] = bms_data["CMU2_Cell_Vtgs"][1]
                response["BMS CMU2_Cell_Vtgs Cell 3"] = bms_data["CMU2_Cell_Vtgs"][2]
                response["BMS CMU2_Cell_Vtgs Cell 4"] = bms_data["CMU2_Cell_Vtgs"][3]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["CMU2_Cell_Vtgs"] = list()
        elif can_id == "117":
            try:
                if "CMU2_Cell_Vtgs" not in bms_data:
                    bms_data["CMU2_Cell_Vtgs"] = []
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU2_Cell_Vtgs Cell 5"] = bms_data["CMU2_Cell_Vtgs"][0]
                response["BMS CMU2_Cell_Vtgs Cell 6"] = bms_data["CMU2_Cell_Vtgs"][1]
                response["BMS CMU2_Cell_Vtgs Cell 7"] = bms_data["CMU2_Cell_Vtgs"][2]
                response["BMS CMU2_Cell_Vtgs Cell 8"] = bms_data["CMU2_Cell_Vtgs"][3]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["CMU2_Cell_Vtgs"] = list()
        elif can_id == "118":
            try:
                if "CMU2_Cell_Vtgs" not in bms_data:
                    bms_data["CMU2_Cell_Vtgs"] = []
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bms_data["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU2_Cell_Vtgs Cell 9"] = bms_data["CMU2_Cell_Vtgs"][0]
                response["BMS CMU2_Cell_Vtgs Cell 10"] = bms_data["CMU2_Cell_Vtgs"][1]
                response["BMS CMU2_Cell_Vtgs Cell 11"] = bms_data["CMU2_Cell_Vtgs"][2]
                response["BMS CMU2_Cell_Vtgs Cell 12"] = bms_data["CMU2_Cell_Vtgs"][3]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["CMU2_Cell_Vtgs"] = list()
        elif can_id == "11c":
            try:
                bms_data["PACK_Q_DESIGN"] = convert_and_get_desired_value(
                    can_data[0:4], multiplier=0.1
                )
                bms_data["PACK_Q_FULL"] = convert_and_get_desired_value(
                    can_data[4:8], multiplier=0.1
                )
                bms_data["CMU1_CELL_BITMASK"] = convert_and_get_desired_value(
                    can_data[8:12]
                )
                bms_data["CMU2_CELL_BITMASK"] = convert_and_get_desired_value(
                    can_data[12:]
                )

                response["BMS PACK_Q_DESIGN"] = bms_data["PACK_Q_DESIGN"]
                response["BMS PACK_Q_FULL"] = bms_data["PACK_Q_FULL"]
                response["BMS CMU1_CELL_BITMASK"] = bms_data["CMU1_CELL_BITMASK"]
                response["BMS CMU2_CELL_BITMASK"] = bms_data["CMU2_CELL_BITMASK"]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["PACK_Q_DESIGN"] = bms_data["PACK_Q_FULL"] = bms_data[
                    "CMU1_CELL_BITMASK"
                ] = bms_data["CMU2_CELL_BITMASK"] = 0
        elif can_id == "12a":
            try:
                bms_data["dynamic_in_limit"] = convert_and_get_desired_value(
                    can_data[:4], multiplier=0.1
                )
                bms_data["dynamic_out_limit"] = convert_and_get_desired_value(
                    can_data[4:8], multiplier=0.1
                )
                response["BMS dynamic_in_limit"] = bms_data["dynamic_in_limit"]
                response["BMS dynamic_out_limit"] = bms_data["dynamic_out_limit"]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                bms_data["dynamic_in_limit"] = bms_data["dynamic_out_limit"] = 0

        elif can_id == "705":
            try:
                controller_data["MotorTemp"] = convert_and_get_temperature(
                    string=can_data[0:2], roundabout=50
                )
                controller_data["Controller_Temp"] = convert_and_get_temperature(
                    string=can_data[2:4], roundabout=50
                )
                controller_data["SOC"] = convert_and_get_desired_value(can_data[4:6])
                controller_data[
                    "Batt_Discharge_Current_Rate"
                ] = convert_and_get_desired_value(can_data[6:8])
                controller_data["Odometer"] = convert_and_get_desired_value(
                    string=can_data[8:], multiplier=0.1
                )
                response["Controller MotorTemp"] = controller_data["MotorTemp"]
                response["Controller Controller_Temp"] = controller_data[
                    "Controller_Temp"
                ]
                response["Controller SOC"] = controller_data["SOC"]
                response["Controller Batt_Discharge_Current_Rate"] = controller_data[
                    "Batt_Discharge_Current_Rate"
                ]
                response["Controller Odometer"] = controller_data["Odometer"]
            except Exception as e:
                controller_data["MotorTemp"] = controller_data[
                    "Controller_Temp"
                ] = controller_data["SOC"] = controller_data[
                    "Batt_Discharge_Current_Rate"
                ] = controller_data[
                    "Odometer"
                ] = 0
        elif can_id == "706":
            try:
                controller_data["Vehicle_Status"] = convert_and_get_desired_value(
                    can_data[0:2]
                )
                controller_data["AssistLevelGear"] = convert_and_get_desired_value(
                    can_data[4:6]
                )
                controller_data["AlarmFault"] = convert_and_get_desired_value(
                    can_data[6:8]
                )
                controller_data["SpeedLowHigh"] = convert_and_handle_negative_values(
                    string=can_data[8:12], multiplier=0.1
                )
                controller_data["TripLowHigh"] = convert_and_get_desired_value(
                    string=can_data[12:]
                )
                response["Controller Vehicle_Status"] = controller_data[
                    "Vehicle_Status"
                ]
                response["Controller AssistLevelGear"] = controller_data[
                    "AssistLevelGear"
                ]
                response["Controller AlarmFault"] = controller_data["AlarmFault"]
                response["Controller SpeedLowHigh"] = controller_data["SpeedLowHigh"]
                response["Controller TripLowHigh"] = controller_data["TripLowHigh"]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["Vehicle_Status"] = controller_data[
                    "controller_mode"
                ] = controller_data["AssistLevelGear"] = controller_data[
                    "AlarmFault"
                ] = controller_data[
                    "SpeedLowHigh"
                ] = controller_data[
                    "TripLowHigh"
                ] = 0
        elif can_id == "708":
            try:
                controller_data["FaultStatus"] = [
                    convert_and_get_desired_value(can_data[0:2]),
                    convert_and_get_desired_value(can_data[2:4]),
                    convert_and_get_desired_value(can_data[4:6]),
                    convert_and_get_desired_value(can_data[6:8]),
                    convert_and_get_desired_value(can_data[8:10]),
                    convert_and_get_desired_value(can_data[10:12]),
                    convert_and_get_desired_value(can_data[12:14]),
                    convert_and_get_desired_value(can_data[14:16]),
                ]
                response["Controller Fault Status"] = ",".join(
                    controller_data["FaultStatus"]
                )
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["FaultStatus"] = list()
        elif can_id == "710":
            try:
                controller_data["ThrottleCommand"] = convert_and_get_desired_value(
                    string=can_data[0:2]
                )
                controller_data["ThrottleMultiplier"] = convert_and_get_desired_value(
                    string=can_data[2:4]
                )
                controller_data["MappedThrottle"] = convert_and_get_desired_value(
                    string=can_data[4:6]
                )
                controller_data[
                    "ThrottlePotentiometer"
                ] = convert_and_get_desired_value(string=can_data[6:8], multiplier=0.1)
                controller_data["BrakeCommand"] = convert_and_get_desired_value(
                    string=can_data[8:10], multiplier=1
                )
                controller_data["MappedBrake"] = convert_and_get_desired_value(
                    string=can_data[10:12], multiplier=1
                )
                controller_data["Potential2Row"] = convert_and_get_desired_value(
                    string=can_data[12:14], multiplier=0.1
                )
                response["Controller ThrottleCommand"] = controller_data[
                    "ThrottleCommand"
                ]
                response["Controller ThrottleMultiplier"] = controller_data[
                    "ThrottleMultiplier"
                ]
                response["Controller MappedThrottle"] = controller_data[
                    "MappedThrottle"
                ]
                response["Controller ThrottlePotentiometer"] = controller_data[
                    "ThrottlePotentiometer"
                ]
                response["Controller BrakeCommand"] = controller_data["BrakeCommand"]
                response["Controller MappedBrake"] = controller_data["MappedBrake"]
                response["Controller Potential2Row"] = controller_data["Potential2Row"]

            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["ThrottleCommand"] = controller_data[
                    "ThrottleMultiplier"
                ] = controller_data["MappedThrottle"] = controller_data[
                    "ThrottlePotentiometer"
                ] = controller_data[
                    "BrakeCommand"
                ] = controller_data[
                    "MappedBrake"
                ] = controller_data[
                    "Potential2Row"
                ] = 0
        elif can_id == "715":
            try:
                controller_data[
                    "BatteryCapacityVoltage"
                ] = convert_and_get_desired_value(string=can_data[8:10], multiplier=1)
                controller_data[
                    "BatteryKeyswitchVoltage"
                ] = convert_and_get_desired_value(string=can_data[10:12], multiplier=1)
                controller_data["MotorRPM"] = convert_and_handle_negative_values(
                    string=can_data[12:], multiplier=1
                )
                response["Controller BatteryCapacityVoltage"] = controller_data[
                    "BatteryCapacityVoltage"
                ]
                response["Controller BatteryKeyswitchVoltage"] = controller_data[
                    "BatteryKeyswitchVoltage"
                ]
                response["Controller MotorRPM"] = controller_data["MotorRPM"]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["BatteryCapacityVoltage"] = controller_data[
                    "BatteryKeyswitchVoltage"
                ] = controller_data["MotorRPM"] = 0
        elif can_id == "716":
            try:
                controller_data[
                    "ControllerMasterTimer"
                ] = convert_and_get_desired_value(string=can_data[2:10], multiplier=0.1)
                controller_data["ControllerCurrentRMS"] = convert_and_get_desired_value(
                    string=can_data[12:14], multiplier=1
                )
                controller_data[
                    "ControllerModulationDepth"
                ] = convert_and_get_desired_value(string=can_data[14:], multiplier=1)
                response["Controller ControllerMasterTimer"] = controller_data[
                    "ControllerMasterTimer"
                ]
                response["Controller ControllerCurrentRMS"] = controller_data[
                    "ControllerCurrentRMS"
                ]
                response["Controller ControllerModulationDepth"] = controller_data[
                    "ControllerModulationDepth"
                ]

            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["ControllerMasterTimer"] = controller_data[
                    "ControllerCurrentRMS"
                ] = controller_data["ControllerModulationDepth"] = 0
        elif can_id == "717":
            try:
                controller_data["ControllerFrequency"] = convert_and_get_desired_value(
                    string=can_data[0:4], multiplier=1
                )
                controller_data["ControllerMainState"] = convert_and_get_desired_value(
                    string=can_data[4:6], multiplier=1
                )
                response["Controller ControllerFrequency"] = controller_data[
                    "ControllerFrequency"
                ]
                response["Controller ControllerMainState"] = controller_data[
                    "ControllerMainState"
                ]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["ControllerFrequency"] = controller_data[
                    "ControllerMainState"
                ] = 0
        elif can_id == "724":
            try:
                controller_data[
                    "MotorTorqueEstimated"
                ] = convert_and_handle_negative_values(
                    string=can_data[0:4], multiplier=0.1
                )

                controller_data["BatteryPowerConsumed"] = convert_and_get_desired_value(
                    string=can_data[4:6], multiplier=0.1
                )
                controller_data[
                    "BatteryEnergyConsumed"
                ] = convert_and_get_desired_value(string=can_data[6:8], multiplier=0.1)
                controller_data["VehiclePowerMode"] = convert_and_get_desired_value(
                    string=can_data[8:10]
                )
                response["Controller MotorTorqueEstimated"] = controller_data[
                    "MotorTorqueEstimated"
                ]
                response["Controller BatteryPowerConsumed"] = controller_data[
                    "BatteryPowerConsumed"
                ]
                response["Controller BatteryEnergyConsumed"] = controller_data[
                    "BatteryEnergyConsumed"
                ]
                response["Controller VehiclePowerMode"] = controller_data[
                    "VehiclePowerMode"
                ]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["MotorTorqueEstimated"] = controller_data[
                    "BatteryPowerConsumed"
                ] = controller_data["BatteryEnergyConsumed"] = controller_data[
                    "VehiclePowerMode"
                ] = 0
        elif can_id == "725":
            try:
                controller_data["AccelerationRate"] = convert_and_get_desired_value(
                    string=can_data[0:2], multiplier=0.1
                )
                controller_data[
                    "AccelerationReleaseRate"
                ] = convert_and_get_desired_value(string=can_data[2:4], multiplier=0.1)
                controller_data["BrakeRate"] = convert_and_get_desired_value(
                    string=can_data[4:6], multiplier=0.1
                )
                controller_data["DriveCurrentLimit"] = convert_and_get_desired_value(
                    string=can_data[6:8], multiplier=1
                )
                controller_data["RegenCurrentLimit"] = convert_and_get_desired_value(
                    string=can_data[8:10], multiplier=1
                )
                controller_data["BrakeCurrentLimit"] = convert_and_get_desired_value(
                    string=can_data[10:12], multiplier=1
                )
                controller_data["RegenOff"] = 0 if can_data[12:14] == "FF" else 1
                controller_data[
                    "ControllerResetCANBaudRate"
                ] = convert_and_get_desired_value(string=can_data[14:], multiplier=1)
                response["Controller AccelerationRate"] = controller_data[
                    "AccelerationRate"
                ]
                response["Controller AccelerationReleaseRate"] = controller_data[
                    "AccelerationReleaseRate"
                ]
                response["Controller BrakeRate"] = controller_data["BrakeRate"]
                response["Controller DriveCurrentLimit"] = controller_data[
                    "DriveCurrentLimit"
                ]
                response["Controller RegenCurrentLimit"] = controller_data[
                    "RegenCurrentLimit"
                ]
                response["Controller BrakeCurrentLimit"] = controller_data[
                    "BrakeCurrentLimit"
                ]
                response["Controller RegenOff"] = controller_data["RegenOff"]
                response["Controller ControllerResetCANBaudRate"] = controller_data[
                    "ControllerResetCANBaudRate"
                ]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["AccelerationRate"] = controller_data[
                    "AccelerationReleaseRate"
                ] = controller_data["BrakeRate"] = controller_data[
                    "DriveCurrentLimit"
                ] = controller_data[
                    "RegenCurrentLimit"
                ] = controller_data[
                    "BrakeCurrentLimit"
                ] = controller_data[
                    "RegenOff"
                ] = controller_data[
                    "ControllerResetCANBaudRate"
                ] = 0
        elif can_id == "726":
            try:
                controller_data[
                    "ControllerSerialNumber"
                ] = convert_and_get_desired_value(can_data[0:8])
                controller_data["VCLVersion"] = convert_and_get_desired_value(
                    can_data[8:10]
                )
                controller_data["VCLBuildNumber"] = convert_and_get_desired_value(
                    can_data[10:12]
                )
                controller_data["OSVersion"] = convert_and_get_desired_value(
                    can_data[12:14]
                )
                controller_data["OSBuildNumber"] = convert_and_get_desired_value(
                    can_data[14:]
                )
                response["Controller ControllerSerialNumber"] = controller_data[
                    "ControllerSerialNumber"
                ]
                response["Controller VCLVersion"] = controller_data["VCLVersion"]
                response["Controller VCLBuildNumber"] = controller_data[
                    "VCLBuildNumber"
                ]
                response["Controller OSVersion"] = controller_data["OSVersion"]
                response["Controller OSBuildNumber"] = controller_data["OSBuildNumber"]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["ControllerSerialNumber"] = controller_data[
                    "VCLVersion"
                ] = controller_data["VCLBuildNumber"] = controller_data[
                    "OSVersion"
                ] = controller_data[
                    "OSBuildNumber"
                ] = 0
        elif can_id == "258":
            try:
                controller_data[
                    "Number_of_Active_Errors"
                ] = convert_and_get_desired_value(string=can_data[8:12], multiplier=1)
                response["Number_of_Active_Errors"] = controller_data[
                    "Number_of_Active_Errors"
                ]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["Number_of_Active_Errors"] = 0
        elif can_id == "259":
            try:
                controller_data[
                    "Sum_of_error_since_boot"
                ] = convert_and_get_desired_value(string=can_data[8:], multiplier=1)
                response["Sum_of_error_since_boot"] = controller_data[
                    "Sum_of_error_since_boot"
                ]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["Sum_of_error_since_boot"] = 0
        elif can_id == "1806e5f4":
            try:
                controller_data["Ch_V"] = convert_and_get_desired_value(
                    string=can_data[:4], multiplier=1
                )
                controller_data["Ch_C"] = convert_and_get_desired_value(
                    string=can_data[4:8], multiplier=1
                )
                controller_data["Ch_S"] = convert_and_get_desired_value(
                    string=can_data[8:10], multiplier=1
                )
                response["Ch_V"] = controller_data["Ch_V"]
                response["Ch_C"] = controller_data["Ch_C"]
                response["Ch_S"] = controller_data["Ch_S"]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["Ch_C"] = controller_data["Ch_V"] = controller_data[
                    "Ch_S"
                ] = 0
        elif can_id == "7a0":
            try:
                controller_data["Device_id_VCU"] = convert_and_get_desired_value(
                    string=can_data[:2], multiplier=1
                )
                controller_data["Version_Major"] = convert_and_get_desired_value(
                    string=can_data[2:4], multiplier=1
                )
                controller_data["Version_Minor"] = convert_and_get_desired_value(
                    string=can_data[4:6], multiplier=1
                )
                controller_data["Patch"] = convert_and_get_desired_value(
                    string=can_data[6:8], multiplier=1
                )
                controller_data[
                    "Build_Type_and_Production_Build"
                ] = convert_and_get_desired_value(string=can_data[8:10], multiplier=1)
                response["Device_id_VCU"] = controller_data["Device_id_VCU"]
                response["Version_Major"] = controller_data["Version_Major"]
                response["Version_Minor"] = controller_data["Version_Minor"]
                response["Patch"] = controller_data["Patch"]
                response["Build_Type_and_Production_Build"] = controller_data[
                    "Build_Type_and_Production_Build"
                ]
            except Exception as e:
                can_logging_parsing_error_logger.error(e)
                controller_data["Ch_C"] = controller_data["Ch_V"] = controller_data[
                    "Ch_S"
                ] = 0

    return response
