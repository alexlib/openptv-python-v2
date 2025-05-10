"""
Target parameters for OpenPTV.

This module provides the TargetParams classes for handling target parameters.
TargetRecParams and DetectPlateParams are just aliases to this one with different
filenames 'targ_rec.par' and 'detect_plate.par'
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g


class TargetParams(Parameters):
    """
    Target parameters for OpenPTV.
    
    This class handles reading and writing target parameters to/from files,
    and converting between Python and C representations.
    """
    
    def __init__(self, gvthres=None, discont=0, nnmin=0, nnmax=0,
                 nxmin=0, nxmax=0, nymin=0, nymax=0, sumg_min=0, cr_sz=0,
                 path=None, filename=None):
        """
        Initialize target parameters.
        
        Args:
            gvthres (list): List of gray value thresholds for each camera.
            discont (int): Discontinuity threshold.
            nnmin (int): Minimum number of pixels.
            nnmax (int): Maximum number of pixels.
            nxmin (int): Minimum number of pixels in x direction.
            nxmax (int): Maximum number of pixels in x direction.
            nymin (int): Minimum number of pixels in y direction.
            nymax (int): Maximum number of pixels in y direction.
            sumg_min (int): Minimum sum of gray values.
            cr_sz (int): Cross size.
            path (str or Path): Path to the parameter file directory.
            filename (str or Path): The filename to use for reading/writing parameters.
        """
        super().__init__(path)
        self._filename = filename
        self.set(gvthres, discont, nnmin, nnmax, nxmin, nxmax, nymin, nymax, sumg_min, cr_sz)
    
    def set(self, gvthres=None, discont=0, nnmin=0, nnmax=0,
            nxmin=0, nxmax=0, nymin=0, nymax=0, sumg_min=0, cr_sz=0):
        """
        Set target parameters.
        
        Args:
            gvthres (list): List of gray value thresholds for each camera.
            discont (int): Discontinuity threshold.
            nnmin (int): Minimum number of pixels.
            nnmax (int): Maximum number of pixels.
            nxmin (int): Minimum number of pixels in x direction.
            nxmax (int): Maximum number of pixels in x direction.
            nymin (int): Minimum number of pixels in y direction.
            nymax (int): Maximum number of pixels in y direction.
            sumg_min (int): Minimum sum of gray values.
            cr_sz (int): Cross size.
        """
        self.gvthres = gvthres or [0, 0, 0, 0]
        self.discont = discont
        self.nnmin = nnmin
        self.nnmax = nnmax
        self.nxmin = nxmin
        self.nxmax = nxmax
        self.nymin = nymin
        self.nymax = nymax
        self.sumg_min = sumg_min
        self.cr_sz = cr_sz
    
    def filename(self):
        """
        Get the filename for target parameters. Must be set explicitly.
        
        Returns:
            str: The filename for target parameters.
        
        Raises:
            ValueError: If filename was not set.
        """
        if self._filename is None:
            raise ValueError("TargetParams: filename must be specified explicitly.")
        return str(self._filename)
    
    def set_filename(self, filename):
        """
        Set the filename for target parameters.
        
        Args:
            filename (str or Path): The filename to use.
        """
        self._filename = filename

    def read(self):
        """
        Read target parameters from file.
        
        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.gvthres = [int(g(f)) for _ in range(4)]
                self.discont = int(g(f))
                self.nnmin = int(g(f))
                self.nnmax = int(g(f))
                self.nxmin = int(g(f))
                self.nxmax = int(g(f))
                self.nymin = int(g(f))
                self.nymax = int(g(f))
                self.sumg_min = int(g(f))
                self.cr_sz = int(g(f))
        except Exception as e:
            raise IOError(f"Error reading target parameters: {e}")
    
    def write(self):
        """
        Write target parameters to file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                for i in range(4):
                    f.write(f"{self.gvthres[i]}\n")
                f.write(f"{self.discont}\n")
                f.write(f"{self.nnmin}\n")
                f.write(f"{self.nnmax}\n")
                f.write(f"{self.nxmin}\n")
                f.write(f"{self.nxmax}\n")
                f.write(f"{self.nymin}\n")
                f.write(f"{self.nymax}\n")
                f.write(f"{self.sumg_min}\n")
                f.write(f"{self.cr_sz}\n")
        except Exception as e:
            raise IOError(f"Error writing target parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert target parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of target parameter values.
        """
        return {
            'gvthres': self.gvthres,
            'discont': self.discont,
            'nnmin': self.nnmin,
            'nnmax': self.nnmax,
            'nxmin': self.nxmin,
            'nxmax': self.nxmax,
            'nymin': self.nymin,
            'nymax': self.nymax,
            'sumg_min': self.sumg_min,
            'cr_sz': self.cr_sz,
        }
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None, filename=None):
        """
        Create a TargetParams object from a C struct.
        
        Args:
            c_struct: A dictionary of target parameter values from a C struct.
            path: Path to the parameter directory.
            filename: The filename to use for reading/writing parameters.
        
        Returns:
            TargetParams: A new TargetParams object.
        """
        return cls(
            gvthres=c_struct['gvthres'],
            discont=c_struct['discont'],
            nnmin=c_struct['nnmin'],
            nnmax=c_struct['nnmax'],
            nxmin=c_struct['nxmin'],
            nxmax=c_struct['nxmax'],
            nymin=c_struct['nymin'],
            nymax=c_struct['nymax'],
            sumg_min=c_struct['sumg_min'],
            cr_sz=c_struct['cr_sz'],
            path=path,
            filename=filename,
        )