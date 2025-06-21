"""
journalist - Universal News Content Extraction Library

A powerful and flexible library for extracting content from news websites worldwide.
"""

__version__ = "0.2.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Public API exports
from .journalist import Journalist
from .exceptions import journalistError, ValidationError, NetworkError, ExtractionError

__all__ = [
    "Journalist",
    "journalistError",
    "ValidationError",
    "NetworkError",
    "ExtractionError",
]
