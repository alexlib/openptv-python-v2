"""
Script to fix the installation of openptv-python.

This script:
1. Creates a clean copy of the binding directory
2. Installs the package from the clean copy
"""

import os
import shutil
import sys
import tempfile
import subprocess

def main():
    """Main function."""
    print("Starting installation fix...")
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory: {temp_dir}")
        
        # Create a clean copy of the package
        package_dir = os.path.join(temp_dir, "openptv-python")
        print(f"Creating clean copy in: {package_dir}")
        
        # Copy the package directory
        shutil.copytree(".", package_dir, 
                       ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyd", "*.so", "*.dll", "*.egg-info"))
        
        # Create the binding directory
        binding_dir = os.path.join(package_dir, "openptv", "binding")
        os.makedirs(binding_dir, exist_ok=True)
        
        # Copy only the .pyx and .pxd files to the binding directory
        src_binding_dir = os.path.join("openptv", "binding")
        for file in os.listdir(src_binding_dir):
            if file.endswith(".pyx") or file.endswith(".pxd"):
                shutil.copy2(os.path.join(src_binding_dir, file), os.path.join(binding_dir, file))
        
        # Create an empty __init__.py file in the binding directory
        with open(os.path.join(binding_dir, "__init__.py"), "w") as f:
            f.write("# This file is intentionally left empty\n")
        
        # Install the package from the clean copy
        print("Installing package from clean copy...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "."],
            cwd=package_dir,
            capture_output=True,
            text=True
        )
        
        # Print the output
        print("\nInstallation output:")
        print(result.stdout)
        
        if result.returncode != 0:
            print("\nInstallation error:")
            print(result.stderr)
            print("\nInstallation failed!")
            return 1
        
        print("\nInstallation successful!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
