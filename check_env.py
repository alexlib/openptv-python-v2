"""
Script to check the current conda environment.
"""

import os
import sys

def main():
    """Main function."""
    print(f"Python executable: {sys.executable}")
    
    # Check if we're in a conda environment
    conda_prefix = os.environ.get('CONDA_PREFIX')
    if conda_prefix:
        print(f"Conda environment: {os.path.basename(conda_prefix)}")
    else:
        print("Not in a conda environment")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
