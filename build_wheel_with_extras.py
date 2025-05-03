#!/usr/bin/env python
"""
Build a wheel with GUI and dev extras included.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_wheel_with_extras():
    """Build a wheel with GUI and dev extras included."""
    # Create a temporary directory for the build
    build_dir = Path("build_wheel_temp")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()
    
    # Create a wheelhouse directory
    wheelhouse = Path("wheelhouse")
    if not wheelhouse.exists():
        wheelhouse.mkdir()
    
    try:
        # Install build dependencies
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "numpy>=1.19.0,<2.0", "cython>=0.29.21", "wheel", "setuptools>=42"
        ])
        
        # Build the wheel with extras
        subprocess.check_call([
            sys.executable, "-m", "pip", "wheel", 
            "--no-deps", 
            "-w", str(build_dir),
            ".[gui,dev]"
        ])
        
        # Copy the wheel to the wheelhouse directory
        for wheel_file in build_dir.glob("*.whl"):
            shutil.copy(wheel_file, wheelhouse)
            print(f"Built wheel: {wheel_file.name}")
            
        print(f"\nWheels are available in the {wheelhouse} directory")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building wheel: {e}")
        return False
    finally:
        # Clean up
        if build_dir.exists():
            shutil.rmtree(build_dir)

if __name__ == "__main__":
    success = build_wheel_with_extras()
    sys.exit(0 if success else 1)
