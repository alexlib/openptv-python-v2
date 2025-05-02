#!/usr/bin/env python
"""
Script to build binary wheels for the OpenPTV Python package.

This script provides a convenient way to build binary wheels for
distribution. It can build wheels for the current platform or
use cibuildwheel to build wheels for multiple platforms.
"""

import os
import sys
import subprocess
import argparse
import platform

def run_command(cmd):
    """Run a command and print its output."""
    print(f"Running: {' '.join(cmd)}")
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    
    for line in process.stdout:
        print(line, end="")
    
    process.wait()
    if process.returncode != 0:
        print(f"Command failed with exit code {process.returncode}")
        sys.exit(process.returncode)

def build_wheel():
    """Build a wheel for the current platform."""
    print("Building wheel for current platform...")
    run_command([sys.executable, "-m", "pip", "install", "build", "wheel"])
    run_command([sys.executable, "-m", "build", "--wheel"])
    print("Wheel built successfully. Check the 'dist/' directory.")

def build_sdist():
    """Build a source distribution."""
    print("Building source distribution...")
    run_command([sys.executable, "-m", "pip", "install", "build"])
    run_command([sys.executable, "-m", "build", "--sdist"])
    print("Source distribution built successfully. Check the 'dist/' directory.")

def build_cibuildwheel(platforms=None):
    """Build wheels for multiple platforms using cibuildwheel."""
    print("Building wheels with cibuildwheel...")
    run_command([sys.executable, "-m", "pip", "install", "cibuildwheel"])
    
    cmd = [sys.executable, "-m", "cibuildwheel", "--output-dir", "wheelhouse"]
    if platforms:
        cmd.extend(["--platform", platforms])
    
    run_command(cmd)
    print("Wheels built successfully. Check the 'wheelhouse/' directory.")

def upload_to_pypi(test=True):
    """Upload wheels to PyPI or TestPyPI."""
    run_command([sys.executable, "-m", "pip", "install", "twine"])
    
    if test:
        print("Uploading to TestPyPI...")
        run_command([
            sys.executable, "-m", "twine", "upload",
            "--repository-url", "https://test.pypi.org/legacy/",
            "dist/*"
        ])
    else:
        print("Uploading to PyPI...")
        run_command([sys.executable, "-m", "twine", "upload", "dist/*"])

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build wheels for OpenPTV Python")
    parser.add_argument("--sdist", action="store_true", help="Build source distribution")
    parser.add_argument("--wheel", action="store_true", help="Build wheel for current platform")
    parser.add_argument("--cibuildwheel", action="store_true", help="Build wheels with cibuildwheel")
    parser.add_argument("--platforms", help="Platforms to build for (linux, macos, windows)")
    parser.add_argument("--upload", action="store_true", help="Upload to PyPI")
    parser.add_argument("--test-upload", action="store_true", help="Upload to TestPyPI")
    
    args = parser.parse_args()
    
    # Default to building a wheel if no options specified
    if not (args.sdist or args.wheel or args.cibuildwheel or args.upload or args.test_upload):
        args.wheel = True
    
    if args.sdist:
        build_sdist()
    
    if args.wheel:
        build_wheel()
    
    if args.cibuildwheel:
        build_cibuildwheel(args.platforms)
    
    if args.upload:
        upload_to_pypi(test=False)
    
    if args.test_upload:
        upload_to_pypi(test=True)

if __name__ == "__main__":
    main()
