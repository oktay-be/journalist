# Configuration Guide

This guide covers how to configure the Journalist library for different use cases.

## Basic Configuration

### Default Settings

The Journalist library works out of the box with sensible defaults:

- **Default Workspace Path**: `.journalist_workspace`
- **Default Persistence**: `True` (files are saved)
- **Default Scrape Depth**: `1` (only initial URLs)

### Initialization Options

```python
from journalist import Journalist

# Default configuration
journalist = Journalist()

# Custom configuration
journalist = Journalist(
    persist=True,          # Enable/disable file persistence
    scrape_depth=2         # Set link discovery depth
)
```

## Persistence Modes

### Filesystem Persistence (persist=True)

When persistence is enabled, the library creates a workspace structure:

```
.journalist_workspace/
└── 20250617_143055_123456/  # Session ID
    ├── articles/            # Individual article files
    │   ├── article_abc123.json
    │   └── article_def456.json
    └── session_data.json    # Session metadata
```

**Use cases:**

- Long-term storage of scraped content
- Audit trails and data analysis
- Batch processing workflows
- Content archiving

**Configuration:**

```python
journalist = Journalist(persist=True)
```

### Memory-Only Mode (persist=False)

When persistence is disabled, all data is kept in memory only:

**Use cases:**

- Real-time processing
- Temporary analysis
- Resource-constrained environments
- Quick content checks

**Configuration:**

```python
journalist = Journalist(persist=False)

# Access articles from memory
articles = journalist.memory_articles
```

## Scrape Depth Configuration

The `scrape_depth` parameter controls how deep the link discovery goes:

### Depth Level 1 (Default)

- Only processes the initially provided URLs
- Fastest processing time
- Lowest resource usage

```python
journalist = Journalist(scrape_depth=1)
```

### Depth Level 2+

- Discovers and processes links found on initial pages
- Increased processing time and resource usage
- More comprehensive content discovery

```python
journalist = Journalist(scrape_depth=2)  # Process links found on initial pages
journalist = Journalist(scrape_depth=3)  # Go one level deeper
```

## Workspace Configuration

### Custom Workspace Path

You can modify the default workspace path by updating the configuration:

```python
from journalist.config import JournalistConfig

# Get current workspace path
current_path = JournalistConfig.get_base_workspace_path()
print(f"Current workspace: {current_path}")

# Note: Currently, workspace path is read-only
# Future versions may support custom paths
```

### Session Management

Each Journalist instance creates a unique session:

```python
journalist = Journalist()
print(f"Session ID: {journalist.session_id}")
print(f"Session Path: {journalist.session_path}")
```

Session IDs follow the format: `YYYYMMDD_HHMMSS_microseconds`

## Environment-Specific Configurations

### Development Environment

For development and testing:

```python
# Fast, memory-only processing
journalist = Journalist(
    persist=False,     # No file I/O
    scrape_depth=1     # Minimal processing
)
```

### Production Environment

For production data collection:

```python
# Persistent, comprehensive processing
journalist = Journalist(
    persist=True,      # Save all data
    scrape_depth=2     # Discover additional content
)
```

### CI/CD Environment

For automated testing:

```python
# Deterministic, lightweight processing
journalist = Journalist(
    persist=False,     # No filesystem dependencies
    scrape_depth=1     # Predictable execution time
)
```

## Keyword Configuration

Configure keyword filtering for content relevance:

```python
# Define keywords for filtering
keywords = [    "technology",     # English for technology
    "ai",             # English for AI
    "innovation",     # English terms also supported
    "startup"
]

# Use keywords in read operation
result = await journalist.read(
    urls=urls,
    keywords=keywords
)
```

## Performance Tuning

### Memory Usage

For memory-constrained environments:

```python
# Minimize memory usage
journalist = Journalist(
    persist=True,      # Offload data to filesystem
    scrape_depth=1     # Reduce processing load
)
```

### Processing Speed

For faster processing:

```python
# Optimize for speed
journalist = Journalist(
    persist=False,     # Skip file I/O
    scrape_depth=1     # Minimal link discovery
)

# Use fewer keywords for faster filtering
keywords = ["main_keyword"]  # Instead of many keywords
```

### Concurrent Operations

For high-throughput scenarios:

```python
async def concurrent_processing():
    # Create multiple instances for parallel processing
    journalists = [
        Journalist(persist=True, scrape_depth=1)
        for _ in range(3)
    ]

    # Distribute URLs across instances
    tasks = [
        journalist.read(urls=url_batch)
        for journalist, url_batch in zip(journalists, url_batches)
    ]

    results = await asyncio.gather(*tasks)
    return results
```

## Error Handling Configuration

Configure error handling strategies:

```python
import logging
from journalist.exceptions import NetworkException, ExtractionException

# Configure logging
logging.basicConfig(level=logging.INFO)

async def robust_scraping():
    journalist = Journalist(persist=True)

    try:
        result = await journalist.read(urls=urls)
        return result
    except NetworkException as e:
        # Handle network issues
        logging.error(f"Network error: {e}")
        return None
    except ExtractionException as e:
        # Handle extraction issues
        logging.warning(f"Extraction error: {e}")
        return None
```

## Best Practices

### 1. Choose Appropriate Persistence Mode

- Use `persist=True` for production data collection
- Use `persist=False` for quick analysis or testing

### 2. Set Reasonable Scrape Depth

- Start with `scrape_depth=1` and increase if needed
- Monitor resource usage with higher depths

### 3. Use Keyword Filtering

- Define specific keywords to improve relevance
- Use appropriate keywords for your target language content

### 4. Handle Errors Gracefully

- Always wrap async operations in try-catch blocks
- Log errors for debugging

### 5. Monitor Resource Usage

- Check memory usage with large datasets
- Monitor filesystem space when using persistence

## Migration Guide

### From Older Versions

If migrating from older versions of the library:

```python
# Old API (deprecated)
# journalist = Journalist(disable_cache=False)

# New API
journalist = Journalist(persist=True)
```

The `persist` parameter replaces the old `disable_cache` parameter with inverted logic:

- `disable_cache=False` → `persist=True`
- `disable_cache=True` → `persist=False`
