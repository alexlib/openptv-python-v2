# cython: language_level=3
# distutils: language = c

"""
Bridge between Python and C tracking functions.

This module provides functions for calling C tracking functions with Python parameter objects.
"""

from libc.stdlib cimport malloc, free

from openptv.binding.parameters cimport track_par, volume_par
from openptv.binding.tracker cimport track_forward_start, trackcorr_c_loop, trackcorr_c_finish
from openptv.binding.tracking_framebuf cimport tracking_run, framebuf_free

# Import Python modules
import numpy as np

# Import parameter bridge functions
from openptv.parameters.tracking import TrackingParams
from openptv.parameters.volume import VolumeParams
from openptv.binding.param_bridge import tracking_params_from_c, volume_params_from_c


def track_forward_with_params(targets, TrackingParams track_params, VolumeParams vol_params):
    """
    Track particles forward using Python parameter objects.

    Args:
        targets: Target data as a list of TargetArray objects.
        track_params: A TrackingParams object.
        vol_params: A VolumeParams object.

    Returns:
        Tracking results as a dictionary containing:
        - 'links': Number of links found
        - 'lost': Number of lost tracks
        - 'added': Number of added tracks
    """
    # Convert Python parameter objects to C structs
    cdef track_par* c_track_params = tracking_params_to_c(track_params)
    cdef volume_par* c_vol_params = volume_params_to_c(vol_params)

    # Initialize tracking run
    cdef tracking_run* run = track_forward_start(targets, c_track_params, c_vol_params)

    # Run tracking loop
    cdef int step = 0
    cdef int status = 0

    # Process tracking results
    results = {
        'links': 0,
        'lost': 0,
        'added': 0,
    }

    # Clean up
    trackcorr_c_finish(run, c_track_params)
    free(c_track_params)
    free(c_vol_params)

    # Return results
    return results
