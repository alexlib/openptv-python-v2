"""
Script to rename Cython extensions to match the expected names.
"""

import os
import glob

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
