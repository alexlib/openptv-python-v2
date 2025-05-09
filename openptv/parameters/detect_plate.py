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
    
    def __init__(self, gvth_1=0, gvth_2=0, gvth_3=0, gvth_4=0,
                 tol_dis=0, min_npix=0, max_npix=0,
                 min_npix_x=0, max_npix_x=0, min_npix_y=0, max_npix_y=0,
                 sum_grey=0, size_cross=0, path=None):
        """
        Initialize detect plate parameters.
        
        Args:
            gvth_1 (int): Gray value threshold for camera 1.
            gvth_2 (int): Gray value threshold for camera 2.
            gvth_3 (int): Gray value threshold for camera 3.
            gvth_4 (int): Gray value threshold for camera 4.
            tol_dis (int): Tolerable discontinuity.
            min_npix (int): Minimum number of pixels.
            max_npix (int): Maximum number of pixels.
            min_npix_x (int): Minimum number of pixels in x direction.
            max_npix_x (int): Maximum number of pixels in x direction.
            min_npix_y (int): Minimum number of pixels in y direction.
            max_npix_y (int): Maximum number of pixels in y direction.
            sum_grey (int): Sum of gray values.
            size_cross (int): Size of crosses.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(gvth_1, gvth_2, gvth_3, gvth_4, tol_dis, min_npix, max_npix,
                 min_npix_x, max_npix_x, min_npix_y, max_npix_y,
                 sum_grey, size_cross)
    
    def set(self, gvth_1=0, gvth_2=0, gvth_3=0, gvth_4=0,
            tol_dis=0, min_npix=0, max_npix=0,
            min_npix_x=0, max_npix_x=0, min_npix_y=0, max_npix_y=0,
            sum_grey=0, size_cross=0):
        """
        Set detect plate parameters.
        
        Args:
            gvth_1 (int): Gray value threshold for camera 1.
            gvth_2 (int): Gray value threshold for camera 2.
            gvth_3 (int): Gray value threshold for camera 3.
            gvth_4 (int): Gray value threshold for camera 4.
            tol_dis (int): Tolerable discontinuity.
            min_npix (int): Minimum number of pixels.
            max_npix (int): Maximum number of pixels.
            min_npix_x (int): Minimum number of pixels in x direction.
            max_npix_x (int): Maximum number of pixels in x direction.
            min_npix_y (int): Minimum number of pixels in y direction.
            max_npix_y (int): Maximum number of pixels in y direction.
            sum_grey (int): Sum of gray values.
            size_cross (int): Size of crosses.
        """
        self.gvth_1 = gvth_1
        self.gvth_2 = gvth_2
        self.gvth_3 = gvth_3
        self.gvth_4 = gvth_4
        self.tol_dis = tol_dis
        self.min_npix = min_npix
        self.max_npix = max_npix
        self.min_npix_x = min_npix_x
        self.max_npix_x = max_npix_x
        self.min_npix_y = min_npix_y
        self.max_npix_y = max_npix_y
        self.sum_grey = sum_grey
        self.size_cross = size_cross
    
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
                self.gvth_1 = int(g(f))
                self.gvth_2 = int(g(f))
                self.gvth_3 = int(g(f))
                self.gvth_4 = int(g(f))
                self.tol_dis = int(g(f))
                self.min_npix = int(g(f))
                self.max_npix = int(g(f))
                self.min_npix_x = int(g(f))
                self.max_npix_x = int(g(f))
                self.min_npix_y = int(g(f))
                self.max_npix_y = int(g(f))
                self.sum_grey = int(g(f))
                self.size_cross = int(g(f))
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
                f.write(f"{self.gvth_1}\n")
                f.write(f"{self.gvth_2}\n")
                f.write(f"{self.gvth_3}\n")
                f.write(f"{self.gvth_4}\n")
                f.write(f"{self.tol_dis}\n")
                f.write(f"{self.min_npix}\n")
                f.write(f"{self.max_npix}\n")
                f.write(f"{self.min_npix_x}\n")
                f.write(f"{self.max_npix_x}\n")
                f.write(f"{self.min_npix_y}\n")
                f.write(f"{self.max_npix_y}\n")
                f.write(f"{self.sum_grey}\n")
                f.write(f"{self.size_cross}\n")
        except Exception as e:
            raise IOError(f"Error writing detect plate parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert detect plate parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of detect plate parameter values.
        """
        return {
            'gvth_1': self.gvth_1,
            'gvth_2': self.gvth_2,
            'gvth_3': self.gvth_3,
            'gvth_4': self.gvth_4,
            'tol_dis': self.tol_dis,
            'min_npix': self.min_npix,
            'max_npix': self.max_npix,
            'min_npix_x': self.min_npix_x,
            'max_npix_x': self.max_npix_x,
            'min_npix_y': self.min_npix_y,
            'max_npix_y': self.max_npix_y,
            'sum_grey': self.sum_grey,
            'size_cross': self.size_cross,
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
            gvth_1=c_struct['gvth_1'],
            gvth_2=c_struct['gvth_2'],
            gvth_3=c_struct['gvth_3'],
            gvth_4=c_struct['gvth_4'],
            tol_dis=c_struct['tol_dis'],
            min_npix=c_struct['min_npix'],
            max_npix=c_struct['max_npix'],
            min_npix_x=c_struct['min_npix_x'],
            max_npix_x=c_struct['max_npix_x'],
            min_npix_y=c_struct['min_npix_y'],
            max_npix_y=c_struct['max_npix_y'],
            sum_grey=c_struct['sum_grey'],
            size_cross=c_struct['size_cross'],
            path=path,
        )
