# Configuration Management

The Journalist library now uses **flexible, external configuration** with no hard-coded URLs or values.

## 🎯 **Configuration Methods**

### 1. **External JSON File** (Recommended)

Create a `selectors.json` file:

```json
{
  "example.com": {
    "title_selector": "h1.article-title",
    "content_selector": ".article-body",
    "date_selector": ".publish-date",
    "author_selector": ".author-name"
  }
}
```

**Usage:**

```python
# Automatic loading (searches for selectors.json in current directory)
config = ScrapingConfig()

# Or specify custom file path
config = ScrapingConfig(config_file="/path/to/my-selectors.json")
```

### 2. **Environment Variables**

Set configuration via environment variables:

```bash
export JOURNALIST_TIMEOUT=10
export JOURNALIST_MAX_RETRIES=5
export JOURNALIST_MIN_BODY_LENGTH=100
```

### 3. **Dynamic Configuration**

Add selectors programmatically:

```python
config = ScrapingConfig()

# Add new site selectors
config.add_site_selectors("newsite.com", {
    "title_selector": "h1.title",
    "content_selector": ".content"
})

# Remove site selectors
config.remove_site_selectors("oldsite.com")
```

## 📁 **File Locations**

The system searches for `selectors.json` in this order:

1. **Current working directory**: `./selectors.json`
2. **Config directory**: `./src/journalist/core/selectors.json`
3. **User home directory**: `~/.journalist/selectors.json`
4. **Custom path**: Via `config_file` parameter

## ⚙️ **Configuration Values**

All configuration values are defined directly in `src/journalist/core/config.py`. You can modify these values by editing the configuration class:

| Setting                     | Default Value  | Description                  |
| --------------------------- | -------------- | ---------------------------- |
| `user_agent`                | Chrome/91.0... | HTTP User Agent string       |
| `request_timeout`           | 5              | Request timeout (seconds)    |
| `http_timeout`              | 5              | HTTP timeout (seconds)       |
| `max_retries`               | 3              | Maximum retry attempts       |
| `min_body_length`           | 50             | Minimum article body length  |
| `min_title_length`          | 10             | Minimum article title length |
| `high_quality_body_length`  | 500            | High quality body threshold  |
| `high_quality_title_length` | 15             | High quality title threshold |

### 📝 **Modifying Configuration**

To change these values, edit `src/journalist/core/config.py`:

```python
class ScrapingConfig:
    def __init__(self, config_file: Optional[str] = None):
        # Modify these values as needed
        self.user_agent = "Your Custom User Agent"
        self.request_timeout = 10  # Increase timeout
        self.min_body_length = 100  # Require longer articles
        # ... other settings
```

## 🚀 **Quick Start**

1. **Create your selectors file (optional):**

   ```json
   {
     "your-news-site.com": {
       "title_selector": "h1.headline",
       "content_selector": ".story-body"
     }
   }
   ```

2. **Modify configuration if needed:**

   Edit `src/journalist/core/config.py`:

   ```python
   class ScrapingConfig:
       def __init__(self, config_file: Optional[str] = None):
           self.request_timeout = 10  # Increase timeout
           self.max_retries = 5      # More retries
           # ... other settings
   ```

3. **Use in code:**

   ```python
   from journalist.core.config import ScrapingConfig

   config = ScrapingConfig()  # Automatically loads external selectors
   ```

## ✅ **Benefits**

- ✅ **No hard-coded values** in source code
- ✅ **Easy to customize** by editing config.py
- ✅ **Version control friendly** (track all configuration in git)
- ✅ **Simple configuration** without environment complexity
- ✅ **Runtime flexibility** with dynamic methods
- ✅ **Backward compatible** (falls back to generic selectors)

## 🔧 **For Developers**

To add support for a new site:

1. **Create selectors** in `selectors.json`
2. **Test the selectors** with your scraper
3. **Share the configuration** (not hard-coded in source)

No more code changes needed for new sites! 🎉
