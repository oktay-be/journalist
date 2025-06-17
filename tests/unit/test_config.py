"""
Unit tests for Journalist configuration.
"""

import os
from journalist.config import JournalistConfig


class TestJournalistConfig:
    """Test JournalistConfig class functionality."""
    
    def test_default_values(self):
        """Test that default configuration values are set correctly."""
        config = JournalistConfig()
        
        assert config.base_workspace_path == ".journalist_workspace"
    
    def test_class_method_base_workspace_path(self):
        """Test get_base_workspace_path class method."""
        workspace_path = JournalistConfig.get_base_workspace_path()
        assert workspace_path == ".journalist_workspace"
        assert isinstance(workspace_path, str)
    
    def test_configuration_consistency(self):
        """Test that instance values match class method values."""
        config = JournalistConfig()
        
        assert config.base_workspace_path == JournalistConfig.get_base_workspace_path()
    
    def test_multiple_instances_same_values(self):
        """Test that multiple config instances have the same default values."""
        config1 = JournalistConfig()
        config2 = JournalistConfig()
        
        assert config1.base_workspace_path == config2.base_workspace_path
    
    def test_class_constants_exist(self):
        """Test that class constants are defined."""
        assert hasattr(JournalistConfig, 'DEFAULT_BASE_WORKSPACE_PATH')
        assert JournalistConfig.DEFAULT_BASE_WORKSPACE_PATH == ".journalist_workspace"


class TestJournalistConfigPaths:
    """Test configuration path handling."""
    
    def test_workspace_path_is_relative(self):
        """Test that default workspace path is relative."""
        path = JournalistConfig.get_base_workspace_path()
        assert not os.path.isabs(path)
        assert path.startswith(".")
    
    def test_path_components_valid(self):
        """Test that paths don't contain invalid characters."""
        workspace_path = JournalistConfig.get_base_workspace_path()
        
        # Should not contain problematic characters
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        for char in invalid_chars:
            assert char not in workspace_path
    
    def test_paths_not_empty(self):
        """Test that configuration paths are not empty."""
        assert len(JournalistConfig.get_base_workspace_path()) > 0


class TestJournalistConfigTypes:
    """Test configuration value types."""
    
    def test_base_workspace_path_type(self):
        """Test base_workspace_path is string type."""
        config = JournalistConfig()
        assert isinstance(config.base_workspace_path, str)
        assert isinstance(JournalistConfig.get_base_workspace_path(), str)


class TestJournalistConfigImmutability:
    """Test that configuration values behave as expected."""
    
    def test_class_method_return_values_consistent(self):
        """Test that class methods return consistent values across calls."""
        # Call multiple times and ensure same values
        workspace_paths = [JournalistConfig.get_base_workspace_path() for _ in range(5)]
        
        # All values should be identical
        assert len(set(workspace_paths)) == 1
    
    def test_instance_modification_independence(self):
        """Test that modifying one instance doesn't affect others."""
        config1 = JournalistConfig()
        config2 = JournalistConfig()
        
        # Modify first instance
        config1.base_workspace_path = "modified_workspace"
        
        # Second instance should remain unchanged
        assert config2.base_workspace_path == ".journalist_workspace"
        
        # Class methods should remain unchanged
        assert JournalistConfig.get_base_workspace_path() == ".journalist_workspace"


class TestJournalistConfigEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_config_initialization_no_args(self):
        """Test config can be initialized without arguments."""
        config = JournalistConfig()
        assert config is not None
        assert hasattr(config, 'base_workspace_path')
    
    def test_config_attributes_not_none(self):
        """Test that no configuration attributes are None."""
        config = JournalistConfig()
        assert config.base_workspace_path is not None
    
    def test_class_methods_not_none(self):
        """Test that class methods don't return None."""
        assert JournalistConfig.get_base_workspace_path() is not None
