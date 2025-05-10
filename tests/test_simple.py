import numpy as np
import pytest
from openptv.binding.parameters import ControlParams
from openptv.binding.calibration import Calibration

def test_control_and_calibration_creation():
    control = ControlParams(4)
    assert control is not None

    calibration = Calibration()
    assert calibration is not None

    # Set some values and check if no exceptions are raised
    calibration.set_pos(np.array([0.0, 0.0, 40.0]))
    calibration.set_angles(np.array([0.0, 0.0, 0.0]))
