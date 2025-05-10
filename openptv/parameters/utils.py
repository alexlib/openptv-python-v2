"""
Utility functions for parameter handling.

This module provides utility functions for parameter handling, such as
copying parameter directories and converting between Python and C types.
"""

import os
import shutil
from pathlib import Path

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

    Args:
        src_path: Source directory path.
        dst_path: Destination directory path.
    """
    # Create destination directory if it doesn't exist
    dst_path = Path(dst_path)
    dst_path.mkdir(exist_ok=True)

    # Copy parameter files
    src_path = Path(src_path)
    for file_path in src_path.glob("*"):
        if file_path.is_file():
            shutil.copy(file_path, dst_path / file_path.name)

# Re-export these for backward compatibility
__all__ = ['par_dir_prefix', 'copy_params_dir', 'bool_to_int', 'int_to_bool', 'read_line', 'write_line',
           'encode_if_needed', 'decode_if_needed', 'prepare_tracker_paths']


def prepare_tracker_paths(paths_dict):
    """
    Prepare file paths for the tracker.

    This function takes a dictionary of file paths and ensures that:
    1. All paths are properly normalized
    2. All directories exist
    3. All paths are encoded to bytes if needed

    Args:
        paths_dict: A dictionary with keys 'corres', 'linkage', 'prio' and
                   string or bytes values

    Returns:
        dict: A dictionary with the same keys but with properly prepared paths
    """
    result = {}

    for key, path in paths_dict.items():
        # Encode the path if it's a string
        if isinstance(path, str):
            # Normalize the path
            import os
            normalized_path = os.path.normpath(path)

            # Make sure we're using forward slashes for consistency
            normalized_path = normalized_path.replace('\\', '/')

            # Ensure the directory exists
            directory = os.path.dirname(normalized_path)
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except OSError:
                    # Directory might have been created by another process
                    pass

            # Use the simplest possible path - just the basename
            # The C code seems to have issues with directory paths
            basename = os.path.basename(normalized_path)
            result[key] = basename.encode('utf-8')
        else:
            # Already bytes or None
            result[key] = path

    return result


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


def int_to_bool(value):
    """
    Convert an integer value (0 or 1) to a boolean.

    Args:
        value: An integer value or a boolean.

    Returns:
        bool: True if value is non-zero, False if value is zero.
    """
    if isinstance(value, int):
        return value != 0
    return value


def g(f):
    """
    Read a line from a file and strip whitespace.

    Args:
        f: A file object.

    Returns:
        str: The line read from the file, with whitespace stripped.
    """
    return f.readline().strip()


def encode_if_needed(s):
    """
    Encode a string to bytes if it's a string, otherwise return it unchanged.

    This function is used to ensure that strings are properly encoded to bytes
    before being passed to C functions that expect byte strings.

    Args:
        s: A string or bytes object, or None

    Returns:
        bytes: The encoded string if s was a string, or s unchanged if it was
               already bytes or None
    """
    if s is None:
        return None
    elif isinstance(s, str):
        # Ensure the path is properly normalized before encoding
        import os
        normalized_path = os.path.normpath(s)

        # Make sure we're using forward slashes for consistency
        normalized_path = normalized_path.replace('\\', '/')

        # Ensure the directory exists if this is a path
        directory = os.path.dirname(normalized_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError:
                # Directory might have been created by another process
                pass

        return normalized_path.encode('utf-8')
    else:
        return s


def decode_if_needed(b):
    """
    Decode bytes to a string if it's bytes, otherwise return it unchanged.

    This function is used to ensure that byte strings returned from C functions
    are properly decoded to Python strings.

    Args:
        b: A bytes or string object, or None

    Returns:
        str: The decoded bytes if b was bytes, or b unchanged if it was
             already a string or None
    """
    if b is None:
        return None
    elif isinstance(b, bytes):
        return b.decode('utf-8')
    else:
        return b


def read_line(f):
    """
    Read a line from a file and strip whitespace.

    Args:
        f: A file object.

    Returns:
        str: The line read from the file, with whitespace stripped.
    """
    return f.readline().strip()


def write_line(f, line):
    """
    Write a line to a file, adding a newline character.

    Args:
        f: A file object.
        line: The line to write.
    """
    f.write(f"{line}\n")
