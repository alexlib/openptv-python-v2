"""
Example of using the GUI components in OpenPTV with PySide6 backend.
"""

import os
import sys
import numpy as np

# Set the toolkit to PySide6 before importing any TraitsUI components
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyside6'

# Import TraitsUI components
from openptv.gui.trajectory_viewer import TrajectoryViewer

def main():
    # Generate some random trajectories
    np.random.seed(42)
    num_trajectories = 5
    trajectories = []
    
    for i in range(num_trajectories):
        # Create a random trajectory with 20 points
        length = np.random.randint(10, 30)
        traj = np.zeros((length, 3))
        
        # Start at a random position
        traj[0] = np.random.rand(3) * 10
        
        # Add random steps
        for j in range(1, length):
            traj[j] = traj[j-1] + np.random.normal(0, 0.5, 3)
        
        trajectories.append(traj)
    
    # Create and show the trajectory viewer
    viewer = TrajectoryViewer(trajectories=trajectories)
    viewer.configure_traits()

if __name__ == "__main__":
    main()
