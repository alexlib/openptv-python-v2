import os
import pytest
from pathlib import Path
import shutil

# Define the order of test modules
test_order = [
    "test_trafo_bindings.py",
    "test_tracker.py",
    "test_segmentation.py",
    # Add other test files here
]

def pytest_collection_modifyitems(items):
    """Modify the order of test items to run problematic tests first."""
    # Create a dictionary mapping test module names to their position in the test_order list
    module_order = {module: i for i, module in enumerate(test_order)}

    # Sort the test items based on their module's position in the test_order list
    # If a module is not in the test_order list, it will be run after all modules in the list
    items.sort(key=lambda item: module_order.get(os.path.basename(item.module.__file__), float('inf')))

# Set GUI backend before any imports
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyside6'

# Skip GUI tests when running headless
@pytest.fixture(scope="session", autouse=True)
def check_display():
    if "DISPLAY" not in os.environ and "WAYLAND_DISPLAY" not in os.environ:
        pytest.skip("GUI tests require a display")


@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture to set up test data directory"""
    # Get the absolute path to the test_cavity directory
    test_dir = Path(__file__).parent / "test_cavity"
    if not test_dir.exists():
        pytest.skip(f"Test data directory {test_dir} not found")
    return test_dir

@pytest.fixture(scope="session")
def clean_test_environment(test_data_dir):
    """Clean up test environment before and after tests"""
    # Clean up any existing test results
    results_dir = test_data_dir / "res"
    if results_dir.exists():
        shutil.rmtree(results_dir)

    # Create fresh directories
    results_dir.mkdir(exist_ok=True)

    yield

    # Cleanup after tests
    if results_dir.exists():
        shutil.rmtree(results_dir)