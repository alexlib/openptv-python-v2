import shutil
import filecmp
from pathlib import Path
import pytest
from openptv.parameters import UnifiedParameters

def test_cavity_parameters_roundtrip(tmp_path):
    # 1. Copy the test_cavity/parameters directory to a temp location
    orig_dir = Path(__file__).parent / "test_cavity" / "parameters"
    legacy_dir = tmp_path / "parameters_legacy"
    shutil.copytree(orig_dir, legacy_dir)

    # 2. Create a unified parameters.yml from the legacy directory
    unified_path = tmp_path / "parameters.yml"
    up = UnifiedParameters(unified_path)
    up.from_legacy_dir(legacy_dir)
    up.write()
    up.pprint()  # Print the unified YAML contents after writing

    # 3. Create a new directory from the unified YAML (parameters_copy)
    copy_dir = tmp_path / "parameters_copy"
    up2 = UnifiedParameters(unified_path)
    up2.read()
    up2.to_legacy_dir(copy_dir)

    # 4. Compare all .par files in legacy_dir and copy_dir
    # Only compare .par files for which there is a parameter class
    from openptv.parameters.unified import PARAMETER_CLASSES
    valid_par_names = set([
        ("track.par" if k == "tracking" else f"{k}.par")
        for k in PARAMETER_CLASSES.keys()
    ])
    orig_pars = sorted(p for p in legacy_dir.glob("*.par") if p.name in valid_par_names)
    copy_pars = sorted(p for p in copy_dir.glob("*.par") if p.name in valid_par_names)
    assert [p.name for p in orig_pars] == [p.name for p in copy_pars]
    # Compare file contents by parameter values (robust to float formatting)
    for orig, copy in zip(orig_pars, copy_pars):
        key = orig.stem if orig.stem != "track" else "tracking"
        cls = PARAMETER_CLASSES[key]
        # Special handling for n_img for sequence and cal_ori
        orig_obj = cls(path=legacy_dir)
        copy_obj = cls(path=copy_dir)
        if key == 'sequence':
            with open(orig) as f:
                lines = f.readlines()
            n_img = len(lines) - 2
            orig_obj.n_img = n_img
            with open(copy) as f:
                lines = f.readlines()
            n_img = len(lines) - 2
            copy_obj.n_img = n_img
        if key == 'cal_ori':
            with open(orig) as f:
                lines = f.readlines()
            n_img = (len(lines) - 1 - 3) // 2
            orig_obj.n_img = n_img
            with open(copy) as f:
                lines = f.readlines()
            n_img = (len(lines) - 1 - 3) // 2
            copy_obj.n_img = n_img
        orig_obj.read()
        copy_obj.read()
        # Compare dicts ignoring 'path' and 'exp_path'
        def filter_dict(d):
            return {k: v for k, v in d.items() if k not in ("path", "exp_path")}
        assert filter_dict(orig_obj.to_dict()) == filter_dict(copy_obj.to_dict()), f"Mismatch in {orig.name}"

if __name__ == "__main__":
    pytest.main([__file__])
