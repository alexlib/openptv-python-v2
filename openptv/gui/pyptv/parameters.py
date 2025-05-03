"""
Parameters module for PyPTV.

This module provides functions for reading and writing parameter files.
"""

import os
import shutil
from pathlib import Path


def g(f):
    """ Returns a line without white spaces """
    return f.readline().strip()


# Base class for all parameters classes
class Parameters:
    # default path of the directory of the param files
    default_path = Path("parameters")

    def __init__(self, path=default_path):
        if isinstance(path, str):
            path = Path(path)
            
        self.path = path.resolve()
        self.exp_path = self.path.parent 

    # returns the name of the specific params file
    def filename(self):
        raise NotImplementedError()

    # returns the path to the specific params file
    def filepath(self):
        return self.path.joinpath(self.filename())

    # sets all variables of the param file (no actual writing to disk)
    def set(self, *vars):
        raise NotImplementedError()

    # reads a param file and stores it in the object
    def read(self):
        raise NotImplementedError()


def copy_params_dir(src_path, dst_path):
    """
    Copy a directory of parameter files.
    
    Args:
        src_path: Source directory path
        dst_path: Destination directory path
    """
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    
    # Copy all files from source to destination
    for item in os.listdir(src_path):
        src_item = os.path.join(src_path, item)
        dst_item = os.path.join(dst_path, item)
        if os.path.isfile(src_item):
            shutil.copy2(src_item, dst_item)
        elif os.path.isdir(src_item):
            shutil.copytree(src_item, dst_item)


# Print detailed error to the console and show the user a friendly error window
def error(owner, msg):
    print(f"Exception caught, message: {msg}")
