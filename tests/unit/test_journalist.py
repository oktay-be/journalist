"""
Unit tests for the main Journalist class.
"""

import sys
import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock, call
from datetime import datetime
from typing import List, Dict, Any

# Add src directory to path for importing modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from journalist import Journalist
from journalist.config import JournalistConfig

from journalist.exceptions import journalistError, ValidationError, NetworkError


from journalist.core.web_scraper import WebScraper

class TestJournalistInitialization:
    """Test Journalist class initialization and configuration."""
    
    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        journalist = Journalist()
        
        assert journalist.persist is True
        assert journalist.scrape_depth == 1
        assert journalist.session_id is not None
        assert len(journalist.session_id) > 0
        assert journalist.web_scraper is not None
    
    def test_init_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        journalist = Journalist(persist=False, scrape_depth=3)
        
        assert journalist.persist is False
        assert journalist.scrape_depth == 3
        assert journalist.session_id is not None
    
    def test_session_id_format(self):
        """Test that session_id follows expected format."""
        journalist = Journalist()
        
        # Should be in format YYYYMMDD_HHMMSS_microseconds
        assert len(journalist.session_id.split('_')) == 3
        date_part, time_part, micro_part = journalist.session_id.split('_')
        
        # Date part should be 8 digits
        assert len(date_part) == 8
        assert date_part.isdigit()
        
        # Time part should be 6 digits
        assert len(time_part) == 6
        assert time_part.isdigit()
        
        # Microseconds part should be digits
        assert micro_part.isdigit()
    
    def test_session_id_uniqueness(self):
        """Test that each journalist instance gets a unique session_id."""
        journalist1 = Journalist()
        journalist2 = Journalist()
        
        assert journalist1.session_id != journalist2.session_id
    
    @patch('journalist.core.file_manager.FileManager')
    @patch('journalist.config.JournalistConfig.get_base_workspace_path')
    def test_persistent_mode_setup(self, mock_get_workspace, mock_file_manager):
        """Test persistent mode filesystem setup."""
        mock_get_workspace.return_value = "/test/workspace"
        mock_fm_instance = MagicMock()
        mock_file_manager.return_value = mock_fm_instance
        mock_fm_instance.create_workspace_directories.return_value = True
        
        journalist = Journalist(persist=True)
        
        assert journalist.persist is True
        assert journalist.session_path is not None
        assert "/test/workspace" in journalist.session_path
        assert journalist.session_id in journalist.session_path
        assert journalist.file_manager is not None
        mock_fm_instance.create_workspace_directories.assert_called_once()
    
    def test_memory_mode_setup(self):
        """Test in-memory mode setup."""
        journalist = Journalist(persist=False)
        
        assert journalist.persist is False
        assert journalist.session_path is None
        assert journalist.news_from_scraping_path is None
        assert journalist.file_manager is None
        assert hasattr(journalist, 'memory_articles')
        assert journalist.memory_articles == []


