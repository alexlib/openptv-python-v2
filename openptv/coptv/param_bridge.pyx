# cython: language_level=3
# distutils: language = c

"""
Bridge between Python parameter objects and C parameter structs.

This module provides functions for converting between Python parameter objects
and C parameter structs.
"""

from libc.stdlib cimport malloc, free
from libc.string cimport strncpy
from cpython.pycapsule cimport PyCapsule_New
from libc.stdint cimport uintptr_t

from openptv.coptv.parameters cimport track_par, sequence_par, volume_par, control_par, target_par
from openptv.coptv.parameters cimport orient_par, mm_np, calibration, Glass, Exterior, Interior, ap_52

# Define SEQ_FNAME_MAX_LEN
cdef int SEQ_FNAME_MAX_LEN = 128

# Import Python modules
import openptv.parameters.tracking
import openptv.parameters.sequence
import openptv.parameters.volume
import openptv.parameters.control
import openptv.parameters.target
import openptv.parameters.orient
import openptv.parameters.calibration
import openptv.parameters.utils


def tracking_params_to_c_capsule(params):
    """Return a PyCapsule wrapping a C track_par pointer from TrackingParams."""
    cdef track_par* ptr = _tracking_params_to_c(params)
    return PyCapsule_New(<void*>ptr, b"track_par", NULL)
cdef track_par* _tracking_params_to_c(object params):
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


def tracking_params_from_c(object c_params, path=None):
    """
    Convert a C track_par struct to a Python TrackingParams object.

    Args:
        c_params: A pointer to a track_par struct.
        path: Path to the parameter directory.

    Returns:
        A TrackingParams object.
    """
    # Create a dictionary of parameter values
    cdef track_par* c_track_params = <track_par*>c_params
    param_dict = {
        'dvxmin': c_track_params.dvxmin,
        'dvxmax': c_track_params.dvxmax,
        'dvymin': c_track_params.dvymin,
        'dvymax': c_track_params.dvymax,
        'dvzmin': c_track_params.dvzmin,
        'dvzmax': c_track_params.dvzmax,
        'dangle': c_track_params.dangle,
        'dacc': c_track_params.dacc,
        'add': c_track_params.add,
        'dsumg': c_track_params.dsumg,
        'dn': c_track_params.dn,
        'dnx': c_track_params.dnx,
        'dny': c_track_params.dny,
    }

    # Create a TrackingParams object from the dictionary
    return openptv.parameters.tracking.TrackingParams.from_c_struct(param_dict, path)


def sequence_params_to_c_capsule(params):
    """Return a PyCapsule wrapping a C sequence_par pointer from SequenceParams."""
    cdef sequence_par* ptr = _sequence_params_to_c(params)
    return PyCapsule_New(<void*>ptr, b"sequence_par", NULL)
cdef sequence_par* _sequence_params_to_c(object params):
    """
    Convert a Python SequenceParams object to a C sequence_par struct.

    Args:
        params: A SequenceParams object.

    Returns:
        A pointer to a newly allocated sequence_par struct.
    """
    cdef sequence_par* c_params = <sequence_par*>malloc(sizeof(sequence_par))

    # Get parameter values as a dictionary
    param_dict = params.to_c_struct()

    # Fill in the C struct
    c_params.first = param_dict['first']
    c_params.last = param_dict['last']

    # Copy base names
    for i in range(len(param_dict['img_base_name'])):
        base_name = openptv.parameters.utils.encode_if_needed(param_dict['img_base_name'][i])
        strncpy(c_params.img_base_name[i], base_name, SEQ_FNAME_MAX_LEN - 1)
        c_params.img_base_name[i][SEQ_FNAME_MAX_LEN - 1] = b'\0'

    return c_params


def sequence_params_from_c(object c_params, path=None):
    """
    Convert a C sequence_par struct to a Python SequenceParams object.

    Args:
        c_params: A pointer to a sequence_par struct.
        path: Path to the parameter directory.

    Returns:
        A SequenceParams object.
    """
    # Create a list of base names
    base_names = []
    # Get the number of cameras from the length of the img_base_name array
    cdef sequence_par* c_seq_params = <sequence_par*>c_params
    cdef int num_cams = 0
    while c_seq_params.img_base_name[num_cams] != NULL:
        base_names.append(openptv.parameters.utils.decode_if_needed(c_seq_params.img_base_name[num_cams]))
        num_cams += 1

    # Create a dictionary of parameter values
    param_dict = {
        'img_base_name': base_names,
        'first': c_params.first,
        'last': c_params.last,
    }

    # Create a SequenceParams object from the dictionary
    return openptv.parameters.sequence.SequenceParams.from_c_struct(param_dict, path)


