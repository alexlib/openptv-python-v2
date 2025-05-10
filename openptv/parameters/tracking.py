"""
Tracking parameters for OpenPTV.

This module provides the TrackingParams class for handling tracking parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import bool_to_int, int_to_bool, g


class TrackingParams(Parameters):
    """
    Tracking parameters for OpenPTV.

    This class handles reading and writing tracking parameters to/from files,
    and converting between Python and C representations.
    """

    def __init__(self, dvxmin=0.0, dvxmax=0.0, dvymin=0.0, dvymax=0.0,
                 dvzmin=0.0, dvzmax=0.0, dangle=0.0, dacc=0.0,
                 flagNewParticles=False, path=None,
                 velocity_lims=None, angle_lim=None, accel_lim=None, add_particle=None, **kwargs):
        """
        Initialize tracking parameters.

        Args:
            dvxmin (float): Minimum velocity in x direction.
            dvxmax (float): Maximum velocity in x direction.
            dvymin (float): Minimum velocity in y direction.
            dvymax (float): Maximum velocity in y direction.
            dvzmin (float): Minimum velocity in z direction.
            dvzmax (float): Maximum velocity in z direction.
            dangle (float): Angle criterion for tracking.
            dacc (float): Acceleration criterion for tracking.
            flagNewParticles (bool): Whether to add new particles.
            path (str or Path): Path to the parameter directory.
            velocity_lims (list): List of [min, max] velocity limits for x, y, z.
            angle_lim (float): Angle criterion for tracking (alternative to dangle).
            accel_lim (float): Acceleration criterion for tracking (alternative to dacc).
            add_particle (int): Whether to add new particles (alternative to flagNewParticles).
        """
        super().__init__(path)

        # Handle velocity_lims if provided
        if velocity_lims is not None:
            dvxmin = velocity_lims[0][0]
            dvxmax = velocity_lims[0][1]
            dvymin = velocity_lims[1][0]
            dvymax = velocity_lims[1][1]
            dvzmin = velocity_lims[2][0]
            dvzmax = velocity_lims[2][1]

        # Handle alternative parameter names
        if angle_lim is not None:
            dangle = angle_lim
        if accel_lim is not None:
            dacc = accel_lim
        if add_particle is not None:
            flagNewParticles = bool(add_particle)

        self.set(dvxmin, dvxmax, dvymin, dvymax, dvzmin, dvzmax,
                 dangle, dacc, flagNewParticles)

    def set(self, dvxmin=0.0, dvxmax=0.0, dvymin=0.0, dvymax=0.0,
            dvzmin=0.0, dvzmax=0.0, dangle=0.0, dacc=0.0,
            flagNewParticles=False):
        """
        Set tracking parameters.

        Args:
            dvxmin (float): Minimum velocity in x direction.
            dvxmax (float): Maximum velocity in x direction.
            dvymin (float): Minimum velocity in y direction.
            dvymax (float): Maximum velocity in y direction.
            dvzmin (float): Minimum velocity in z direction.
            dvzmax (float): Maximum velocity in z direction.
            dangle (float): Angle criterion for tracking.
            dacc (float): Acceleration criterion for tracking.
            flagNewParticles (bool): Whether to add new particles.
        """
        self.dvxmin = dvxmin
        self.dvxmax = dvxmax
        self.dvymin = dvymin
        self.dvymax = dvymax
        self.dvzmin = dvzmin
        self.dvzmax = dvzmax
        self.dangle = dangle  # Store as angle internally for backward compatibility
        self.dacc = dacc
        self.flagNewParticles = flagNewParticles

    def filename(self):
        """
        Get the filename for tracking parameters.

        Returns:
            str: The filename for tracking parameters.
        """
        return "track.par"

    def read(self):
        """
        Read tracking parameters from file.

        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.dvxmin = float(g(f))
                self.dvxmax = float(g(f))
                self.dvymin = float(g(f))
                self.dvymax = float(g(f))
                self.dvzmin = float(g(f))
                self.dvzmax = float(g(f))
                self.dangle = float(g(f))
                self.dacc = float(g(f))
                self.flagNewParticles = int_to_bool(int(g(f)))
        except Exception as e:
            raise IOError(f"Error reading tracking parameters: {e}")

    def write(self):
        """
        Write tracking parameters to file.

        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                f.write(f"{self.dvxmin}\n")
                f.write(f"{self.dvxmax}\n")
                f.write(f"{self.dvymin}\n")
                f.write(f"{self.dvymax}\n")
                f.write(f"{self.dvzmin}\n")
                f.write(f"{self.dvzmax}\n")
                f.write(f"{self.dangle}\n")
                f.write(f"{self.dacc}\n")
                f.write(f"{bool_to_int(self.flagNewParticles)}\n")
        except Exception as e:
            raise IOError(f"Error writing tracking parameters: {e}")

    def to_c_struct(self):
        """
        Convert tracking parameters to a dictionary suitable for creating a C struct.

        Returns:
            dict: A dictionary of tracking parameter values.
        """
        return {
            'dvxmin': self.dvxmin,
            'dvxmax': self.dvxmax,
            'dvymin': self.dvymin,
            'dvymax': self.dvymax,
            'dvzmin': self.dvzmin,
            'dvzmax': self.dvzmax,
            'dangle': self.dangle,
            'dacc': self.dacc,
            'add': bool_to_int(self.flagNewParticles),
            # Additional fields that are not used in the GUI but are in the C struct
            'dsumg': 0,
            'dn': 0,
            'dnx': 0,
            'dny': 0,
        }

    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a TrackingParams object from a C struct.

        Args:
            c_struct: A dictionary of tracking parameter values from a C struct.
            path: Path to the parameter directory.

        Returns:
            TrackingParams: A new TrackingParams object.
        """
        return cls(
            dvxmin=c_struct['dvxmin'],
            dvxmax=c_struct['dvxmax'],
            dvymin=c_struct['dvymin'],
            dvymax=c_struct['dvymax'],
            dvzmin=c_struct['dvzmin'],
            dvzmax=c_struct['dvzmax'],
            dangle=c_struct['dangle'],
            dacc=c_struct['dacc'],
            flagNewParticles=int_to_bool(c_struct['add']),
            path=path,
        )
