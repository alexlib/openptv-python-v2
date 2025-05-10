# Unified Parameter Module for OpenPTV

The unified parameter module provides a single source of truth for parameter handling in OpenPTV. It replaces the separate parameter handling in `openptv.gui.parameters` and `openptv.binding.parameters`.

## Design Goals

- **Single Source of Truth**: One set of parameter classes for both GUI and C code
- **Clean Separation**: Python handles file I/O, C handles computation
- **Type Safety**: Strong typing in both Python and C
- **Maintainability**: Easier to update parameter formats
- **Testability**: Easier to test parameter handling in isolation

## Module Structure

The unified parameter module is organized as follows:

```
openptv/
  parameters/
    __init__.py        # Imports and exports all parameter classes
    base.py            # Base parameter class
    utils.py           # Utility functions
    tracking.py        # Tracking parameters
    sequence.py        # Sequence parameters
    volume.py          # Volume parameters
    control.py         # Control parameters and PTV parameters
    target.py          # Target parameters and target recognition parameters
    calibration.py     # Calibration and orientation parameters
    orient.py          # Orientation parameters
    man_ori.py         # Manual orientation parameters
    examine.py         # Examine parameters
    criteria.py        # Criteria parameters
    detect_plate.py    # Detect plate parameters
    dumbbell.py        # Dumbbell parameters
    shaking.py         # Shaking parameters
    pft_version.py     # PFT version parameters
```

## Parameter Classes

The following parameter classes are available in the unified module:

- `Parameters`: Base class for all parameter types
- `TrackingParams`: Tracking parameters
- `SequenceParams`: Sequence parameters
- `VolumeParams`: Volume parameters
- `ControlParams`: Control parameters
- `PtvParams`: PTV parameters
- `TargetParams`: Target parameters
- `CalOriParams`: Calibration and orientation parameters
- `OrientParams`: Orientation parameters
- `ManOriParams`: Manual orientation parameters
- `ExamineParams`: Examine parameters
- `CriteriaParams`: Criteria parameters
- `DumbbellParams`: Dumbbell parameters
- `ShakingParams`: Shaking parameters
- `PftVersionParams`: PFT version parameters

## Bridge Functions

The bridge functions in `openptv.binding.param_bridge` provide a way to convert between Python parameter objects and C parameter structs:

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

## Usage Examples

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

### Converting Between Python and C

```python
from openptv.parameters import TrackingParams
from openptv.binding.param_bridge import tracking_params_to_c, tracking_params_from_c

# Create a parameter object
params = TrackingParams(
    dvxmin=-10.0,
    dvxmax=10.0,
    dvymin=-10.0,
    dvymax=10.0,
    dvzmin=-10.0,
    dvzmax=10.0,
    angle=0.5,
    dacc=0.5,
    flagNewParticles=True,
)

# Convert to C struct
c_params = tracking_params_to_c(params)

# Use C struct with C functions
# ...

# Convert back to Python object
params2 = tracking_params_from_c(c_params)

# Clean up
free(c_params)
```

## Implementation Details

### Base Parameter Class

All parameter classes inherit from the `Parameters` base class, which provides common functionality:

```python
class Parameters:
    """Base class for all parameter types."""
    
    def __init__(self, path=None):
        """Initialize a Parameters object."""
        self.path = path
    
    def filename(self):
        """Get the filename for this parameter type."""
        raise NotImplementedError("Subclasses must implement filename()")
    
    def read(self):
        """Read parameter values from file."""
        raise NotImplementedError("Subclasses must implement read()")
    
    def write(self):
        """Write parameter values to file."""
        raise NotImplementedError("Subclasses must implement write()")
    
    def to_c_struct(self):
        """Convert parameter values to a dictionary suitable for creating a C struct."""
        raise NotImplementedError("Subclasses must implement to_c_struct()")
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """Create a Parameters object from a C struct."""
        raise NotImplementedError("Subclasses must implement from_c_struct()")
```

### Parameter Class Implementation

Each parameter class implements the methods defined in the base class:

```python
class TrackingParams(Parameters):
    """Tracking parameters for OpenPTV."""
    
    def __init__(self, dvxmin=0.0, dvxmax=0.0, dvymin=0.0, dvymax=0.0,
                 dvzmin=0.0, dvzmax=0.0, angle=0.0, dacc=0.0,
                 flagNewParticles=False, path=None):
        """Initialize tracking parameters."""
        super().__init__(path)
        self.set(dvxmin, dvxmax, dvymin, dvymax, dvzmin, dvzmax,
                 angle, dacc, flagNewParticles)
    
    def set(self, dvxmin=0.0, dvxmax=0.0, dvymin=0.0, dvymax=0.0,
            dvzmin=0.0, dvzmax=0.0, angle=0.0, dacc=0.0,
            flagNewParticles=False):
        """Set tracking parameters."""
        self.dvxmin = dvxmin
        self.dvxmax = dvxmax
        self.dvymin = dvymin
        self.dvymax = dvymax
        self.dvzmin = dvzmin
        self.dvzmax = dvzmax
        self.angle = angle
        self.dacc = dacc
        self.flagNewParticles = flagNewParticles
    
    def filename(self):
        """Get the filename for tracking parameters."""
        return "track.par"
    
    def read(self):
        """Read tracking parameters from file."""
        # Implementation...
    
    def write(self):
        """Write tracking parameters to file."""
        # Implementation...
    
    def to_c_struct(self):
        """Convert tracking parameters to a dictionary suitable for creating a C struct."""
        # Implementation...
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """Create a TrackingParams object from a C struct."""
        # Implementation...
```

### Bridge Function Implementation

The bridge functions convert between Python parameter objects and C parameter structs:

```python
cdef track_par* tracking_params_to_c(TrackingParams params):
    """Convert a Python TrackingParams object to a C track_par struct."""
    cdef track_par* c_params = <track_par*>malloc(sizeof(track_par))
    
    # Get parameter values as a dictionary
    param_dict = params.to_c_struct()
    
    # Fill in the C struct
    c_params.dvxmin = param_dict['dvxmin']
    c_params.dvxmax = param_dict['dvxmax']
    # ... other fields
    
    return c_params

def tracking_params_from_c(track_par* c_params, path=None):
    """Convert a C track_par struct to a Python TrackingParams object."""
    # Create a dictionary of parameter values
    param_dict = {
        'dvxmin': c_params.dvxmin,
        'dvxmax': c_params.dvxmax,
        # ... other fields
    }
    
    # Create a TrackingParams object from the dictionary
    return TrackingParams.from_c_struct(param_dict, path)
```
