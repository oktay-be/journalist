# Quick Start Guide

This guide will get you up and running with Journalist in minutes.

## Basic Usage

### 1. Simple Article Extraction

```python
import asyncio
from journalist import Journalist

async def simple_example():
    # Create a journalist instance
    journalist = Journalist()

    # Extract articles from a news site
    result = await journalist.read(
        urls=["https://www.bbc.com/news"]
    )

    # Print results
    print(f"Found {len(result['articles'])} articles")
    for article in result['articles']:
        print(f"- {article['title']}")

asyncio.run(simple_example())
```

### 2. Keyword-Filtered Extraction

```python
import asyncio
from journalist import Journalist

async def keyword_example():
    journalist = Journalist(persist=True, scrape_depth=1)    result = await journalist.read(
        urls=[
            "https://www.reuters.com/",
            "https://www.cnn.com/"
        ],
        keywords=["technology", "sports", "economy"]
    )

    for article in result['articles']:
        print(f"Title: {article['title']}")
        print(f"Keywords found: {article.get('keywords_found', [])}")
        print(f"URL: {article['url']}")
        print("-" * 50)

asyncio.run(keyword_example())
```

### 3. Memory-Only Mode (Fast & Temporary)

```python
import asyncio
from journalist import Journalist

async def memory_mode_example():
    # Use memory-only mode - no files created
    journalist = Journalist(persist=False)

    result = await journalist.read(        urls=["https://www.bbc.com/news"],
        keywords=["breaking", "news"]
    )

    print(f"Session: {result['session_id']}")
    print(f"Articles: {len(result['articles'])}")
    print(f"Time taken: {result['extraction_summary']['extraction_time_seconds']}s")

asyncio.run(memory_mode_example())
```

## Understanding the Response

The `read()` method returns a dictionary with this structure:

```python
{
    'articles': [
        {
            'title': 'Article Title',
            'url': 'https://example.com/article',
            'content': 'Full article content...',
            'author': 'Author Name',
            'published_date': '2025-06-17',
            'keywords_found': ['teknologi', 'yazılım']
        }
    ],
    'session_id': '20250617_143052_123456',
    'extraction_summary': {
        'session_id': '20250617_143052_123456',
        'urls_requested': 2,
        'urls_processed': 2,
        'articles_extracted': 5,
        'extraction_time_seconds': 3.45,
        'keywords_used': ['teknologi', 'spor']
    }
}
```

## Configuration Options

### Journalist Parameters

```python
# Full configuration example
journalist = Journalist(
    persist=True,      # Enable file persistence (default: True)
    scrape_depth=2     # Link discovery depth (default: 1)
)
```

### Persistence Modes

#### Persistent Mode (Default)

```python
journalist = Journalist(persist=True)
# Creates session folders under .journalist_workspace/
# Saves articles as JSON files
# Useful for: long-term storage, analysis, debugging
```

#### Memory-Only Mode

```python
journalist = Journalist(persist=False)
# No files created
# Articles stored in memory only
# Useful for: temporary scraping, testing, CI/CD
```

## Error Handling

```python
import asyncio
from journalist import Journalist
from journalist.exceptions import NetworkError, ExtractionError

async def robust_example():
    try:
        journalist = Journalist()
        result = await journalist.read(
            urls=["https://example-news.com/"],
            keywords=["news"]
        )
        return result

    except NetworkError as e:
        print(f"Network issue: {e}")
        if hasattr(e, 'status_code'):
            print(f"HTTP Status: {e.status_code}")

    except ExtractionError as e:
        print(f"Extraction failed: {e}")
        if hasattr(e, 'url'):
            print(f"Problem URL: {e.url}")

    except Exception as e:
        print(f"Unexpected error: {e}")

asyncio.run(robust_example())
```

## Common Patterns

### 1. Concurrent Scraping

```python
import asyncio
from journalist import Journalist

async def concurrent_scraping():
    # Create separate journalists for different topics
    sports_journalist = Journalist(persist=True, scrape_depth=2)
    tech_journalist = Journalist(persist=True, scrape_depth=1)

    # Create concurrent tasks
    sports_task = asyncio.create_task(
        sports_journalist.read(
            urls=["https://www.espn.com/"],
            keywords=["futbol", "basketbol"]
        )
    )

    tech_task = asyncio.create_task(
        tech_journalist.read(
            urls=["https://www.techcrunch.com/"],
            keywords=["teknologi", "donanım"]
        )
    )

    # Wait for both to complete
    sports_result, tech_result = await asyncio.gather(sports_task, tech_task)

    print(f"Sports: {len(sports_result['articles'])} articles")
    print(f"Tech: {len(tech_result['articles'])} articles")

asyncio.run(concurrent_scraping())
```

### 2. Batch Processing

```python
import asyncio
from journalist import Journalist

async def batch_process_sites():
    sites = [        "https://www.bbc.com/news",
        "https://www.reuters.com/",
        "https://www.cnn.com/",
        "https://www.techcrunch.com/"
    ]

    journalist = Journalist(persist=True)

    # Process in batches of 2
    batch_size = 2
    all_articles = []

    for i in range(0, len(sites), batch_size):
        batch = sites[i:i+batch_size]
        print(f"Processing batch: {batch}")

        result = await journalist.read(
            urls=batch,
            keywords=["important", "breaking"]
        )

        all_articles.extend(result['articles'])
        print(f"Batch completed: {len(result['articles'])} articles")

    print(f"Total articles: {len(all_articles)}")

asyncio.run(batch_process_sites())
```

## Next Steps

- Explore [Configuration Options](configuration.md)
- Learn about [Error Handling](error-handling.md)
- Check out more [Examples](examples.md)
- Read the [API Reference](api-reference.md)
