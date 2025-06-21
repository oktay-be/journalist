# feat!: Refactor to source-specific session data with process_articles() extraction

## Summary
Refactored the journalist system to return source-specific session data instead of unified session data, enabling per-source analysis and better data organization.

## Key Changes

### Core Architecture
- **Major `Journalist` class refactoring** - extracted 60+ lines of article processing logic from `read()` method into new `process_articles()` method
- **Single responsibility principle** - `read()` now focuses on orchestration, `process_articles()` handles all article processing
- **Source-specific session files** - replaces single `session_data.json` with `session_data_<domain>.json` files  
- **Consistent return format** - same data structure regardless of persist mode

### File Changes
- `src/journalist/journalist.py` - Added `process_articles()` and `_group_articles_by_source()` methods
- `src/journalist/core/file_manager.py` - Added source-specific session data methods
- `src/journalist/core/web_scraper.py` - Added `create_source_session_data()` method

### Return Value
**Before:**
```python
{
  'articles': [...],
  'session_metadata': {...}
}
```

**After:**
```python
[
  {
    'source_domain': 'www.fanatik.com.tr',
    'source_url': 'https://www.fanatik.com.tr', 
    'articles': [...],
    'articles_count': 5
  },
  {
    'source_domain': 'www.ntvspor.net',
    'source_url': 'https://www.ntvspor.net',
    'articles': [...], 
    'articles_count': 3
  }
]
```

## Benefits
- **Better code organization** - `process_articles()` method separates concerns and improves maintainability
- **Source isolation** - separate analysis per news source
- **Better file organization** - one session file per source domain
- **Consistent behavior** - same output for persist=True/False
- **Cleaner architecture** - single responsibility principle enforced

## Breaking Changes
- ⚠️ **Return format changed** - no backward compatibility maintained
- **File structure** - session data now split by source

## Testing
- Works with both `persist=True` and `persist=False`
- Tested with Turkish sports news sources
- Maintains individual article saving functionality
