"""
Test roundtrip: legacy .par files, legacy .yaml files, and unified parameters.yaml.
This test demonstrates:
- Writing .par files for tracking and sequence
- Writing .yaml files for tracking and sequence (with identical content)
- Reading both formats into parameter classes
- Writing a unified parameters.yaml with all sections
- Reading back from unified parameters.yaml and verifying values
"""
import os
import yaml
from pathlib import Path
from openptv.parameters import UnifiedParameters, TrackingParams, SequenceParams

def write_tracking_par(path):
    # Write to 'track.par' to match TrackingParams.filename()
    with open(path / "track.par", "w") as f:
        f.write("-1\n1\n-2\n2\n-3\n3\n0.5\n0.1\n1\n")

def write_sequence_par(path):
    # Write to 'sequence.par' to match SequenceParams.filename()
    with open(path / "sequence.par", "w") as f:
        f.write("img\nimg\n0\n0\n")

def write_tracking_yaml(path):
    data = dict(dvxmin=-1, dvxmax=1, dvymin=-2, dvymax=2, dvzmin=-3, dvzmax=3, dangle=0.5, dacc=0.1, flagNewParticles=True)
    with open(path, "w") as f:
        yaml.safe_dump(data, f)

def write_sequence_yaml(path):
    data = dict(n_img=2, base_name=["img", "img"], first=0, last=0)
    with open(path, "w") as f:
        yaml.safe_dump(data, f)

def filter_param_dict(d):
    return {k: v for k, v in d.items() if k not in ("path", "exp_path")}

def test_legacy_and_unified_yaml(tmp_path):
    d = tmp_path / "params"
    d.mkdir()
    # Write legacy .par files
    write_tracking_par(d)
    write_sequence_par(d)
    # Write legacy .yaml files
    write_tracking_yaml(d / "track.yaml")
    write_sequence_yaml(d / "sequence.yaml")
    # Read from .par files
    t_par = TrackingParams(path=d)
    t_par.read()
    s_par = SequenceParams(n_img=2, path=d)
    s_par.read()
    # Read from .yaml files
    with open(d / "track.yaml") as f:
        t_yaml = TrackingParams.from_dict(yaml.safe_load(f))
    with open(d / "sequence.yaml") as f:
        s_yaml = SequenceParams.from_dict(yaml.safe_load(f))
    # Check values are identical (ignore path/exp_path)
    assert filter_param_dict(t_par.to_dict()) == filter_param_dict(t_yaml.to_dict())
    assert filter_param_dict(s_par.to_dict()) == filter_param_dict(s_yaml.to_dict())
    # Write unified parameters.yaml
    unified_path = d / "parameters.yaml"
    up = UnifiedParameters(unified_path)
    up.set_section("tracking", t_par)
    up.set_section("sequence", s_par)
    up.write()
    # Read back unified parameters.yaml
    up2 = UnifiedParameters(unified_path)
    up2.read()
    t_uni = up2.get_section("tracking")
    s_uni = up2.get_section("sequence")
    assert filter_param_dict(t_uni.to_dict()) == filter_param_dict(t_par.to_dict())
    assert filter_param_dict(s_uni.to_dict()) == filter_param_dict(s_par.to_dict())
    # Print for demonstration
    print("Legacy .par:", (d / "track.par").read_text())
    print("Legacy .yaml:", (d / "track.yaml").read_text())
    print("Unified parameters.yaml:", (d / "parameters.yaml").read_text())