def volume_params_to_c_capsule(params):
    """Return a PyCapsule wrapping a C volume_par pointer from VolumeParams."""
    cdef volume_par* ptr = _volume_params_to_c(params)
    return PyCapsule_New(<void*>ptr, b"volume_par", NULL)
cdef volume_par* _volume_params_to_c(object params):
    """
    Convert a Python VolumeParams object to a C volume_par struct.

    Args:
        params: A VolumeParams object.

    Returns:
        A pointer to a newly allocated volume_par struct.
    """
    cdef volume_par* c_params = <volume_par*>malloc(sizeof(volume_par))

    # Get parameter values as a dictionary
    param_dict = params.to_c_struct()

    # Fill in the C struct
    for i in range(2):
        c_params.X_lay[i] = param_dict['X_lay'][i]
        c_params.Zmin_lay[i] = param_dict['Zmin_lay'][i]
        c_params.Zmax_lay[i] = param_dict['Zmax_lay'][i]

    c_params.cnx = param_dict['cnx']
    c_params.cny = param_dict['cny']
    c_params.cn = param_dict['cn']
    c_params.csumg = param_dict['csumg']
    c_params.corrmin = param_dict['corrmin']
    c_params.eps0 = param_dict['eps0']

    return c_params


def volume_params_from_c(object c_params, path=None):
    """
    Convert a C volume_par struct to a Python VolumeParams object.

    Args:
        c_params: A pointer to a volume_par struct.
        path: Path to the parameter directory.

    Returns:
        A VolumeParams object.
    """
    # Create lists for X_lay, Zmin_lay, and Zmax_lay
    cdef volume_par* c_vol_params = <volume_par*>c_params
    X_lay = [c_vol_params.X_lay[0], c_vol_params.X_lay[1]]
    Zmin_lay = [c_vol_params.Zmin_lay[0], c_vol_params.Zmin_lay[1]]
    Zmax_lay = [c_vol_params.Zmax_lay[0], c_vol_params.Zmax_lay[1]]

    # Create a dictionary of parameter values
    param_dict = {
        'X_lay': X_lay,
        'Zmin_lay': Zmin_lay,
        'Zmax_lay': Zmax_lay,
        'cnx': c_vol_params.cnx,
        'cny': c_vol_params.cny,
        'cn': c_vol_params.cn,
        'csumg': c_vol_params.csumg,
        'corrmin': c_vol_params.corrmin,
        'eps0': c_vol_params.eps0,
    }

    # Create a VolumeParams object from the dictionary
    return openptv.parameters.volume.VolumeParams.from_c_struct(param_dict, path)


def control_params_to_c_capsule(params):
    """Return a PyCapsule wrapping a C control_par pointer from ControlParams."""
    cdef control_par* ptr = _control_params_to_c(params)
    return PyCapsule_New(<void*>ptr, b"control_par", NULL)
