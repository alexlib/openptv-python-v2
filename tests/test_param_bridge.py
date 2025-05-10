#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the parameter bridge between Python and Cython.
"""

import sys
import os

# Add the parent directory to the path so we can import openptv
sys.path.append(os.path.abspath('..'))

from openptv.parameters import TrackingParams
from openptv.binding.parameters import TrackingParams as CythonTrackingParams

def test_tracking_params_to_cython():
    """Test converting a Python TrackingParams to a Cython TrackingParams."""
    # Create a Python TrackingParams object
    py_params = TrackingParams(
        dvxmin=-10.0,
        dvxmax=10.0,
        dvymin=-10.0,
        dvymax=10.0,
        dvzmin=-10.0,
        dvzmax=10.0,
        dangle=30.0,
        dacc=0.5,
        flagNewParticles=True
    )

    # Convert to a Cython TrackingParams object
    print("Converting Python TrackingParams to Cython TrackingParams...")
    try:
        cy_params = py_params.to_cython_object()
        print("Conversion successful!")
    except Exception as e:
        print(f"Error during conversion: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Check that it's the right type
    assert isinstance(cy_params, CythonTrackingParams)

    # Check that the values were transferred correctly
    assert cy_params.get_dvxmin() == py_params.dvxmin
    assert cy_params.get_dvxmax() == py_params.dvxmax
    assert cy_params.get_dvymin() == py_params.dvymin
    assert cy_params.get_dvymax() == py_params.dvymax
    assert cy_params.get_dvzmin() == py_params.dvzmin
    assert cy_params.get_dvzmax() == py_params.dvzmax
    assert cy_params.get_dangle() == py_params.dangle
    assert cy_params.get_dacc() == py_params.dacc
    assert cy_params.get_add() == 1  # True is converted to 1

    print("✅ test_tracking_params_to_cython passed")

if __name__ == "__main__":
    test_tracking_params_to_cython()
    print("All tests passed!")
