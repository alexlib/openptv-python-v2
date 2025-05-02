"""
Example that creates a mockup of what the TraitsUI interface would look like.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Generate some random trajectories (same as in gui_example.py)
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

# Create a figure that mimics the TraitsUI interface
fig = plt.figure(figsize=(12, 10))
fig.suptitle('OpenPTV Trajectory Viewer (GUI Mockup)', fontsize=16)

# Use GridSpec to create a layout similar to the TraitsUI interface
gs = GridSpec(20, 20, figure=fig)

# Main plot area (similar to the Chaco plot in TraitsUI)
ax_main = fig.add_subplot(gs[0:18, 0:20], projection='3d')

# Plot the first trajectory
current_traj_idx = 0
traj = trajectories[current_traj_idx]
ax_main.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'b-o', markersize=4)
ax_main.set_xlabel('X')
ax_main.set_ylabel('Y')
ax_main.set_zlabel('Z')
ax_main.set_title(f'Trajectory {current_traj_idx + 1} of {len(trajectories)}')

# Add a status bar and navigation buttons (similar to the TraitsUI controls)
ax_prev = fig.add_subplot(gs[18:20, 0:6])
ax_prev.axis('off')
ax_prev.text(0.5, 0.5, 'Previous', ha='center', va='center', fontsize=12, 
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgrey'))

ax_status = fig.add_subplot(gs[18:20, 6:14])
ax_status.axis('off')
ax_status.text(0.5, 0.5, f'Trajectory {current_traj_idx + 1} of {len(trajectories)}', 
               ha='center', va='center', fontsize=12)

ax_next = fig.add_subplot(gs[18:20, 14:20])
ax_next.axis('off')
ax_next.text(0.5, 0.5, 'Next', ha='center', va='center', fontsize=12,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgrey'))

# Add a note about the GUI
fig.text(0.5, 0.01, 'Note: This is a mockup of the TraitsUI interface. The actual GUI would be interactive.', 
         ha='center', fontsize=10, style='italic')

# Save the figure
plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.savefig('gui_mockup.png', dpi=300)
print("GUI mockup saved as 'gui_mockup.png'")

# Create a second figure showing what the interface would look like when navigating
# through different trajectories
fig2 = plt.figure(figsize=(15, 10))
fig2.suptitle('OpenPTV Trajectory Viewer - Multiple Views (GUI Mockup)', fontsize=16)

# Create a 2x2 grid to show different trajectories
for i in range(4):
    if i < len(trajectories):
        ax = fig2.add_subplot(2, 2, i+1, projection='3d')
        traj = trajectories[i]
        ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], 'b-o', markersize=3)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'Trajectory {i + 1}')

plt.tight_layout()
plt.savefig('gui_mockup_multiple.png', dpi=300)
print("Multiple trajectories mockup saved as 'gui_mockup_multiple.png'")