cdef control_par* _control_params_to_c(object params):
    """
    Convert a Python ControlParams object to a C control_par struct.

    Args:
        params: A ControlParams object.

    Returns:
        A pointer to a newly allocated control_par struct.
    """
    cdef control_par* c_params = <control_par*>malloc(sizeof(control_par))

    # Get parameter values as a dictionary
    param_dict = params.to_c_struct()

    # Fill in the C struct
    c_params.num_cams = param_dict['num_cams']

    # Copy base names
    for i in range(len(param_dict['img_base_name'])):
        img_name = openptv.parameters.utils.encode_if_needed(param_dict['img_base_name'][i])
        strncpy(c_params.img_base_name[i], img_name, SEQ_FNAME_MAX_LEN - 1)
        c_params.img_base_name[i][SEQ_FNAME_MAX_LEN - 1] = b'\0'

    for i in range(len(param_dict['cal_img_base_name'])):
        cal_name = openptv.parameters.utils.encode_if_needed(param_dict['cal_img_base_name'][i])
        strncpy(c_params.cal_img_base_name[i], cal_name, SEQ_FNAME_MAX_LEN - 1)
        c_params.cal_img_base_name[i][SEQ_FNAME_MAX_LEN - 1] = b'\0'

    c_params.hp_flag = param_dict['hp_flag']
    c_params.allCam_flag = param_dict['allCam_flag']
    c_params.tiff_flag = param_dict['tiff_flag']
    c_params.imx = param_dict['imx']
    c_params.imy = param_dict['imy']
    c_params.pix_x = param_dict['pix_x']
    c_params.pix_y = param_dict['pix_y']
    c_params.chfield = param_dict['chfield']

    # Fill in multimedia parameters
    c_params.mm.nlay = param_dict['mm']['nlay']
    c_params.mm.n1 = param_dict['mm']['n1']
    c_params.mm.n3 = param_dict['mm']['n3']

    for i in range(3):
        if i < len(param_dict['mm']['n2']):
            c_params.mm.n2[i] = param_dict['mm']['n2'][i]
        if i < len(param_dict['mm']['d']):
            c_params.mm.d[i] = param_dict['mm']['d'][i]

    return c_params


def control_params_from_c(object c_params, path=None):
    """
    Convert a C control_par struct to a Python ControlParams object.

    Args:
        c_params: A pointer to a control_par struct.
        path: Path to the parameter directory.

    Returns:
        A ControlParams object.
    """
    # Create lists for img_base_name and cal_img_base_name
    img_base_name = []
    cal_img_base_name = []

    cdef control_par* c_ctrl_params = <control_par*>c_params
    for i in range(c_ctrl_params.num_cams):
        if c_ctrl_params.img_base_name[i] != NULL:
            img_base_name.append(openptv.parameters.utils.decode_if_needed(c_ctrl_params.img_base_name[i]))
        if c_ctrl_params.cal_img_base_name[i] != NULL:
            cal_img_base_name.append(openptv.parameters.utils.decode_if_needed(c_ctrl_params.cal_img_base_name[i]))

    # Create multimedia parameters
    mm_np = {
        'nlay': c_ctrl_params.mm.nlay,
        'n1': c_ctrl_params.mm.n1,
        'n2': [c_ctrl_params.mm.n2[0], c_ctrl_params.mm.n2[1], c_ctrl_params.mm.n2[2]],
        'n3': c_ctrl_params.mm.n3,
        'd': [c_ctrl_params.mm.d[0], c_ctrl_params.mm.d[1], c_ctrl_params.mm.d[2]],
    }

    # Create a dictionary of parameter values
    param_dict = {
        'num_cams': c_ctrl_params.num_cams,
        'img_base_name': img_base_name,
        'cal_img_base_name': cal_img_base_name,
        'hp_flag': c_ctrl_params.hp_flag,
        'allCam_flag': c_ctrl_params.allCam_flag,
        'tiff_flag': c_ctrl_params.tiff_flag,
        'imx': c_ctrl_params.imx,
        'imy': c_ctrl_params.imy,
        'pix_x': c_ctrl_params.pix_x,
        'pix_y': c_ctrl_params.pix_y,
        'chfield': c_ctrl_params.chfield,
        'mm': mm_np,
    }

    # Create a ControlParams object from the dictionary
    return openptv.parameters.control.ControlParams.from_c_struct(param_dict, path)


def target_params_to_c_capsule(params):
    """Return a PyCapsule wrapping a C target_par pointer from TargetParams."""
    cdef target_par* ptr = _target_params_to_c(params)
    return PyCapsule_New(<void*>ptr, b"target_par", NULL)
cdef target_par* _target_params_to_c(object params):
    """
    Convert a Python TargetParams object to a C target_par struct.

    Args:
        params: A TargetParams object.

    Returns:
        A pointer to a newly allocated target_par struct.
    """
    cdef target_par* c_params = <target_par*>malloc(sizeof(target_par))

    # Get parameter values as a dictionary
    param_dict = params.to_c_struct()

    # Fill in the C struct
    for i in range(4):
        if i < len(param_dict['gvthres']):
            c_params.gvthres[i] = param_dict['gvthres'][i]

    c_params.discont = param_dict['discont']
    c_params.nnmin = param_dict['nnmin']
    c_params.nnmax = param_dict['nnmax']
    c_params.nxmin = param_dict['nxmin']
    c_params.nxmax = param_dict['nxmax']
    c_params.nymin = param_dict['nymin']
    c_params.nymax = param_dict['nymax']
    c_params.sumg_min = param_dict['sumg_min']
    c_params.cr_sz = param_dict['cr_sz']

    return c_params


