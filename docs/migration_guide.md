# Migration Guide for Unified Parameter Module

This guide explains how to migrate from the old parameter handling to the new unified parameter module.

## Overview

The new unified parameter module (`openptv.parameters`) replaces the separate parameter handling in `openptv.gui.parameters` and `openptv.binding.parameters`. It provides a single source of truth for parameter handling in OpenPTV.

## Benefits

- **Single Source of Truth**: One set of parameter classes for both GUI and C code
- **Clean Separation**: Python handles file I/O, C handles computation
- **Type Safety**: Strong typing in both Python and C
- **Maintainability**: Easier to update parameter formats
- **Testability**: Easier to test parameter handling in isolation

## Migration Steps

### 1. Update Imports

Replace imports from `openptv.gui.parameters` with imports from `openptv.parameters`:

```python
# Old code
from openptv.gui.parameters import TrackingParams, SequenceParams

# New code
from openptv.parameters import TrackingParams, SequenceParams
```

Replace imports from `openptv.binding.parameters` with imports from `openptv.parameters`:

```python
# Old code
from openptv.binding.parameters import TrackingParams, SequenceParams

# New code
from openptv.parameters import TrackingParams, SequenceParams
```

### 2. Update Parameter Usage in Python Code

The new parameter classes have the same interface as the old ones, so you can use them in the same way:

```python
# Old code
params = TrackingParams(path="path/to/parameters")
params.read()
params.dvxmin = -10.0
params.write()

# New code (same as old code)
params = TrackingParams(path="path/to/parameters")
params.read()
params.dvxmin = -10.0
params.write()
```

### 3. Update Parameter Usage in Cython Code

If you're using parameters in Cython code, you'll need to use the bridge functions from `openptv.binding.param_bridge`:

```python
# Old code
from openptv.binding.parameters import TrackingParams
params = TrackingParams(path="path/to/parameters")
params.read()
result = track_forward(targets, params, vol_params)

# New code
from openptv.parameters import TrackingParams
from openptv.binding.param_bridge import tracking_params_to_c

params = TrackingParams(path="path/to/parameters")
params.read()
c_params = tracking_params_to_c(params)
result = c_track_forward(targets, c_params, c_vol_params)
free(c_params)  # Don't forget to free the memory
```

Or use the new wrapper functions that handle the conversion for you:

```python
# New code with wrapper function
from openptv.parameters import TrackingParams
from openptv.binding.tracker_bridge import track_forward_with_params

params = TrackingParams(path="path/to/parameters")
params.read()
result = track_forward_with_params(targets, params, vol_params)
```

### 4. Update Parameter Usage in GUI Code

The GUI code should continue to work with the new parameter classes, as they have the same interface as the old ones. However, you'll need to update the imports:

```python
# Old code
from openptv.gui.parameters import TrackingParams, SequenceParams

# New code
from openptv.parameters import TrackingParams, SequenceParams
```

## Parameter Classes

The following parameter classes are available in the new unified module:

- `Parameters`: Base class for all parameter types
- `TrackingParams`: Tracking parameters
- `SequenceParams`: Sequence parameters
- `VolumeParams`: Volume parameters
- `ControlParams`: Control parameters
- `PtvParams`: PTV parameters
- `TargetParams`: Target parameters
- `TargRecParams`: Target recognition parameters
- `CalOriParams`: Calibration and orientation parameters
- `OrientParams`: Orientation parameters
- `ManOriParams`: Manual orientation parameters
- `ExamineParams`: Examine parameters
- `CriteriaParams`: Criteria parameters
- `DetectPlateParams`: Detect plate parameters
- `DumbbellParams`: Dumbbell parameters
- `ShakingParams`: Shaking parameters
- `PftVersionParams`: PFT version parameters

## Bridge Functions

The following bridge functions are available in `openptv.binding.param_bridge`:

- `tracking_params_to_c`: Convert a Python `TrackingParams` object to a C `track_par` struct
- `tracking_params_from_c`: Convert a C `track_par` struct to a Python `TrackingParams` object
- `sequence_params_to_c`: Convert a Python `SequenceParams` object to a C `sequence_par` struct
- `sequence_params_from_c`: Convert a C `sequence_par` struct to a Python `SequenceParams` object
- `volume_params_to_c`: Convert a Python `VolumeParams` object to a C `volume_par` struct
- `volume_params_from_c`: Convert a C `volume_par` struct to a Python `VolumeParams` object
- `control_params_to_c`: Convert a Python `ControlParams` object to a C `control_par` struct
- `control_params_from_c`: Convert a C `control_par` struct to a Python `ControlParams` object
- `target_params_to_c`: Convert a Python `TargetParams` object to a C `target_par` struct
- `target_params_from_c`: Convert a C `target_par` struct to a Python `TargetParams` object
- `orient_params_to_c`: Convert a Python `OrientParams` object to a C `orient_par` struct
- `orient_params_from_c`: Convert a C `orient_par` struct to a Python `OrientParams` object

## Example Usage

### Reading and Writing Parameters

```python
from openptv.parameters import TrackingParams

# Create a parameter object
params = TrackingParams(path="path/to/parameters")

# Read parameters from file
params.read()

# Modify parameters
params.dvxmin = -10.0
params.dvxmax = 10.0

# Write parameters to file
params.write()
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

## YAML Parameter Files (May 2025 Update)

OpenPTV now uses YAML as the default format for all parameter files. The legacy `.par` files are still supported for backward compatibility, but all new files will be written as `.yaml`.

### What Changed?
- All parameter classes now read and write `.yaml` files by default.
- If a `.yaml` file is not found, the code will attempt to read the corresponding `.par` file and automatically convert it to YAML.
- You can migrate all your `.par` files to YAML using the provided script:

```bash
python examples/convert_par_to_yaml.py <parameters_directory>
```

### Why YAML?
- Human-readable and editable
- Supports comments and complex data structures
- Easier to maintain and version control

### Backward Compatibility
- If you have existing `.par` files, you do not need to convert them immediately. The software will read them and create `.yaml` files automatically.
- It is recommended to migrate to YAML for consistency and future compatibility.
