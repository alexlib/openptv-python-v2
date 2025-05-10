"""
Utility functions for parameter handling.

This module provides utility functions for parameter handling, such as
copying parameter directories and converting between Python and C types.
"""

import os
import shutil
from pathlib import Path
from typing import Union, TextIO

# Re-export these for backward compatibility
__all__ = ['par_dir_prefix', 'copy_params_dir', 'bool_to_int', 'int_to_bool', 'write_line_to_file']

# Define these functions here directly
def par_dir_prefix():
    """
    Get the prefix for parameter directories.

    Returns:
        str: The prefix for parameter directories.
    """
    return "parameters"


def copy_params_dir(src_path, dst_path):
    """
    Copy parameter files from one directory to another.
    """
    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)



def bool_to_int(value):
    """
    Convert a boolean value to an integer (0 or 1).

    Args:
        value: A boolean value or an integer.

    Returns:
        int: 1 if value is True, 0 if value is False.
    """
    if isinstance(value, bool):
        return 1 if value else 0
    return value


def int_to_bool(value: int) -> bool:
    """
    Convert an integer value (0 or 1) to a boolean.
    """
    return bool(value)


def g(f):
    """
    Read a line from a file and strip whitespace.

    Args:
        f: A file object.

    Returns:
        str: The line read from the file, with whitespace stripped.
    """
    return f.readline().strip()


def encode_if_needed(s: Union[str, bytes, None]) -> Union[bytes, None]:
    """
    Encode a string to bytes if it's a string, otherwise return it unchanged.

    Args:
        s: A string, bytes object, or None.

    Returns:
        Union[bytes, None]: The encoded string if s was a string, or s unchanged if it was
                            already bytes or None.
    """
    return s.encode('utf-8') if isinstance(s, str) else s


def decode_if_needed(b: Union[bytes, str, None]) -> Union[str, None]:
    """
    Decode bytes to a string if needed, otherwise return as is.
    """
    if isinstance(b, bytes):
        return b.decode('utf-8')
    return b


# Removed the redundant read_line function as it duplicates the functionality of g.



def write_line_to_file(f: TextIO, line):
    """
    Write a line to a file, adding a newline character.

    Args:
        f: A file object.
        line: The line to write.
    """
    try:
        f.write(f"{line}\n")
    except IOError as e:
        raise IOError(f"Failed to write to file: {e}")
