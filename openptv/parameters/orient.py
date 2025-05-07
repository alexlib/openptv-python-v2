"""
Orientation parameters for OpenPTV.

This module provides the OrientParams class for handling orientation parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g, bool_to_int, int_to_bool


class OrientParams(Parameters):
    """
    Orientation parameters for OpenPTV.
    
    This class handles reading and writing orientation parameters to/from files.
    """
    
    def __init__(self, pnfo=0, cc=False, xh=False, yh=False, k1=False, k2=False,
                 k3=False, p1=False, p2=False, scale=False, shear=False,
                 interf=False, path=None):
        """
        Initialize orientation parameters.
        
        Args:
            pnfo (int): Point number for orientation.
            cc (bool): Principal distance flag.
            xh (bool): xh flag.
            yh (bool): yh flag.
            k1 (bool): k1 flag.
            k2 (bool): k2 flag.
            k3 (bool): k3 flag.
            p1 (bool): p1 flag.
            p2 (bool): p2 flag.
            scale (bool): Scale flag.
            shear (bool): Shear flag.
            interf (bool): Interface flag.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(pnfo, cc, xh, yh, k1, k2, k3, p1, p2, scale, shear, interf)
    
    def set(self, pnfo=0, cc=False, xh=False, yh=False, k1=False, k2=False,
            k3=False, p1=False, p2=False, scale=False, shear=False, interf=False):
        """
        Set orientation parameters.
        
        Args:
            pnfo (int): Point number for orientation.
            cc (bool): Principal distance flag.
            xh (bool): xh flag.
            yh (bool): yh flag.
            k1 (bool): k1 flag.
            k2 (bool): k2 flag.
            k3 (bool): k3 flag.
            p1 (bool): p1 flag.
            p2 (bool): p2 flag.
            scale (bool): Scale flag.
            shear (bool): Shear flag.
            interf (bool): Interface flag.
        """
        self.pnfo = pnfo
        self.cc = cc
        self.xh = xh
        self.yh = yh
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.p1 = p1
        self.p2 = p2
        self.scale = scale
        self.shear = shear
        self.interf = interf
    
    def filename(self):
        """
        Get the filename for orientation parameters.
        
        Returns:
            str: The filename for orientation parameters.
        """
        return "orient.par"
    
    def read(self):
        """
        Read orientation parameters from file.
        
        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.pnfo = int(g(f))
                self.cc = int_to_bool(int(g(f)))
                self.xh = int_to_bool(int(g(f)))
                self.yh = int_to_bool(int(g(f)))
                self.k1 = int_to_bool(int(g(f)))
                self.k2 = int_to_bool(int(g(f)))
                self.k3 = int_to_bool(int(g(f)))
                self.p1 = int_to_bool(int(g(f)))
                self.p2 = int_to_bool(int(g(f)))
                self.scale = int_to_bool(int(g(f)))
                self.shear = int_to_bool(int(g(f)))
                self.interf = int_to_bool(int(g(f)))
        except Exception as e:
            raise IOError(f"Error reading orientation parameters: {e}")
    
    def write(self):
        """
        Write orientation parameters to file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                f.write(f"{self.pnfo}\n")
                f.write(f"{bool_to_int(self.cc)}\n")
                f.write(f"{bool_to_int(self.xh)}\n")
                f.write(f"{bool_to_int(self.yh)}\n")
                f.write(f"{bool_to_int(self.k1)}\n")
                f.write(f"{bool_to_int(self.k2)}\n")
                f.write(f"{bool_to_int(self.k3)}\n")
                f.write(f"{bool_to_int(self.p1)}\n")
                f.write(f"{bool_to_int(self.p2)}\n")
                f.write(f"{bool_to_int(self.scale)}\n")
                f.write(f"{bool_to_int(self.shear)}\n")
                f.write(f"{bool_to_int(self.interf)}\n")
        except Exception as e:
            raise IOError(f"Error writing orientation parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert orientation parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of orientation parameter values.
        """
        return {
            'pnfo': self.pnfo,
            'cc': bool_to_int(self.cc),
            'xh': bool_to_int(self.xh),
            'yh': bool_to_int(self.yh),
            'k1': bool_to_int(self.k1),
            'k2': bool_to_int(self.k2),
            'k3': bool_to_int(self.k3),
            'p1': bool_to_int(self.p1),
            'p2': bool_to_int(self.p2),
            'scale': bool_to_int(self.scale),
            'shear': bool_to_int(self.shear),
            'interf': bool_to_int(self.interf),
        }
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create an OrientParams object from a C struct.
        
        Args:
            c_struct: A dictionary of orientation parameter values from a C struct.
            path: Path to the parameter directory.
        
        Returns:
            OrientParams: A new OrientParams object.
        """
        return cls(
            pnfo=c_struct['pnfo'],
            cc=int_to_bool(c_struct['cc']),
            xh=int_to_bool(c_struct['xh']),
            yh=int_to_bool(c_struct['yh']),
            k1=int_to_bool(c_struct['k1']),
            k2=int_to_bool(c_struct['k2']),
            k3=int_to_bool(c_struct['k3']),
            p1=int_to_bool(c_struct['p1']),
            p2=int_to_bool(c_struct['p2']),
            scale=int_to_bool(c_struct['scale']),
            shear=int_to_bool(c_struct['shear']),
            interf=int_to_bool(c_struct['interf']),
            path=path,
        )
