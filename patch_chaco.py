#!/usr/bin/env python
"""
Patch script for Chaco compatibility with newer NumPy versions.

This script can be run directly to patch Chaco files to work with newer versions of NumPy
by replacing deprecated functions:
- sometrue -> any
- alltrue -> all

Usage:
    python patch_chaco.py

The script will automatically find and patch the relevant files in your Python environment.
"""

import os
import re
import site
import sys


def patch_chaco_for_numpy_compatibility():
    """
    Patch Chaco files to work with newer versions of NumPy.
    
    This function patches the Chaco library files to replace deprecated NumPy functions
    with their modern equivalents:
    - sometrue -> any
    - alltrue -> all
    """
    try:
        # Find all site-packages directories
        site_packages = site.getsitepackages()
        
        # Add user site-packages if it exists
        if site.USER_SITE:
            site_packages.append(site.USER_SITE)
        
        # Files to patch and their replacements
        files_to_patch = {
            'chaco/log_mapper.py': [
                (r'from numpy import \(([^)]*?)sometrue([^)]*?)\)', r'from numpy import \g<1>any as sometrue\g<2>)'),
                (r'from numpy import \(([^)]*?)alltrue([^)]*?)\)', r'from numpy import \g<1>all as alltrue\g<2>)')
            ],
            'chaco/grid_mapper.py': [
                (r'from numpy import \(([^)]*?)sometrue([^)]*?)\)', r'from numpy import \g<1>any as sometrue\g<2>)'),
                (r'from numpy import \(([^)]*?)alltrue([^)]*?)\)', r'from numpy import \g<1>all as alltrue\g<2>)')
            ]
        }
        
        patched_files = []
        
        # Try to find and patch each file
        for site_pkg in site_packages:
            for file_path, replacements in files_to_patch.items():
                full_path = os.path.join(site_pkg, file_path)
                if os.path.exists(full_path):
                    try:
                        with open(full_path, 'r') as f:
                            content = f.read()
                        
                        # Apply all replacements
                        modified = False
                        for pattern, replacement in replacements:
                            new_content = re.sub(pattern, replacement, content)
                            if new_content != content:
                                content = new_content
                                modified = True
                        
                        # Only write if changes were made
                        if modified:
                            with open(full_path, 'w') as f:
                                f.write(content)
                            patched_files.append(full_path)
                            print(f"Patched {full_path} for NumPy compatibility")
                    except Exception as e:
                        print(f"Error patching {full_path}: {str(e)}")
        
        if not patched_files:
            print("No Chaco files were found or needed patching")
            
        return patched_files
    
    except Exception as e:
        print(f"Error during patching: {str(e)}")
        return []


if __name__ == "__main__":
    print("Applying patches for NumPy compatibility...")
    patched = patch_chaco_for_numpy_compatibility()
    
    if patched:
        print(f"Successfully patched {len(patched)} files:")
        for file in patched:
            print(f"  - {file}")
    else:
        print("No files were patched. Either the files don't exist, are already patched, or an error occurred.")
