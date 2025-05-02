# OpenPTV GUI

This document provides instructions for installing and running the OpenPTV GUI application.

## Installation

### Option 1: Install from PyPI (when available)

```bash
# Install the base package
pip install openptv-python

# Install with GUI dependencies
pip install openptv-python[gui]
```

### Option 2: Install from source

```bash
# Clone the repository
git clone https://github.com/yourusername/openptv-python-v2.git
cd openptv-python-v2

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package with GUI dependencies
pip install -e .[gui]

# Build the Cython extensions
python setup.py build_ext --inplace
```

## Running the GUI

### Option 1: Using the entry point (if installed with [gui] extras)

```bash
openptv-gui
```

### Option 2: Running the module directly

```bash
python -m openptv.gui.main
```

### Option 3: Running the example script

```bash
python examples/gui_example_pyside6.py
```

## GUI Features

The OpenPTV GUI provides the following features:

1. **Trajectory Viewer**: Visualize 3D particle trajectories
   - Navigate through multiple trajectories using "Next" and "Previous" buttons
   - View trajectory information in the status bar
   - Rotate and zoom the 3D view to examine trajectories from different angles

2. **Future Components** (planned):
   - Vector Field Viewer
   - Calibration Tool
   - Tracking Control Panel
   - Data Import/Export Tools

## Requirements for Running the GUI

To run the GUI, you need:

1. A Python environment with the required dependencies:
   - traits, traitsui, chaco, enable, pyface
   - A GUI backend: pyside6 or pyqt5

2. A display server:
   - On desktop systems: Your normal display
   - On remote servers: X11 forwarding, VNC, or Xvfb

## Troubleshooting

### Missing Backend

If you get an error about a missing backend:

```
NotImplementedError: the 'null' toolkit does not implement this method
```

Make sure you have a GUI backend installed:
```bash
pip install pyside6  # or pyqt5
```

### Display Issues

If you're on a headless server:
```bash
# Use Xvfb for a virtual display
sudo apt-get install xvfb
xvfb-run -a python -m openptv.gui.main
```

## Screenshots

If you can't run the GUI directly, you can find screenshots in the `screenshots/` directory that show what the interface looks like.

## Creating a Standalone Executable

You can create a standalone executable using PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Create the executable
pyinstaller --onefile --windowed openptv/gui/main.py
```

The executable will be in the `dist/` directory.
