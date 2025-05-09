"""
Cython declarations for the parameter bridge.

This file contains Cython declarations for the parameter bridge functions.
"""

# cython: language_level=3
# distutils: language = c

from openptv.binding.parameters cimport track_par, sequence_par, volume_par, control_par, target_par, orient_par, calibration
from openptv.binding.vec_utils cimport vec3d


cdef track_par* _tracking_params_to_c(object params)
cdef sequence_par* _sequence_params_to_c(object params)
cdef volume_par* _volume_params_to_c(object params)
cdef control_par* _control_params_to_c(object params)
cdef target_par* _target_params_to_c(object params)
cdef orient_par* _orient_params_to_c(object params)
