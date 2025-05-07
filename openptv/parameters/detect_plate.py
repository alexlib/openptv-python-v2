"""
Detect plate parameters for OpenPTV.

This module provides the DetectPlateParams class for handling detect plate parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g, bool_to_int, int_to_bool


class DetectPlateParams(Parameters):
    """
    Detect plate parameters for OpenPTV.
    
    This class handles reading and writing detect plate parameters to/from files.
    """
    
    def __init__(self, gvthres=0, tolerable_discontinuity=0, min_npix=0, max_npix=0,
                 min_npix_x=0, max_npix_x=0, min_npix_y=0, max_npix_y=0,
                 sum_of_grey=0, size_of_crosses=0, path=None):
        """
        Initialize detect plate parameters.
        
        Args:
            gvthres (int): Gray value threshold.
            tolerable_discontinuity (int): Tolerable discontinuity.
            min_npix (int): Minimum number of pixels.
            max_npix (int): Maximum number of pixels.
            min_npix_x (int): Minimum number of pixels in x direction.
            max_npix_x (int): Maximum number of pixels in x direction.
            min_npix_y (int): Minimum number of pixels in y direction.
            max_npix_y (int): Maximum number of pixels in y direction.
            sum_of_grey (int): Sum of gray values.
            size_of_crosses (int): Size of crosses.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(gvthres, tolerable_discontinuity, min_npix, max_npix,
                 min_npix_x, max_npix_x, min_npix_y, max_npix_y,
                 sum_of_grey, size_of_crosses)
    
    def set(self, gvthres=0, tolerable_discontinuity=0, min_npix=0, max_npix=0,
            min_npix_x=0, max_npix_x=0, min_npix_y=0, max_npix_y=0,
            sum_of_grey=0, size_of_crosses=0):
        """
        Set detect plate parameters.
        
        Args:
            gvthres (int): Gray value threshold.
            tolerable_discontinuity (int): Tolerable discontinuity.
            min_npix (int): Minimum number of pixels.
            max_npix (int): Maximum number of pixels.
            min_npix_x (int): Minimum number of pixels in x direction.
            max_npix_x (int): Maximum number of pixels in x direction.
            min_npix_y (int): Minimum number of pixels in y direction.
            max_npix_y (int): Maximum number of pixels in y direction.
            sum_of_grey (int): Sum of gray values.
            size_of_crosses (int): Size of crosses.
        """
        self.gvthres = gvthres
        self.tolerable_discontinuity = tolerable_discontinuity
        self.min_npix = min_npix
        self.max_npix = max_npix
        self.min_npix_x = min_npix_x
        self.max_npix_x = max_npix_x
        self.min_npix_y = min_npix_y
        self.max_npix_y = max_npix_y
        self.sum_of_grey = sum_of_grey
        self.size_of_crosses = size_of_crosses
    
    def filename(self):
        """
        Get the filename for detect plate parameters.
        
        Returns:
            str: The filename for detect plate parameters.
        """
        return "detect_plate.par"
    
    def read(self):
        """
        Read detect plate parameters from file.
        
        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.gvthres = int(g(f))
                self.tolerable_discontinuity = int(g(f))
                self.min_npix = int(g(f))
                self.max_npix = int(g(f))
                self.min_npix_x = int(g(f))
                self.max_npix_x = int(g(f))
                self.min_npix_y = int(g(f))
                self.max_npix_y = int(g(f))
                self.sum_of_grey = int(g(f))
                self.size_of_crosses = int(g(f))
        except Exception as e:
            raise IOError(f"Error reading detect plate parameters: {e}")
    
    def write(self):
        """
        Write detect plate parameters to file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                f.write(f"{self.gvthres}\n")
                f.write(f"{self.tolerable_discontinuity}\n")
                f.write(f"{self.min_npix}\n")
                f.write(f"{self.max_npix}\n")
                f.write(f"{self.min_npix_x}\n")
                f.write(f"{self.max_npix_x}\n")
                f.write(f"{self.min_npix_y}\n")
                f.write(f"{self.max_npix_y}\n")
                f.write(f"{self.sum_of_grey}\n")
                f.write(f"{self.size_of_crosses}\n")
        except Exception as e:
            raise IOError(f"Error writing detect plate parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert detect plate parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of detect plate parameter values.
        """
        return {
            'gvthres': self.gvthres,
            'tolerable_discontinuity': self.tolerable_discontinuity,
            'min_npix': self.min_npix,
            'max_npix': self.max_npix,
            'min_npix_x': self.min_npix_x,
            'max_npix_x': self.max_npix_x,
            'min_npix_y': self.min_npix_y,
            'max_npix_y': self.max_npix_y,
            'sum_of_grey': self.sum_of_grey,
            'size_of_crosses': self.size_of_crosses,
        }
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a DetectPlateParams object from a C struct.
        
        Args:
            c_struct: A dictionary of detect plate parameter values from a C struct.
            path: Path to the parameter directory.
        
        Returns:
            DetectPlateParams: A new DetectPlateParams object.
        """
        return cls(
            gvthres=c_struct['gvthres'],
            tolerable_discontinuity=c_struct['tolerable_discontinuity'],
            min_npix=c_struct['min_npix'],
            max_npix=c_struct['max_npix'],
            min_npix_x=c_struct['min_npix_x'],
            max_npix_x=c_struct['max_npix_x'],
            min_npix_y=c_struct['min_npix_y'],
            max_npix_y=c_struct['max_npix_y'],
            sum_of_grey=c_struct['sum_of_grey'],
            size_of_crosses=c_struct['size_of_crosses'],
            path=path,
        )
