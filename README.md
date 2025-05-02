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

```bash
# For development installation
pip install -e .

# For users
pip install openptv-python
```

## Development

The package supports two development workflows:

1. **C/Cython Development**: For performance-critical components
2. **Python Development**: For rapid prototyping and algorithm development

See the documentation for more details on the development workflow.

## License

[Add license information here]
