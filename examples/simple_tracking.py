"""
Simple example of tracking particles using OpenPTV.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Import from openptv
from openptv import using_cython

# The main package handles the import routing
from openptv import track_particles

print("Using Cython implementation" if using_cython() else "Using Python implementation")

# Generate some random particle positions
np.random.seed(42)
num_frames = 10
num_particles = 20
particles = []

for i in range(num_frames):
    # Create particles with small random movements
    if i == 0:
        frame_particles = np.random.rand(num_particles, 3) * 10
    else:
        # Add small random displacements to previous positions
        frame_particles = particles[-1] + np.random.normal(0, 0.2, (num_particles, 3))

    particles.append(frame_particles)

# Convert to a single array for the tracker
all_particles = np.vstack(particles)

# Track particles
trajectories = track_particles(all_particles, max_link_distance=1.0)

# In a real implementation, trajectories would contain meaningful data
# For this example, we'll create some dummy trajectories
dummy_trajectories = []
for i in range(num_particles):
    traj = np.array([particles[j][i] for j in range(num_frames)])
    dummy_trajectories.append(traj)

# Plot the trajectories
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for traj in dummy_trajectories:
    ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], '-o', markersize=3)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Particle Trajectories')

plt.tight_layout()
plt.show()
