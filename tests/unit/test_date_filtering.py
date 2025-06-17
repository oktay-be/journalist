"""
Test date filtering functionality for articles.
"""

import pytest
import tempfile
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from journalist import Journalist
from journalist.core.file_manager import FileManager


class TestURLDateExtraction:
    """Test date extraction from URLs."""
    
    def test_extract_dates_from_url_with_various_formats(self):
        """Test extraction of dates from URLs with different date formats."""
        with tempfile.TemporaryDirectory() as temp_dir:
            fm = FileManager(temp_dir)
            
            test_cases = [
                ("https://example.com/news/2023/11/08/article", True),
                ("https://example.com/archive_2022_12_25_christmas", True),
                ("https://site.com/2024/03/20/article", True),
                ("https://example.com/no-date-article", False),
                ("https://example.com/current-news", False),
            ]
            
            for url, should_find_date in test_cases:
                dates = fm._extract_dates_from_url(url)
                if should_find_date:
                    assert len(dates) > 0, f"Should find date in URL: {url}"
                else:
                    assert len(dates) == 0, f"Should not find date in URL: {url}"
    
    def test_is_url_too_old(self):
        """Test checking if URL contains old dates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            fm = FileManager(temp_dir)
            
            # Old URLs (should be considered too old)
            old_urls = [
                "https://example.com/news/2023/01/15/old-news",
                "https://example.com/archive_2022_12_25_christmas",
            ]
            
            # Recent/no-date URLs (should not be considered too old)
            recent_urls = [
                "https://example.com/news/2025/06/17/fresh-news",
                "https://example.com/current-news",
                "https://example.com/no-date-article",
            ]
            
            for url in old_urls:
                assert fm._is_url_too_old(url, max_age_days=7), f"Should be too old: {url}"
            
            for url in recent_urls:
                assert not fm._is_url_too_old(url, max_age_days=7), f"Should not be too old: {url}"


class TestArticleDateFiltering:
    """Test article date filtering functionality."""
    
    def test_filter_articles_by_url_dates(self):
        """Test filtering articles based on dates found in URLs."""
        journalist = Journalist(persist=False)
        
        test_articles = [
            # Old URLs (should be filtered)
            {'url': 'https://example.com/news/2023/01/15/old-news', 'published_at': None},
            {'url': 'https://example.com/archive_2022_12_25_christmas', 'published_at': None},
            
            # Recent URLs (should pass)
            {'url': 'https://example.com/news/2025/06/17/fresh-news', 'published_at': None},
            {'url': 'https://example.com/current-news', 'published_at': None},
            
            # No date URLs (should pass)
            {'url': 'https://example.com/no-date-article', 'published_at': None},
        ]
        
        filtered_articles = journalist._filter_articles_by_date(test_articles, max_age_days=7)
        
        # Should filter out the 2 old articles
        assert len(filtered_articles) == 3
        
        # Check that old articles were removed
        filtered_urls = [article['url'] for article in filtered_articles]
        assert 'https://example.com/news/2023/01/15/old-news' not in filtered_urls
        assert 'https://example.com/archive_2022_12_25_christmas' not in filtered_urls
        
        # Check that recent/no-date articles were kept
        assert 'https://example.com/news/2025/06/17/fresh-news' in filtered_urls
        assert 'https://example.com/current-news' in filtered_urls
        assert 'https://example.com/no-date-article' in filtered_urls
    
    def test_filter_articles_by_published_at_dates(self):
        """Test filtering articles based on published_at metadata."""
        journalist = Journalist(persist=False)
        
        # Calculate test dates
        old_date = (datetime.now() - timedelta(days=30)).isoformat()
        recent_date = (datetime.now() - timedelta(days=1)).isoformat()
        
        test_articles = [
            # Old published_at (should be filtered)
            {
                'url': 'https://example.com/article1',
                'title': 'Old Article',
                'published_at': old_date,
                'body': 'Old content'
            },
            
            # Recent published_at (should pass)
            {
                'url': 'https://example.com/article2',
                'title': 'Recent Article',
                'published_at': recent_date,
                'body': 'Recent content'
            },
            
            # No published_at (should pass)
            {
                'url': 'https://example.com/article3',
                'title': 'No Date Article',
                'published_at': None,
                'body': 'No date content'
            }
        ]
        
        filtered_articles = journalist._filter_articles_by_date(test_articles, max_age_days=7)
        
        # Should filter out the 1 old article
        assert len(filtered_articles) == 2
        
        # Check that old article was removed
        filtered_titles = [article['title'] for article in filtered_articles]
        assert 'Old Article' not in filtered_titles
        
        # Check that recent/no-date articles were kept
        assert 'Recent Article' in filtered_titles
        assert 'No Date Article' in filtered_titles
    
    def test_filter_mixed_date_sources(self):
        """Test filtering with both URL dates and published_at dates."""
        journalist = Journalist(persist=False)
        
        test_articles = [
            # Old URL date, should be filtered
            {
                'url': 'https://example.com/news/2023/01/15/old-url',
                'published_at': None,
                'title': 'Old URL'
            },
            
            # Old published_at, should be filtered
            {
                'url': 'https://example.com/current-article',
                'published_at': '2023-01-15T10:00:00',
                'title': 'Old Published Date'
            },
            
            # Fresh article, should pass
            {
                'url': 'https://example.com/fresh-article',
                'published_at': (datetime.now() - timedelta(days=1)).isoformat(),
                'title': 'Fresh Article'
            },
            
            # No date info, should pass
            {
                'url': 'https://example.com/no-date',
                'published_at': None,
                'title': 'No Date Info'
            }
        ]
        
        filtered_articles = journalist._filter_articles_by_date(test_articles, max_age_days=7)
        
        # Should keep only the fresh article and no-date article
        assert len(filtered_articles) == 2
        
        filtered_titles = [article['title'] for article in filtered_articles]
        assert 'Fresh Article' in filtered_titles
        assert 'No Date Info' in filtered_titles
        assert 'Old URL' not in filtered_titles
        assert 'Old Published Date' not in filtered_titles
    
    @patch('journalist.journalist.datetime')
    def test_filter_articles_custom_max_age(self, mock_datetime):
        """Test filtering with custom max_age_days parameter."""
        # Mock current time
        mock_now = datetime(2025, 6, 17, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat
        
        journalist = Journalist(persist=False)
        
        test_articles = [
            {
                'url': 'https://example.com/article',
                'published_at': '2025-06-10T12:00:00',  # 7 days old
                'title': 'Week Old Article'
            }
        ]
        
        # With max_age_days=7, should be filtered (exactly at cutoff)
        filtered_30_days = journalist._filter_articles_by_date(test_articles, max_age_days=30)
        filtered_6_days = journalist._filter_articles_by_date(test_articles, max_age_days=6)
        
        assert len(filtered_30_days) == 1  # Should pass with 30-day limit
        assert len(filtered_6_days) == 0   # Should be filtered with 6-day limit


class TestDateFilteringEdgeCases:
    """Test edge cases in date filtering."""
    
    def test_filter_with_invalid_published_at_formats(self):
        """Test handling of invalid published_at date formats."""
        journalist = Journalist(persist=False)
        
        test_articles = [
            {
                'url': 'https://example.com/article1',
                'published_at': 'invalid-date-format',
                'title': 'Invalid Date Format'
            },
            {
                'url': 'https://example.com/article2',
                'published_at': '',
                'title': 'Empty Date'
            },
            {
                'url': 'https://example.com/article3',
                'published_at': 123456,  # Wrong type
                'title': 'Wrong Type Date'
            }
        ]
        
        # Should not crash and should keep all articles (invalid dates ignored)
        filtered_articles = journalist._filter_articles_by_date(test_articles, max_age_days=7)
        assert len(filtered_articles) == 3
    
    def test_filter_with_empty_articles_list(self):
        """Test filtering with empty articles list."""
        journalist = Journalist(persist=False)
        
        filtered_articles = journalist._filter_articles_by_date([], max_age_days=7)
        assert len(filtered_articles) == 0
    
    def test_filter_preserves_article_structure(self):
        """Test that filtering preserves the complete article structure."""
        journalist = Journalist(persist=False)
        
        original_article = {
            'url': 'https://example.com/current-article',
            'title': 'Test Article',
            'content': 'Article content',
            'author': 'Test Author',
            'published_at': (datetime.now() - timedelta(days=1)).isoformat(),
            'keywords_found': ['test', 'article'],
            'custom_field': 'custom_value'
        }
        
        filtered_articles = journalist._filter_articles_by_date([original_article], max_age_days=7)
        
        assert len(filtered_articles) == 1
        assert filtered_articles[0] == original_article  # Should be identical
