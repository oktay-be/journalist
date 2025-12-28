"""
Unit tests for Journalist custom exceptions.
"""

import pytest
from journalist.exceptions import (
    journalistError,
    ValidationError,
    NetworkError,
    ExtractionError
)


class TestJournalistError:
    """Test base journalistError exception."""
    
    def test_journalist_error_inheritance(self):
        """Test that journalistError inherits from Exception."""
        assert issubclass(journalistError, Exception)
    
    def test_journalist_error_instantiation(self):
        """Test that journalistError can be instantiated."""
        error = journalistError("Test error message")
        assert str(error) == "Test error message"
    
    def test_journalist_error_raise(self):
        """Test that journalistError can be raised and caught."""
        with pytest.raises(journalistError) as exc_info:
            raise journalistError("Test error")
        
        assert str(exc_info.value) == "Test error"
    
    def test_journalist_error_empty_message(self):
        """Test journalistError with empty message."""
        error = journalistError("")
        assert str(error) == ""
    
    def test_journalist_error_none_message(self):
        """Test journalistError with None message."""
        error = journalistError(None)
        assert str(error) == "None"


class TestValidationError:
    """Test ValidationError exception."""
    
    def test_validation_error_inheritance(self):
        """Test that ValidationError inherits from journalistError."""
        assert issubclass(ValidationError, journalistError)
        assert issubclass(ValidationError, Exception)
    
    def test_validation_error_instantiation(self):
        """Test ValidationError instantiation."""
        error = ValidationError("Invalid input")
        assert str(error) == "Invalid input"
    
    def test_validation_error_raise_and_catch_specific(self):
        """Test raising and catching ValidationError specifically."""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Validation failed")
        
        assert str(exc_info.value) == "Validation failed"
    
    def test_validation_error_catch_as_base_class(self):
        """Test that ValidationError can be caught as journalistError."""
        with pytest.raises(journalistError):
            raise ValidationError("Validation failed")
    
    def test_validation_error_message_types(self):
        """Test ValidationError with different message types."""
        # String message
        error1 = ValidationError("String message")
        assert str(error1) == "String message"
        
        # Numeric message
        error2 = ValidationError(123)
        assert str(error2) == "123"


class TestNetworkError:
    """Test NetworkError exception."""
    
    def test_network_error_inheritance(self):
        """Test that NetworkError inherits from journalistError."""
        assert issubclass(NetworkError, journalistError)
        assert issubclass(NetworkError, Exception)
    
    def test_network_error_basic_instantiation(self):
        """Test NetworkError with just message."""
        error = NetworkError("Connection failed")
        assert str(error) == "Connection failed"
        assert error.status_code is None
    
    def test_network_error_with_status_code(self):
        """Test NetworkError with message and status code."""
        error = NetworkError("HTTP Error", status_code=404)
        assert str(error) == "HTTP Error"
        assert error.status_code == 404
    
    def test_network_error_status_code_attribute(self):
        """Test that status_code attribute is accessible."""
        error = NetworkError("Timeout", status_code=408)
        assert hasattr(error, 'status_code')
        assert error.status_code == 408
    
    def test_network_error_status_code_none(self):
        """Test NetworkError when status_code is explicitly None."""
        error = NetworkError("Generic error", status_code=None)
        assert error.status_code is None
    
    def test_network_error_raise_and_catch(self):
        """Test raising and catching NetworkError."""
        with pytest.raises(NetworkError) as exc_info:
            raise NetworkError("Network timeout", status_code=504)
        
        assert str(exc_info.value) == "Network timeout"
        assert exc_info.value.status_code == 504
    
    def test_network_error_various_status_codes(self):
        """Test NetworkError with various HTTP status codes."""
        status_codes = [400, 401, 403, 404, 500, 502, 503, 504]
        
        for status_code in status_codes:
            error = NetworkError(f"HTTP {status_code}", status_code=status_code)
            assert error.status_code == status_code
            assert str(error) == f"HTTP {status_code}"


