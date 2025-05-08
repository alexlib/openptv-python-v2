"""
Examine parameters for OpenPTV.

This module provides the ExamineParams class for handling examine parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g, bool_to_int, int_to_bool


class ExamineParams(Parameters):
    """
    Examine parameters for OpenPTV.

    This class handles reading and writing examine parameters to/from files.
    """

    def __init__(self, Examine_Flag=False, Combine_Flag=False, path=None):
        """
        Initialize examine parameters.

        Args:
            Examine_Flag (bool): Examine flag.
            Combine_Flag (bool): Combine flag.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(Examine_Flag, Combine_Flag)

    def set(self, Examine_Flag=False, Combine_Flag=False):
        """
        Set examine parameters.

        Args:
            Examine_Flag (bool): Examine flag.
            Combine_Flag (bool): Combine flag.
        """
        self.Examine_Flag = Examine_Flag
        self.Combine_Flag = Combine_Flag

    def filename(self):
        """
        Get the filename for examine parameters.

        Returns:
            str: The filename for examine parameters.
        """
        return "examine.par"

    def _read_from_file(self):
        """
        Read examine parameters from file.

        Raises:
            IOError: If the file cannot be read.
        """
        if not self.filepath().exists():
            # Create default file if it doesn't exist
            self.write()
            return

        try:
            with open(self.filepath(), "r") as f:
                self.Examine_Flag = int_to_bool(int(g(f)))
                self.Combine_Flag = int_to_bool(int(g(f)))
        except Exception as e:
            raise IOError(f"Error reading examine parameters: {e}")

    def read(self):
        """
        Read examine parameters from file.

        Raises:
            IOError: If the file cannot be read.
        """
        self._read_from_file()
        return self

    @classmethod
    def from_file(cls, path):
        """
        Class method to create an instance and read parameters from file.

        Args:
            path: Path to the parameter directory.

        Returns:
            ExamineParams: A new ExamineParams object with parameters read from file.

        Raises:
            IOError: If the file cannot be read.
        """
        instance = cls(path=path)
        instance._read_from_file()
        return instance

    def write(self):
        """
        Write examine parameters to file.

        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                f.write(f"{bool_to_int(self.Examine_Flag)}\n")
                f.write(f"{bool_to_int(self.Combine_Flag)}\n")
        except Exception as e:
            raise IOError(f"Error writing examine parameters: {e}")

    def to_c_struct(self):
        """
        Convert examine parameters to a dictionary suitable for creating a C struct.

        Returns:
            dict: A dictionary of examine parameter values.
        """
        return {
            'Examine_Flag': bool_to_int(self.Examine_Flag),
            'Combine_Flag': bool_to_int(self.Combine_Flag),
        }

    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create an ExamineParams object from a C struct.

        Args:
            c_struct: A dictionary of examine parameter values from a C struct.
            path: Path to the parameter directory.

        Returns:
            ExamineParams: A new ExamineParams object.
        """
        return cls(
            Examine_Flag=int_to_bool(c_struct['Examine_Flag']),
            Combine_Flag=int_to_bool(c_struct['Combine_Flag']),
            path=path,
        )
