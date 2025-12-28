# API Reference

This document provides detailed information about the Journalist library's API.

## Core Classes

### Journalist

The main class for content extraction operations.

```python
from journalist import Journalist

# Initialize with persistence (default)
journalist = Journalist(persist=True, scrape_depth=1)

# Initialize for memory-only operation
journalist = Journalist(persist=False, scrape_depth=2)
```

#### Constructor Parameters

- **persist** (bool, default=True): If True, creates filesystem workspace and saves data. If False, operates in memory only.
- **scrape_depth** (int, default=1): Depth level for link discovery during scraping.

#### Methods

##### async read(urls, keywords=None)

Extract content from the provided URLs with optional keyword filtering.

**Parameters:**

- **urls** (List[str]): List of website URLs to process
- **keywords** (Optional[List[str]]): Optional list of keywords for relevance filtering

**Returns:**

- Dict containing extracted articles and metadata

**Example:**

```python
import asyncio
from journalist import Journalist

async def main():
    journalist = Journalist(persist=True)

    urls = ["https://www.example-news.com"]
    keywords = ["technology", "innovation"]

    result = await journalist.read(urls=urls, keywords=keywords)

    print(f"Found {len(result['articles'])} articles")
    for article in result['articles']:
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")

# Run the async function
asyncio.run(main())
```

#### Properties

- **session_id** (str): Unique session identifier
- **persist** (bool): Whether persistence is enabled
- **scrape_depth** (int): Current scrape depth setting
- **session_path** (str): Path to session directory (if persist=True)
- **memory_articles** (list): In-memory article storage (if persist=False)

## Configuration

### JournalistConfig

Central configuration class for the library.

```python
from journalist.config import JournalistConfig

# Get default workspace path
workspace_path = JournalistConfig.get_base_workspace_path()
```

#### Methods

##### get_base_workspace_path()

Returns the base workspace path for file operations.

**Returns:**

- str: Base workspace path (default: ".journalist_workspace")

## Exceptions

### JournalistException

Base exception class for all journalist-related errors.

```python
from journalist.exceptions import JournalistException
```

### NetworkException

Raised when network-related errors occur during scraping.

```python
from journalist.exceptions import NetworkException
```

### ExtractionException

Raised when content extraction fails.

```python
from journalist.exceptions import ExtractionException
```

### ConfigurationException

Raised when configuration is invalid or missing.

```python
from journalist.exceptions import ConfigurationException
```

## Return Data Structures

### Article Structure

Each article returned by the `read()` method contains:

```python
{
    'id': 'unique_article_id',
    'url': 'https://example.com/article',
    'title': 'Article Title',
    'content': 'Extracted article content...',
    'author': 'Author Name',
    'published_date': '2025-06-17T10:30:00',
    'scraped_at': '2025-06-17T10:35:00',
    'keywords_matched': ['keyword1', 'keyword2'],
    'metadata': {
        'extraction_method': 'readability',
        'language': 'tr',
        'word_count': 450
    }
}
```

### Result Structure

The `read()` method returns:

```python
{
    'articles': [
        # List of article dictionaries
    ],
    'session_id': 'session_identifier',
    'extraction_summary': {
        'session_id': 'session_identifier',
        'urls_requested': 1,
        'urls_processed': 1,
        'articles_extracted': 5,
        'extraction_time_seconds': 12.34,
        'keywords_used': ['keyword1', 'keyword2']
    }
}
```

## Usage Patterns

### Memory-Only Operation

For lightweight operations without file persistence:

```python
journalist = Journalist(persist=False)
result = await journalist.read(urls=urls)
# Articles are stored in journalist.memory_articles
```

### Persistent Operation

For operations that need file storage:

```python
journalist = Journalist(persist=True)
result = await journalist.read(urls=urls)
# Articles are saved to filesystem in session directory
```

### Concurrent Operations

Multiple journalist instances can run simultaneously:

```python
async def concurrent_scraping():
    journalist1 = Journalist(persist=True)
    journalist2 = Journalist(persist=True)

    task1 = asyncio.create_task(journalist1.read(urls1))
    task2 = asyncio.create_task(journalist2.read(urls2))

    results = await asyncio.gather(task1, task2)
    return results
```

## Performance Considerations

- Use `persist=False` for memory-only operations when file storage is not needed
- Higher `scrape_depth` values increase processing time but may find more content
- Concurrent operations are supported but monitor resource usage
- Consider using keyword filtering to reduce processing overhead

## Error Handling

Always wrap async operations in try-catch blocks:

```python
try:
    result = await journalist.read(urls=urls)
except NetworkException as e:
    print(f"Network error: {e}")
except ExtractionException as e:
    print(f"Extraction error: {e}")
except JournalistException as e:
    print(f"General journalist error: {e}")
```
