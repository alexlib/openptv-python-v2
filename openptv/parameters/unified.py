"""
Unified parameter YAML file support for OpenPTV.
Handles reading/writing all parameters from/to a single YAML file.
Explicit mapping, no magic conversion. Each section is mapped to a known parameter class.
"""

import yaml
from pathlib import Path
from openptv.parameters.control import ControlParams
from openptv.parameters.sequence import SequenceParams
from openptv.parameters.volume import VolumeParams
from openptv.parameters.tracking import TrackingParams
from openptv.parameters.target import TargetParams
from openptv.parameters.examine import ExamineParams
from openptv.parameters.criteria import CriteriaParams
from openptv.parameters.calibration import CalOriParams
from openptv.parameters.man_ori import ManOriParams
from openptv.parameters.multi_plane import MultiPlaneParams
from openptv.parameters.pft_version import PftVersionParams
from openptv.parameters.shaking import ShakingParams
from openptv.parameters.dumbbell import DumbbellParams


# Add more imports if you add more parameter types

class UnifiedParameters:
    def __init__(self, path):
        self.path = Path(path)
        self.data = {}

    def read(self):
        with open(self.path, 'r') as f:
            self.data = yaml.safe_load(f)

    def write(self):
        with open(self.path, 'w') as f:
            yaml.safe_dump(self.data, f, sort_keys=False)

    def to_classes(self):
        """Convert loaded YAML to parameter class instances. Section names are not tied to file names."""
        cpar = ControlParams(**self.data.get('control', {}))
        sequence = SequenceParams(**self.data.get('sequence', {}))
        volume = VolumeParams(**self.data.get('volume', {}))
        tracking = TrackingParams(**self.data.get('tracking', {}))
        # TargetParams can be used for multiple sections
        target = TargetParams(**self.data.get('target', {}))
        detect_plate = TargetParams(**self.data.get('detect_plate', {}))
        targ_rec = TargetParams(**self.data.get('targ_rec', {}))
        criteria = CriteriaParams(**self.data.get('criteria', {}))
        examine = ExamineParams(**self.data.get('examine', {}))
        # In to_classes:
        cal_ori = CalOriParams(**self.data.get('cal_ori', {}))
        man_ori = ManOriParams(**self.data.get('man_ori', {}))
        multi_plane = MultiPlaneParams(**self.data.get('multi_plane', {}))
        pft_version = PftVersionParams(**self.data.get('pft_version', {}))
        shaking = ShakingParams(**self.data.get('shaking', {}))
        dumbbell = DumbbellParams(**self.data.get('dumbbell', {}))

        return cpar, sequence, volume, tracking, target, detect_plate, targ_rec, criteria, examine, cal_ori, man_ori, multi_plane, pft_version, shaking, dumbbell

    def from_classes(self, cpar, sequence, volume, tracking, target, detect_plate, targ_rec, criteria, examine, cal_ori, man_ori, multi_plane, pft_version, shaking, dumbbell):
        """Update YAML data from parameter class instances. Section names are not tied to file names."""
        def clean_dict(d):
            out = {}
            for k, v in d.items():
                if k.startswith('_') or k == 'exp_path':
                    continue
                if isinstance(v, Path):
                    out[k] = str(v)
                else:
                    out[k] = v
            return out
        self.data['control'] = clean_dict(cpar.__dict__)
        self.data['sequence'] = clean_dict(sequence.__dict__)
        self.data['volume'] = clean_dict(volume.__dict__)
        self.data['tracking'] = clean_dict(tracking.__dict__)
        self.data['target'] = clean_dict(target.__dict__)
        self.data['detect_plate'] = clean_dict(detect_plate.__dict__)
        self.data['targ_rec'] = clean_dict(targ_rec.__dict__)
        self.data['criteria'] = clean_dict(criteria.__dict__)
        self.data['examine'] = clean_dict(examine.__dict__)
        # In from_classes:
        self.data['cal_ori'] = clean_dict(cal_ori.__dict__)
        self.data['man_ori'] = clean_dict(man_ori.__dict__)
        self.data['multi_plane'] = clean_dict(multi_plane.__dict__)
        self.data['pft_version'] = clean_dict(pft_version.__dict__)
        self.data['shaking'] = clean_dict(shaking.__dict__)
        self.data['dumbbell'] = clean_dict(dumbbell.__dict__)


        

