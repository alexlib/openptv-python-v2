#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test all parameter conversions between Python and Cython.
"""

import sys
import os

# Add the parent directory to the path so we can import openptv
sys.path.append(os.path.abspath('..'))

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

def test_tracking_params():
    """Test converting a Python TrackingParams to a Cython TrackingParams."""
    print("\nTesting TrackingParams conversion...")
    py_params = TrackingParams(
        dvxmin=-10.0, dvxmax=10.0,
        dvymin=-10.0, dvymax=10.0,
        dvzmin=-10.0, dvzmax=10.0,
        dangle=30.0, dacc=0.5,
        flagNewParticles=True
    )
    
    cy_params = py_params.to_cython_object()
    assert isinstance(cy_params, CythonTrackingParams)
    print("✅ TrackingParams conversion passed")

def test_sequence_params():
    """Test converting a Python SequenceParams to a Cython SequenceParams."""
    print("\nTesting SequenceParams conversion...")
    py_params = SequenceParams(
        n_img=4,
        base_name=["cam1", "cam2", "cam3", "cam4"],
        first=1, last=100
    )
    
    cy_params = py_params.to_cython_object()
    assert isinstance(cy_params, CythonSequenceParams)
    print("✅ SequenceParams conversion passed")

def test_volume_params():
    """Test converting a Python VolumeParams to a Cython VolumeParams."""
    print("\nTesting VolumeParams conversion...")
    py_params = VolumeParams(
        X_lay=[-40, 40],
        Zmin_lay=[-10, -10],
        Zmax_lay=[10, 10],
        cnx=0.02, cny=0.02, cn=0.01,
        csumg=0.5, corrmin=0.5, eps0=0.5
    )
    
    cy_params = py_params.to_cython_object()
    assert isinstance(cy_params, CythonVolumeParams)
    print("✅ VolumeParams conversion passed")

def test_control_params():
    """Test converting a Python ControlParams to a Cython ControlParams."""
    print("\nTesting ControlParams conversion...")
    py_params = ControlParams(
        n_img=4,
        img_base_name=["img1", "img2", "img3", "img4"],
        cal_img_base_name=["cal1", "cal2", "cal3", "cal4"],
        hp_flag=True, allcam_flag=True, tiff_flag=True,
        imx=1280, imy=1024,
        pix_x=0.01, pix_y=0.01,
        chfield=0,
        mmp_n1=1.0, mmp_n2=1.33, mmp_n3=1.0, mmp_d=10.0
    )
    
    cy_params = py_params.to_cython_object()
    assert isinstance(cy_params, CythonControlParams)
    print("✅ ControlParams conversion passed")

def test_target_params():
    """Test converting a Python TargetParams to a Cython TargetParams."""
    print("\nTesting TargetParams conversion...")
    py_params = TargetParams(
        gvthresh=[20, 20, 20, 20],
        discont=5,
        nnmin=5, nnmax=100,
        nxmin=5, nxmax=100,
        nymin=5, nymax=100,
        sumg_min=10,
        cr_sz=10
    )
    
    cy_params = py_params.to_cython_object()
    assert isinstance(cy_params, CythonTargetParams)
    print("✅ TargetParams conversion passed")

if __name__ == "__main__":
    print("Testing parameter conversions...")
    test_tracking_params()
    test_sequence_params()
    test_volume_params()
    test_control_params()
    test_target_params()
    print("\nAll parameter conversion tests passed!")
