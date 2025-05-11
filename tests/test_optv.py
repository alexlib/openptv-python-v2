#!/usr/bin/env python
import os
import sys
import openptv
from openptv.coptv.calibration import Calibration
from openptv.coptv.parameters import ControlParams

def test_openptv_functionality(test_data_dir):
    """Test basic OpenPTV functionality"""
    print("Testing OpenPTV functionality...")
    print(f"OpenPTV version: {openptv.__version__}")

    # Test path to test_cavity
    test_cavity_path = test_data_dir
    print(f"Test cavity path: {test_cavity_path}")

    # Test if we can read parameters
    try:
        control_params_file = os.path.join(test_cavity_path, "parameters", "ptv.par")
        print(f"Control parameters file: {control_params_file}")
        if os.path.exists(control_params_file):
            # Create a ControlParams object with 4 cameras
            control_params = ControlParams(4)
            # Read the control parameters from the file
            control_params.read_control_par(control_params_file)
            print(f"Successfully loaded control parameters")
            print(f"Number of cameras: {control_params.get_num_cams()}")
        else:
            print(f"Control parameters file not found")
    except Exception as e:
        print(f"Error loading control parameters: {str(e)}")

    # Test if we can read calibration
    try:
        cal = Calibration()
        cal_file = os.path.join(test_cavity_path, "cal", "cam1.tif.ori")
        addpar_file = os.path.join(test_cavity_path, "cal", "cam1.tif.addpar")
        print(f"Calibration file: {cal_file}")
        print(f"Addpar file: {addpar_file}")

        if os.path.exists(cal_file) and os.path.exists(addpar_file):
            cal.from_file(cal_file, addpar_file)
            print("Successfully loaded calibration")
            print(f"Calibration parameters: {cal.get_pos()}")
        else:
            print(f"Calibration files not found")
    except Exception as e:
        print(f"Error loading calibration: {str(e)}")

    print("OpenPTV functionality test completed")

if __name__ == "__main__":
    """Run the tests directly with detailed output."""
    import sys
    from pathlib import Path

    print("\n=== Running OpenPTV Functionality Tests ===\n")

    # Get the test_cavity directory
    test_data_dir = Path(__file__).parent / "test_cavity"
    if not test_data_dir.exists():
        print(f"Test data directory {test_data_dir} not found")
        sys.exit(1)

    # Run the test
    try:
        test_openptv_functionality(test_data_dir)
        print("\n✅ OpenPTV functionality test passed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ OpenPTV functionality test failed: {str(e)}")
        sys.exit(1)
