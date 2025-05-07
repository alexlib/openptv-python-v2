"""
Bridge between Python parameter objects and C parameter structs.

This module provides functions for converting between Python parameter objects
and C parameter structs.
"""

# cython: language_level=3
# distutils: language = c

from libc.stdlib cimport malloc, free
from libc.string cimport strncpy

from openptv.binding.parameters cimport track_par, sequence_par, volume_par, control_par, target_par
from openptv.binding.parameters cimport SEQ_FNAME_MAX_LEN

from openptv.parameters.tracking import TrackingParams
from openptv.parameters.sequence import SequenceParams
from openptv.parameters.volume import VolumeParams
from openptv.parameters.control import ControlParams
from openptv.parameters.target import TargetParams


cdef track_par* tracking_params_to_c(TrackingParams params):
    """
    Convert a Python TrackingParams object to a C track_par struct.
    
    Args:
        params: A TrackingParams object.
    
    Returns:
        A pointer to a newly allocated track_par struct.
    """
    cdef track_par* c_params = <track_par*>malloc(sizeof(track_par))
    
    # Get parameter values as a dictionary
    param_dict = params.to_c_struct()
    
    # Fill in the C struct
    c_params.dvxmin = param_dict['dvxmin']
    c_params.dvxmax = param_dict['dvxmax']
    c_params.dvymin = param_dict['dvymin']
    c_params.dvymax = param_dict['dvymax']
    c_params.dvzmin = param_dict['dvzmin']
    c_params.dvzmax = param_dict['dvzmax']
    c_params.dangle = param_dict['dangle']
    c_params.dacc = param_dict['dacc']
    c_params.add = param_dict['add']
    c_params.dsumg = param_dict['dsumg']
    c_params.dn = param_dict['dn']
    c_params.dnx = param_dict['dnx']
    c_params.dny = param_dict['dny']
    
    return c_params


def tracking_params_from_c(track_par* c_params, path=None):
    """
    Convert a C track_par struct to a Python TrackingParams object.
    
    Args:
        c_params: A pointer to a track_par struct.
        path: Path to the parameter directory.
    
    Returns:
        A TrackingParams object.
    """
    # Create a dictionary of parameter values
    param_dict = {
        'dvxmin': c_params.dvxmin,
        'dvxmax': c_params.dvxmax,
        'dvymin': c_params.dvymin,
        'dvymax': c_params.dvymax,
        'dvzmin': c_params.dvzmin,
        'dvzmax': c_params.dvzmax,
        'dangle': c_params.dangle,
        'dacc': c_params.dacc,
        'add': c_params.add,
    }
    
    # Create a TrackingParams object from the dictionary
    return TrackingParams.from_c_struct(param_dict, path)


# Add similar functions for other parameter types as needed
