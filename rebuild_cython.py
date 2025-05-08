"""
Script to rebuild the Cython extensions with the correct compiler flags.
"""

import os
import sys
import glob
import shutil
import tempfile
import subprocess
import numpy as np
from setuptools import Extension
from Cython.Build import cythonize

def get_liboptv_sources():
    """Get all C source files from liboptv."""
    return glob.glob('./openptv/liboptv/src/*.c')

def build_extensions():
    """Build all Cython extensions."""
    print("Building Cython extensions...")
    
    # Get all .pyx files
    pyx_files = glob.glob('./openptv/binding/*.pyx')
    
    # Create extensions for all .pyx files
    extensions = []
    for pyx_file in pyx_files:
        # Get the module name from the .pyx file path
        module_name = os.path.splitext(os.path.basename(pyx_file))[0]
        module_path = f"openptv.binding.{module_name}"
        
        # Create an extension for this module
        extensions.append(
            Extension(
                module_path,
                [pyx_file] + get_liboptv_sources(),
                include_dirs=[
                    np.get_include(),
                    './openptv/liboptv/include/',
                    './openptv/binding/',
                    os.path.abspath('./openptv/liboptv/include/'),
                    os.path.abspath('./openptv/binding/'),
                ],
                extra_compile_args=['/W4', '/O2'] if sys.platform.startswith('win') else ['-Wno-cpp', '-Wno-unused-function', '-O3'],
                define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
            )
        )
    
    # Build the extensions
    cythonize(
        extensions,
        compiler_directives={
            'language_level': '3',
            'boundscheck': False,
            'wraparound': False,
            'initializedcheck': False,
        },
        force=True,
    )
    
    print("Cython extensions built successfully!")

def rename_extensions():
    """Rename the extensions to match the expected names."""
    print("Renaming extensions...")
    
    # Get all compiled extensions
    extensions = glob.glob('./openptv/binding/binding.*.cp310-win_amd64.pyd')
    
    for ext in extensions:
        # Get the module name
        module_name = ext.split('binding.')[1].split('.cp310')[0]
        # Create the new name
        new_name = ext.replace('binding.', '')
        # Remove the existing file if it exists
        if os.path.exists(new_name):
            os.remove(new_name)
        # Rename the file
        os.rename(ext, new_name)
        print(f"Renamed {ext} to {new_name}")
    
    print("All extensions renamed successfully!")

def install_package():
    """Install the package."""
    print("Installing package...")
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory: {temp_dir}")
        
        # Create a clean copy of the package
        package_dir = os.path.join(temp_dir, "openptv-python")
        print(f"Creating clean copy in: {package_dir}")
        
        # Copy the package directory
        shutil.copytree(".", package_dir, 
                       ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.egg-info"))
        
        # Copy the compiled extensions to the binding directory
        binding_dir = os.path.join(package_dir, "openptv", "binding")
        for ext in glob.glob('./openptv/binding/*.pyd'):
            shutil.copy2(ext, os.path.join(binding_dir, os.path.basename(ext)))
        
        # Install the package
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
            return False
        
        print("\nInstallation successful!")
        return True

def main():
    """Main function."""
    # Build the extensions
    build_extensions()
    
    # Rename the extensions
    rename_extensions()
    
    # Install the package
    if not install_package():
        return 1
    
    print("\nAll done!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
