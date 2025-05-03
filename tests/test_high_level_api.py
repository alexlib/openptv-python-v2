"""
Test the high-level API of the openptv package.
"""

import pytest
import numpy as np


def test_using_cython():
    """Test that we can determine which implementation is being used."""
    from openptv import using_cython

    # Check that using_cython() returns a boolean
    assert isinstance(using_cython(), bool)

    # We expect Cython to be available since we just built it
    assert using_cython() is True, "Cython implementation should be available"


if __name__ == "__main__":
    # This allows running the tests directly with python
    import sys
    sys.exit(pytest.main(["-v", __file__]))