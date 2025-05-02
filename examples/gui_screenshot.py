"""
Example that takes a screenshot of the TraitsUI GUI.
"""

import os
import sys
import time
import numpy as np
from PIL import ImageGrab

# Set the toolkit to PySide6 before importing any TraitsUI components
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyside6'

# Import TraitsUI components
from traits.api import HasTraits, Instance, List, Float, Str, Button, on_trait_change
from traitsui.api import View, Item, Group, HGroup, VGroup
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor
from pyface.timer.api import Timer

# Import our trajectory viewer
from openptv.gui.trajectory_viewer import TrajectoryViewer

class ScreenshotApp(HasTraits):
    """Application that takes a screenshot of the TrajectoryViewer."""
    
    viewer = Instance(TrajectoryViewer)
    timer = Instance(Timer)
    
    traits_view = View(
        Item('viewer', style='custom', show_label=False),
        title='OpenPTV Trajectory Viewer',
        width=800,
        height=600,
        resizable=True,
    )
    
    def __init__(self, **traits):
        super(ScreenshotApp, self).__init__(**traits)
        self.timer = Timer(5000, self.take_screenshot)
    
    def take_screenshot(self):
        """Take a screenshot of the application window."""
        print("Taking screenshot...")
        try:
            # Take a screenshot of the entire screen
            screenshot = ImageGrab.grab()
            screenshot.save('gui_screenshot.png')
            print("Screenshot saved as 'gui_screenshot.png'")
        except Exception as e:
            print(f"Error taking screenshot: {e}")
        
        # Exit the application after taking the screenshot
        print("Exiting application...")
        os._exit(0)

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
    
    # Create the trajectory viewer
    viewer = TrajectoryViewer(trajectories=trajectories)
    
    # Create the screenshot application
    app = ScreenshotApp(viewer=viewer)
    
    # Start the timer and show the application
    app.timer.start()
    app.configure_traits()

if __name__ == "__main__":
    main()