class TestJournalistReadMethod:
    """Test the main read() method functionality."""
    
    @pytest.mark.asyncio
    async def test_read_empty_urls(self):
        """Test read method with empty URL list."""
        journalist = Journalist(persist=False)
        
        result = await journalist.read([])
        
        assert result['articles'] == []
        assert result['session_metadata']['total_articles'] == 0
        assert result['session_metadata']['session_id'] == journalist.session_id
        assert result['session_metadata']['persist_mode'] is False
    
    @pytest.mark.asyncio
    async def test_read_invalid_urls_type(self):
        """Test read method with invalid URL type."""
        journalist = Journalist(persist=False)
        
        # Test with None - should raise TypeError due to type checking
        # In practice, this would be caught by type checkers before runtime
        with pytest.raises((TypeError, AttributeError)):
            # Use type: ignore to bypass type checking for this test
            await journalist.read(None)  # type: ignore
    
    @pytest.mark.asyncio
    @patch('journalist.core.web_scraper.WebScraper.execute_scraping_for_session')
    async def test_read_with_urls_memory_mode(self, mock_scraper):
        """Test read method with URLs in memory mode."""
        # Mock scraper response
        mock_articles = [
            {'title': 'Test Article 1', 'url': 'https://example.com/1', 'content': 'Test content 1'},
            {'title': 'Test Article 2', 'url': 'https://example.com/2', 'content': 'Test content 2'}
        ]
        mock_scraper.return_value = {
            'articles': mock_articles,
            'metadata': {'total_links': 2}
        }
        
        journalist = Journalist(persist=False)
        urls = ['https://example.com', 'https://test.com']
        keywords = ['test', 'example']
        
        # Mock the web scraper context manager
        with patch.object(journalist.web_scraper, '__aenter__', return_value=journalist.web_scraper):
            with patch.object(journalist.web_scraper, '__aexit__', return_value=None):
                result = await journalist.read(urls=urls, keywords=keywords)
        
        assert len(result['articles']) == 2
        assert result['session_id'] == journalist.session_id
        assert result['extraction_summary']['urls_requested'] == 2
        assert result['extraction_summary']['keywords_used'] == keywords
        assert journalist.memory_articles == mock_articles
        
        mock_scraper.assert_called_once_with(
            session_id=journalist.session_id,
            keywords=keywords,
            sites=urls,
            scrape_depth=1
        )
    
    @pytest.mark.asyncio
    @patch('journalist.core.web_scraper.WebScraper.execute_scraping_for_session')
    @patch('journalist.core.file_manager.FileManager')
    async def test_read_with_urls_persistent_mode(self, mock_file_manager_class, mock_scraper):
        """Test read method with URLs in persistent mode."""
        # Setup mocks
        mock_articles = [{'title': 'Test Article', 'url': 'https://example.com', 'content': 'Test content'}]
        mock_scraper.return_value = {
            'articles': mock_articles,
            'metadata': {'total_links': 1}
        }
        
        mock_fm_instance = MagicMock()
        mock_file_manager_class.return_value = mock_fm_instance
        mock_fm_instance.create_workspace_directories.return_value = True
        
        with patch('journalist.config.JournalistConfig.get_base_workspace_path', return_value='/test'):
            journalist = Journalist(persist=True)
        
        urls = ['https://example.com']
        
        # Mock the web scraper context manager
        with patch.object(journalist.web_scraper, '__aenter__', return_value=journalist.web_scraper):
            with patch.object(journalist.web_scraper, '__aexit__', return_value=None):
                result = await journalist.read(urls=urls)
        
        assert len(result['articles']) == 1
        assert result['articles'][0]['title'] == 'Test Article'
        mock_fm_instance.save_workspace_data.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('journalist.core.web_scraper.WebScraper.execute_scraping_for_session')
    async def test_read_with_scraper_exception(self, mock_scraper):
        """Test read method when scraper raises exception."""
        mock_scraper.side_effect = NetworkError("Network error occurred")
        
        journalist = Journalist(persist=False)
        urls = ['https://example.com']
        
        # Mock the web scraper context manager
        with patch.object(journalist.web_scraper, '__aenter__', return_value=journalist.web_scraper):
            with patch.object(journalist.web_scraper, '__aexit__', return_value=None):
                result = await journalist.read(urls=urls)
        
        # Should not crash, but return empty articles due to exception handling
        assert result['articles'] == []
        assert result['extraction_summary']['urls_requested'] == 1
    
    @pytest.mark.asyncio
    async def test_read_response_structure(self):
        """Test that read method returns expected response structure."""
        journalist = Journalist(persist=False)
        
        result = await journalist.read([])
        
        # Check main structure
        assert 'articles' in result
        assert 'session_metadata' in result
        
        # Check session_metadata structure
        metadata = result['session_metadata']
        assert 'session_id' in metadata
        assert 'total_articles' in metadata
        assert 'total_links_processed' in metadata
        assert 'keywords_used' in metadata
        assert 'scrape_depth' in metadata
        assert 'persist_mode' in metadata
        
        assert metadata['session_id'] == journalist.session_id
        assert metadata['scrape_depth'] == 1
        assert metadata['persist_mode'] is False


class TestJournalistSessionManagement:
    """Test session management and potential race conditions."""
    
    def test_concurrent_session_creation(self):
        """Test creating multiple journalists concurrently to check for session ID collisions."""
        import threading
        import time
        
        session_ids = []
        
        def create_journalist():
            journalist = Journalist(persist=False)
            session_ids.append(journalist.session_id)
        
        # Create multiple journalists in quick succession
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=create_journalist)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All session IDs should be unique
        assert len(session_ids) == len(set(session_ids)), f"Found duplicate session IDs: {session_ids}"
    
    @patch('journalist.config.JournalistConfig.get_base_workspace_path')
    def test_session_path_generation(self, mock_get_workspace):
        """Test session path generation for persistent mode."""
        mock_get_workspace.return_value = "/test/workspace"
        
        with patch('journalist.core.file_manager.FileManager') as mock_fm:
            mock_fm.return_value.create_workspace_directories.return_value = True
            journalist = Journalist(persist=True)
        
        expected_session_path = f"/test/workspace/{journalist.session_id}"
        assert journalist.session_path == expected_session_path
        
        expected_news_path = f"{expected_session_path}/news_from_scraping"
        assert journalist.news_from_scraping_path == expected_news_path


