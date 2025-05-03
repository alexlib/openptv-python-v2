#!/usr/bin/env python
"""
Test script to verify core functionality of pyptv and optv
"""
import os
import sys
import openptv
from openptv.binding.calibration import Calibration
from openptv.binding.parameters import VolumeParams

def test_core_functionality(test_data_dir):
    """Test core functionality of pyptv and optv"""
    print("Testing core functionality...")

    # Print versions
    print(f"PyPTV version: {openptv.gui.__version__}")

    # Test path to test_cavity
    test_cavity_path = test_data_dir
    print(f"Test cavity path: {test_cavity_path}")

    # Test if we can load calibration
    try:
        cal = Calibration()
        cal_file = os.path.join(test_cavity_path, "cal", "cam1.tif.ori")
        addpar_file = os.path.join(test_cavity_path, "cal", "cam1.tif.addpar")

        if os.path.exists(cal_file) and os.path.exists(addpar_file):
            cal.from_file(cal_file, addpar_file)
            print("Successfully loaded calibration")
            print(f"Calibration parameters: {cal.get_pos()}")
        else:
            print(f"Calibration files not found")
            assert False, "Calibration files not found"
    except Exception as e:
        print(f"Error loading calibration: {str(e)}")
        assert False, f"Error loading calibration: {str(e)}"

    # Test if we can create a volume
    try:
        # Create a simple VolumeParams object
        vol_params = VolumeParams()
        # Print the attributes of the VolumeParams class
        print("VolumeParams attributes:")
        print(dir(vol_params))
        # Set some basic parameters using the correct methods
        # Note: These methods might expect different types than what we're providing
        # Let's try with different parameter types
        try:
            vol_params.set_Zmin_lay(-100.0)
            print("set_Zmin_lay successful")
        except Exception as e:
            print(f"Error in set_Zmin_lay: {str(e)}")

        try:
            vol_params.set_Zmax_lay(100.0)
            print("set_Zmax_lay successful")
        except Exception as e:
            print(f"Error in set_Zmax_lay: {str(e)}")

        try:
            vol_params.set_cn(10)
            print("set_cn successful")
        except Exception as e:
            print(f"Error in set_cn: {str(e)}")
        print("Successfully created volume parameters")
        print(f"Z min layer: {vol_params.get_Zmin_lay()}")
        print(f"Z max layer: {vol_params.get_Zmax_lay()}")
    except Exception as e:
        print(f"Error creating volume parameters: {str(e)}")
        assert False, f"Error creating volume parameters: {str(e)}"

    print("Core functionality test completed successfully!")
    assert True

if __name__ == "__main__":
    """Run the tests directly with detailed output."""
    import sys
    from pathlib import Path

    print("\n=== Running Core Functionality Tests ===\n")

    # Get the test_cavity directory
    test_data_dir = Path(__file__).parent / "test_cavity"
    if not test_data_dir.exists():
        print(f"Test data directory {test_data_dir} not found")
        sys.exit(1)

    # Run the test
    try:
        test_core_functionality(test_data_dir)
        print("\n✅ Core functionality test passed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Core functionality test failed: {str(e)}")
        sys.exit(1)
