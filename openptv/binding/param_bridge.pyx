# cython: language_level=3
# distutils: language = c

"""
Bridge between Python parameter objects and C parameter structs.

This module provides functions for converting between Python parameter objects
and C parameter structs.
"""

from libc.stdlib cimport malloc, free
from libc.string cimport strncpy

from openptv.binding.parameters cimport track_par, sequence_par, volume_par, control_par, target_par
from openptv.binding.parameters cimport orient_par, mm_np, calibration, Glass, Exterior, Interior, ap_52
from openptv.binding.parameters cimport SEQ_FNAME_MAX_LEN

from openptv.parameters.tracking import TrackingParams
from openptv.parameters.sequence import SequenceParams
from openptv.parameters.volume import VolumeParams
from openptv.parameters.control import ControlParams
from openptv.parameters.target import TargetParams
from openptv.parameters.orient import OrientParams
from openptv.parameters.calibration import CalOriParams
from openptv.parameters.utils import encode_if_needed, decode_if_needed


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
        'dsumg': c_params.dsumg,
        'dn': c_params.dn,
        'dnx': c_params.dnx,
        'dny': c_params.dny,
    }

    # Create a TrackingParams object from the dictionary
    return TrackingParams.from_c_struct(param_dict, path)


cdef sequence_par* sequence_params_to_c(SequenceParams params):
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
    c_params.num_cams = param_dict['num_cams']
    c_params.first = param_dict['first']
    c_params.last = param_dict['last']

    # Copy base names
    for i in range(param_dict['num_cams']):
        if i < len(param_dict['img_base_name']):
            base_name = encode_if_needed(param_dict['img_base_name'][i])
            strncpy(c_params.img_base_name[i], base_name, SEQ_FNAME_MAX_LEN - 1)
            c_params.img_base_name[i][SEQ_FNAME_MAX_LEN - 1] = b'\0'

    return c_params


def sequence_params_from_c(sequence_par* c_params, path=None):
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
    for i in range(c_params.num_cams):
        base_names.append(decode_if_needed(c_params.img_base_name[i]))

    # Create a dictionary of parameter values
    param_dict = {
        'num_cams': c_params.num_cams,
        'img_base_name': base_names,
        'first': c_params.first,
        'last': c_params.last,
    }

    # Create a SequenceParams object from the dictionary
    return SequenceParams.from_c_struct(param_dict, path)


cdef volume_par* volume_params_to_c(VolumeParams params):
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


def volume_params_from_c(volume_par* c_params, path=None):
    """
    Convert a C volume_par struct to a Python VolumeParams object.

    Args:
        c_params: A pointer to a volume_par struct.
        path: Path to the parameter directory.

    Returns:
        A VolumeParams object.
    """
    # Create lists for X_lay, Zmin_lay, and Zmax_lay
    X_lay = [c_params.X_lay[0], c_params.X_lay[1]]
    Zmin_lay = [c_params.Zmin_lay[0], c_params.Zmin_lay[1]]
    Zmax_lay = [c_params.Zmax_lay[0], c_params.Zmax_lay[1]]

    # Create a dictionary of parameter values
    param_dict = {
        'X_lay': X_lay,
        'Zmin_lay': Zmin_lay,
        'Zmax_lay': Zmax_lay,
        'cnx': c_params.cnx,
        'cny': c_params.cny,
        'cn': c_params.cn,
        'csumg': c_params.csumg,
        'corrmin': c_params.corrmin,
        'eps0': c_params.eps0,
    }

    # Create a VolumeParams object from the dictionary
    return VolumeParams.from_c_struct(param_dict, path)


cdef control_par* control_params_to_c(ControlParams params):
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
    for i in range(param_dict['num_cams']):
        if i < len(param_dict['img_base_name']):
            img_name = encode_if_needed(param_dict['img_base_name'][i])
            strncpy(c_params.img_base_name[i], img_name, SEQ_FNAME_MAX_LEN - 1)
            c_params.img_base_name[i][SEQ_FNAME_MAX_LEN - 1] = b'\0'

        if i < len(param_dict['cal_img_base_name']):
            cal_name = encode_if_needed(param_dict['cal_img_base_name'][i])
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


