"""
Example of using the unified parameter module.

This script demonstrates how to use the unified parameter module to read, modify,
and write parameter files, and how to use the parameters with C functions.
"""

import os
from pathlib import Path

# Import parameter classes from the unified module
from openptv.parameters import TrackingParams, SequenceParams, VolumeParams

# Import bridge functions for calling C functions with Python parameter objects
from openptv.coptv.tracker_bridge import track_forward_with_params


def main():
    """
    Main function for the parameter example.
    """
    # Get the path to the parameter directory
    par_path = Path("path/to/parameters")
    
    # Create a TrackingParams object
    track_params = TrackingParams(path=par_path)
    
    # Read parameters from file
    track_params.read()
    
    # Modify parameters
    track_params.dvxmin = -10.0
    track_params.dvxmax = 10.0
    
    # Write parameters to file
    track_params.write()
    
    # Create a VolumeParams object
    vol_params = VolumeParams(path=par_path)
    
    # Read parameters from file
    vol_params.read()
    
    # Use parameters with C functions
    targets = []  # TODO: Load targets
    results = track_forward_with_params(targets, track_params, vol_params)
    
    print("Tracking results:", results)


if __name__ == "__main__":
    main()
