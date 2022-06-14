"""
This module will take raw can log data from .txt file and
will output the processed data in a .csv file
"""

import codecs
import csv

from .can_id_data_extract import extract_can_id_data
from .stark_parser import stark_parser_function

from ..shared import can_logging_parsing_error_logger


def parse_can_data(vehicle_session_id: str):
    """
    This module will take raw can log data from *.txt file and
    will output the processed data in a *.csv file
    """
    try:
        trimmed_can_ids, can_data = extract_can_id_data(vehicle_session_id)

        with codecs.open(
            "testing_module/can_data_logging_and_parsing/"
            + vehicle_session_id
            + ".csv",
            "w",
            "UTF8",
        ) as output_file:
            header = ["Name", "Value"]
            writer = csv.writer(output_file)
            writer.writerow(header)

            for idx in range(len(trimmed_can_ids)):
                response = stark_parser_function(trimmed_can_ids[idx], can_data[idx])
                # response is a dict object with data_name as key and data_value as value
                for key in response.keys():
                    writer.writerow([key, response[key]])
    except Exception as e:
        can_logging_parsing_error_logger.exception(
            "UUID is: %s - Exception is: %s" % (vehicle_session_id, e)
        )
        return "Please log data again."
