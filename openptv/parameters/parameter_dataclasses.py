\
\"\"\"
Defines standard Python dataclasses for OpenPTV parameters.
These are used by the PTV_Interface and GUI to ensure a consistent
way of handling parameters regardless of the backend implementation (C or Python).
\"\"\"
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import numpy as np

# Calibration Parameter Dataclasses

@dataclass
class ExteriorParameters:
    \"\"\"Exterior orientation parameters for a camera.\"\"\"
    x0: float = 0.0
    y0: float = 0.0
    z0: float = 0.0
    omega: float = 0.0
    phi: float = 0.0
    kappa: float = 0.0
    dm: np.ndarray = field(default_factory=lambda: np.eye(3, dtype=np.float64)) # Rotation matrix

    def __array__(self, dtype=None): # For easy conversion to numpy structured array if needed
        return np.array((self.x0, self.y0, self.z0, self.omega, self.phi, self.kappa, self.dm),
                        dtype=object if dtype is None else dtype) # dtype=object for mixed types

@dataclass
class InteriorParameters:
    \"\"\"Interior orientation parameters for a camera.\"\"\"
    xh: float = 0.0
    yh: float = 0.0
    cc: float = 0.0  # Principal distance

    def __array__(self, dtype=None):
        return np.array((self.xh, self.yh, self.cc), dtype=np.float64 if dtype is None else dtype)

@dataclass
class GlassParameters:
    \"\"\"Glass vector parameters (refraction at air-glass-water interface).\"\"\"
    vec_x: float = 0.0
    vec_y: float = 0.0
    vec_z: float = 1.0 # Default for normal vector if not specified

    def __array__(self, dtype=None):
        return np.array((self.vec_x, self.vec_y, self.vec_z), dtype=np.float64 if dtype is None else dtype)

@dataclass
class AddedParameters:
    \"\"\"Additional distortion parameters (radial, decentering, affine).\"\"\"
    k1: float = 0.0  # Radial distortion
    k2: float = 0.0
    k3: float = 0.0
    p1: float = 0.0  # Decentering distortion
    p2: float = 0.0
    scx: float = 1.0 # Affine distortion (scale for x)
    she: float = 0.0 # Affine distortion (shear)

    def __array__(self, dtype=None):
        return np.array((self.k1, self.k2, self.k3, self.p1, self.p2, self.scx, self.she),
                        dtype=np.float64 if dtype is None else dtype)

@dataclass
class MMLUTParameters: # Multimedia Lookup Table
    \"\"\"Parameters for Multimedia Lookup Table, if used.\"\"\"
    origin: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    nr: int = 0 # Number of rows
    nz: int = 0 # Number of columns/depth slices
    rw: int = 0 # Not always used, depends on specific MMLUT format
    data: Optional[np.ndarray] = None # The actual LUT data

    def __post_init__(self):
        if self.data is None and self.nr > 0 and self.nz > 0:
            self.data = np.zeros((self.nr, self.nz), dtype=np.float64)
        elif self.data is not None:
            if self.data.shape != (self.nr, self.nz):
                raise ValueError(f\"MMLUT data shape {self.data.shape} does not match nr={self.nr}, nz={self.nz}\")

@dataclass
class CalibrationParameters:
    \"\"\"
    Container for all calibration-related parameters for a single camera.
    This object is what the PTV_Interface will primarily deal with for calibration.
    \"\"\"
    camera_id: int = 0 # Or some unique identifier
    exterior: ExteriorParameters = field(default_factory=ExteriorParameters)
    interior: InteriorParameters = field(default_factory=InteriorParameters)
    glass: GlassParameters = field(default_factory=GlassParameters)
    added: AddedParameters = field(default_factory=AddedParameters)
    mmlut: Optional[MMLUTParameters] = None # MMLUT is optional

    # File paths from which these parameters might have been loaded, or to which they might be saved.
    # These are more for state tracking if needed, not strictly part of the core calibration math.
    ori_file_path: Optional[str] = None
    add_file_path: Optional[str] = None
    mmlut_file_path: Optional[str] = None


# Placeholder for other parameter sets
@dataclass
class TrackingParameters:
    \"\"\"Parameters for the tracking algorithms.\"\"\"
    example_tracking_param: float = 1.0
    # Add actual tracking parameters here based on existing .par files or C structures

@dataclass
class VolumeParameters:
    \"\"\"Parameters defining the 3D volume of interest and related settings.\"\"\"
    example_volume_param: str = \"test\"
    # Add actual volume parameters here

@dataclass
class DetectionParameters:
    \"\"\"Parameters for particle detection in images (can be per camera).\"\"\"
    threshold: int = 100
    min_area: int = 5
    max_area: int = 1000
    # Add other detection parameters

@dataclass
class AllParametersContainer:
    \"\"\"
    A top-level container to hold all parameter objects for a project or session.
    Useful for loading/saving the entire state.
    \"\"\"
    calibration_params_per_camera: List[CalibrationParameters] = field(default_factory=list)
    tracking_params: Optional[TrackingParameters] = None
    volume_params: Optional[VolumeParameters] = None
    # Detection parameters might be stored per camera within CalibrationParameters
    # or as a separate list if they can vary independently of calibration objects.
    # For now, let's assume they might be part of CalibrationParameters or a separate list.
    # detection_params_per_camera: List[DetectionParameters] = field(default_factory=list)

    def get_camera_calibration(self, camera_id: int) -> Optional[CalibrationParameters]:
        for cal_params in self.calibration_params_per_camera:
            if cal_params.camera_id == camera_id:
                return cal_params
        return None

    def add_camera_calibration(self, cal_params: CalibrationParameters) -> None:
        if self.get_camera_calibration(cal_params.camera_id) is not None:
            # Or update existing
            raise ValueError(f\"Camera with ID {cal_params.camera_id} already exists.\")
        self.calibration_params_per_camera.append(cal_params)
