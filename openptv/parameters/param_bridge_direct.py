"""
Direct parameter bridge between Python and Cython parameter objects.

This module provides direct conversion functions between Python parameter objects
and Cython parameter objects, without using PyCapsules.
"""

from openptv.parameters import (
    TrackingParams, SequenceParams, VolumeParams, ControlParams, TargetParams
)
from openptv.binding.parameters import (
    TrackingParams as CythonTrackingParams,
    SequenceParams as CythonSequenceParams,
    VolumeParams as CythonVolumeParams,
    ControlParams as CythonControlParams,
    TargetParams as CythonTargetParams
)
from openptv.parameters.utils import encode_if_needed, bool_to_int


def tracking_params_to_c(params):
    """
    Convert a Python TrackingParams object to a Cython TrackingParams object.
    
    Args:
        params: A Python TrackingParams object.
        
    Returns:
        A Cython TrackingParams object.
    """
    return CythonTrackingParams(
        dvxmin=params.dvxmin,
        dvxmax=params.dvxmax,
        dvymin=params.dvymin,
        dvymax=params.dvymax,
        dvzmin=params.dvzmin,
        dvzmax=params.dvzmax,
        dangle=params.dangle,
        dacc=params.dacc,
        add=bool_to_int(params.flagNewParticles)
    )


def sequence_params_to_c(params):
    """
    Convert a Python SequenceParams object to a Cython SequenceParams object.
    
    Args:
        params: A Python SequenceParams object.
        
    Returns:
        A Cython SequenceParams object.
    """
    # Convert base names to bytes if needed
    base_names = [encode_if_needed(name) for name in params.img_base_name]
    
    return CythonSequenceParams(
        first=params.first,
        last=params.last,
        base_name=base_names
    )


def volume_params_to_c(params):
    """
    Convert a Python VolumeParams object to a Cython VolumeParams object.
    
    Args:
        params: A Python VolumeParams object.
        
    Returns:
        A Cython VolumeParams object.
    """
    return CythonVolumeParams(
        X_lay=params.X_lay,
        Zmin_lay=params.Zmin_lay,
        Zmax_lay=params.Zmax_lay,
        cnx=params.cnx,
        cny=params.cny,
        cn=params.cn,
        csumg=params.csumg,
        corrmin=params.corrmin,
        eps0=params.eps0
    )


def control_params_to_c(params):
    """
    Convert a Python ControlParams object to a Cython ControlParams object.
    
    Args:
        params: A Python ControlParams object.
        
    Returns:
        A Cython ControlParams object.
    """
    # Convert image names and calibration image names to bytes if needed
    img_names = [encode_if_needed(name) for name in params.img_name]
    cal_img_names = [encode_if_needed(name) for name in params.img_cal]
    
    return CythonControlParams(
        num_cams=params.n_img,
        img_name=img_names,
        img_cal=cal_img_names,
        hp_flag=params.hp_flag,
        allcam_flag=params.allcam_flag,
        tiff_flag=params.tiff_flag,
        imx=params.imx,
        imy=params.imy,
        pix_x=params.pix_x,
        pix_y=params.pix_y,
        chfield=params.chfield,
        mmp_n1=params.mmp_n1,
        mmp_n2=params.mmp_n2,
        mmp_n3=params.mmp_n3,
        mmp_d=params.mmp_d
    )


def target_params_to_c(params):
    """
    Convert a Python TargetParams object to a Cython TargetParams object.
    
    Args:
        params: A Python TargetParams object.
        
    Returns:
        A Cython TargetParams object.
    """
    return CythonTargetParams(
        gvthres=params.gvthres,
        discont=params.discont,
        nnmin=params.nnmin,
        nnmax=params.nnmax,
        nxmin=params.nxmin,
        nxmax=params.nxmax,
        nymin=params.nymin,
        nymax=params.nymax,
        sumg_min=params.sumg_min,
        cr_sz=params.cr_sz
    )