def control_params_from_c(control_par* c_params, path=None):
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

    for i in range(c_params.num_cams):
        img_base_name.append(decode_if_needed(c_params.img_base_name[i]))
        cal_img_base_name.append(decode_if_needed(c_params.cal_img_base_name[i]))

    # Create multimedia parameters
    mm_np = {
        'nlay': c_params.mm.nlay,
        'n1': c_params.mm.n1,
        'n2': [c_params.mm.n2[0], c_params.mm.n2[1], c_params.mm.n2[2]],
        'n3': c_params.mm.n3,
        'd': [c_params.mm.d[0], c_params.mm.d[1], c_params.mm.d[2]],
    }

    # Create a dictionary of parameter values
    param_dict = {
        'num_cams': c_params.num_cams,
        'img_base_name': img_base_name,
        'cal_img_base_name': cal_img_base_name,
        'hp_flag': c_params.hp_flag,
        'allCam_flag': c_params.allCam_flag,
        'tiff_flag': c_params.tiff_flag,
        'imx': c_params.imx,
        'imy': c_params.imy,
        'pix_x': c_params.pix_x,
        'pix_y': c_params.pix_y,
        'chfield': c_params.chfield,
        'mm': mm_np,
    }

    # Create a ControlParams object from the dictionary
    return ControlParams.from_c_struct(param_dict, path)


cdef target_par* target_params_to_c(TargetParams params):
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


def target_params_from_c(target_par* c_params, path=None):
    """
    Convert a C target_par struct to a Python TargetParams object.

    Args:
        c_params: A pointer to a target_par struct.
        path: Path to the parameter directory.

    Returns:
        A TargetParams object.
    """
    # Create a list for gvthres
    gvthres = [c_params.gvthres[0], c_params.gvthres[1], c_params.gvthres[2], c_params.gvthres[3]]

    # Create a dictionary of parameter values
    param_dict = {
        'gvthres': gvthres,
        'discont': c_params.discont,
        'nnmin': c_params.nnmin,
        'nnmax': c_params.nnmax,
        'nxmin': c_params.nxmin,
        'nxmax': c_params.nxmax,
        'nymin': c_params.nymin,
        'nymax': c_params.nymax,
        'sumg_min': c_params.sumg_min,
        'cr_sz': c_params.cr_sz,
    }

    # Create a TargetParams object from the dictionary
    return TargetParams.from_c_struct(param_dict, path)


cdef orient_par* orient_params_to_c(OrientParams params):
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


def orient_params_from_c(orient_par* c_params, path=None):
    """
    Convert a C orient_par struct to a Python OrientParams object.

    Args:
        c_params: A pointer to an orient_par struct.
        path: Path to the parameter directory.

    Returns:
        An OrientParams object.
    """
    # Create a dictionary of parameter values
    param_dict = {
        'useflag': c_params.useflag,
        'ccflag': c_params.ccflag,
        'xhflag': c_params.xhflag,
        'yhflag': c_params.yhflag,
        'k1flag': c_params.k1flag,
        'k2flag': c_params.k2flag,
        'k3flag': c_params.k3flag,
        'p1flag': c_params.p1flag,
        'p2flag': c_params.p2flag,
        'scxflag': c_params.scxflag,
        'sheflag': c_params.sheflag,
        'interfflag': c_params.interfflag,
    }

    # Create an OrientParams object from the dictionary
    return OrientParams.from_c_struct(param_dict, path)