class TestExtractionError:
    """Test ExtractionError exception."""
    
    def test_extraction_error_inheritance(self):
        """Test that ExtractionError inherits from journalistError."""
        assert issubclass(ExtractionError, journalistError)
        assert issubclass(ExtractionError, Exception)
    
    def test_extraction_error_basic_instantiation(self):
        """Test ExtractionError with just message."""
        error = ExtractionError("Failed to extract content")
        assert str(error) == "Failed to extract content"
        assert error.url is None
    
    def test_extraction_error_with_url(self):
        """Test ExtractionError with message and URL."""
        error = ExtractionError("Parse error", url="https://example.com")
        assert str(error) == "Parse error"
        assert error.url == "https://example.com"
    
    def test_extraction_error_url_attribute(self):
        """Test that url attribute is accessible."""
        error = ExtractionError("Content missing", url="https://test.com/article")
        assert hasattr(error, 'url')
        assert error.url == "https://test.com/article"
    
    def test_extraction_error_url_none(self):
        """Test ExtractionError when url is explicitly None."""
        error = ExtractionError("Generic extraction error", url=None)
        assert error.url is None
    
    def test_extraction_error_raise_and_catch(self):
        """Test raising and catching ExtractionError."""
        with pytest.raises(ExtractionError) as exc_info:
            raise ExtractionError("Selector not found", url="https://news.com")
        
        assert str(exc_info.value) == "Selector not found"
        assert exc_info.value.url == "https://news.com"
    
    def test_extraction_error_various_urls(self):
        """Test ExtractionError with various URL formats."""
        urls = [
            "https://example.com",
            "http://test.com/article",
            "https://news.site.com/category/article?id=123",
            "https://localhost:8080/test"
        ]
        
        for url in urls:
            error = ExtractionError("Extraction failed", url=url)
            assert error.url == url


class TestExceptionInteractions:
    """Test interactions between different exception types."""
    
    def test_all_inherit_from_journalist_error(self):
        """Test that all custom exceptions inherit from journalistError."""
        exceptions = [ValidationError, NetworkError, ExtractionError]
        
        for exc_class in exceptions:
            assert issubclass(exc_class, journalistError)
    
    def test_catch_all_as_journalist_error(self):
        """Test that all custom exceptions can be caught as journalistError."""
        exceptions_to_test = [
            ValidationError("validation"),
            NetworkError("network"),
            ExtractionError("extraction")
        ]
        
        for exc in exceptions_to_test:
            with pytest.raises(journalistError):
                raise exc
    
    def test_specific_exception_catching(self):
        """Test catching specific exception types."""
        # Should catch ValidationError specifically
        with pytest.raises(ValidationError):
            raise ValidationError("test")
        
        # Should catch NetworkError specifically  
        with pytest.raises(NetworkError):
            raise NetworkError("test")
        
        # Should catch ExtractionError specifically
        with pytest.raises(ExtractionError):
            raise ExtractionError("test")
    
    def test_exception_type_differentiation(self):
        """Test that exceptions can be differentiated by type."""
        validation_error = ValidationError("validation")
        network_error = NetworkError("network") 
        extraction_error = ExtractionError("extraction")
        
        assert isinstance(validation_error, ValidationError)
        assert isinstance(network_error, NetworkError)
        assert isinstance(extraction_error, ExtractionError)
        
        assert not isinstance(validation_error, NetworkError)
        assert not isinstance(network_error, ExtractionError)
        assert not isinstance(extraction_error, ValidationError)


class TestExceptionAttributes:
    """Test exception-specific attributes."""
    
    def test_network_error_attributes(self):
        """Test NetworkError specific attributes."""
        error = NetworkError("HTTP 404", status_code=404)
        
        # Should have both base Exception attributes and custom ones
        assert hasattr(error, 'args')
        assert hasattr(error, 'status_code')
        assert error.args == ("HTTP 404",)
        assert error.status_code == 404
    
    def test_extraction_error_attributes(self):
        """Test ExtractionError specific attributes."""
        error = ExtractionError("Parse failed", url="https://example.com")
        
        # Should have both base Exception attributes and custom ones
        assert hasattr(error, 'args')
        assert hasattr(error, 'url')
        assert error.args == ("Parse failed",)
        assert error.url == "https://example.com"
    
    def test_validation_error_attributes(self):
        """Test ValidationError basic attributes."""
        error = ValidationError("Invalid data")
        
        # Should have base Exception attributes
        assert hasattr(error, 'args')
        assert error.args == ("Invalid data",)


class TestExceptionEdgeCases:
    """Test edge cases for exceptions."""
    
    def test_empty_message_exceptions(self):
        """Test exceptions with empty messages."""
        validation_error = ValidationError("")
        network_error = NetworkError("")
        extraction_error = ExtractionError("")
        
        assert str(validation_error) == ""
        assert str(network_error) == ""
        assert str(extraction_error) == ""
    
    def test_multiple_args_exceptions(self):
        """Test exceptions with multiple arguments."""
        error = ValidationError("Error", "Additional info")
        assert error.args == ("Error", "Additional info")
    
    def test_exception_repr(self):
        """Test string representation of exceptions."""
        validation_error = ValidationError("test validation")
        network_error = NetworkError("test network", status_code=500)
        extraction_error = ExtractionError("test extraction", url="https://test.com")
        
        # All should have meaningful string representations
        assert "test validation" in str(validation_error)
        assert "test network" in str(network_error)
        assert "test extraction" in str(extraction_error)
