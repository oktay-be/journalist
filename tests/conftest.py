"""
Global test configuration for pytest.
"""
import os
import sys
import pytest

# Add src directory to Python path for all tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Setup test environment for journalist package.
    """
    # Ensure src directory is in path
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    if src_path not in sys.path:        sys.path.insert(0, src_path)
    
    yield  # This allows tests to run
