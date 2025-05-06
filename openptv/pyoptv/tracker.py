"""
Tracker module for OpenPTV.
"""

from typing import List, Tuple, Dict, Any, Optional
import os
import numpy as np

from .tracking_frame_buf import TargetArray, Target, Frame
from .parameters import TrackPar, VolumePar, ControlPar
from .calibration import Calibration
from .track import track_forward_start, trackcorr_c_loop
from .tracking import tr_new, tr_free, tr_write, tr_write_ascii_data
from .tracking_run import tracking_run


class Tracker:
    """Tracker class for OpenPTV."""

    def __init__(
        self,
        cpar: ControlPar,
        vpar: VolumePar,
        tpar: TrackPar,
        calib: List[Calibration],
        seq_par: Dict[str, Any],
        output_directory: str,
    ):
        """Initialize the tracker.

        Args:
            cpar: Control parameters
            vpar: Volume parameters
            tpar: Tracking parameters
            calib: List of calibration objects
            seq_par: Sequence parameters
            output_directory: Output directory
        """
        self.cpar = cpar
        self.vpar = vpar
        self.tpar = tpar
        self.calib = calib
        self.seq_par = seq_par
        self.output_directory = output_directory

    def track_forward(
        self,
        corres_file_base: str,
        linkage_file_base: str,
        prio_file_base: str,
        first: int,
        last: int,
    ) -> None:
        """Track forward.

        Args:
            corres_file_base: Correspondence file base
            linkage_file_base: Linkage file base
            prio_file_base: Priority file base
            first: First frame
            last: Last frame
        """
        tracking_run(
            self.cpar,
            self.vpar,
            self.tpar,
            self.seq_par,
            self.calib,
            corres_file_base,
            linkage_file_base,
            prio_file_base,
            first,
            last,
            self.output_directory,
        )


def default_naming(directory: str, casename: str, step: int) -> Dict[str, str]:
    """Default naming scheme for tracking files.

    Args:
        directory: Directory
        casename: Case name
        step: Step

    Returns:
        Dictionary with file names
    """
    return {
        "corres": os.path.join(directory, f"{casename}_{step:04d}.corres"),
        "linkage": os.path.join(directory, f"{casename}_{step:04d}.linkage"),
        "prio": os.path.join(directory, f"{casename}_{step:04d}.prio"),
    }
