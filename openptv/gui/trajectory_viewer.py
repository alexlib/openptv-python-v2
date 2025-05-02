"""
Trajectory viewer component based on TraitsUI and Chaco.
"""

from traits.api import HasTraits, Instance, List, Float, Str, Button
from traitsui.api import View, Item, Group, HGroup, VGroup
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor
import numpy as np

class TrajectoryViewer(HasTraits):
    """
    A viewer for 3D particle trajectories.
    
    This component uses TraitsUI for the interface and Chaco for plotting.
    """
    
    # Data
    trajectories = List  # List of trajectory arrays
    
    # Plot components
    plot = Instance(Plot)
    plot_data = Instance(ArrayPlotData)
    
    # Controls
    trajectory_id = Float(0)
    next_button = Button("Next")
    prev_button = Button("Previous")
    status = Str("No trajectories loaded")
    
    def __init__(self, trajectories=None, **traits):
        """Initialize with optional trajectories."""
        super(TrajectoryViewer, self).__init__(**traits)
        
        # Initialize plot data
        self.plot_data = ArrayPlotData(x=np.array([]), y=np.array([]), z=np.array([]))
        
        # Create plot
        plot = Plot(self.plot_data)
        plot.plot(("x", "y"), type="line", color="blue")
        plot.title = "Particle Trajectory"
        plot.x_axis.title = "X"
        plot.y_axis.title = "Y"
        self.plot = plot
        
        # Set trajectories if provided
        if trajectories is not None:
            self.trajectories = trajectories
            if len(trajectories) > 0:
                self.status = f"Trajectory 1 of {len(trajectories)}"
                self._update_plot()
    
    def _next_button_fired(self):
        """Handle next button click."""
        if len(self.trajectories) > 0:
            self.trajectory_id = (self.trajectory_id + 1) % len(self.trajectories)
            self._update_plot()
    
    def _prev_button_fired(self):
        """Handle previous button click."""
        if len(self.trajectories) > 0:
            self.trajectory_id = (self.trajectory_id - 1) % len(self.trajectories)
            self._update_plot()
    
    def _update_plot(self):
        """Update the plot with the current trajectory."""
        if 0 <= self.trajectory_id < len(self.trajectories):
            trajectory = self.trajectories[int(self.trajectory_id)]
            self.plot_data.set_data("x", trajectory[:, 0])
            self.plot_data.set_data("y", trajectory[:, 1])
            self.plot_data.set_data("z", trajectory[:, 2])
            self.status = f"Trajectory {int(self.trajectory_id)+1} of {len(self.trajectories)}"
    
    # TraitsUI view
    traits_view = View(
        VGroup(
            Item('plot', editor=ComponentEditor(), show_label=False),
            HGroup(
                Item('prev_button', show_label=False),
                Item('status', style='readonly', show_label=False),
                Item('next_button', show_label=False),
            ),
        ),
        resizable=True,
        width=800,
        height=600,
        title="Trajectory Viewer"
    )
