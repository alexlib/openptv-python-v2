"""
Target parameters for OpenPTV.

This module provides the TargetParams and TargRecParams classes for handling target parameters.
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
                 path=None):
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
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
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
        Get the filename for target parameters.
        
        Returns:
            str: The filename for target parameters.
        """
        return "target.par"
    
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
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a TargetParams object from a C struct.
        
        Args:
            c_struct: A dictionary of target parameter values from a C struct.
            path: Path to the parameter directory.
        
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
        )


class TargRecParams(Parameters):
    """
    Target recognition parameters for OpenPTV.
    
    This class handles reading and writing target recognition parameters to/from files.
    It's a specialized version of TargetParams used in the GUI.
    """
    
    def __init__(self, n_img=0, gvthres=None, disco=0, nnmin=0, nnmax=0,
                 nxmin=0, nxmax=0, nymin=0, nymax=0, sumg_min=0, cr_sz=0,
                 path=None):
        """
        Initialize target recognition parameters.
        
        Args:
            n_img (int): Number of cameras.
            gvthres (list): List of gray value thresholds for each camera.
            disco (int): Discontinuity threshold.
            nnmin (int): Minimum number of pixels.
            nnmax (int): Maximum number of pixels.
            nxmin (int): Minimum number of pixels in x direction.
            nxmax (int): Maximum number of pixels in x direction.
            nymin (int): Minimum number of pixels in y direction.
            nymax (int): Maximum number of pixels in y direction.
            sumg_min (int): Minimum sum of gray values.
            cr_sz (int): Cross size.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(n_img, gvthres, disco, nnmin, nnmax, nxmin, nxmax, nymin, nymax, sumg_min, cr_sz)
    
    def set(self, n_img=0, gvthres=None, disco=0, nnmin=0, nnmax=0,
            nxmin=0, nxmax=0, nymin=0, nymax=0, sumg_min=0, cr_sz=0):
        """
        Set target recognition parameters.
        
        Args:
            n_img (int): Number of cameras.
            gvthres (list): List of gray value thresholds for each camera.
            disco (int): Discontinuity threshold.
            nnmin (int): Minimum number of pixels.
            nnmax (int): Maximum number of pixels.
            nxmin (int): Minimum number of pixels in x direction.
            nxmax (int): Maximum number of pixels in x direction.
            nymin (int): Minimum number of pixels in y direction.
            nymax (int): Maximum number of pixels in y direction.
            sumg_min (int): Minimum sum of gray values.
            cr_sz (int): Cross size.
        """
        self.n_img = n_img
        self.gvthres = gvthres or [0] * n_img
        
        # Ensure gvthres has n_img elements
        if len(self.gvthres) < self.n_img:
            self.gvthres.extend([0] * (self.n_img - len(self.gvthres)))
        
        self.disco = disco
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
        Get the filename for target recognition parameters.
        
        Returns:
            str: The filename for target recognition parameters.
        """
        return "targ_rec.par"
    
    def read(self):
        """
        Read target recognition parameters from file.
        
        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.gvthres = [int(g(f)) for _ in range(self.n_img)]
                self.disco = int(g(f))
                self.nnmin = int(g(f))
                self.nnmax = int(g(f))
                self.nxmin = int(g(f))
                self.nxmax = int(g(f))
                self.nymin = int(g(f))
                self.nymax = int(g(f))
                self.sumg_min = int(g(f))
                self.cr_sz = int(g(f))
        except Exception as e:
            raise IOError(f"Error reading target recognition parameters: {e}")
    
    def write(self):
        """
        Write target recognition parameters to file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                for i in range(self.n_img):
                    f.write(f"{self.gvthres[i]}\n")
                f.write(f"{self.disco}\n")
                f.write(f"{self.nnmin}\n")
                f.write(f"{self.nnmax}\n")
                f.write(f"{self.nxmin}\n")
                f.write(f"{self.nxmax}\n")
                f.write(f"{self.nymin}\n")
                f.write(f"{self.nymax}\n")
                f.write(f"{self.sumg_min}\n")
                f.write(f"{self.cr_sz}\n")
        except Exception as e:
            raise IOError(f"Error writing target recognition parameters: {e}")
    
    def to_target_params(self):
        """
        Convert target recognition parameters to TargetParams.
        
        Returns:
            TargetParams: A TargetParams object.
        """
        # Ensure gvthres has 4 elements
        gvthres = self.gvthres.copy()
        if len(gvthres) < 4:
            gvthres.extend([0] * (4 - len(gvthres)))
        
        return TargetParams(
            gvthres=gvthres,
            discont=self.disco,
            nnmin=self.nnmin,
            nnmax=self.nnmax,
            nxmin=self.nxmin,
            nxmax=self.nxmax,
            nymin=self.nymin,
            nymax=self.nymax,
            sumg_min=self.sumg_min,
            cr_sz=self.cr_sz,
            path=self.path,
        )
    
    @classmethod
    def from_target_params(cls, target_params, n_img):
        """
        Create a TargRecParams object from a TargetParams object.
        
        Args:
            target_params: A TargetParams object.
            n_img: Number of cameras.
        
        Returns:
            TargRecParams: A new TargRecParams object.
        """
        return cls(
            n_img=n_img,
            gvthres=target_params.gvthres[:n_img],
            disco=target_params.discont,
            nnmin=target_params.nnmin,
            nnmax=target_params.nnmax,
            nxmin=target_params.nxmin,
            nxmax=target_params.nxmax,
            nymin=target_params.nymin,
            nymax=target_params.nymax,
            sumg_min=target_params.sumg_min,
            cr_sz=target_params.cr_sz,
            path=target_params.path,
        )
