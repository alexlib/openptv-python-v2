"""
Cython declarations for the parameter bridge.

This file contains Cython declarations for the parameter bridge functions.
"""

# cython: language_level=3
# distutils: language = c

from openptv.binding.parameters cimport track_par, sequence_par, volume_par, control_par, target_par, orient_par

from openptv.parameters.tracking import TrackingParams
from openptv.parameters.sequence import SequenceParams
from openptv.parameters.volume import VolumeParams
from openptv.parameters.control import ControlParams
from openptv.parameters.target import TargetParams
from openptv.parameters.orient import OrientParams


cdef track_par* tracking_params_to_c(TrackingParams params)
cdef sequence_par* sequence_params_to_c(SequenceParams params)
cdef volume_par* volume_params_to_c(VolumeParams params)
cdef control_par* control_params_to_c(ControlParams params)
cdef target_par* target_params_to_c(TargetParams params)
cdef orient_par* orient_params_to_c(OrientParams params)
