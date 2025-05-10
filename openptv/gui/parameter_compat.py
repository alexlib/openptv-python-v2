"""
Compatibility layer for transitioning from old parameter classes to new ones.

This module provides functions to convert between the old parameter classes
in openptv.gui.parameters and the new ones in openptv.parameters.
"""

from pathlib import Path

# Import old parameter classes
# Import old parameter classes - these are now the same as the new ones
from openptv.parameters import (
    Parameters as OldParameters,
    PtvParams as OldPtvParams,
    CalOriParams as OldCalOriParams,
    SequenceParams as OldSequenceParams,
    CriteriaParams as OldCriteriaParams,
    ManOriParams as OldManOriParams,
    DetectPlateParams as OldDetectPlateParams,
    OrientParams as OldOrientParams,
    TrackingParams as OldTrackingParams,
    PftVersionParams as OldPftVersionParams,
    ExamineParams as OldExamineParams,
    DumbbellParams as OldDumbbellParams,
    ShakingParams as OldShakingParams,
    par_dir_prefix as old_par_dir_prefix,
    copy_params_dir as old_copy_params_dir,
)

# Import new parameter classes
from openptv.parameters import (
    Parameters as NewParameters,
    PtvParams as NewPtvParams,
    CalOriParams as NewCalOriParams,
    SequenceParams as NewSequenceParams,
    CriteriaParams as NewCriteriaParams,
    ManOriParams as NewManOriParams,
    DetectPlateParams as NewDetectPlateParams,
    OrientParams as NewOrientParams,
    TrackingParams as NewTrackingParams,
    PftVersionParams as NewPftVersionParams,
    ExamineParams as NewExamineParams,
    DumbbellParams as NewDumbbellParams,
    ShakingParams as NewShakingParams,
    par_dir_prefix as new_par_dir_prefix,
    copy_params_dir as new_copy_params_dir,
)


def convert_old_to_new_ptv_params(old_params: OldPtvParams) -> NewPtvParams:
    """
    Convert old PtvParams to new PtvParams.

    Args:
        old_params: Old PtvParams object.

    Returns:
        New PtvParams object.
    """
    return NewPtvParams(
        n_img=old_params.n_img,
        img_name=old_params.img_name,
        img_cal=old_params.img_cal,
        hp_flag=old_params.hp_flag,
        allcam_flag=old_params.allcam_flag,
        tiff_flag=old_params.tiff_flag,
        imx=old_params.imx,
        imy=old_params.imy,
        pix_x=old_params.pix_x,
        pix_y=old_params.pix_y,
        chfield=old_params.chfield,
        mmp_n1=old_params.mmp_n1,
        mmp_n2=old_params.mmp_n2,
        mmp_n3=old_params.mmp_n3,
        mmp_d=old_params.mmp_d,
        path=old_params.path,
    )


def convert_old_to_new_cal_ori_params(old_params: OldCalOriParams) -> NewCalOriParams:
    """
    Convert old CalOriParams to new CalOriParams.

    Args:
        old_params: Old CalOriParams object.

    Returns:
        New CalOriParams object.
    """
    return NewCalOriParams(
        n_img=old_params.n_img,
        fixp_name=old_params.fixp_name,
        img_cal_name=old_params.img_cal_name,
        img_ori=old_params.img_ori,
        tiff_flag=old_params.tiff_flag,
        pair_flag=old_params.pair_flag,
        chfield=old_params.chfield,
        path=old_params.path,
    )


def convert_old_to_new_sequence_params(old_params: OldSequenceParams) -> NewSequenceParams:
    """
    Convert old SequenceParams to new SequenceParams.

    Args:
        old_params: Old SequenceParams object.

    Returns:
        New SequenceParams object.
    """
    return NewSequenceParams(
        n_img=old_params.n_img,
        base_name=old_params.base_name,
        first=old_params.first,
        last=old_params.last,
        path=old_params.path,
    )


def convert_old_to_new_criteria_params(old_params: OldCriteriaParams) -> NewCriteriaParams:
    """
    Convert old CriteriaParams to new CriteriaParams.

    Args:
        old_params: Old CriteriaParams object.

    Returns:
        New CriteriaParams object.
    """
    return NewCriteriaParams(
        X_lay=old_params.X_lay,
        Zmin_lay=old_params.Zmin_lay,
        Zmax_lay=old_params.Zmax_lay,
        cnx=old_params.cnx,
        cny=old_params.cny,
        cn=old_params.cn,
        csumg=old_params.csumg,
        corrmin=old_params.corrmin,
        eps0=old_params.eps0,
        path=old_params.path,
    )


