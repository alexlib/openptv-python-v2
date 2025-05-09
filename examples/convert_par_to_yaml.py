"""
Script to convert all .par parameter files in a directory to YAML format using OpenPTV parameter classes.
"""
import sys
from pathlib import Path
from openptv.parameters import (
    PtvParams, CalOriParams, SequenceParams, CriteriaParams, TargRecParams, ManOriParams,
    DetectPlateParams, OrientParams, TrackingParams, PftVersionParams, ExamineParams,
    DumbbellParams, ShakingParams, MultiPlaneParams
)

PARAM_CLASSES = [
    PtvParams, CalOriParams, SequenceParams, CriteriaParams, TargRecParams, ManOriParams,
    DetectPlateParams, OrientParams, TrackingParams, PftVersionParams, ExamineParams,
    DumbbellParams, ShakingParams, MultiPlaneParams
]

def convert_all_par_to_yaml(param_dir):
    param_dir = Path(param_dir)
    for cls in PARAM_CLASSES:
        try:
            obj = cls(n_img=4, path=param_dir)
        except TypeError:
            obj = cls(path=param_dir)
        par_file = param_dir / obj.filename()
        if par_file.exists():
            print(f"Converting {par_file} to YAML...")
            obj.read()
            yaml_file = par_file.with_suffix('.yaml')
            obj.to_yaml()
            print(f"Saved {yaml_file}")
        else:
            print(f"{par_file} not found, skipping.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_par_to_yaml.py <parameters_directory>")
        sys.exit(1)
    convert_all_par_to_yaml(sys.argv[1])
