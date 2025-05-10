"""
Unified parameter YAML file support for OpenPTV.
Handles reading/writing all parameters from/to a single YAML file.
Explicit mapping, no magic conversion. Each section is mapped to a known parameter class.
"""

import yaml
import os
import shutil
from pathlib import Path
from openptv.parameters.control import ControlParams
from openptv.parameters.sequence import SequenceParams
from openptv.parameters.volume import VolumeParams
from openptv.parameters.tracking import TrackingParams
from openptv.parameters.target import TargetParams
from openptv.parameters.examine import ExamineParams
from openptv.parameters.calibration import CalOriParams
from openptv.parameters.man_ori import ManOriParams
from openptv.parameters.multi_plane import MultiPlaneParams
from openptv.parameters.pft_version import PftVersionParams
from openptv.parameters.shaking import ShakingParams
from openptv.parameters.dumbbell import DumbbellParams


# Add more imports if you add more parameter types

class UnifiedParameters:
    def __init__(self, path=None):
        self.path = Path(path) if path is not None else None
        self.data = {}

    def read(self):
        """Read parameters from YAML file.

        Raises:
            ValueError: If path is None.
            FileNotFoundError: If the file does not exist.
        """
        if self.path is None:
            raise ValueError("Path is not set. Use set_path() to set the path before reading.")

        if not self.path.exists():
            raise FileNotFoundError(f"File {self.path} does not exist.")

        with open(self.path, 'r') as f:
            self.data = yaml.safe_load(f) or {}

    def write(self):
        """Write parameters to YAML file.

        Raises:
            ValueError: If path is None.
        """
        if self.path is None:
            raise ValueError("Path is not set. Use set_path() to set the path before writing.")

        # Create parent directories if they don't exist
        self.path.parent.mkdir(parents=True, exist_ok=True)

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
        # Criteria is the same as volume in the C code
        criteria = VolumeParams(**self.data.get('criteria', {}))
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
                if k.startswith('_') or k in ['path', 'exp_path']:
                    continue
                if isinstance(v, Path):
                    out[k] = str(v)
                else:
                    out[k] = v
            return out

        # Parameter name mapping for storing in YAML (reverse of get_section mapping)
        # param_name_mapping = {
        #     'control': {
        #         'img_base_name': 'img_name',
        #         'cal_img_base_name': 'img_cal',
        #         'allcam_flag': 'allCam_flag',
        #     },
        #     'sequence': {
        #         'base_name': 'img_base_name',
        #     },
        #     'target': {
        #         'discont': 'disco',
        #         'nnmin': 'min_npix',
        #         'nnmax': 'max_npix',
        #         'nxmin': 'min_npix_x',
        #         'nxmax': 'max_npix_x',
        #         'nymin': 'min_npix_y',
        #         'nymax': 'max_npix_y',
        #         'sumg_min': 'sum_grey',
        #         'cr_sz': 'size_cross',
        #     },
        #     'detect_plate': {
        #         'discont': 'disco',
        #         'nnmin': 'min_npix',
        #         'nnmax': 'max_npix',
        #         'nxmin': 'min_npix_x',
        #         'nxmax': 'max_npix_x',
        #         'nymin': 'min_npix_y',
        #         'nymax': 'max_npix_y',
        #         'sumg_min': 'sum_grey',
        #         'cr_sz': 'size_cross',
        #     },
        #     'targ_rec': {
        #         'discont': 'disco',
        #         'nnmin': 'min_npix',
        #         'nnmax': 'max_npix',
        #         'nxmin': 'min_npix_x',
        #         'nxmax': 'max_npix_x',
        #         'nymin': 'min_npix_y',
        #         'nymax': 'max_npix_y',
        #         'sumg_min': 'sum_grey',
        #         'cr_sz': 'size_cross',
        #     }
        # }

        # Process control parameters
        control_dict = clean_dict(cpar.__dict__)
        # if 'control' in param_name_mapping:
        #     for new_name, old_name in param_name_mapping['control'].items():
        #         if new_name in control_dict:
        #             control_dict[old_name] = control_dict.pop(new_name)
        self.data['control'] = control_dict

        # Process sequence parameters
        sequence_dict = clean_dict(sequence.__dict__)
        self.data['sequence'] = sequence_dict

        # Process other parameters
        self.data['volume'] = clean_dict(volume.__dict__)
        self.data['tracking'] = clean_dict(tracking.__dict__)
        self.data['target'] = clean_dict(target.__dict__)
        self.data['detect_plate'] = clean_dict(detect_plate.__dict__)
        self.data['targ_rec'] = clean_dict(targ_rec.__dict__)
        self.data['criteria'] = clean_dict(criteria.__dict__)
        self.data['examine'] = clean_dict(examine.__dict__)
        self.data['cal_ori'] = clean_dict(cal_ori.__dict__)
        self.data['man_ori'] = clean_dict(man_ori.__dict__)
        self.data['multi_plane'] = clean_dict(multi_plane.__dict__)
        self.data['pft_version'] = clean_dict(pft_version.__dict__)
        self.data['shaking'] = clean_dict(shaking.__dict__)
        self.data['dumbbell'] = clean_dict(dumbbell.__dict__)

    def from_legacy_dir(self, legacy_dir):
        """
        Convert a legacy parameters directory to a unified YAML file.

        Args:
            legacy_dir: Path to the legacy parameters directory.
        """
        legacy_dir = Path(legacy_dir)

        # Create parameter objects with the legacy directory path
        cpar = ControlParams(path=legacy_dir)
        sequence = SequenceParams(n_img = cpar.n_img, path=legacy_dir)
        volume = VolumeParams(path=legacy_dir)
        tracking = TrackingParams(path=legacy_dir)
        target = TargetParams(path=legacy_dir)
        detect_plate = TargetParams(path=legacy_dir)
        targ_rec = TargetParams(path=legacy_dir)
        criteria = VolumeParams(path=legacy_dir)
        examine = ExamineParams(path=legacy_dir)
        cal_ori = CalOriParams(path=legacy_dir)
        man_ori = ManOriParams(path=legacy_dir)
        multi_plane = MultiPlaneParams(path=legacy_dir)
        pft_version = PftVersionParams(path=legacy_dir)
        shaking = ShakingParams(path=legacy_dir)
        dumbbell = DumbbellParams(path=legacy_dir)

        # Read parameters from files if they exist
        try:
            cpar.read()
        except Exception as e:
            print(f"Warning: Could not read control parameters: {e}")

        try:
            sequence.read()
        except Exception as e:
            print(f"Warning: Could not read sequence parameters: {e}")

        try:
            volume.read()
        except Exception as e:
            print(f"Warning: Could not read volume parameters: {e}")

        try:
            tracking.read()
        except Exception as e:
            print(f"Warning: Could not read tracking parameters: {e}")

        try:
            target.read()
        except Exception as e:
            print(f"Warning: Could not read target parameters: {e}")

        try:
            detect_plate.read()
        except Exception as e:
            print(f"Warning: Could not read detect_plate parameters: {e}")

        try:
            targ_rec.read()
        except Exception as e:
            print(f"Warning: Could not read targ_rec parameters: {e}")

        try:
            criteria.read()
        except Exception as e:
            print(f"Warning: Could not read criteria parameters: {e}")

        try:
            examine.read()
        except Exception as e:
            print(f"Warning: Could not read examine parameters: {e}")

        try:
            cal_ori.read()
        except Exception as e:
            print(f"Warning: Could not read cal_ori parameters: {e}")

        try:
            man_ori.read()
        except Exception as e:
            print(f"Warning: Could not read man_ori parameters: {e}")

        try:
            multi_plane.read()
        except Exception as e:
            print(f"Warning: Could not read multi_plane parameters: {e}")

        try:
            pft_version.read()
        except Exception as e:
            print(f"Warning: Could not read pft_version parameters: {e}")

        try:
            shaking.read()
        except Exception as e:
            print(f"Warning: Could not read shaking parameters: {e}")

        try:
            dumbbell.read()
        except Exception as e:
            print(f"Warning: Could not read dumbbell parameters: {e}")

        # Update the YAML data from the parameter objects
        self.from_classes(cpar, sequence, volume, tracking, target, detect_plate, targ_rec, criteria, examine, cal_ori, man_ori, multi_plane, pft_version, shaking, dumbbell)

        # Also read any YAML files in the legacy directory
        for yaml_file in legacy_dir.glob("*.yaml"):
            with open(yaml_file, 'r') as f:
                try:
                    section_name = yaml_file.stem  # Use the filename without extension as the section name
                    section_data = yaml.safe_load(f)
                    if section_data:
                        self.data[section_name] = section_data
                except Exception as e:
                    print(f"Warning: Could not read YAML file {yaml_file}: {e}")

    def to_legacy_dir(self, legacy_dir):
        """
        Convert a unified YAML file to a legacy parameters directory.

        Args:
            legacy_dir: Path to the legacy parameters directory.
        """
        legacy_dir = Path(legacy_dir)
        legacy_dir.mkdir(parents=True, exist_ok=True)

        # Convert YAML data to parameter objects
        cpar, sequence, volume, tracking, target, detect_plate, targ_rec, criteria, examine, cal_ori, man_ori, multi_plane, pft_version, shaking, dumbbell = self.to_classes()

        # Set the path for each parameter object
        cpar.path = legacy_dir
        sequence.path = legacy_dir
        volume.path = legacy_dir
        tracking.path = legacy_dir
        target.path = legacy_dir
        detect_plate.path = legacy_dir
        targ_rec.path = legacy_dir
        criteria.path = legacy_dir
        examine.path = legacy_dir
        cal_ori.path = legacy_dir
        man_ori.path = legacy_dir
        multi_plane.path = legacy_dir
        pft_version.path = legacy_dir
        shaking.path = legacy_dir
        dumbbell.path = legacy_dir

        # Write parameters to files
        cpar.write()
        sequence.write()
        volume.write()
        tracking.write()
        target.write()
        detect_plate.write()
        targ_rec.write()
        criteria.write()
        examine.write()
        cal_ori.write()
        man_ori.write()
        multi_plane.write()
        pft_version.write()
        shaking.write()
        dumbbell.write()

        # Also write any additional sections as YAML files
        for section_name, section_data in self.data.items():
            if section_name not in ['control', 'sequence', 'volume', 'tracking', 'target', 'detect_plate', 'targ_rec', 'criteria', 'examine', 'cal_ori', 'man_ori', 'multi_plane', 'pft_version', 'shaking', 'dumbbell']:
                with open(legacy_dir / f"{section_name}.yaml", 'w') as f:
                    yaml.safe_dump(section_data, f, sort_keys=False)

    def get_section(self, section_name):
        """
        Get a parameter object for a specific section.

        Args:
            section_name: Name of the section.

        Returns:
            A parameter object for the specified section.
        """
        # Parameter name mapping to handle different naming conventions
        # param_name_mapping = {
        #     'control': {
        #         'img_name': 'img_base_name',
        #         'img_cal': 'cal_img_base_name',
        #         'allCam_flag': 'allcam_flag',
        #     },
        #     'sequence': {
        #         'img_base_name': 'base_name',
        #     },
        #     'target': {
        #         'tol_dis': 'discont',
        #         'disco': 'discont',
        #         'min_npix': 'nnmin',
        #         'max_npix': 'nnmax',
        #         'min_npix_x': 'nxmin',
        #         'max_npix_x': 'nxmax',
        #         'min_npix_y': 'nymin',
        #         'max_npix_y': 'nymax',
        #         'sum_grey': 'sumg_min',
        #         'size_cross': 'cr_sz',
        #     },
        #     'detect_plate': {
        #         'tol_dis': 'discont',
        #         'disco': 'discont',
        #         'min_npix': 'nnmin',
        #         'max_npix': 'nnmax',
        #         'min_npix_x': 'nxmin',
        #         'max_npix_x': 'nxmax',
        #         'min_npix_y': 'nymin',
        #         'max_npix_y': 'nymax',
        #         'sum_grey': 'sumg_min',
        #         'size_cross': 'cr_sz',
        #     },
        #     'targ_rec': {
        #         'tol_dis': 'discont',
        #         'disco': 'discont',
        #         'min_npix': 'nnmin',
        #         'max_npix': 'nnmax',
        #         'min_npix_x': 'nxmin',
        #         'max_npix_x': 'nxmax',
        #         'min_npix_y': 'nymin',
        #         'max_npix_y': 'nymax',
        #         'sum_grey': 'sumg_min',
        #         'size_cross': 'cr_sz',
        #     }
        # }

        if section_name in self.data:
            # Get the section data
            section_data = self.data.get(section_name, {}).copy()

            # Apply parameter name mapping if available
            # if section_name in param_name_mapping:
            #     mapping = param_name_mapping[section_name]
            #     for old_name, new_name in mapping.items():
            #         if old_name in section_data:
            #             section_data[new_name] = section_data.pop(old_name)

            # Create and return the appropriate parameter object
            if section_name == 'control':
                return ControlParams(**section_data)
            elif section_name == 'sequence':
                return SequenceParams(**section_data)
            elif section_name == 'volume':
                return VolumeParams(**section_data)
            elif section_name == 'tracking':
                return TrackingParams(**section_data)
            elif section_name == 'target':
                return TargetParams(**section_data)
            elif section_name == 'detect_plate':
                return TargetParams(**section_data)
            elif section_name == 'targ_rec':
                return TargetParams(**section_data)
            elif section_name == 'criteria':
                return VolumeParams(**section_data)
            elif section_name == 'examine':
                return ExamineParams(**section_data)
            elif section_name == 'cal_ori':
                return CalOriParams(**section_data)
            elif section_name == 'man_ori':
                return ManOriParams(**section_data)
            elif section_name == 'multi_plane':
                return MultiPlaneParams(**section_data)
            elif section_name == 'pft_version':
                return PftVersionParams(**section_data)
            elif section_name == 'shaking':
                return ShakingParams(**section_data)
            elif section_name == 'dumbbell':
                return DumbbellParams(**section_data)

        # If section doesn't exist or is not recognized, return None
        return None

    def get_gui_param(self, param_name):
        """
        Get a GUI parameter value.

        Args:
            param_name: Name of the parameter.

        Returns:
            The parameter value, or None if not found.
        """
        if 'gui' in self.data and param_name in self.data['gui']:
            return self.data['gui'][param_name]
        return None

    def set_path(self, path):
        """
        Set the path for the YAML file.

        Args:
            path: Path to the YAML file.
        """
        self.path = Path(path)

    def pprint(self):
        """
        Pretty print the parameters.

        Returns:
            A formatted string representation of the parameters.
        """
        import pprint
        return pprint.pformat(self.data, indent=4)

    def set_section(self, section_name, section_data):
        """
        Set a parameter section.

        Args:
            section_name: Name of the section.
            section_data: Parameter object or dictionary with section data.
        """
        if hasattr(section_data, 'to_dict'):
            # If it's a parameter object with a to_dict method, use it
            self.data[section_name] = section_data.to_dict()
        elif hasattr(section_data, '__dict__'):
            # If it's an object with a __dict__ attribute, clean it and use it
            def clean_dict(d):
                out = {}
                for k, v in d.items():
                    if k.startswith('_') or k in ['path', 'exp_path']:
                        continue
                    if isinstance(v, Path):
                        out[k] = str(v)
                    else:
                        out[k] = v
                return out
            self.data[section_name] = clean_dict(section_data.__dict__)
        else:
            # Otherwise, assume it's already a dictionary
            self.data[section_name] = section_data

    def get_num_cams(self) -> int:
        """
        Get the number of cameras from the control section.

        Returns:
            The number of cameras, or 0 if not found.
        """
        if 'control' in self.data and 'n_img' in self.data['control']:
            return int(self.data['control']['n_img'])
        return 0
