# OpenPTV Architecture - Parameter Handling

## Three-Layer Architecture

1. **Core Layer** (`coptv/`):
   - Cython bindings to C library
   - Direct mapping to C structs
   - Minimal Python-specific features
   - Names should match C structs with "Params" suffix (e.g., `TrackingParams`)

2. **Python API Layer** (`pyoptv/`):
   - Pure Python implementations
   - Compatible API with Core Layer
   - More Pythonic features
   - Names should match Core Layer but with "Par" suffix (e.g., `TrackPar`)

3. **GUI Layer** (`gui/`):
   - GUI-specific parameter classes
   - Traits-based for UI binding
   - Convert to/from Core/Python API parameters
   - Names should have descriptive prefixes (e.g., `GuiTrackingParams`)

## Parameter Flow

1. GUI parameters (traits-based) ↔ Convert ↔ Core/Python parameters
2. Core/Python parameters ↔ Used for actual processing

## Implementation Guidelines

1. Always use explicit imports to avoid confusion
2. Use factory functions to create appropriate parameter objects
3. Implement conversion functions between parameter types
4. Document parameter mappings clearly