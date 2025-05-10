"""
Target parameters for OpenPTV.

This module provides the TargetParams class for handling target parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g
from typing import List, Union


class TargetParams(Parameters):
    """
    Target parameters for OpenPTV.

    This class handles reading and writing target parameters to/from files,
    and converting between Python and C representations.
    """

    def __init__(self, gvthresh: Union[List, None]=None, discont: int=0, nnmin: int=0, nnmax: int=0,
                 nxmin: int=0, nxmax: int=0, nymin: int=0, nymax: int=0, sumg_min: int=0, cr_sz: int=0,
                 path: Union[str, None]=None):
        """
        Initialize target parameters.

        Args:
            gvthresh (list): List of gray value thresholds for each camera.
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
        self.set(gvthresh, discont, nnmin, nnmax, nxmin, nxmax, nymin, nymax, sumg_min, cr_sz)

    def set(self, gvthresh=None, discont=0, nnmin=0, nnmax=0,
            nxmin=0, nxmax=0, nymin=0, nymax=0, sumg_min=0, cr_sz=0):
        """
        Set target parameters.

        Args:
            gvthresh (list): List of gray value thresholds for each camera.
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
        self.gvthresh = gvthresh or [0, 0, 0, 0]
        self.discont = discont
        self.nnmin = nnmin
        self.nnmax = nnmax
        self.nxmin = nxmin
        self.nxmax = nxmax
        self.nymin = nymin
        self.nymax = nymax
        self.sumg_min = sumg_min
        self.cr_sz = cr_sz

        # Add aliases for backward compatibility with GUI code
        self.tol_dis = self.discont  # For backward compatibility
        self.disco = self.discont  # For backward compatibility (another name for discont)
        self.min_npix = self.nnmin  # For backward compatibility
        self.max_npix = self.nnmax  # For backward compatibility
        self.min_npix_x = self.nxmin  # For backward compatibility
        self.max_npix_x = self.nxmax  # For backward compatibility
        self.min_npix_y = self.nymin  # For backward compatibility
        self.max_npix_y = self.nymax  # For backward compatibility
        self.sum_grey = self.sumg_min  # For backward compatibility
        self.size_cross = self.cr_sz  # For backward compatibility

    def filename(self):
        """
        Get the filename for target parameters.

        Returns:
            str: The filename for target parameters.
        """
        return "targ_rec.par"

    def read(self):
        """
        Read target parameters from file.

        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.gvthresh = [int(g(f)) for _ in range(4)]
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
                    f.write(f"{self.gvthresh[i]}\n")
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
            'gvthresh': self.gvthresh,
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

    def to_cython_object(self):
        """
        Convert to a Cython TargetParams object.

        Returns:
            openptv.binding.parameters.TargetParams: A Cython TargetParams object.
        """
        from openptv.binding.parameters import TargetParams as CythonTargetParams

        # Create a Cython TargetParams object
        # Note: The Cython TargetParams constructor doesn't have direct parameters,
        # so we'll need to create it and then set the values
        cython_params = CythonTargetParams()

        # Set the values using the correct method names
        cython_params.set_grey_thresholds(self.gvthresh)
        cython_params.set_max_discontinuity(self.discont)
        cython_params.set_pixel_count_bounds((self.nnmin, self.nnmax))
        cython_params.set_xsize_bounds((self.nxmin, self.nxmax))
        cython_params.set_ysize_bounds((self.nymin, self.nymax))
        cython_params.set_min_sum_grey(self.sumg_min)
        cython_params.set_cross_size(self.cr_sz)

        return cython_params

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
            gvthresh=c_struct['gvthresh'],
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


# TargRecParams and DetectPlateParams are aliases for TargetParams for backward compatibility
TargRecParams = TargetParams
DetectPlateParams = TargetParams