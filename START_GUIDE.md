# Journalist Library - Start Guide

This guide documents the setup and testing process for the journalist library with a focus on Turkish sports news extraction.

## Project Overview

The journalist library is a Python tool for web scraping and content extraction from news websites. It supports keyword-based filtering and can extract articles from multiple URLs concurrently.

## Environment Setup

### 1. Python Environment Configuration

The project uses Python with pip-tools for dependency management. Follow these steps to set up your environment:

```bash
# Configure Python environment
python -m venv venv
venv\Scripts\activate

# Install pip-tools
pip install pip-tools

# Compile requirements from requirements.in
pip-compile requirements.in

# Install all dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### 2. Project Structure

```
journalist/
├── src/journalist/           # Main package
│   ├── __init__.py
│   ├── journalist.py         # Main Journalist class
│   ├── config.py            # Configuration management
│   ├── core/                # Core functionality
│   └── extractors/          # Content extractors
├── examples/                # Example scripts
├── tests/                   # Test suite
├── docs/                    # Documentation
├── requirements.in          # Dependency specifications
├── requirements.txt         # Compiled dependencies
└── README.md               # Project documentation
```

## Test Case: Turkish Sports News

### Objective
Extract news articles about Fenerbahçe and Galatasaray from Turkish sports websites.

### Target Configuration
- **Keywords**: `["fenerbahce", "galatasaray"]`
- **URLs**: 
  - `https://www.fanatik.com.tr`
  - `https://www.fotomac.com.tr`

### Test Script

Created `test_turkish_sports.py` with the following features:

#### Key Components

1. **Journalist Instance Configuration**:
   ```python
   journalist = Journalist(persist=True, scrape_depth=1)
   ```

2. **Async Content Extraction**:
   ```python
   result = await journalist.read(
       urls=urls,
       keywords=keywords
   )
   ```

3. **Result Processing**:
   - Article extraction and display
   - Extraction summary with metrics
   - Error handling and reporting

#### Script Features

- **Comprehensive Logging**: Detailed output showing extraction progress
- **Article Display**: Shows title, URL, publication date, and content preview
- **Keyword Matching**: Displays which keywords were matched in each article
- **Performance Metrics**: Shows processing time and article counts
- **Error Handling**: Catches and displays any extraction errors
- **Resource Cleanup**: Properly closes journalist instance

### Running the Test

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the Turkish sports news test
python test_turkish_sports.py
```

### Expected Output Format

```
🚀 Starting Turkish Sports News Extraction Test
============================================================
📰 Target URLs: ['https://www.fanatik.com.tr', 'https://www.fotomac.com.tr']
🔍 Keywords: ['fenerbahce', 'galatasaray']
------------------------------------------------------------
⏳ Starting content extraction...
✅ Content extraction completed!
============================================================
📄 Found X articles:
------------------------------------------------------------

🏆 Article 1:
   Title: [Article Title]
   URL: [Article URL]
   Published: [Publication Date]
   Content Preview: [First 200 characters]...
   Matched Keywords: [Keywords found]
----------------------------------------

📊 Extraction Summary:
   URLs Processed: 2
   Articles Extracted: X
   Extraction Time: X.XX seconds

🎉 Test completed successfully!
```

## Library Features Demonstrated

### Core Functionality
- **Multi-URL Processing**: Concurrent extraction from multiple websites
- **Keyword Filtering**: Content filtering based on specified keywords
- **Async Operations**: Non-blocking asynchronous content extraction
- **Persistence**: Option to cache results for improved performance

### Content Extraction
- **Multiple Extractors**: Uses various extraction methods for robust content retrieval
- **Article Metadata**: Extracts titles, URLs, publication dates, and content
- **Keyword Matching**: Identifies which keywords appear in each article

### Error Handling
- **Graceful Degradation**: Continues processing even if some URLs fail
- **Detailed Error Reporting**: Provides specific error information
- **Resource Management**: Proper cleanup of network resources

## Configuration Options

The journalist library supports various configuration options:

- `persist`: Enable/disable result caching
- `scrape_depth`: Control how deep to crawl linked pages
- `keywords`: Filter content by specific terms
- `urls`: Target websites for content extraction

## Next Steps

1. **Run the Test**: Execute the Turkish sports news test to validate setup
2. **Explore Examples**: Check the `examples/` directory for more use cases
3. **Read Documentation**: Review files in `docs/` for detailed API reference
4. **Customize Configuration**: Modify test parameters for different scenarios

## Troubleshooting

### Common Issues
- **Import Errors**: Ensure the virtual environment is activated
- **Network Issues**: Check internet connectivity and website accessibility
- **Dependency Issues**: Verify all requirements are installed correctly

### Debug Information
The test script includes comprehensive error reporting with:
- Exception type and message
- Full stack trace for debugging
- Processing metrics for performance analysis

---

*This guide was generated during the initial setup and testing of the journalist library for Turkish sports news extraction.*
