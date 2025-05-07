"""
Dumbbell parameters for OpenPTV.

This module provides the DumbbellParams class for handling dumbbell parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g, bool_to_int, int_to_bool


class DumbbellParams(Parameters):
    """
    Dumbbell parameters for OpenPTV.
    
    This class handles reading and writing dumbbell parameters to/from files.
    """
    
    def __init__(self, acc=0.0, dumbbell_scale=0.0, eps0=0.0, path=None):
        """
        Initialize dumbbell parameters.
        
        Args:
            acc (float): Accuracy.
            dumbbell_scale (float): Dumbbell scale.
            eps0 (float): Epipolar line width.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(acc, dumbbell_scale, eps0)
    
    def set(self, acc=0.0, dumbbell_scale=0.0, eps0=0.0):
        """
        Set dumbbell parameters.
        
        Args:
            acc (float): Accuracy.
            dumbbell_scale (float): Dumbbell scale.
            eps0 (float): Epipolar line width.
        """
        self.acc = acc
        self.dumbbell_scale = dumbbell_scale
        self.eps0 = eps0
    
    def filename(self):
        """
        Get the filename for dumbbell parameters.
        
        Returns:
            str: The filename for dumbbell parameters.
        """
        return "dumbbell.par"
    
    def read(self):
        """
        Read dumbbell parameters from file.
        
        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.acc = float(g(f))
                self.dumbbell_scale = float(g(f))
                self.eps0 = float(g(f))
        except Exception as e:
            raise IOError(f"Error reading dumbbell parameters: {e}")
    
    def write(self):
        """
        Write dumbbell parameters to file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                f.write(f"{self.acc}\n")
                f.write(f"{self.dumbbell_scale}\n")
                f.write(f"{self.eps0}\n")
        except Exception as e:
            raise IOError(f"Error writing dumbbell parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert dumbbell parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of dumbbell parameter values.
        """
        return {
            'acc': self.acc,
            'dumbbell_scale': self.dumbbell_scale,
            'eps0': self.eps0,
        }
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a DumbbellParams object from a C struct.
        
        Args:
            c_struct: A dictionary of dumbbell parameter values from a C struct.
            path: Path to the parameter directory.
        
        Returns:
            DumbbellParams: A new DumbbellParams object.
        """
        return cls(
            acc=c_struct['acc'],
            dumbbell_scale=c_struct['dumbbell_scale'],
            eps0=c_struct['eps0'],
            path=path,
        )
