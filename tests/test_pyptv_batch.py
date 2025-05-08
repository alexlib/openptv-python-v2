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
