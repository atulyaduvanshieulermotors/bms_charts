from typing import Dict, List

import ast
from matplotlib import pyplot as plt    

from bms_validation_map import bms_validation

from testing_module.can_data_logging_and_parsing import extract_can_id_data, log_can_data

reverse_string_in_pair = lambda string: "".join(
    reversed([string[idx : idx + 2] for idx in range(0, len(string), 2)])
)

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

def convert_and_get_current_val(string: str, roundabout, multiplier) -> float:
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
    if new_string[0:4] == "ffff":
        val = int("FFFF", 16) - int(new_string[4:], 16)
        if multiplier:
            val *= multiplier
    else:
        val = convert_and_get_desired_value(string, multiplier=multiplier)

    return float(format(val, ".2f"))

def desired_decimal_number(data, roundabout, multiplier):
    '''
        This function will reverse the string and convert hex format into decimal format.
    '''
    
    hex_string = "".join(reversed([data[idx : idx + 2] for idx in range(0, len(data), 2)]))

    return (int(hex_string, 16)-roundabout) * multiplier


def get_values():

    print("Logging Data....")

    log_can_data()
    
    print("Reading and Plotting....")
    can_ids, can_data = extract_can_id_data()
    
    pack_voltage = []
    pack_current = []
    pack_soc = []
    avg_aux_temp = []
    aux_temp = []
    for idx, can_id in enumerate(can_ids):
        for mapp in bms_validation:
            if mapp["can_id"] == can_id:
                
                start_bit = mapp["can_id_start_bit"]*2
                end_bit = (mapp["can_id_end_bit"]+1)*2

                # data_point_value = desired_decimal_number( can_data[idx][start_bit : end_bit], mapp["roundabout"], mapp["multiplier"] )
                
                if can_id == "111" and mapp["can_id_start_bit"] == 6 and mapp["can_id_end_bit"] == 7:
                    
                    res = convert_and_get_desired_value(string=can_data[idx][12:], multiplier=0.1)
                    pack_voltage.append(res)
                
                if can_id == "110" and mapp["can_id_start_bit"] == 4 and mapp["can_id_end_bit"] == 7:
                    # res = ast.literal_eval(can_data[idx][8:])
                    res = convert_and_handle_negative_values(string=can_data[idx][8:], multiplier=0.01)
                    pack_current.append(res)

                if can_id == "111" and mapp["can_id_start_bit"] == 0 and mapp["can_id_end_bit"] == 1:
                    
                    res = convert_and_get_desired_value(string=can_data[idx][0:4], multiplier=0.01)
                    
                    pack_soc.append(res)

                if can_id == "112" and mapp["name"][:8] == "Aux Temp":
                    
                    if mapp["name"] == "Aux Temperature_1":
                        res = convert_and_get_temperatures(string=can_data[idx][0:12])
                        print(sum(res)/6)
                        avg_aux_temp.append(sum(res)/6)


    return [pack_current, pack_voltage, pack_soc, avg_aux_temp]