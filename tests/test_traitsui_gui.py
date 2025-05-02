"""
Test script to demonstrate the TraitsUI GUI components in a headless environment.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

# Set the toolkit to null for headless operation
os.environ['ETS_TOOLKIT'] = 'null'

# Import TraitsUI components
from traits.api import HasTraits, Instance, List, Float, Str, Button, on_trait_change
from traitsui.api import View, Item, Group, HGroup, VGroup, Handler
from chaco.api import Plot, ArrayPlotData
from enable.component_editor import ComponentEditor

# Import our trajectory viewer
from openptv.gui.trajectory_viewer import TrajectoryViewer

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

# Create a custom handler to capture the UI layout
class ScreenshotHandler(Handler):
    def init(self, info):
        super().init(info)
        return True

# Create a function to simulate the TraitsUI interface
def simulate_traitsui_interface():
    """Create a matplotlib figure that simulates the TraitsUI interface."""

    # Create a figure to represent the TraitsUI layout
    fig = plt.figure(figsize=(12, 10))
    fig.suptitle('TrajectoryViewer - TraitsUI Simulation', fontsize=16)

    # Main plot area (3D plot)
    ax_main = fig.add_subplot(111, projection='3d')

    # Plot the current trajectory
    current_traj_idx = 0
    traj = trajectories[current_traj_idx]
    ax_main.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'b-o', markersize=4)
    ax_main.set_xlabel('X')
    ax_main.set_ylabel('Y')
    ax_main.set_zlabel('Z')
    ax_main.set_title(f'Trajectory {current_traj_idx + 1} of {len(trajectories)}')

    # Add controls at the bottom
    plt.figtext(0.2, 0.05, 'Previous', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgrey'))
    plt.figtext(0.5, 0.05, f'Trajectory {current_traj_idx + 1} of {len(trajectories)}',
                ha='center', va='center')
    plt.figtext(0.8, 0.05, 'Next', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgrey'))

    # Add TraitsUI layout indicators
    plt.figtext(0.02, 0.98, 'VGroup', ha='left', va='top', fontsize=8, color='gray')
    plt.figtext(0.02, 0.1, 'HGroup', ha='left', va='center', fontsize=8, color='gray')

    # Add a note about the simulation
    plt.figtext(0.5, 0.01, 'Note: This is a simulation of the TraitsUI interface using matplotli',
                ha='center', fontsize=8, style='italic')

    plt.tight_layout(rect=[0, 0.07, 1, 0.97])
    return fig

# Create a function to show the TraitsUI code
def show_traitsui_code():
    """Display the TraitsUI code that would create this interface."""
    code = """
class TrajectoryViewer(HasTraits):
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

    # Event handlers
    def _next_button_fired(self):
        if len(self.trajectories) > 0:
            self.trajectory_id = (self.trajectory_id + 1) % len(self.trajectories)
            self._update_plot()

    def _prev_button_fired(self):
        if len(self.trajectories) > 0:
            self.trajectory_id = (self.trajectory_id - 1) % len(self.trajectories)
            self._update_plot()
    """
    return code

# Test the TrajectoryViewer
def test_trajectory_viewer():
    """Test the TrajectoryViewer component."""
    print("Testing TrajectoryViewer component...")

    # Create the viewer
    viewer = TrajectoryViewer(trajectories=trajectories)

    # Print information about the viewer
    print(f"Viewer created with {len(trajectories)} trajectories")
    print(f"Current trajectory ID: {viewer.trajectory_id}")
    print(f"Status: {viewer.status}")

    # Simulate button clicks
    print("\nSimulating button clicks:")
    print("Initial state:", viewer.trajectory_id)

    viewer._next_button_fired()
    print("After Next button:", viewer.trajectory_id)

    viewer._next_button_fired()
    print("After Next button:", viewer.trajectory_id)

    viewer._prev_button_fired()
    print("After Previous button:", viewer.trajectory_id)

    # Create a simulation of the TraitsUI interface
    print("\nCreating TraitsUI interface simulation...")
    fig = simulate_traitsui_interface()

    # Save the simulation
    fig.savefig('traitsui_simulation.png', dpi=300)
    print("TraitsUI simulation saved as 'traitsui_simulation.png'")

    # Show the TraitsUI code
    print("\nTraitsUI code that creates this interface:")
    print(show_traitsui_code())

    # Create a multi-view simulation
    print("\nCreating multi-view simulation...")
    fig_multi = plt.figure(figsize=(15, 10))
    fig_multi.suptitle('TrajectoryViewer - Multiple States', fontsize=16)

    # Show different states of the viewer
    for i in range(4):
        if i < len(trajectories):
            ax = fig_multi.add_subplot(2, 2, i+1, projection='3d')
            traj = trajectories[i]
            ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'b-o', markersize=3)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(f'Trajectory {i + 1}')

    plt.tight_layout()
    fig_multi.savefig('traitsui_multi_view.png', dpi=300)
    print("Multi-view simulation saved as 'traitsui_multi_view.png'")

def test_trajectory_viewer_component():
    """Pytest test for the TrajectoryViewer component."""
    test_trajectory_viewer()
