# Submodules in OpenPTV Python v2

This project uses Git submodules to integrate code from other repositories. This approach allows us to leverage existing, well-maintained codebases while still having the flexibility to develop and extend the package.

## Submodule Structure

The project includes the following submodules:

1. **liboptv** - The core C library and Cython bindings from [openptv/openptv](https://github.com/openptv/openptv)
   - Located at: `liboptv/`
   - Contains the high-performance C implementation of the tracking algorithms
   - Includes Cython bindings for Python access

2. **pyptv-gui** - The GUI components from [alexlib/pyptv](https://github.com/alexlib/pyptv)
   - Located at: `pyptv-gui/`
   - Contains the TraitsUI/Chaco/Enable/Pyface-based GUI
   - Provides visualization and user interface components

## Working with Submodules

### Initializing Submodules

When you first clone the repository, the submodules are not automatically initialized. You can initialize them with:

```bash
git submodule update --init --recursive
```

The setup.py script will attempt to do this automatically when you install the package.

### Updating Submodules

To update the submodules to the latest version from their respective repositories:

```bash
git submodule update --remote
```

### Making Changes to Submodules

If you need to make changes to a submodule, you should:

1. Fork the original repository
2. Make your changes in your fork
3. Submit a pull request to the original repository
4. Update the submodule reference in this repository once your changes are merged

## Adapter Layers

This project includes adapter layers that provide a unified API for working with the submodules:

1. **openptv/coptv/** - Adapter for the C library and Cython bindings
2. **openptv/gui/** - Adapter for the GUI components
3. **openptv/pyoptv/** - Pure Python implementation that can be used as a fallback

The main package automatically selects the appropriate implementation based on what's available.

## Fallback Mechanism

If the Cython bindings are not available (e.g., if the C library couldn't be compiled), the package will automatically fall back to the pure Python implementation in `openptv/pyoptv/`. This ensures that the package can be used even in environments where compilation is not possible.

Similarly, if the GUI components are not available, the package will provide appropriate error messages and fallback to command-line operation.
