# OpenPTV Python Distribution Guide

This guide provides instructions for distributing the OpenPTV Python package, including creating binary wheels and running the GUI application.

## Creating Binary Wheels

Binary wheels are pre-built distributions that can be installed without requiring compilation. This is especially useful for packages with C extensions like OpenPTV.

### Prerequisites

- Python 3.7 or higher
- pip
- wheel
- setuptools
- cibuildwheel (for cross-platform wheels)

### Building Wheels Locally

1. Install the required tools:
   ```bash
   pip install wheel setuptools build
   ```

2. Build a wheel for your current platform:
   ```bash
   python -m build --wheel
   ```
   
   This will create a `.whl` file in the `dist/` directory.

3. To create a source distribution as well:
   ```bash
   python -m build --sdist
   ```

### Building Cross-Platform Wheels with cibuildwheel

For creating wheels for multiple platforms (Windows, macOS, Linux), you can use cibuildwheel:

1. Install cibuildwheel:
   ```bash
   pip install cibuildwheel
   ```

2. Create a `pyproject.toml` file with cibuildwheel configuration:
   ```toml
   [build-system]
   requires = ["setuptools>=42", "wheel", "Cython>=0.29.21", "numpy>=1.19.0"]
   build-backend = "setuptools.build_meta"

   [tool.cibuildwheel]
   skip = ["cp36-*", "pp*"]
   ```

3. Run cibuildwheel:
   ```bash
   python -m cibuildwheel --platform linux
   ```
   
   Replace `linux` with `windows` or `macos` as needed.

4. For GitHub Actions integration, create a workflow file `.github/workflows/build_wheels.yml`:
   ```yaml
   name: Build Wheels

   on:
     push:
       tags:
         - 'v*'
     workflow_dispatch:

   jobs:
     build_wheels:
       name: Build wheels on ${{ matrix.os }}
       runs-on: ${{ matrix.os }}
       strategy:
         matrix:
           os: [ubuntu-latest, windows-latest, macos-latest]

       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.8'
         - name: Install cibuildwheel
           run: python -m pip install cibuildwheel
         - name: Build wheels
           run: python -m cibuildwheel --output-dir wheelhouse
         - uses: actions/upload-artifact@v3
           with:
             name: wheels-${{ matrix.os }}
             path: ./wheelhouse/*.whl
   ```

### Publishing to PyPI

1. Install twine:
   ```bash
   pip install twine
   ```

2. Upload to TestPyPI first to verify everything works:
   ```bash
   python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```

3. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

## Running the GUI Application

### Option 1: Run Locally with a Display

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/openptv-python-v2.git
   cd openptv-python-v2
   ```

2. Set up the environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install numpy scipy cython
   pip install traits traitsui chaco enable pyface
   pip install pyside6  # or pyqt5
   pip install -e .
   python setup.py build_ext --inplace
   ```

3. Run the GUI example:
   ```bash
   python examples/gui_example_pyside6.py
   ```

### Option 2: Run with a Remote Display

If you're on a remote server without a display:

1. Install a VNC server:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install tightvncserver
   
   # On CentOS/RHEL
   sudo yum install tigervnc-server
   ```

2. Start the VNC server:
   ```bash
   vncserver :1 -geometry 1280x800 -depth 24
   ```

3. Connect to the VNC server using a VNC client from your local machine.

4. Run the GUI application within the VNC session.

### Option 3: Create a Standalone Executable

You can create standalone executables using PyInstaller:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create the executable:
   ```bash
   pyinstaller --onefile --windowed examples/gui_example_pyside6.py
   ```

3. The executable will be in the `dist/` directory.

## Creating an Installable Package with GUI

To create a package that includes the GUI and can be installed by users:

1. Update `setup.py` to include GUI dependencies:
   ```python
   setup(
       # ... other parameters ...
       install_requires=[
           "numpy",
           "scipy",
           "traits",
           "traitsui",
           "chaco",
           "enable",
           "pyface",
       ],
       extras_require={
           "gui": ["pyside6"],  # or "pyqt5"
       },
       entry_points={
           "console_scripts": [
               "openptv-gui=openptv.gui.main:main",
           ],
       },
   )
   ```

2. Create a main entry point in `openptv/gui/main.py`:
   ```python
   import os
   import sys
   import numpy as np
   from openptv.gui.trajectory_viewer import TrajectoryViewer

   def main():
       # Set the toolkit
       os.environ['ETS_TOOLKIT'] = 'qt4'
       os.environ['QT_API'] = 'pyside6'  # or 'pyqt5'
       
       # Create a sample application or load data
       # ...
       
       # Launch the GUI
       viewer = TrajectoryViewer(trajectories=trajectories)
       viewer.configure_traits()
       
   if __name__ == "__main__":
       main()
   ```

3. Build the package:
   ```bash
   python -m build
   ```

4. Users can then install and run it:
   ```bash
   pip install openptv-python[gui]
   openptv-gui
   ```

## Troubleshooting GUI Issues

### Missing Backend

If you get an error about a missing backend:

```
NotImplementedError: the 'null' toolkit does not implement this method
```

Make sure you have a GUI backend installed:
```bash
pip install pyside6  # or pyqt5
```

And set the environment variables:
```python
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyside6'  # or 'pyqt5'
```

### Display Issues

If you're on a headless server:
```bash
# Use Xvfb for a virtual display
sudo apt-get install xvfb
xvfb-run -a python examples/gui_example_pyside6.py
```

### Backend Compatibility

Different versions of TraitsUI may work better with different backends:

- For newer versions: PySide6 or PyQt6
- For older versions: PySide2, PyQt5, or wxPython

Try different backends if you encounter issues.