cdef calibration* cal_ori_params_to_c(CalOriParams params):
    """
    Convert a Python CalOriParams object to a C calibration struct.

    Args:
        params: A CalOriParams object.

    Returns:
        A pointer to a newly allocated calibration struct.
    """
    cdef calibration* c_params = <calibration*>malloc(sizeof(calibration))

    # Initialize mmlut data to NULL
    c_params.mmlut.data = NULL

    # Get parameter values as a dictionary
    param_dict = params.to_c_struct()

    # Fill in the exterior parameters
    c_params.ext_par.x0 = param_dict['ext_par']['x0']
    c_params.ext_par.y0 = param_dict['ext_par']['y0']
    c_params.ext_par.z0 = param_dict['ext_par']['z0']
    c_params.ext_par.omega = param_dict['ext_par']['omega']
    c_params.ext_par.phi = param_dict['ext_par']['phi']
    c_params.ext_par.kappa = param_dict['ext_par']['kappa']

    # Fill in the rotation matrix
    for i in range(3):
        for j in range(3):
            c_params.ext_par.dm[i][j] = param_dict['ext_par']['dm'][i][j]

    # Fill in the interior parameters
    c_params.int_par.xh = param_dict['int_par']['xh']
    c_params.int_par.yh = param_dict['int_par']['yh']
    c_params.int_par.cc = param_dict['int_par']['cc']

    # Fill in the glass parameters
    c_params.glass_par.vec_x = param_dict['glass_par']['vec_x']
    c_params.glass_par.vec_y = param_dict['glass_par']['vec_y']
    c_params.glass_par.vec_z = param_dict['glass_par']['vec_z']
    c_params.glass_par.n1 = param_dict['glass_par']['n1']
    c_params.glass_par.n2 = param_dict['glass_par']['n2']
    c_params.glass_par.n3 = param_dict['glass_par']['n3']
    c_params.glass_par.d = param_dict['glass_par']['d']

    # Fill in the added parameters
    c_params.added_par.k1 = param_dict['added_par']['k1']
    c_params.added_par.k2 = param_dict['added_par']['k2']
    c_params.added_par.k3 = param_dict['added_par']['k3']
    c_params.added_par.p1 = param_dict['added_par']['p1']
    c_params.added_par.p2 = param_dict['added_par']['p2']
    c_params.added_par.scx = param_dict['added_par']['scx']
    c_params.added_par.she = param_dict['added_par']['she']
    c_params.added_par.field = param_dict['added_par']['field']

    return c_params


def cal_ori_params_from_c(calibration* c_params, path=None):
    """
    Convert a C calibration struct to a Python CalOriParams object.

    Args:
        c_params: A pointer to a calibration struct.
        path: Path to the parameter directory.

    Returns:
        A CalOriParams object.
    """
    # Create a dictionary for exterior parameters
    ext_par = {
        'x0': c_params.ext_par.x0,
        'y0': c_params.ext_par.y0,
        'z0': c_params.ext_par.z0,
        'omega': c_params.ext_par.omega,
        'phi': c_params.ext_par.phi,
        'kappa': c_params.ext_par.kappa,
        'dm': [[c_params.ext_par.dm[i][j] for j in range(3)] for i in range(3)],
    }

    # Create a dictionary for interior parameters
    int_par = {
        'xh': c_params.int_par.xh,
        'yh': c_params.int_par.yh,
        'cc': c_params.int_par.cc,
    }

    # Create a dictionary for glass parameters
    glass_par = {
        'vec_x': c_params.glass_par.vec_x,
        'vec_y': c_params.glass_par.vec_y,
        'vec_z': c_params.glass_par.vec_z,
        'n1': c_params.glass_par.n1,
        'n2': c_params.glass_par.n2,
        'n3': c_params.glass_par.n3,
        'd': c_params.glass_par.d,
    }

    # Create a dictionary for added parameters
    added_par = {
        'k1': c_params.added_par.k1,
        'k2': c_params.added_par.k2,
        'k3': c_params.added_par.k3,
        'p1': c_params.added_par.p1,
        'p2': c_params.added_par.p2,
        'scx': c_params.added_par.scx,
        'she': c_params.added_par.she,
        'field': c_params.added_par.field,
    }

    # Create a dictionary of parameter values
    param_dict = {
        'ext_par': ext_par,
        'int_par': int_par,
        'glass_par': glass_par,
        'added_par': added_par,
    }

    # Create a CalOriParams object from the dictionary
    return CalOriParams.from_c_struct(param_dict, path)
