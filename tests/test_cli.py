"""
Tests for the CLI module in openptv.gui.cli

This module tests the command-line interface functionality and provides clear feedback
on test success or failure.
"""
import pytest
from openptv.gui import cli


def test_cli_template():
    """Test the basic CLI template function"""
    print("\nTesting CLI template function...")
    try:
        result = cli.cli()
        expected = 'CLI template'

        if result != expected:
            pytest.fail(f"Expected '{expected}', but got '{result}'")

        print(f"✓ CLI template test passed successfully! Result: '{result}'")
    except Exception as e:
        pytest.fail(f"CLI template test failed with error: {str(e)}")


if __name__ == "__main__":
    """Run the tests directly with detailed output."""
    import sys
    import pytest

    print("\n=== Running CLI Tests ===\n")

    # Run the tests with verbose output
    result = pytest.main(["-v", __file__])

    if result == 0:
        print("\n✅ All CLI tests passed successfully!")
    else:
        print("\n❌ Some CLI tests failed. See details above.")

    sys.exit(result)
