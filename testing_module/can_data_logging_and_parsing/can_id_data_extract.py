'''
This module will be used to extract CAN ID and CAN data present in CAN log.
'''
import codecs
import re

from ..can_module import CANDataLoggingError
from ..shared import can_logging_parsing_error_logger

def extract_can_id_data():
    """
    It takes a vehicle session id as input and returns a list of can ids and a list of can data
    
    :param vehicle_session_id: This is the UUID of the vehicle session
    :type vehicle_session_id: str
    :return: A list of can_ids and a list of can_data
    Exceptions:
        CANDataLoggingError
    """

    try:
        with codecs.open(
            "testing_module/can_data_logging_and_parsing/recent_can_log.txt",
            "r",
            "UTF8",
        ) as can_log_file:
            input_file = can_log_file.readlines()

        can_ids = []
        can_data = []

        for line in input_file:
            try:
                req = [s for s in line.split(" ") if s != ""]
                # 3rd index contains can_id
                if req == None or req[0] == None:
                    continue
                can_ids.append(req[3])

                # from index 8 to 16 in req contains can_id_data in hex format
                can_data.append("".join(req[8:16]))
            except Exception as e:
                can_logging_parsing_error_logger.exception(e)

        trimmed_can_ids = []
        for can_id in can_ids:
            # can ids come in format like "0020" but we want our can id only as "20"
            if can_id[0] == "0":
                for idx in range(len(can_id)):
                    if can_id[idx] != "0":
                        trimmed_can_ids.append(can_id[idx:])
                        break
            else:
                trimmed_can_ids.append(can_id)

        return trimmed_can_ids, can_data
    
    except Exception as e:
        can_logging_parsing_error_logger.exception(
            "Exception is: %s" % (e)
        )
        raise CANDataLoggingError