class TestJournalistConfiguration:
    """Test configuration handling."""
    
    def test_default_configuration(self):
        """Test that journalist uses default configuration values."""
        journalist = Journalist()
    
        assert journalist.scrape_depth == 1
        assert journalist.persist is True

    def test_custom_scrape_depth(self):
        """Test custom scrape depth parameter."""
        journalist = Journalist(scrape_depth=5)
        
        assert journalist.scrape_depth == 5
    
    @patch('journalist.config.JournalistConfig.get_base_workspace_path')
    def test_workspace_path_configuration(self, mock_get_workspace):
        """Test workspace path configuration."""
        custom_path = "/custom/workspace/path"
        mock_get_workspace.return_value = custom_path
        
        with patch('journalist.core.file_manager.FileManager') as mock_fm:
            mock_fm.return_value.create_workspace_directories.return_value = True
            journalist = Journalist(persist=True)
        
        assert journalist.session_path is not None
        assert custom_path in journalist.session_path


class TestJournalistErrorHandling:
    """Test error handling scenarios."""
    
    @pytest.mark.asyncio
    @patch('journalist.core.web_scraper.WebScraper.execute_scraping_for_session')
    async def test_network_error_handling(self, mock_scraper):
        """Test handling of network errors during scraping."""
        mock_scraper.side_effect = NetworkError("Connection timeout", status_code=408)
        
        journalist = Journalist(persist=False)
        
        # Mock the web scraper context manager
        with patch.object(journalist.web_scraper, '__aenter__', return_value=journalist.web_scraper):
            with patch.object(journalist.web_scraper, '__aexit__', return_value=None):
                result = await journalist.read(['https://example.com'])
        
        # Should handle gracefully without crashing
        assert isinstance(result, dict)
        assert 'articles' in result
        assert result['articles'] == []
    
    @patch('journalist.core.file_manager.FileManager')
    def test_file_manager_creation_failure(self, mock_file_manager_class):
        """Test handling when file manager creation fails."""
        mock_file_manager_class.side_effect = Exception("File system error")
        
        with patch('journalist.config.JournalistConfig.get_base_workspace_path', return_value='/test'):
            # Should not crash during initialization
            with pytest.raises(Exception):
                Journalist(persist=True)


class TestJournalistIntegration:
    """Integration tests for journalist functionality."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_memory_mode(self):
        """Test complete workflow in memory mode."""
        journalist = Journalist(persist=False, scrape_depth=2)
        
        # Mock successful scraping
        mock_articles = [
            {'title': 'Article 1', 'url': 'https://site1.com/article1', 'content': 'Content 1'},
            {'title': 'Article 2', 'url': 'https://site2.com/article2', 'content': 'Content 2'}
        ]
        
        with patch.object(journalist.web_scraper, 'execute_scraping_for_session') as mock_scraper:
            mock_scraper.return_value = {'articles': mock_articles, 'metadata': {}}
            
            # Mock the web scraper context manager
            with patch.object(journalist.web_scraper, '__aenter__', return_value=journalist.web_scraper):
                with patch.object(journalist.web_scraper, '__aexit__', return_value=None):
                    result = await journalist.read(
                        urls=['https://site1.com', 'https://site2.com'],
                        keywords=['test', 'article']
                    )
        
        # Verify complete workflow
        assert len(result['articles']) == 2
        assert result['extraction_summary']['urls_requested'] == 2
        assert result['extraction_summary']['keywords_used'] == ['test', 'article']
        assert len(journalist.memory_articles) == 2
        
        # Verify scraper was called with correct parameters
        mock_scraper.assert_called_once_with(
            session_id=journalist.session_id,
            keywords=['test', 'article'],
            sites=['https://site1.com', 'https://site2.com'],
            scrape_depth=2
        )
