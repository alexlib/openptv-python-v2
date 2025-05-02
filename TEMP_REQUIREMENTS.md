# Temporary Requirements Document

This document captures the initial requirements for the openptv-python-v2 package structure.

## Core Requirements

The package should have 4 main components:

1. **C library (liboptv)**
   - A compiled C library for performance-critical algorithms
   - Will be the foundation for high-performance operations

2. **Cython bindings**
   - Provides Python access to the C library
   - Enables fast performance by calling compiled C code from Python

3. **Pure Python alternative**
   - A drop-in replacement for the C library + Cython bindings
   - Used when C is not available or during development
   - Allows for prototyping and debugging new algorithms before converting to C + Cython

4. **GUI components**
   - Based on TraitsUI, Chaco, Enable, Pyface, etc.
   - Provides visualization and user interface for the package

This structure allows for both high performance (via C/Cython) and flexibility (via Python) while maintaining a consistent API across both implementations.
