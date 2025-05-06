"""
Simple test script to verify that the package is installed correctly.
"""

import os
import sys
import numpy as np

# Print Python version and path
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Try to import numpy
print(f"NumPy version: {np.__version__}")

# Try to import the package
try:
    import openptv
    print(f"OpenPTV version: {openptv.__version__}")
    print("OpenPTV imported successfully!")
except ImportError as e:
    print(f"Failed to import OpenPTV: {e}")

# Print the current working directory
print(f"Current working directory: {os.getcwd()}")

# Print the contents of the site-packages directory
import site
site_packages = site.getsitepackages()[0]
print(f"Site-packages directory: {site_packages}")
print("Contents of site-packages directory:")
for item in os.listdir(site_packages):
    if item.startswith('openptv'):
        print(f"  {item}")
