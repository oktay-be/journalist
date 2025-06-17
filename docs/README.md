# Journalist Documentation

Welcome to the Journalist library documentation - a powerful async news content extraction library.

## Table of Contents

- [Installation Guide](installation.md)
- [Quick Start Guide](quickstart.md)
- [API Reference](api-reference.md)
- [Configuration](configuration.md)
- [Error Handling](error-handling.md)
- [Examples](examples.md)
- [Contributing](contributing.md)
- [Changelog](changelog.md)

## Overview

Journalist is designed to extract content from news websites efficiently using modern async Python patterns. It provides both memory-only and filesystem persistence modes, making it suitable for various use cases from quick scraping to enterprise-level news aggregation.

## Key Features

- **Async/Await Support**: Built with asyncio for high-performance concurrent operations
- **Universal News Support**: Works with news websites from any language or region
- **Multiple Extraction Methods**: Readability, CSS selectors, JSON-LD, and more
- **Flexible Persistence**: Choose between memory-only or filesystem persistence
- **Session Management**: Built-in session tracking with race condition protection
- **Error Handling**: Comprehensive custom exception types
- **Well Tested**: High test coverage with unit and integration tests

## Quick Example

```python
import asyncio
from journalist import Journalist

async def main():
    journalist = Journalist(persist=True, scrape_depth=1)

    result = await journalist.read(
        urls=["https://www.bbc.com/news"],
        keywords=["teknologi", "spor"]
    )

    print(f"Found {len(result['articles'])} articles")

asyncio.run(main())
```

## Getting Help

- **Documentation**: Browse the guides in this docs folder
- **Examples**: Check the [examples](examples.md) for common usage patterns
- **Issues**: Report bugs or request features on GitHub
- **Email**: Contact the author at oktay.burak.ertas@gmail.com

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
