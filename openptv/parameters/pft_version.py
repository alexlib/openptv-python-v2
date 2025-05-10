"""
PFT version parameters for OpenPTV.

This module provides the PftVersionParams class for handling PFT version parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g


class PftVersionParams(Parameters):
    """
    PFT version parameters for OpenPTV.

    This class handles reading and writing PFT version parameters to/from files.
    """

    def __init__(self, existing_target=False, Existing_Target=None, path=None, **kwargs):
        """
        Initialize PFT version parameters.

        Args:
            existing_target (bool): Whether to use existing targets.
            Existing_Target (bool): Alternative name for existing_target (for backward compatibility).
            path (str or Path): Path to the parameter directory.
            **kwargs: Additional keyword arguments to ignore.
        """
        super().__init__(path)
        # Use Existing_Target if provided, otherwise use existing_target
        et = Existing_Target if Existing_Target is not None else existing_target
        self.set(existing_target=et)

    def set(self, version=0, existing_target=False):
        """
        Set PFT version parameters.

        Args:
            version (int): PFT version.
            existing_target (bool): Whether to use existing targets.
        """
        self.existing_target = existing_target

    def filename(self):
        """
        Get the filename for PFT version parameters.

        Returns:
            str: The filename for PFT version parameters.
        """
        return "pft_version.par"

    def read(self):
        """
        Read PFT version parameters from file.

        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                # self.version = int(g(f))
                try:
                    self.existing_target = bool(int(g(f)))
                except:
                    # If the file doesn't have the existing_target parameter, use the default
                    self.existing_target = False
        except Exception as e:
            raise IOError(f"Error reading PFT version parameters: {e}")

    def write(self):
        """
        Write PFT version parameters to file.

        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                # f.write(f"{self.version}\n")
                f.write(f"{int(self.existing_target)}\n")
        except Exception as e:
            raise IOError(f"Error writing PFT version parameters: {e}")

    def to_c_struct(self):
        """
        Convert PFT version parameters to a dictionary suitable for creating a C struct.

        Returns:
            dict: A dictionary of PFT version parameter values.
        """
        return {
            # 'version': self.version,
            'existing_target': self.existing_target,
        }

    # Add property for backward compatibility
    @property
    def Existing_Target(self):
        """Backward compatibility property for existing_target."""
        return self.existing_target

    @Existing_Target.setter
    def Existing_Target(self, value):
        """Backward compatibility setter for existing_target."""
        self.existing_target = value

    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a PftVersionParams object from a C struct.

        Args:
            c_struct: A dictionary of PFT version parameter values from a C struct.
            path: Path to the parameter directory.

        Returns:
            PftVersionParams: A new PftVersionParams object.
        """
        return cls(
            # version=c_struct['version'],
            existing_target=c_struct.get('existing_target', False),
            path=path,
        )
