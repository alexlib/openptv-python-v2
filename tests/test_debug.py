#!/usr/bin/env python
import os
import pytest
from openptv.binding.parameters import ControlParams
from openptv.binding.calibration import Calibration

def test_control_and_calibration_files():
    # Always resolve test data paths relative to this test file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    fodder_dir = os.path.join(test_dir, "testing_fodder")

    # Try to read the control parameters
    control = ControlParams(4)
    control_file = os.path.join(fodder_dir, "control_parameters", "control.par")
    assert os.path.exists(control_file), f"Missing control file: {control_file}"
    control.read_control_par(control_file)

    # Try to read the calibration files
    ori_file = os.path.join(fodder_dir, "calibration", "cam1.tif.ori")
    add_file = os.path.join(fodder_dir, "calibration", "cam2.tif.addpar")
    assert os.path.exists(ori_file), f"Missing ori file: {ori_file}"
    assert os.path.exists(add_file), f"Missing addpar file: {add_file}"

    calibration = Calibration()
    calibration.from_file(ori_file, add_file)
