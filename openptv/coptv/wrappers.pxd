"""
Cython declarations for wrapper functions.

This file contains Cython declarations for wrapper functions that take
parameter objects as arguments.
"""

# cython: language_level=3
# distutils: language = c

from libc.stdlib cimport malloc, free
import numpy as np
cimport numpy as np

from openptv.coptv.parameters cimport track_par, volume_par, control_par, target_par, orient_par
from openptv.coptv.tracker cimport track_forward_start, trackcorr_c_loop, trackcorr_c_finish
from openptv.coptv.tracking_frame_buf cimport tracking_frame_buf, new_tracking_frame_buf
from openptv.coptv.calibration cimport calibration, read_calibration
from openptv.coptv.orientation cimport orient, read_orient

from openptv.parameters.tracking import TrackingParams
from openptv.parameters.sequence import SequenceParams
from openptv.parameters.volume import VolumeParams
from openptv.parameters.control import ControlParams
from openptv.parameters.target import TargetParams
from openptv.parameters.orient import OrientParams

from openptv.coptv.param_bridge cimport (
    tracking_params_to_c,
    sequence_params_to_c,
    volume_params_to_c,
    control_params_to_c,
    target_params_to_c,
    orient_params_to_c,
)


cpdef track_forward_using_parameters(targets, TrackingParams track_params, VolumeParams vol_params)
cpdef calibrate_using_parameters(TargetParams target_params, OrientParams orient_params)
cpdef detect_targets_using_parameters(image, TargetParams target_params)
cpdef correspondences_using_parameters(targets, ControlParams control_params, VolumeParams vol_params)
cpdef track_backward_using_parameters(targets, TrackingParams track_params, VolumeParams vol_params)
