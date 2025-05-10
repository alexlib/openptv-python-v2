"""
Sequence parameters for OpenPTV.

This module provides the SequenceParams class for handling sequence parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g


class SequenceParams(Parameters):
    """
    Sequence parameters for OpenPTV.
    
    This class handles reading and writing sequence parameters to/from files,
    and converting between Python and C representations.
    """
    
    def __init__(self, num_cams=0, base_name=None, first=0, last=0, path=None):
        """
        Initialize sequence parameters.
        
        Args:
            num_cams (int): Number of cameras.
            base_name (list): List of base names for image sequences.
            first (int): First frame number.
            last (int): Last frame number.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(num_cams, base_name, first, last)
    
    def set(self, num_cams=0, base_name=None, first=0, last=0):
        """
        Set sequence parameters.
        
        Args:
            num_cams (int): Number of cameras.
            base_name (list): List of base names for image sequences.
            first (int): First frame number.
            last (int): Last frame number.
        """
        self.num_cams = num_cams
        self.base_name = base_name or []
        # Ensure base_name has num_cams elements
        if len(self.base_name) < self.num_cams:
            self.base_name.extend([''] * (self.num_cams - len(self.base_name)))
        self.first = first
        self.last = last
    
    def filename(self):
        """
        Get the filename for sequence parameters.
        
        Returns:
            str: The filename for sequence parameters.
        """
        return "sequence.par"
    
    def read(self):
        """
        Read sequence parameters from file.
        
        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.base_name = []
                for i in range(self.num_cams):
                    self.base_name.append(g(f))
                self.first = int(g(f))
                self.last = int(g(f))
        except Exception as e:
            raise IOError(f"Error reading sequence parameters: {e}")
    
    def write(self):
        """
        Write sequence parameters to file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                for i in range(self.num_cams):
                    f.write(f"{self.base_name[i]}\n")
                f.write(f"{self.first}\n")
                f.write(f"{self.last}\n")
        except Exception as e:
            raise IOError(f"Error writing sequence parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert sequence parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of sequence parameter values.
        """
        return {
            'num_cams': self.num_cams,
            'img_base_name': self.base_name,
            'first': self.first,
            'last': self.last,
        }
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a SequenceParams object from a C struct.
        
        Args:
            c_struct: A dictionary of sequence parameter values from a C struct.
            path: Path to the parameter directory.
        
        Returns:
            SequenceParams: A new SequenceParams object.
        """
        return cls(
            num_cams=c_struct['num_cams'],
            base_name=c_struct['img_base_name'],
            first=c_struct['first'],
            last=c_struct['last'],
            path=path,
        )
    
    def to_cython(self):
        from openptv.binding.param_bridge import sequence_params_to_c
        return sequence_params_to_c(self)
