"""
Manual orientation parameters for OpenPTV.

This module provides the ManOriParams class for handling manual orientation parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g


class ManOriParams(Parameters):
    """
    Manual orientation parameters for OpenPTV.
    
    This class handles reading and writing manual orientation parameters to/from files.
    """
    
    def __init__(self, n_img=0, nr=None, path=None):
        """
        Initialize manual orientation parameters.
        
        Args:
            n_img (int): Number of cameras.
            nr (list): List of point numbers.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(n_img, nr)
    
    def set(self, n_img=0, nr=None):
        """
        Set manual orientation parameters.
        
        Args:
            n_img (int): Number of cameras.
            nr (list): List of point numbers.
        """
        self.n_img = n_img
        self.nr = nr or []
        
        # Ensure nr has n_img * 4 elements (4 points per camera)
        if len(self.nr) < self.n_img * 4:
            self.nr.extend([0] * (self.n_img * 4 - len(self.nr)))
    
    def filename(self):
        """
        Get the filename for manual orientation parameters.
        
        Returns:
            str: The filename for manual orientation parameters.
        """
        return "man_ori.par"
    
    def read(self):
        """
        Read manual orientation parameters from file.
        
        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.nr = []
                for i in range(self.n_img * 4):
                    self.nr.append(int(g(f)))
        except Exception as e:
            raise IOError(f"Error reading manual orientation parameters: {e}")
    
    def write(self):
        """
        Write manual orientation parameters to file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                for i in range(self.n_img * 4):
                    f.write(f"{self.nr[i]}\n")
        except Exception as e:
            raise IOError(f"Error writing manual orientation parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert manual orientation parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of manual orientation parameter values.
        """
        return {
            'n_img': self.n_img,
            'nr': self.nr,
        }
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a ManOriParams object from a C struct.
        
        Args:
            c_struct: A dictionary of manual orientation parameter values from a C struct.
            path: Path to the parameter directory.
        
        Returns:
            ManOriParams: A new ManOriParams object.
        """
        return cls(
            n_img=c_struct['n_img'],
            nr=c_struct['nr'],
            path=path,
        )
