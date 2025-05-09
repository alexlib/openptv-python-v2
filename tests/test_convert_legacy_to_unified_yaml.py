"""
Test converting a legacy parameters directory to a single unified YAML file using UnifiedParameters.
"""
import tempfile
from pathlib import Path
import yaml
import pytest
from openptv.parameters import UnifiedParameters, TrackingParams, SequenceParams

def make_legacy_dir(tmp_path):
    d = tmp_path / "legacy_params"
    d.mkdir()
    # Write track.par (not tracking.par)
    t = TrackingParams(dvxmin=-1, dvxmax=1, dvymin=-2, dvymax=2, dvzmin=-3, dvzmax=3, dangle=0.5, dacc=0.1)
    t.path = d
    t.write()
    # Write sequence.par
    s = SequenceParams(n_img=2, base_name=["img", "img"], first=0, last=0)
    s.path = d
    s.write()
    # Write gui.yaml
    with open(d / "gui.yaml", "w") as f:
        yaml.safe_dump({"window_size": [800, 600]}, f)
    return d

def test_convert_legacy_to_unified_yaml(tmp_path):
    legacy_dir = make_legacy_dir(tmp_path)
    unified_path = tmp_path / "parameters.yaml"
    up = UnifiedParameters(unified_path)
    up.from_legacy_dir(legacy_dir)
    up.write()
    # Read back unified YAML
    up2 = UnifiedParameters(unified_path)
    up2.read()
    assert up2.get_section("tracking").dvxmin == -1
    assert up2.get_section("sequence").n_img == 2
    assert up2.get_gui_param("window_size") == [800, 600]

if __name__ == "__main__":
    pytest.main([__file__])