def target_params_from_c(object c_params, path=None):
    """
    Convert a C target_par struct to a Python TargetParams object.

    Args:
        c_params: A pointer to a target_par struct.
        path: Path to the parameter directory.

    Returns:
        A TargetParams object.
    """
    # Create a list for gvthres
    cdef target_par* c_targ_params = <target_par*>c_params
    gvthres = [c_targ_params.gvthres[0], c_targ_params.gvthres[1], c_targ_params.gvthres[2], c_targ_params.gvthres[3]]

    # Create a dictionary of parameter values
    param_dict = {
        'gvthres': gvthres,
        'discont': c_targ_params.discont,
        'nnmin': c_targ_params.nnmin,
        'nnmax': c_targ_params.nnmax,
        'nxmin': c_targ_params.nxmin,
        'nxmax': c_targ_params.nxmax,
        'nymin': c_targ_params.nymin,
        'nymax': c_targ_params.nymax,
        'sumg_min': c_targ_params.sumg_min,
        'cr_sz': c_targ_params.cr_sz,
    }

    # Create a TargetParams object from the dictionary
    return openptv.parameters.target.TargetParams.from_c_struct(param_dict, path)


def orient_params_to_c_capsule(params):
    """Return a PyCapsule wrapping a C orient_par pointer from OrientParams."""
    cdef orient_par* ptr = _orient_params_to_c(params)
    return PyCapsule_New(<void*>ptr, b"orient_par", NULL)
cdef orient_par* _orient_params_to_c(object params):
    """
    Convert a Python OrientParams object to a C orient_par struct.

    Args:
        params: An OrientParams object.

    Returns:
        A pointer to a newly allocated orient_par struct.
    """
    cdef orient_par* c_params = <orient_par*>malloc(sizeof(orient_par))

    # Get parameter values as a dictionary
    param_dict = params.to_c_struct()

    # Fill in the C struct
    c_params.useflag = param_dict['useflag']
    c_params.ccflag = param_dict['ccflag']
    c_params.xhflag = param_dict['xhflag']
    c_params.yhflag = param_dict['yhflag']
    c_params.k1flag = param_dict['k1flag']
    c_params.k2flag = param_dict['k2flag']
    c_params.k3flag = param_dict['k3flag']
    c_params.p1flag = param_dict['p1flag']
    c_params.p2flag = param_dict['p2flag']
    c_params.scxflag = param_dict['scxflag']
    c_params.sheflag = param_dict['sheflag']
    c_params.interfflag = param_dict['interfflag']

    return c_params


def orient_params_from_c(object c_params, path=None):
    """
    Convert a C orient_par struct to a Python OrientParams object.

    Args:
        c_params: A pointer to an orient_par struct.
        path: Path to the parameter directory.

    Returns:
        An OrientParams object.
    """
    # Create a dictionary of parameter values
    cdef orient_par* c_orient_params = <orient_par*>c_params
    param_dict = {
        'useflag': c_orient_params.useflag,
        'ccflag': c_orient_params.ccflag,
        'xhflag': c_orient_params.xhflag,
        'yhflag': c_orient_params.yhflag,
        'k1flag': c_orient_params.k1flag,
        'k2flag': c_orient_params.k2flag,
        'k3flag': c_orient_params.k3flag,
        'p1flag': c_orient_params.p1flag,
        'p2flag': c_orient_params.p2flag,
        'scxflag': c_orient_params.scxflag,
        'sheflag': c_orient_params.sheflag,
        'interfflag': c_orient_params.interfflag,
    }

    # Create an OrientParams object from the dictionary
    return openptv.parameters.orient.OrientParams.from_c_struct(param_dict, path)


# TODO: Implement cal_ori_params_to_c and cal_ori_params_from_c functions
