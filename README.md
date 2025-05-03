# OpenPTV Python v2

A Python package for Particle Tracking Velocimetry (PTV) analysis.

## Overview

This package provides tools for PTV analysis with a flexible architecture that includes:

- High-performance C implementation (`liboptv`)
- Cython bindings for Python access to C functions
- Pure Python implementation for development and fallback
- GUI components based on TraitsUI/Chaco/Enable/Pyface

## Architecture

The package is structured to allow both high-performance processing via C/Cython and flexible development via pure Python:

```
openptv-python/
├── liboptv/            # C library implementation
├── openptv/            # Main Python package
│   ├── binding/        # Cython bindings to liboptv
│   ├── pyoptv/         # Pure Python implementation
│   ├── gui/            # TraitsUI-based GUI components
│   └── utils/          # Utility functions
├── tests/              # Test suite
└── examples/           # Example scripts and notebooks
```

## Installation

### Using pre-built wheels (recommended)

Pre-built binary wheels are available for Windows, macOS, and Linux:

```bash
pip install openptv-python
```

This will automatically download and install the appropriate wheel for your platform.

### From source

If you need to install from source:

```bash
# Install build dependencies
pip install numpy cython

# Install the package
pip install openptv-python
```

### For development

```bash
# Clone the repository
git clone https://github.com/alexlib/openptv-python-v2.git
cd openptv-python-v2

# Install in development mode
pip install -e .
```

## Development

The package supports two development workflows:

1. **C/Cython Development**: For performance-critical components
2. **Python Development**: For rapid prototyping and algorithm development

See the documentation for more details on the development workflow.

### Building Wheels

To build binary wheels for distribution:

```bash
# Install cibuildwheel
pip install cibuildwheel

# Build wheels for the current platform
python -m cibuildwheel --output-dir wheelhouse
```

The GitHub Actions workflow will automatically build wheels for all supported platforms when:
- A tag starting with 'v' is pushed (e.g., v0.1.1)
- Changes are pushed to the 'build_wheels' branch
- The workflow is manually triggered

The wheels will be uploaded as artifacts and can be downloaded from the GitHub Actions page.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
