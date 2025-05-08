"""
Script to run the tests for the openptv-python package.
"""

import os
import sys
import subprocess

def main():
    """Main function."""
    print("Running tests for openptv-python...")
    
    # Run the import tests
    print("\nRunning import tests...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_imports.py", "-v"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.returncode != 0:
        print("Import tests failed!")
        print(result.stderr)
        return 1
    
    # Run the version test
    print("\nRunning version test...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_version.py", "-v"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.returncode != 0:
        print("Version test failed!")
        print(result.stderr)
        return 1
    
    print("\nAll tests passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
