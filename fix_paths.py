"""
Script to fix the paths for the compiled extensions.
"""

import os
import shutil
import site
import sys

# Get the site-packages directory
site_packages = site.getsitepackages()[0]

# Create the openptv/binding directory in site-packages if it doesn't exist
binding_dir = os.path.join(site_packages, 'openptv', 'binding')
os.makedirs(binding_dir, exist_ok=True)

# Copy all .pyd files from the local binding directory to the site-packages binding directory
local_binding_dir = os.path.join(os.getcwd(), 'openptv', 'binding')
for file in os.listdir(local_binding_dir):
    if file.endswith('.pyd'):
        src = os.path.join(local_binding_dir, file)
        dst = os.path.join(binding_dir, file)
        print(f"Copying {src} to {dst}")
        shutil.copy2(src, dst)

print("Done!")