def convert_old_to_new_man_ori_params(old_params: OldManOriParams) -> NewManOriParams:
    """
    Convert old ManOriParams to new ManOriParams.

    Args:
        old_params: Old ManOriParams object.

    Returns:
        New ManOriParams object.
    """
    return NewManOriParams(
        n_img=old_params.n_img,
        nr=old_params.nr,
        path=old_params.path,
    )


def convert_old_to_new_detect_plate_params(old_params: OldDetectPlateParams) -> NewDetectPlateParams:
    """
    Convert old DetectPlateParams to new DetectPlateParams.

    Args:
        old_params: Old DetectPlateParams object.

    Returns:
        New DetectPlateParams object.
    """
    return NewDetectPlateParams(
        gvthres=old_params.gvthres,
        tolerable_discontinuity=old_params.tolerable_discontinuity,
        min_npix=old_params.min_npix,
        max_npix=old_params.max_npix,
        min_npix_x=old_params.min_npix_x,
        max_npix_x=old_params.max_npix_x,
        min_npix_y=old_params.min_npix_y,
        max_npix_y=old_params.max_npix_y,
        sum_of_grey=old_params.sum_of_grey,
        size_of_crosses=old_params.size_of_crosses,
        path=old_params.path,
    )


def convert_old_to_new_orient_params(old_params: OldOrientParams) -> NewOrientParams:
    """
    Convert old OrientParams to new OrientParams.

    Args:
        old_params: Old OrientParams object.

    Returns:
        New OrientParams object.
    """
    return NewOrientParams(
        pnfo=old_params.pnfo,
        cc=old_params.cc,
        xh=old_params.xh,
        yh=old_params.yh,
        k1=old_params.k1,
        k2=old_params.k2,
        k3=old_params.k3,
        p1=old_params.p1,
        p2=old_params.p2,
        scale=old_params.scale,
        shear=old_params.shear,
        interf=old_params.interf,
        path=old_params.path,
    )


def convert_old_to_new_tracking_params(old_params: OldTrackingParams) -> NewTrackingParams:
    """
    Convert old TrackingParams to new TrackingParams.

    Args:
        old_params: Old TrackingParams object.

    Returns:
        New TrackingParams object.
    """
    return NewTrackingParams(
        dvxmin=old_params.dvxmin,
        dvxmax=old_params.dvxmax,
        dvymin=old_params.dvymin,
        dvymax=old_params.dvymax,
        dvzmin=old_params.dvzmin,
        dvzmax=old_params.dvzmax,
        angle=old_params.angle,
        dacc=old_params.dacc,
        flagNewParticles=old_params.flagNewParticles,
        path=old_params.path,
    )


def read_params_dir(par_path: Path) -> dict:
    """
    Read a parameters directory and return a dictionary with all parameter objects.

    This function is a drop-in replacement for openptv.gui.parameters.readParamsDir
    that uses the new parameter classes.

    Args:
        par_path: Path to the parameter directory.

    Returns:
        Dictionary with all parameter objects.
    """
    # Read PTV parameters
    ptv_params = NewPtvParams(path=par_path)
    ptv_params.read()
    n_img = ptv_params.n_img

    # Create parameter objects
    ret = {
        NewCalOriParams: NewCalOriParams(n_img, path=par_path),
        NewSequenceParams: NewSequenceParams(n_img, path=par_path),
        NewCriteriaParams: NewCriteriaParams(path=par_path),
        NewTargRecParams: NewTargRecParams(n_img, path=par_path),
        NewManOriParams: NewManOriParams(n_img, [], path=par_path),
        NewDetectPlateParams: NewDetectPlateParams(path=par_path),
        NewOrientParams: NewOrientParams(path=par_path),
        NewTrackingParams: NewTrackingParams(path=par_path),
        NewPftVersionParams: NewPftVersionParams(path=par_path),
        NewExamineParams: NewExamineParams(path=par_path),
        NewDumbbellParams: NewDumbbellParams(path=par_path),
        NewShakingParams: NewShakingParams(path=par_path),
    }

    # Read parameter files
    for par_type in list(ret.keys()):
        if par_type == NewPtvParams:
            continue
        par_obj = ret[par_type]
        par_obj.read()

    return ret
