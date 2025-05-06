"""
Test script to verify that openptv-python is installed correctly.
"""

try:
    import openptv
    print(f"openptv version: {openptv.__version__}")
    print("openptv imported successfully!")
    
    # Try to import some modules
    try:
        from openptv.binding import calibration
        print("Successfully imported calibration module from binding")
    except ImportError as e:
        print(f"Failed to import calibration from binding: {e}")
        
    try:
        from openptv.pyoptv import calibration
        print("Successfully imported calibration module from pyoptv")
    except ImportError as e:
        print(f"Failed to import calibration from pyoptv: {e}")
        
except ImportError as e:
    print(f"Failed to import openptv: {e}")
