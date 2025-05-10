"""
Test script to verify that tracking works correctly with the test_cavity directory.
"""

import os
from pathlib import Path
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from openptv.gui.ptv import py_start_proc_c, py_trackcorr_init

def main():
    """Run tracking on the test_cavity directory."""
    # Change to the test_cavity directory
    os.chdir('tests/test_cavity')
    
    # Initialize the parameters
    print("Initializing parameters...")
    num_cams = 4
    cpar, spar, vpar, track_par, tpar, cals, epar = py_start_proc_c(num_cams=num_cams)
    
    # Set the sequence parameters
    spar.set_first(10000)
    spar.set_last(10004)
    
    # Create an experiment object
    exp = {
        'cpar': cpar,
        'spar': spar,
        'vpar': vpar,
        'track_par': track_par,
        'tpar': tpar,
        'cals': cals,
        'epar': epar,
        'num_cams': num_cams,
    }
    
    # Convert dictionary keys to attributes
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self
    
    exp = AttrDict(exp)
    
    # Initialize the tracker
    print("Initializing tracker...")
    tracker = py_trackcorr_init(exp)
    
    # Run forward tracking
    print("Running forward tracking...")
    tracker.full_forward()
    
    # Run backward tracking
    print("Running backward tracking...")
    tracker.full_backward()
    
    print("Tracking completed successfully!")
    
    # Change back to the original directory
    os.chdir('../..')

if __name__ == "__main__":
    main()
