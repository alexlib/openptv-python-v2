#!/usr/bin/env python
"""
Test script to verify that the wheel installation works correctly.
This script is used by cibuildwheel to test the wheels after building.
"""
import sys
import importlib.util

def test_imports():
    """Test importing key modules from the package."""
    modules_to_test = [
        "openptv",
        "openptv.coptv.calibration",
        "openptv.coptv.parameters",
        "openptv.coptv.tracking_framebuf",
        "openptv.coptv.transforms",
    ]

    for module_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            print(f"✅ Successfully imported {module_name}")
        except ImportError as e:
            print(f"❌ Failed to import {module_name}: {str(e)}")
            assert False, f"Failed to import {module_name}: {str(e)}"

    # If we get here, all imports succeeded
    assert True

def test_basic_functionality():
    """Test basic functionality of the package."""
    try:
        # Import key classes
        from openptv.coptv.calibration import Calibration
        from openptv.coptv.parameters import ControlParams

        # Create instances
        cal = Calibration()
        control = ControlParams(4)  # 4 cameras

        # Test that instances are of the correct type
        assert isinstance(cal, Calibration)
        assert isinstance(control, ControlParams)

        print(f"✅ Successfully created Calibration and ControlParams instances")
    except Exception as e:
        print(f"❌ Failed to test basic functionality: {str(e)}")
        assert False, f"Failed to test basic functionality: {str(e)}"

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print(f"Testing wheel installation...")

    import_success = test_imports()
    functionality_success = test_basic_functionality()

    if import_success and functionality_success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
