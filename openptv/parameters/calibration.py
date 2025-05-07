"""
Calibration parameters for OpenPTV.

This module provides the CalOriParams class for handling calibration parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g, bool_to_int, int_to_bool


class CalOriParams(Parameters):
    """
    Calibration and orientation parameters for OpenPTV.
    
    This class handles reading and writing calibration parameters to/from files.
    """
    
    def __init__(self, n_img=0, fixp_name="", img_cal_name=None, img_ori=None,
                 tiff_flag=False, pair_flag=False, chfield=0, path=None):
        """
        Initialize calibration parameters.
        
        Args:
            n_img (int): Number of cameras.
            fixp_name (str): Name of the fixpoint file.
            img_cal_name (list): List of calibration image names.
            img_ori (list): List of orientation image names.
            tiff_flag (bool): TIFF flag.
            pair_flag (bool): Pair flag.
            chfield (int): Camera field (0=frame, 1=odd, 2=even).
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(n_img, fixp_name, img_cal_name, img_ori, tiff_flag, pair_flag, chfield)
    
    def set(self, n_img=0, fixp_name="", img_cal_name=None, img_ori=None,
            tiff_flag=False, pair_flag=False, chfield=0):
        """
        Set calibration parameters.
        
        Args:
            n_img (int): Number of cameras.
            fixp_name (str): Name of the fixpoint file.
            img_cal_name (list): List of calibration image names.
            img_ori (list): List of orientation image names.
            tiff_flag (bool): TIFF flag.
            pair_flag (bool): Pair flag.
            chfield (int): Camera field (0=frame, 1=odd, 2=even).
        """
        self.n_img = n_img
        self.fixp_name = fixp_name
        self.img_cal_name = img_cal_name or []
        self.img_ori = img_ori or []
        
        # Ensure img_cal_name and img_ori have n_img elements
        if len(self.img_cal_name) < self.n_img:
            self.img_cal_name.extend([''] * (self.n_img - len(self.img_cal_name)))
        if len(self.img_ori) < self.n_img:
            self.img_ori.extend([''] * (self.n_img - len(self.img_ori)))
        
        self.tiff_flag = tiff_flag
        self.pair_flag = pair_flag
        self.chfield = chfield
    
    def filename(self):
        """
        Get the filename for calibration parameters.
        
        Returns:
            str: The filename for calibration parameters.
        """
        return "cal_ori.par"
    
    def read(self):
        """
        Read calibration parameters from file.
        
        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.fixp_name = g(f)
                self.istherefile(self.fixp_name)
                
                self.img_cal_name = []
                self.img_ori = []
                for i in range(self.n_img):
                    self.img_cal_name.append(g(f))
                    self.img_ori.append(g(f))
                
                self.tiff_flag = int_to_bool(int(g(f)))
                self.pair_flag = int_to_bool(int(g(f)))
                self.chfield = int(g(f))
                
                # Test if files are present, issue warnings
                for i in range(self.n_img):
                    self.istherefile(self.img_cal_name[i])
                    self.istherefile(self.img_ori[i])
        except Exception as e:
            raise IOError(f"Error reading calibration parameters: {e}")
    
    def write(self):
        """
        Write calibration parameters to file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                f.write(f"{self.fixp_name}\n")
                
                for i in range(self.n_img):
                    f.write(f"{self.img_cal_name[i]}\n")
                    f.write(f"{self.img_ori[i]}\n")
                
                f.write(f"{bool_to_int(self.tiff_flag)}\n")
                f.write(f"{bool_to_int(self.pair_flag)}\n")
                f.write(f"{self.chfield}\n")
        except Exception as e:
            raise IOError(f"Error writing calibration parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert calibration parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of calibration parameter values.
        """
        return {
            'n_img': self.n_img,
            'fixp_name': self.fixp_name,
            'img_cal_name': self.img_cal_name,
            'img_ori': self.img_ori,
            'tiff_flag': bool_to_int(self.tiff_flag),
            'pair_flag': bool_to_int(self.pair_flag),
            'chfield': self.chfield,
        }
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a CalOriParams object from a C struct.
        
        Args:
            c_struct: A dictionary of calibration parameter values from a C struct.
            path: Path to the parameter directory.
        
        Returns:
            CalOriParams: A new CalOriParams object.
        """
        return cls(
            n_img=c_struct['n_img'],
            fixp_name=c_struct['fixp_name'],
            img_cal_name=c_struct['img_cal_name'],
            img_ori=c_struct['img_ori'],
            tiff_flag=int_to_bool(c_struct['tiff_flag']),
            pair_flag=int_to_bool(c_struct['pair_flag']),
            chfield=c_struct['chfield'],
            path=path,
        )
