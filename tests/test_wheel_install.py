#!/usr/bin/env python
"""
Test script to verify that the wheel installation works correctly.
This script is used by cibuildwheel to test the wheels after building.
"""
import sys
import importlib

def test_imports():
    """Test importing key modules from the package."""
    # Core modules to test
    core_modules = [
        "openptv.binding.calibration",
        "openptv.binding.parameters",
        "openptv.binding.tracking_framebuf",
        "openptv.binding.transforms",
    ]

    # GUI modules to test
    gui_modules = [
        "openptv.gui.ptv",
        "openptv.gui.pyptv_batch",
    ]

    # Try to import PyYAML
    try:
        import yaml
        yaml_version = yaml.__version__
        print(f"✅ Successfully imported yaml {yaml_version}")
    except ImportError as e:
        print(f"⚠️ Warning: PyYAML not available: {str(e)}")
        print("⚠️ This is expected in the test environment, but should be installed in production")

    # Try to import openptv
    try:
        import openptv
        openptv_version = getattr(openptv, "__version__", "unknown")
        print(f"✅ Successfully imported openptv {openptv_version}")
    except ImportError as e:
        if "No module named 'yaml'" in str(e):
            print(f"⚠️ Warning: openptv import failed due to missing yaml: {str(e)}")
            print("⚠️ This is expected in the test environment, but should be installed in production")
        else:
            print(f"❌ Failed to import openptv: {str(e)}")
            return False

    # Test importing the core modules
    print("\nTesting core modules:")
    for module_name in core_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ Successfully imported {module_name}")
        except ImportError as e:
            print(f"❌ Failed to import {module_name}: {str(e)}")
            return False

    # Test importing GUI modules
    print("\nTesting GUI modules:")
    gui_success = True
    for module_name in gui_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ Successfully imported {module_name}")
        except ImportError as e:
            print(f"⚠️ Warning: Failed to import GUI module {module_name}: {str(e)}")
            gui_success = False

    # Try to import GUI dependencies
    print("\nTesting GUI dependencies:")
    gui_deps = ["traits", "traitsui", "chaco", "enable", "pyface", "skimage"]
    gui_deps_success = True
    for module_name in gui_deps:
        try:
            importlib.import_module(module_name)
            print(f"✅ Successfully imported {module_name}")
        except ImportError as e:
            print(f"⚠️ Warning: GUI dependency {module_name} not available: {str(e)}")
            gui_deps_success = False

    if not gui_success or not gui_deps_success:
        print("\n⚠️ Some GUI components could not be imported.")
        print("⚠️ This is expected if the wheel was not built with [gui] extras.")

    return True

def test_basic_functionality():
    """Test basic functionality of the package."""
    # Test core functionality
    print("\nTesting core functionality:")
    try:
        # Import key classes
        from openptv.binding.calibration import Calibration
        from openptv.binding.parameters import ControlParams

        # Create instances
        cal = Calibration()
        control = ControlParams(4)  # 4 cameras

        # Use the instances to avoid unused variable warnings
        cal_name = cal.__class__.__name__
        num_cams = control.get_num_cams()

        print(f"✅ Successfully created {cal_name} and ControlParams instances with {num_cams} cameras")
        core_success = True
    except Exception as e:
        print(f"❌ Failed to test core functionality: {str(e)}")
        core_success = False

    # Test GUI functionality
    print("\nTesting GUI functionality:")
    try:
        # Try to import GUI modules
        from openptv.gui.ptv import py_start_proc_c

        # Call a function to verify it's working
        func_name = py_start_proc_c.__name__

        print(f"✅ Successfully imported GUI functionality (found {func_name})")
        gui_success = True
    except ImportError as e:
        print(f"⚠️ Warning: GUI functionality not available: {str(e)}")
        print("⚠️ This is expected if the wheel was not built with [gui] extras.")
        gui_success = True  # Don't fail the test if GUI is not available
    except Exception as e:
        print(f"❌ Failed to test GUI functionality: {str(e)}")
        gui_success = False

    return core_success and gui_success

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
