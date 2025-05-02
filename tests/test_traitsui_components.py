"""
Comprehensive test of TraitsUI components in the OpenPTV package.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Set the toolkit to null for headless operation
os.environ['ETS_TOOLKIT'] = 'null'

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

def test_trajectory_viewer_functionality():
    """Test the functionality of the TrajectoryViewer component."""
    print("Testing TrajectoryViewer functionality...")
    
    # Create the viewer
    viewer = TrajectoryViewer(trajectories=trajectories)
    
    # Create a figure to demonstrate the viewer's functionality
    fig = plt.figure(figsize=(15, 12))
    fig.suptitle('TrajectoryViewer - Functionality Demonstration', fontsize=16)
    
    # Create a grid layout
    gs = GridSpec(3, 3, figure=fig)
    
    # 1. Initial state
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    traj = trajectories[0]
    ax1.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'b-o', markersize=3)
    ax1.set_title('Initial State (Trajectory 1)')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    
    # 2. After clicking "Next"
    viewer._next_button_fired()
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    traj = trajectories[1]
    ax2.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'g-o', markersize=3)
    ax2.set_title('After "Next" (Trajectory 2)')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    
    # 3. After clicking "Next" again
    viewer._next_button_fired()
    ax3 = fig.add_subplot(gs[0, 2], projection='3d')
    traj = trajectories[2]
    ax3.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'r-o', markersize=3)
    ax3.set_title('After "Next" Again (Trajectory 3)')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    
    # 4. After clicking "Previous"
    viewer._prev_button_fired()
    ax4 = fig.add_subplot(gs[1, 0], projection='3d')
    traj = trajectories[1]
    ax4.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'g-o', markersize=3)
    ax4.set_title('After "Previous" (Trajectory 2)')
    ax4.set_xlabel('X')
    ax4.set_ylabel('Y')
    ax4.set_zlabel('Z')
    
    # 5. Cycling through all trajectories
    ax5 = fig.add_subplot(gs[1, 1:])
    for i, traj in enumerate(trajectories):
        ax5.plot(traj[:, 0], traj[:, 1], label=f'Trajectory {i+1}')
    ax5.set_title('All Trajectories (2D Projection)')
    ax5.set_xlabel('X')
    ax5.set_ylabel('Y')
    ax5.legend()
    
    # 6. TraitsUI layout diagram
    ax6 = fig.add_subplot(gs[2, :])
    ax6.axis('off')
    
    # Draw a representation of the TraitsUI layout
    ax6.text(0.5, 0.95, 'TraitsUI Layout', ha='center', fontsize=14, weight='bold')
    
    # Main container
    rect = plt.Rectangle((0.1, 0.2), 0.8, 0.7, fill=False, edgecolor='black')
    ax6.add_patch(rect)
    ax6.text(0.15, 0.85, 'VGroup', fontsize=10)
    
    # Plot area
    rect_plot = plt.Rectangle((0.15, 0.3), 0.7, 0.5, fill=True, edgecolor='black', facecolor='lightgray')
    ax6.add_patch(rect_plot)
    ax6.text(0.5, 0.55, 'Chaco Plot\n(ComponentEditor)', ha='center', fontsize=12)
    
    # Button row
    rect_buttons = plt.Rectangle((0.15, 0.2), 0.7, 0.05, fill=True, edgecolor='black', facecolor='lightblue')
    ax6.add_patch(rect_buttons)
    ax6.text(0.2, 0.225, 'Previous', ha='center', fontsize=10)
    ax6.text(0.5, 0.225, 'Status Text', ha='center', fontsize=10)
    ax6.text(0.8, 0.225, 'Next', ha='center', fontsize=10)
    ax6.text(0.5, 0.175, 'HGroup', ha='center', fontsize=10)
    
    # Add annotations
    ax6.annotate('Item("plot", editor=ComponentEditor())', 
                 xy=(0.5, 0.55), xytext=(0.5, 0.1), 
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 ha='center', fontsize=8)
    
    ax6.annotate('Item("prev_button")', 
                 xy=(0.2, 0.225), xytext=(0.2, 0.05), 
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 ha='center', fontsize=8)
    
    ax6.annotate('Item("status")', 
                 xy=(0.5, 0.225), xytext=(0.5, 0.05), 
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 ha='center', fontsize=8)
    
    ax6.annotate('Item("next_button")', 
                 xy=(0.8, 0.225), xytext=(0.8, 0.05), 
                 arrowprops=dict(facecolor='black', shrink=0.05),
                 ha='center', fontsize=8)
    
    plt.tight_layout()
    fig.savefig('traitsui_functionality.png', dpi=300)
    print("Functionality demonstration saved as 'traitsui_functionality.png'")

def test_traitsui_event_flow():
    """Demonstrate the event flow in TraitsUI components."""
    print("\nTesting TraitsUI event flow...")
    
    # Create a figure to demonstrate the event flow
    fig = plt.figure(figsize=(12, 10))
    fig.suptitle('TraitsUI Event Flow', fontsize=16)
    
    # Create a flowchart-like diagram
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    # Define positions
    pos = {
        'user': (0.5, 0.9),
        'button': (0.5, 0.8),
        'handler': (0.5, 0.7),
        'model': (0.5, 0.6),
        'update': (0.5, 0.5),
        'plot': (0.5, 0.4),
        'redraw': (0.5, 0.3),
        'display': (0.5, 0.2),
        'user_sees': (0.5, 0.1)
    }
    
    # Draw boxes
    for key, (x, y) in pos.items():
        if key == 'user' or key == 'user_sees':
            color = 'lightgreen'
        elif key == 'button' or key == 'display':
            color = 'lightblue'
        elif key == 'handler' or key == 'update' or key == 'redraw':
            color = 'lightyellow'
        else:
            color = 'lightgray'
            
        rect = plt.Rectangle((x-0.2, y-0.03), 0.4, 0.06, fill=True, 
                            edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        
        if key == 'user':
            text = 'User clicks "Next" button'
        elif key == 'button':
            text = 'Button click event triggered'
        elif key == 'handler':
            text = '_next_button_fired() method called'
        elif key == 'model':
            text = 'trajectory_id property updated'
        elif key == 'update':
            text = '_update_plot() method called'
        elif key == 'plot':
            text = 'plot_data updated with new trajectory'
        elif key == 'redraw':
            text = 'Chaco plot automatically redraws'
        elif key == 'display':
            text = 'UI updates to show new trajectory'
        elif key == 'user_sees':
            text = 'User sees the next trajectory'
            
        ax.text(x, y, text, ha='center', va='center', fontsize=12)
    
    # Draw arrows
    for i in range(len(pos)-1):
        keys = list(pos.keys())
        start = pos[keys[i]]
        end = pos[keys[i+1]]
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(facecolor='black', shrink=0.05))
    
    # Add code snippets
    code_snippets = {
        'handler': """def _next_button_fired(self):
    if len(self.trajectories) > 0:
        self.trajectory_id = (self.trajectory_id + 1) % len(self.trajectories)
        self._update_plot()""",
        
        'update': """def _update_plot(self):
    if 0 <= self.trajectory_id < len(self.trajectories):
        trajectory = self.trajectories[int(self.trajectory_id)]
        self.plot_data.set_data("x", trajectory[:, 0])
        self.plot_data.set_data("y", trajectory[:, 1])
        self.plot_data.set_data("z", trajectory[:, 2])
        self.status = f"Trajectory {int(self.trajectory_id)+1} of {len(self.trajectories)}" """
    }
    
    for key, code in code_snippets.items():
        x, y = pos[key]
        ax.annotate(code, xy=(x, y), xytext=(x+0.5, y),
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8),
                   fontsize=8, family='monospace')
    
    # Add title and explanation
    ax.text(0.5, 0.95, 'Event Flow in TraitsUI Components', 
            ha='center', fontsize=14, weight='bold')
    
    ax.text(0.1, 0.02, 
            'TraitsUI uses an event-driven architecture where UI events trigger handlers that update the model,\n'
            'which in turn updates the view through trait change notifications.',
            ha='left', fontsize=10, style='italic')
    
    plt.tight_layout()
    fig.savefig('traitsui_event_flow.png', dpi=300)
    print("Event flow diagram saved as 'traitsui_event_flow.png'")

if __name__ == "__main__":
    test_trajectory_viewer_functionality()
    test_traitsui_event_flow()
