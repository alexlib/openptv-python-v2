# cython: language_level=3
# distutils: language = c

"""
Cython declarations for the tracker bridge.

This file contains Cython declarations for the tracker bridge functions.
"""

from openptv.coptv.parameters cimport track_par, volume_par
from openptv.coptv.param_bridge cimport _tracking_params_to_c, _volume_params_to_c
