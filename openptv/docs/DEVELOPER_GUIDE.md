# OpenPTV Python Developer Guide

This guide provides instructions for developers working on the OpenPTV Python package. The package consists of four main components:

1. **C Library (liboptv)** - Core performance-critical algorithms
2. **Cython Bindings** - Python interface to the C library
3. **Pure Python Implementation** - Alternative implementation for development and fallback
4. **GUI Components** - TraitsUI/Chaco-based visualization tools

## Getting Started

### Prerequisites

- Python 3.7 or higher
- C compiler (GCC, Clang, MSVC)
- Git

### Setting Up the Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/openptv-python-v2.git
   cd openptv-python-v2
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # On Linux/macOS
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install numpy scipy cython wheel setuptools
   pip install pytest pytest-cov black flake8
   pip install traits traitsui chaco enable pyface
   pip install matplotlib
   ```

4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

5. Build the Cython extensions:
   ```bash
   python setup.py build_ext --inplace
   ```

## Project Structure

```
openptv-python/
├── liboptv/            # C library implementation
│   ├── include/        # Header files
│   └── src/            # Source files
├── openptv/            # Main Python package
│   ├── binding/        # Cython bindings to liboptv
│   ├── pyoptv/         # Pure Python implementation
│   ├── gui/            # TraitsUI-based GUI components
│   └── utils/          # Utility functions
├── tests/              # Test suite
└── examples/           # Example scripts and notebooks
```

## Fallback Mechanism

The package implements an automatic fallback mechanism that allows it to work even when the Cython extensions are not available. This is handled in the main `__init__.py` file:

```python
# Try to import the Cython bindings
try:
    from openptv.binding.tracking_cy import track_particles_py as track_particles
    from openptv.binding.tracking_cy import find_correspondences_py as find_correspondences
    _using_cython = True
except ImportError:
    # Fall back to pure Python implementation
    from openptv.pyoptv.tracking import track_particles, find_correspondences
    _using_cython = False
    warnings.warn(
        "Cython bindings not available, using pure Python implementation. "
        "This may be significantly slower for large datasets."
    )
