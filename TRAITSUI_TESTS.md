# TraitsUI Components Testing

This document summarizes the tests performed on the TraitsUI-based GUI components of the OpenPTV Python package.

## Overview

The OpenPTV Python package includes GUI components built with TraitsUI, Chaco, Enable, and Pyface. These components provide interactive visualization and control for working with PTV data. Since we're in a headless environment, we've created simulations and diagrams to demonstrate how these components work.

## Tests Performed

### 1. Basic TraitsUI Simulation

**File:** `test_traitsui_gui.py`

This test creates a simulation of the TraitsUI interface using matplotlib. It demonstrates:
- The basic layout of the TrajectoryViewer component
- The structure of the TraitsUI code that creates this interface
- Multiple views of different trajectories

**Output:**
- `traitsui_simulation.png` - Basic simulation of the TraitsUI interface
- `traitsui_multi_view.png` - Multiple views of different trajectories

### 2. TraitsUI Component Functionality

**File:** `test_traitsui_components.py`

This test demonstrates the functionality of the TraitsUI components in more detail:
- The initial state of the TrajectoryViewer
- The effect of clicking the "Next" and "Previous" buttons
- The TraitsUI layout with detailed annotations
- The event flow in TraitsUI components

**Output:**
- `traitsui_functionality.png` - Detailed demonstration of component functionality
- `traitsui_event_flow.png` - Diagram showing the event flow in TraitsUI components

### 3. Integration with Tracking Functionality

**File:** `test_traitsui_integration.py`

This test demonstrates how the TraitsUI components integrate with the rest of the OpenPTV package:
- The flow from raw particle data to tracking results to visualization
- The complete workflow of the OpenPTV package with GUI components
- The layered architecture of the package

**Output:**
- `traitsui_integration.png` - Demonstration of integration with tracking functionality
- `traitsui_workflow.png` - Diagram showing the complete workflow with GUI components

## TraitsUI Components

### TrajectoryViewer

The main GUI component tested is the `TrajectoryViewer`, which is defined in `openptv/gui/trajectory_viewer.py`. This component:

- Displays 3D particle trajectories using Chaco
- Provides navigation controls to browse through multiple trajectories
- Updates the display when the user clicks the "Next" or "Previous" buttons
- Shows status information about the current trajectory

The TrajectoryViewer is implemented as a HasTraits class with the following key components:

```python
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
```

### Event Handling

The TraitsUI components use an event-driven architecture:

1. User interactions (like button clicks) trigger events
2. Event handlers (like `_next_button_fired()`) respond to these events
3. The handlers update the model (like `trajectory_id`)
4. Trait change notifications automatically update the view

This architecture makes the code clean and maintainable, with a clear separation of concerns.

## Integration with OpenPTV

The GUI components integrate with the rest of the OpenPTV package:

1. The tracking functionality (`track_particles()`) produces trajectories
2. These trajectories can be visualized using the TrajectoryViewer
3. The user can interactively explore the trajectories
4. The same API works with both the Cython and Python implementations

This integration provides a complete workflow from raw data to analysis and visualization.

## Running in a GUI Environment

To run these components in an actual GUI environment:

1. Install a GUI backend like PyQt5 or WxPython:
   ```bash
   pip install pyqt5
   # or
   pip install wxpython
   ```

2. Run the example script:
   ```bash
   python examples/gui_example.py
   ```

This will open an interactive window where you can use the TrajectoryViewer to explore the trajectories.

## Conclusion

The TraitsUI-based GUI components provide a powerful and flexible interface for working with PTV data. They integrate seamlessly with the rest of the OpenPTV package, providing a complete solution for particle tracking velocimetry analysis.
