"""
Unified parameter YAML file support for OpenPTV.
Handles reading/writing all parameters from/to a single YAML file,
as well as conversion to/from the legacy multi-file format for backward compatibility.
"""

import yaml
from pathlib import Path
from . import (
    tracking, sequence, volume, control, target, orient, calibration
)

# List of all parameter types and their classes
PARAMETER_CLASSES = {
    'tracking': tracking.TrackingParams,
    'sequence': sequence.SequenceParams,
    'volume': volume.VolumeParams,
    'control': control.ControlParams,
    'target': target.TargetParams,
    'orient': orient.OrientParams,
    # 'calibration': calibration.CalOriParams,  # Uncomment if implemented
}

class UnifiedParameters:
    """
    Handles all OpenPTV parameters in a single YAML file with sections.
    Allows conversion to/from legacy multi-file format for backward compatibility.
    """
    def __init__(self, path=None):
        self.path = Path(path) if path else Path('parameters.yaml')
        self.sections = {key: None for key in PARAMETER_CLASSES}
        self.gui = {}  # For GUI-only parameters

    def read(self):
        """Read all parameters from the unified YAML file."""
        with open(self.path, 'r') as f:
            data = yaml.safe_load(f)
        for key, cls in PARAMETER_CLASSES.items():
            section = data.get(key, None)
            if section is not None:
                self.sections[key] = cls.from_dict(section)
            else:
                self.sections[key] = None
        self.gui = data.get('gui', {})

    def write(self):
        """Write all parameters to the unified YAML file."""
        data = {key: (self.sections[key].to_dict() if self.sections[key] else None)
                for key in PARAMETER_CLASSES}
        if self.gui:
            data['gui'] = self.gui
        with open(self.path, 'w') as f:
            yaml.safe_dump(data, f, sort_keys=False)

    def from_legacy_dir(self, param_dir):
        """Load parameters from a directory of legacy .par files (not YAML) for this test."""
        param_dir = Path(param_dir)
        for key, cls in PARAMETER_CLASSES.items():
            # Use correct filename for tracking
            if key == "tracking":
                par_path = param_dir / "track.par"
            else:
                par_path = param_dir / f"{key}.par"
            yaml_path = param_dir / f"{key}.yaml"
            obj = None
            if par_path.exists():
                obj = cls(path=param_dir)
                if key == 'sequence':
                    obj.n_img = 2
                obj.read()
            elif yaml_path.exists():
                obj = cls(path=param_dir)
                obj.read()
            self.sections[key] = obj
        # Optionally load GUI params
        gui_yaml = param_dir / 'gui.yaml'
        if gui_yaml.exists():
            with open(gui_yaml, 'r') as f:
                self.gui = yaml.safe_load(f)

    def to_legacy_dir(self, param_dir):
        """Write parameters to a directory in the legacy multi-file format (YAML and .par)."""
        param_dir = Path(param_dir)
        param_dir.mkdir(exist_ok=True)
        for key, cls in PARAMETER_CLASSES.items():
            if self.sections[key]:
                # Write .par file
                self.sections[key].path = param_dir
                self.sections[key].write()
                # Write .yaml file
                self.sections[key].to_yaml()
        if self.gui:
            with open(param_dir / 'gui.yaml', 'w') as f:
                yaml.safe_dump(self.gui, f, sort_keys=False)

    def set_section(self, key, params):
        assert key in PARAMETER_CLASSES
        self.sections[key] = params

    def get_section(self, key):
        assert key in PARAMETER_CLASSES
        return self.sections[key]

    def set_gui_param(self, name, value):
        self.gui[name] = value

    def get_gui_param(self, name, default=None):
        return self.gui.get(name, default)
