"""
Example of using the GUI components in OpenPTV in headless mode.
This version saves the trajectories as a matplotlib plot instead of using the GUI.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

# Create a matplotlib 3D plot instead of using the TraitsUI viewer
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot each trajectory with a different color
colors = ['', 'g', 'r', 'c', 'm', 'y', 'k']
for i, traj in enumerate(trajectories):
    color = colors[i % len(colors)]
    ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], color=color, marker='o', markersize=3, label=f'Trajectory {i+1}')

# Add labels and legend
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Particle Trajectories')
ax.legend()

# Save the figure instead of displaying it
plt.tight_layout()
plt.savefig('trajectories.png', dpi=300)
print("Trajectories plot saved as 'trajectories.png'")
