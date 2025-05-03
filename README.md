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

### Basic Installation

```bash
# For users (when available on PyPI)
pip install openptv-python
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/openptv-python-v2.git
cd openptv-python-v2

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Build the Cython extensions
python setup.py build_ext --inplace
```

### With GUI Dependencies

```bash
# Install with GUI dependencies
pip install openptv-python[gui]
```

## Development

The package supports two development workflows:

1. **C/Cython Development**: For performance-critical components
2. **Python Development**: For rapid prototyping and algorithm development

See the [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for more details on the development workflow.

## Running the GUI

```bash
# Run the GUI application
openptv-gui

# Or directly
python -m openptv.gui.main
```

See [GUI_README.md](GUI_README.md) for more information on the GUI components.

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific tests
python -m pytest tests/test_tracking.py
```

## Git Workflow

See [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for information on the Git workflow for this project.

## License

[Add license information here]
