"""
Volume parameters for OpenPTV.

This module provides the VolumeParams class for handling volume parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g


class VolumeParams(Parameters):
    """
    Volume parameters for OpenPTV.
    
    This class handles reading and writing volume parameters to/from files,
    and converting between Python and C representations.
    """
    
    def __init__(self, X_lay=None, Zmin_lay=None, Zmax_lay=None, 
                 cnx=0.0, cny=0.0, cn=0.0, csumg=0.0, corrmin=0.0, eps0=0.0, 
                 path=None):
        """
        Initialize volume parameters.
        
        Args:
            X_lay (list): X coordinates of the layers.
            Zmin_lay (list): Minimum Z coordinates of the layers.
            Zmax_lay (list): Maximum Z coordinates of the layers.
            cnx (float): Correlation threshold for x ratio.
            cny (float): Correlation threshold for y ratio.
            cn (float): Correlation threshold for total pixels.
            csumg (float): Correlation threshold for sum of grey values.
            corrmin (float): Minimum correlation value.
            eps0 (float): Epipolar line width.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(X_lay, Zmin_lay, Zmax_lay, cnx, cny, cn, csumg, corrmin, eps0)
    
    def set(self, X_lay=None, Zmin_lay=None, Zmax_lay=None, 
            cnx=0.0, cny=0.0, cn=0.0, csumg=0.0, corrmin=0.0, eps0=0.0):
        """
        Set volume parameters.
        
        Args:
            X_lay (list): X coordinates of the layers.
            Zmin_lay (list): Minimum Z coordinates of the layers.
            Zmax_lay (list): Maximum Z coordinates of the layers.
            cnx (float): Correlation threshold for x ratio.
            cny (float): Correlation threshold for y ratio.
            cn (float): Correlation threshold for total pixels.
            csumg (float): Correlation threshold for sum of grey values.
            corrmin (float): Minimum correlation value.
            eps0 (float): Epipolar line width.
        """
        self.X_lay = X_lay or [0.0, 0.0]
        self.Zmin_lay = Zmin_lay or [0.0, 0.0]
        self.Zmax_lay = Zmax_lay or [0.0, 0.0]
        self.cnx = cnx
        self.cny = cny
        self.cn = cn
        self.csumg = csumg
        self.corrmin = corrmin
        self.eps0 = eps0
    
    def filename(self):
        """
        Get the filename for volume parameters.
        
        Returns:
            str: The filename for volume parameters.
        """
        return "criteria.par"
    
    def read(self):
        """
        Read volume parameters from file.
        
        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.X_lay = []
                self.Zmin_lay = []
                self.Zmax_lay = []
                self.X_lay.append(float(g(f)))
                self.Zmin_lay.append(float(g(f)))
                self.Zmax_lay.append(float(g(f)))
                self.X_lay.append(float(g(f)))
                self.Zmin_lay.append(float(g(f)))
                self.Zmax_lay.append(float(g(f)))
                self.cnx = float(g(f))
                self.cny = float(g(f))
                self.cn = float(g(f))
                self.csumg = float(g(f))
                self.corrmin = float(g(f))
                self.eps0 = float(g(f))
        except Exception as e:
            raise IOError(f"Error reading volume parameters: {e}")
    
    def write(self):
        """
        Write volume parameters to file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                f.write(f"{self.X_lay[0]}\n")
                f.write(f"{self.Zmin_lay[0]}\n")
                f.write(f"{self.Zmax_lay[0]}\n")
                f.write(f"{self.X_lay[1]}\n")
                f.write(f"{self.Zmin_lay[1]}\n")
                f.write(f"{self.Zmax_lay[1]}\n")
                f.write(f"{self.cnx}\n")
                f.write(f"{self.cny}\n")
                f.write(f"{self.cn}\n")
                f.write(f"{self.csumg}\n")
                f.write(f"{self.corrmin}\n")
                f.write(f"{self.eps0}\n")
        except Exception as e:
            raise IOError(f"Error writing volume parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert volume parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of volume parameter values.
        """
        return {
            'X_lay': self.X_lay,
            'Zmin_lay': self.Zmin_lay,
            'Zmax_lay': self.Zmax_lay,
            'cnx': self.cnx,
            'cny': self.cny,
            'cn': self.cn,
            'csumg': self.csumg,
            'corrmin': self.corrmin,
            'eps0': self.eps0,
        }
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a VolumeParams object from a C struct.
        
        Args:
            c_struct: A dictionary of volume parameter values from a C struct.
            path: Path to the parameter directory.
        
        Returns:
            VolumeParams: A new VolumeParams object.
        """
        return cls(
            X_lay=c_struct['X_lay'],
            Zmin_lay=c_struct['Zmin_lay'],
            Zmax_lay=c_struct['Zmax_lay'],
            cnx=c_struct['cnx'],
            cny=c_struct['cny'],
            cn=c_struct['cn'],
            csumg=c_struct['csumg'],
            corrmin=c_struct['corrmin'],
            eps0=c_struct['eps0'],
            path=path,
        )
    
    def to_cython_object(self):
        """
        Convert the Python VolumeParams instance to a Cython VolumeParams object.
        
        Returns:
            object: A Cython VolumeParams object with the same parameter values.
        """
        from openptv.binding.parameters import VolumeParams as CythonVolumeParams
        
        # Create z_spans from Zmin_lay and Zmax_lay
        z_spans = [(self.Zmin_lay[i], self.Zmax_lay[i]) for i in range(len(self.Zmin_lay))]
        
        # Create a new Cython VolumeParams object with the same values
        cython_params = CythonVolumeParams(
            x_span=self.X_lay,
            z_spans=z_spans,
            pixels_x=self.cnx,
            pixels_y=self.cny,
            pixels_tot=self.cn,
            ref_gray=self.csumg,
            min_correlation=self.corrmin,
            epipolar_band=self.eps0
        )
        
        return cython_params