import pytest
from openptv.gui import pyptv_batch
from pathlib import Path

def test_pyptv_batch(test_data_dir):
    """Test batch processing with test cavity data"""
    # Skip this test while we're transitioning to the new parameter module
    # pytest.skip("Skipping while transitioning to the new parameter module")

    test_dir = test_data_dir
    assert test_dir.exists(), f"Test directory {test_dir} not found"

    # Test specific frame range
    start_frame = 10000
    end_frame = 10004

    try:
        pyptv_batch.main(str(test_dir), start_frame, end_frame)
    except Exception as e:
        pytest.fail(f"Batch processing failed: {str(e)}")

def test_pyptv_batch_with_unified_yaml(tmp_path):
    """Test batch processing using only parameters.yml in the parameters directory."""
    import shutil
    from openptv.parameters import UnifiedParameters
    from openptv.gui import pyptv_batch
    import os

    # Copy test_cavity directory to temp
    orig_dir = Path(__file__).parent / "test_cavity"
    test_dir = tmp_path / "test_cavity"
    shutil.copytree(orig_dir, test_dir)
    param_dir = test_dir / "parameters"

    # Create parameters.yml in the parameters directory
    unified_path = param_dir / "parameters.yml"
    up = UnifiedParameters(unified_path)
    up.from_legacy_dir(param_dir)
    up.write()

    # Optionally, remove all .par/.yaml files except parameters.yml to ensure only unified is used
    for f in param_dir.glob("*.par"): f.unlink()
    for f in param_dir.glob("*.yaml"): f.unlink()

    # Run batch using only parameters.yml
    start_frame = 10000
    end_frame = 10004
    try:
        pyptv_batch.main(str(test_dir), start_frame, end_frame)
    except Exception as e:
        pytest.fail(f"Batch processing with parameters.yml failed: {str(e)}")



if __name__ == "__main__":
    """Run the tests directly with detailed output."""
    import sys

    print("\n=== Running pyptv_batch with unified parameters.yml Tests ===\n")

    # Run the tests with verbose output
    import pytest
    result = pytest.main(["-v", __file__])

    if result == 0:
        print("\n✅ All pyptv_batch tests passed successfully!")
    else:
        print("\n❌ Some pyptv_batch tests failed. See details above.")

    sys.exit(result)
