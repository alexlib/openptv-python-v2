"""
Launcher script for the OpenPTV GUI.

This script provides a simple way to launch the PyPTV GUI from the command line.
It handles setting up the environment and importing the necessary components.
"""

import os
import sys
import argparse

def main():
    """Main entry point for the GUI launcher."""
    parser = argparse.ArgumentParser(description='Launch the OpenPTV GUI')
    parser.add_argument('--working-dir', '-w', help='Working directory for the GUI')
    args = parser.parse_args()
    
    # Set the working directory if specified
    if args.working_dir:
        os.chdir(args.working_dir)
    
    # Add the pyptv-gui directory to the Python path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pyptv_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'pyptv-gui'))
    if pyptv_path not in sys.path:
        sys.path.insert(0, pyptv_path)
    
    # Try to import and launch the GUI
    try:
        from pyptv.pyptv_gui import PYPTV_GUI
        print("Launching PyPTV GUI...")
        gui = PYPTV_GUI()
        gui.configure_traits()
    except ImportError as e:
        print(f"Error: Could not import PyPTV GUI components: {e}")
        print("Make sure the pyptv-gui submodule is properly initialized and installed.")
        print("You can initialize it with: git submodule update --init --recursive")
        sys.exit(1)

if __name__ == "__main__":
    main()
