"""
This module is used to hash any string using sha_256 converter
"""
import hashlib

def converter(string: str) -> str:
    """This function will take any string and will hash is using sha256 converter.

    Args:
        string (str): This is the raw string(unhashed)

    Returns:
        string (str): It will output hashed string
    """

    bytes_string = string.encode()
    res = hashlib.sha256(bytes_string).hexdigest()
    return res
