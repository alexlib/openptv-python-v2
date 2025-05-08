"""
Script to check DLL dependencies of Cython extensions.
"""

import os
import sys
import ctypes
from ctypes import windll
import glob

def main():
    """Main function."""
    print("Checking DLL dependencies of Cython extensions...")
    
    # Get the binding directory
    binding_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openptv', 'binding')
    
    # Find all .pyd files
    pyd_files = glob.glob(os.path.join(binding_dir, '*.pyd'))
    
    if not pyd_files:
        print("No .pyd files found in the binding directory!")
        return 1
    
    # Try to load each .pyd file
    for pyd_file in pyd_files:
        print(f"\nTrying to load: {os.path.basename(pyd_file)}")
        try:
            # Try to load the DLL
            dll = ctypes.cdll.LoadLibrary(pyd_file)
            print(f"  Successfully loaded {os.path.basename(pyd_file)}")
        except Exception as e:
            print(f"  Failed to load {os.path.basename(pyd_file)}: {e}")
            
            # Try to get more information about the missing DLL
            try:
                error_code = ctypes.GetLastError()
                print(f"  Error code: {error_code}")
                
                # Use windll.kernel32.FormatMessageA to get the error message
                error_msg = ctypes.create_string_buffer(256)
                windll.kernel32.FormatMessageA(
                    0x1300,  # FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS
                    None,
                    error_code,
                    0,
                    error_msg,
                    256,
                    None
                )
                print(f"  Error message: {error_msg.value.decode('utf-8')}")
            except Exception as e2:
                print(f"  Failed to get error details: {e2}")
    
    # Print the current PATH
    print("\nCurrent PATH:")
    for path in os.environ['PATH'].split(os.pathsep):
        print(f"  {path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
