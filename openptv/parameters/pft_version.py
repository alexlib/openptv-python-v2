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
    
    def __init__(self, version=0, path=None):
        """
        Initialize PFT version parameters.
        
        Args:
            version (int): PFT version.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(version)
    
    def set(self, version=0):
        """
        Set PFT version parameters.
        
        Args:
            version (int): PFT version.
        """
        self.version = version
    
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
                self.version = int(g(f))
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
                f.write(f"{self.version}\n")
        except Exception as e:
            raise IOError(f"Error writing PFT version parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert PFT version parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of PFT version parameter values.
        """
        return {
            'version': self.version,
        }
    
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
            version=c_struct['version'],
            path=path,
        )
