"""
Cython declarations for the parameter bridge.

This file contains Cython declarations for the parameter bridge functions.
"""

# cython: language_level=3
# distutils: language = c

from openptv.binding.parameters cimport track_par, sequence_par, volume_par, control_par, target_par, orient_par, calibration
from openptv.binding.vec_utils cimport vec3d


cdef track_par* tracking_params_to_c(object params)
cdef sequence_par* sequence_params_to_c(object params)
cdef volume_par* volume_params_to_c(object params)
cdef control_par* control_params_to_c(object params)
cdef target_par* target_params_to_c(object params)
cdef orient_par* orient_params_to_c(object params)
