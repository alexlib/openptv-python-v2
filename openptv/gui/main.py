"""
Main entry point for the OpenPTV GUI application.

This module provides a main function that can be used as an entry point
when the package is installed. It sets up the environment and launches
either the full PyPTV GUI or the simplified TrajectoryViewer.
"""

import os
import sys
import numpy as np
import argparse

def main():
    """Main entry point for the OpenPTV GUI application."""
    # Set the toolkit before importing TraitsUI components
    os.environ['ETS_TOOLKIT'] = 'qt4'
    os.environ['QT_API'] = 'pyside6'  # or 'pyqt5'

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='OpenPTV GUI Application')
    parser.add_argument('--file', '-f', help='Path to trajectory data file')
    parser.add_argument('--demo', '-d', action='store_true', help='Use demo data')
    parser.add_argument('--viewer-only', '-v', action='store_true',
                        help='Launch only the trajectory viewer, not the full GUI')
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

    # Check if we should launch the full GUI or just the trajectory viewer
    if not args.viewer_only:
        try:
            from pyptv.pyptv_gui import PYPTV_GUI
            print("Launching PyPTV GUI...")
            gui = PYPTV_GUI()
            gui.configure_traits()
            return
        except ImportError as e:
            print(f"Warning: Could not import PyPTV GUI components: {e}")
            print("Falling back to trajectory viewer.")

    # If we're here, we're launching the trajectory viewer
    from openptv.gui.trajectory_viewer import TrajectoryViewer

    # Load trajectories
    trajectories = []

    if args.file:
        # Load trajectories from file
        try:
            # This is a placeholder - implement actual file loading based on your format
            print(f"Loading trajectories from {args.file}")
            # trajectories = load_trajectories(args.file)

            # For now, just generate some random data
            trajectories = generate_demo_trajectories()
        except Exception as e:
            print(f"Error loading file: {e}")
            print("Using demo data instead.")
            trajectories = generate_demo_trajectories()
    else:
        # Use demo data
        print("Using demo trajectories")
        trajectories = generate_demo_trajectories()

    # Create and show the trajectory viewer
    viewer = TrajectoryViewer(trajectories=trajectories)
    viewer.configure_traits()

def generate_demo_trajectories(num_trajectories=5):
    """Generate some random trajectories for demo purposes."""
    np.random.seed(42)
    trajectories = []

    for i in range(num_trajectories):
        # Create a random trajectory with 20 points
        length = np.random.randint(10, 30)
        traj = np.zeros((length, 3))

        # Start at a random position
        traj[0] = np.random.rand(3) * 10

        # Add random steps
        for j in range(1, length):
            traj[j] = traj[j-1] + np.random.normal(0, 0.2, 3)

        trajectories.append(traj)

    return trajectories

if __name__ == "__main__":
    main()
