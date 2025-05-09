# Unified Parameter Module for OpenPTV

This module provides a unified interface for parameter handling in OpenPTV. It replaces the separate parameter handling in `openptv.gui.parameters` and `openptv.binding.parameters`.

## Design Goals

- **Single Source of Truth**: One set of parameter classes for both GUI and C code
- **Clean Separation**: Python handles file I/O, C handles computation
- **Type Safety**: Strong typing in both Python and C
- **Maintainability**: Easier to update parameter formats
- **Testability**: Easier to test parameter handling in isolation

## Usage

### Reading and Writing Parameters

```python
from openptv.parameters import TrackingParams

# Create a TrackingParams object
track_params = TrackingParams(path="path/to/parameters")

# Read parameters from file
track_params.read()

# Modify parameters
track_params.dvxmin = -10.0
track_params.dvxmax = 10.0

# Write parameters to file
track_params.write()
```

### Using Parameters with C Functions

```python
from openptv.parameters import TrackingParams, VolumeParams
from openptv.binding.tracker_bridge import track_forward_with_params

# Create parameter objects
track_params = TrackingParams(path="path/to/parameters")
vol_params = VolumeParams(path="path/to/parameters")

# Read parameters from file
track_params.read()
vol_params.read()

# Use parameters with C functions
targets = []  # Load targets
results = track_forward_with_params(targets, track_params, vol_params)
```

## Parameter Classes

- `Parameters`: Base class for all parameter types
- `TrackingParams`: Tracking parameters
- `SequenceParams`: Sequence parameters
- `VolumeParams`: Volume parameters
- `ControlParams`: Control parameters
- `PtvParams`: PTV parameters
- `TargetParams`: Target parameters
- `CalOriParams`: Calibration and orientation parameters
- `VolumeParams`: Criteria parameters
- `ExamineParams`: Examine parameters
- `OrientParams`: Orientation parameters
- `DetectPlateParams`: Detect plate parameters
- `DumbbellParams`: Dumbbell parameters
- `ShakingParams`: Shaking parameters
- `PftVersionParams`: PFT version parameters
- `ManOriParams`: Manual orientation parameters

## Bridge Functions

The `openptv.binding.param_bridge` module provides functions for converting between Python parameter objects and C parameter structs:

- `tracking_params_to_c`: Convert a Python `TrackingParams` object to a C `track_par` struct
- `tracking_params_from_c`: Convert a C `track_par` struct to a Python `TrackingParams` object
- (Similar functions for other parameter types)

## Migration Guide

To migrate from the old parameter handling to the new unified module:

1. Replace imports from `openptv.gui.parameters` with imports from `openptv.parameters`
2. Replace imports from `openptv.binding.parameters` with imports from `openptv.parameters`
3. Use bridge functions from `openptv.binding.param_bridge` to convert between Python and C parameter objects

## Implementation Details

- Parameter classes inherit from the `Parameters` base class
- Each parameter class implements `read()`, `write()`, `to_c_struct()`, and `from_c_struct()` methods
- Bridge functions handle the conversion between Python parameter objects and C parameter structs
- String/bytes conversion is handled consistently using utility functions
