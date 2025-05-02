"""
Test the integration of TraitsUI components with the rest of the OpenPTV package.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Set the toolkit to null for headless operation
os.environ['ETS_TOOLKIT'] = 'null'

# Import from openptv
from openptv import using_cython, track_particles, find_correspondences
from openptv.gui.trajectory_viewer import TrajectoryViewer

def test_integration_with_tracking():
    """Test the integration of TraitsUI components with tracking functionality."""
    print("Testing integration with tracking functionality...")
    
    # Generate some random particle positions
    np.random.seed(42)
    num_frames = 5
    num_particles = 10
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
    print(f"Using Cython implementation: {using_cython()}")
    trajectories = track_particles(all_particles, max_link_distance=1.0)
    
    # In a real implementation, trajectories would contain meaningful data
    # For this test, we'll create some dummy trajectories
    dummy_trajectories = []
    for i in range(num_particles):
        traj = np.array([particles[j][i] for j in range(num_frames)])
        dummy_trajectories.append(traj)
    
    # Create a TrajectoryViewer with these trajectories
    viewer = TrajectoryViewer(trajectories=dummy_trajectories)
    print(f"Created viewer with {len(dummy_trajectories)} trajectories")
    print(f"Current trajectory: {int(viewer.trajectory_id) + 1}")
    print(f"Status: {viewer.status}")
    
    # Create a figure to demonstrate the integration
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle('Integration of Tracking and GUI Components', fontsize=16)
    
    gs = GridSpec(2, 3, figure=fig)
    
    # 1. Raw particle data
    ax1 = fig.add_subplot(gs[0, 0], projection='3d')
    for frame_particles in particles:
        ax1.scatter(frame_particles[:, 0], frame_particles[:, 1], frame_particles[:, 2], 
                   s=20, alpha=0.5)
    ax1.set_title('Raw Particle Data')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    
    # 2. Tracking result
    ax2 = fig.add_subplot(gs[0, 1:], projection='3d')
    for traj in dummy_trajectories:
        ax2.plot(traj[:, 0], traj[:, 1], traj[:, 2], '-o', markersize=3)
    ax2.set_title('Tracking Result')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    
    # 3. TrajectoryViewer display
    ax3 = fig.add_subplot(gs[1, :], projection='3d')
    current_traj = dummy_trajectories[int(viewer.trajectory_id)]
    ax3.plot(current_traj[:, 0], current_traj[:, 1], current_traj[:, 2], 
            'b-o', linewidth=2, markersize=5)
    ax3.set_title(f'TrajectoryViewer Display (Trajectory {int(viewer.trajectory_id) + 1})')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    
    # Add controls at the bottom to simulate the TraitsUI interface
    plt.figtext(0.3, 0.05, 'Previous', ha='center', va='center', 
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgrey'))
    plt.figtext(0.5, 0.05, viewer.status, ha='center', va='center')
    plt.figtext(0.7, 0.05, 'Next', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgrey'))
    
    # Add a note about the integration
    plt.figtext(0.5, 0.01, 
                'The TrajectoryViewer provides an interactive interface to explore the trajectories produced by the tracking algorithm.',
                ha='center', fontsize=10, style='italic')
    
    plt.tight_layout(rect=[0, 0.07, 1, 0.97])
    fig.savefig('traitsui_integration.png', dpi=300)
    print("Integration demonstration saved as 'traitsui_integration.png'")

def test_workflow_diagram():
    """Create a diagram showing the complete workflow with GUI components."""
    print("\nCreating workflow diagram...")
    
    # Create a figure for the workflow diagram
    fig = plt.figure(figsize=(12, 8))
    fig.suptitle('OpenPTV Workflow with GUI Components', fontsize=16)
    
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    # Define the workflow steps
    steps = [
        ('Raw Data', 'Camera images with particles', (0.2, 0.9)),
        ('Calibration', 'Camera calibration using TraitsUI', (0.5, 0.9)),
        ('Detection', 'Particle detection in images', (0.8, 0.9)),
        ('Correspondence', 'find_correspondences() function', (0.2, 0.7)),
        ('Tracking', 'track_particles() function', (0.5, 0.7)),
        ('Filtering', 'Trajectory filtering', (0.8, 0.7)),
        ('Analysis', 'Statistical analysis', (0.2, 0.5)),
        ('Visualization', 'TrajectoryViewer component', (0.5, 0.5)),
        ('Export', 'Data export tools', (0.8, 0.5)),
        ('GUI Layer', 'TraitsUI/Chaco/Enable/Pyface', (0.5, 0.3)),
        ('Core Layer', 'C/Cython and Python implementations', (0.5, 0.1))
    ]
    
    # Draw boxes for each step
    for name, desc, (x, y) in steps:
        if 'TraitsUI' in desc or name == 'Visualization' or name == 'GUI Layer':
            color = 'lightblue'
        elif name == 'Core Layer' or name == 'Tracking' or name == 'Correspondence':
            color = 'lightgreen'
        else:
            color = 'lightyellow'
            
        rect = plt.Rectangle((x-0.15, y-0.05), 0.3, 0.1, fill=True, 
                            edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        ax.text(x, y+0.02, name, ha='center', va='center', fontsize=12, weight='bold')
        ax.text(x, y-0.02, desc, ha='center', va='center', fontsize=8)
    
    # Draw arrows between steps
    arrows = [
        ((0.2, 0.85), (0.2, 0.75)),  # Raw Data -> Correspondence
        ((0.5, 0.85), (0.5, 0.75)),  # Calibration -> Tracking
        ((0.8, 0.85), (0.8, 0.75)),  # Detection -> Filtering
        ((0.2, 0.75), (0.5, 0.75)),  # Correspondence -> Tracking
        ((0.5, 0.75), (0.8, 0.75)),  # Tracking -> Filtering
        ((0.2, 0.65), (0.2, 0.55)),  # Correspondence -> Analysis
        ((0.5, 0.65), (0.5, 0.55)),  # Tracking -> Visualization
        ((0.8, 0.65), (0.8, 0.55)),  # Filtering -> Export
        ((0.2, 0.55), (0.5, 0.55)),  # Analysis -> Visualization
        ((0.5, 0.55), (0.8, 0.55)),  # Visualization -> Export
        ((0.5, 0.45), (0.5, 0.35)),  # Visualization -> GUI Layer
        ((0.5, 0.25), (0.5, 0.15)),  # GUI Layer -> Core Layer
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(facecolor='black', shrink=0.05))
    
    # Add legend
    legend_items = [
        ('GUI Components', 'lightblue'),
        ('Core Functionality', 'lightgreen'),
        ('Data Processing', 'lightyellow')
    ]
    
    for i, (label, color) in enumerate(legend_items):
        rect = plt.Rectangle((0.1, 0.2 - i*0.05), 0.05, 0.03, fill=True, 
                            edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        ax.text(0.17, 0.215 - i*0.05, label, ha='left', va='center', fontsize=10)
    
    # Add a note about the workflow
    ax.text(0.5, 0.02, 
            'The OpenPTV package integrates GUI components with core functionality to provide\n'
            'a complete workflow from raw data to analysis and visualization.',
            ha='center', fontsize=10, style='italic')
    
    plt.tight_layout()
    fig.savefig('traitsui_workflow.png', dpi=300)
    print("Workflow diagram saved as 'traitsui_workflow.png'")

if __name__ == "__main__":
    test_integration_with_tracking()
    test_workflow_diagram()
