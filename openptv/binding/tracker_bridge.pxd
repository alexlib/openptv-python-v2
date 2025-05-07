# cython: language_level=3
# distutils: language = c

"""
Cython declarations for the tracker bridge.

This file contains Cython declarations for the tracker bridge functions.
"""

from openptv.binding.parameters cimport track_par, volume_par
from openptv.binding.param_bridge cimport tracking_params_to_c, volume_params_to_c

from openptv.parameters.tracking import TrackingParams
from openptv.parameters.volume import VolumeParams