```

This approach provides several benefits:

1. **Development Flexibility**: Developers can work on the Python implementation without needing to compile the C code
2. **Cross-Platform Compatibility**: The package works even on platforms where compiling the C extensions might be difficult
3. **Educational Value**: The Python implementation serves as a clear, readable reference for understanding the algorithms
4. **Debugging**: The Python implementation is easier to debug and modify for testing new ideas

You can check which implementation is being used with:

```python
from openptv import using_cython
print(f"Using Cython implementation: {using_cython()}")
```

## Development Workflow

### 1. C Library Development

When working on the C library:

1. Add or modify header files in `liboptv/include/`
2. Implement functionality in `liboptv/src/`
3. Write tests for the C functions
4. Rebuild the Cython extensions after changes:
   ```bash
   python setup.py build_ext --inplace
   ```

**Coding Standards:**
- Follow the C99 standard
- Use clear function and variable names
- Document functions with comments
- Handle memory allocation/deallocation carefully

### 2. Cython Bindings Development

When working on the Cython bindings:

1. Define C function declarations in `.pxd` files
2. Implement Python wrappers in `.pyx` files
3. Update `openptv/binding/__init__.py` to expose the functions
4. Rebuild after changes:
   ```bash
   python setup.py build_ext --inplace
   ```

**Important Notes:**
- Ensure proper memory management (malloc/free)
- Handle NumPy array conversions carefully
- Maintain consistent API between Cython and Python implementations

### 3. Python Implementation Development

When working on the pure Python implementation:

1. Implement algorithms in `openptv/pyoptv/`
2. Ensure the API matches the Cython bindings
3. Update `openptv/pyoptv/__init__.py` to expose the functions

**Best Practices:**
- Use NumPy for efficient array operations
- Document functions with docstrings
- Write clear, readable code for educational purposes
- Optimize where possible, but prioritize clarity

### 4. GUI Development

When working on the GUI components:

1. Implement UI components in `openptv/gui/`
2. Use TraitsUI for the interface and Chaco for plotting
3. Test GUI components with example scripts

**Guidelines:**
- Follow the Model-View-Controller (MVC) pattern
- Create reusable components
- Provide sensible defaults
- Document UI components

## Testing

Run the test suite:
```bash
python -m pytest
```

Run with coverage:
```bash
python -m pytest --cov=openptv
```

### Writing Tests

1. Add test files in the `tests/` directory
2. Test both Cython and Python implementations
3. Use pytest fixtures for common setup
4. Mock external dependencies when appropriate

### Testing the Dual Implementation

The package is designed to work with either the Cython or Python implementation. To test both:

1. **Test with Cython implementation**:
   - Make sure the Cython extensions are built: `python setup.py build_ext --inplace`
   - Run your tests, which will use the Cython implementation by default

2. **Test with Python implementation**:
   - Temporarily move or rename the Cython .so file:
     ```python
     import os
     import shutil

     # Find the .so file
     so_file = None
     for file in os.listdir("openptv/binding"):
         if file.endswith(".so"):
             so_file = os.path.join("openptv/binding", file)
             break

     # Temporarily move it
     if so_file:
         backup_file = so_file + ".bak"
         shutil.move(so_file, backup_file)
     ```
   - Run your tests, which will now use the Python implementation
   - Restore the .so file:
     ```python
     if so_file and os.path.exists(backup_file):
         shutil.move(backup_file, so_file)
     ```

3. **Verify implementation in use**:
   - Use the `using_cython()` function to check which implementation is active:
     ```python
     from openptv import using_cython
     print(f"Using Cython implementation: {using_cython()}")
     ```

4. **Example test script**:
   - See `test_separate_processes.py` for an example of testing both implementations

## Documentation

- Document C functions with comments
- Document Python functions with docstrings
- Update README.md with new features
- Create examples for new functionality

## Debugging Tips

### Debugging C Code

1. Compile with debug symbols:
   ```bash
   CFLAGS="-g -O0" python setup.py build_ext --inplace
   ```

2. Use GDB or LLDB to debug:
   ```bash
   gdb python
   (gdb) run -m pytest tests/test_file.py
   ```

### Debugging Cython Code

1. Enable Cython line tracing:
   ```python
   # In setup.py
   ext_modules = cythonize(extensions, gdb_debug=True)
   ```

2. Use print statements in Cython code for simple debugging

### Debugging Python Code

1. Use the Python debugger:
   ```python
   import pdb; pdb.set_trace()
   ```

2. Or use an IDE with debugging support (VSCode, PyCharm)

## Development Cycle

1. **Plan**: Understand the algorithm or feature to implement
2. **Prototype**: Implement in Python first for rapid development
3. **Test**: Write tests to verify the implementation
4. **Optimize**: Convert to C/Cython if performance is critical
5. **Document**: Add documentation and examples
6. **Review**: Have your code reviewed by other developers

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Run tests to ensure everything works
4. Submit a pull request
5. Address review comments

## Building for Distribution

Create source distribution:
```bash
python setup.py sdist
```

Create wheel:
```bash
python setup.py bdist_wheel
```

## Common Issues and Solutions

### Cython Build Errors

- Check that header files are in the correct location
- Verify that C functions are declared correctly in Cython
- Ensure NumPy headers are included

### Import Errors

- Verify that `__init__.py` files expose the correct functions
- Check that Cython extensions are built correctly
- Ensure the package is installed in development mode

### GUI Issues

- Make sure a GUI backend is available (Qt, WxPython)
- Check that TraitsUI and Chaco are installed correctly
- Verify that the environment supports GUI applications

## Performance Optimization

1. Profile Python code to identify bottlenecks:
   ```python
   import cProfile
   cProfile.run('function_to_profile()')
   ```

2. Move performance-critical sections to C/Cython

3. Use NumPy vectorized operations where possible

4. Consider parallel processing for independent operations

## Additional Resources

- [Cython Documentation](https://cython.readthedocs.io/)
- [TraitsUI Documentation](https://docs.enthought.com/traitsui/)
- [Chaco Documentation](https://docs.enthought.com/chaco/)
- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Documentation](https://docs.scipy.org/doc/scipy/)
