# Session Data Segregation Refactoring Plan

## Overview
This refactoring will segregate session data by source domain/hostname instead of having one unified `session_data.json` file. Each source will have its own session data file, and the system will return a list of these JSON files.

## Current Architecture Analysis

### Current Session Data Structure
- **Location**: `{session_path}/session_data.json`
- **Content Structure**:
  ```json
  {
    "saved_at": "2025-06-21T...",
    "articles_count": 10,
    "articles": [...],
    "session_metadata": {
      "session_id": "...",
      "start_time": "...",
      "end_time": "...",
      "duration_seconds": 123.45,
      "links_discovered": 25,
      "articles_scraped": 10,
      "success_rate": 0.4,
      "scraper_version": "modular-v1.0"
    }
  }
  ```

### Current File Structure
```
.journalist_workspace/
└── {session_id}/
    ├── articles/
    │   ├── article_abc123.json
    │   └── article_def456.json
    └── session_data.json  ← Current unified file
```

## Proposed New Architecture

### New Session Data Structure
```
.journalist_workspace/
└── {session_id}/
    ├── articles/
    │   ├── article_abc123.json
    │   └── article_def456.json
    ├── session_data_www_fanatik_com_tr.json
    ├── session_data_www_fotomac_com_tr.json
    └── session_data_www_ntvspor_net.json
```

### New Session Data File Content
Each source-specific session data file will contain:
```json
{
  "source_domain": "www.fanatik.com.tr",
  "source_url": "https://www.fanatik.com.tr",
  "saved_at": "2025-06-21T...",
  "articles_count": 5,
  "articles": [...],  // Only articles from this source
  "session_metadata": {
    "session_id": "...",
    "source_specific": true,
    "start_time": "...",
    "end_time": "...",
    "duration_seconds": 67.89,
    "links_discovered": 12,
    "articles_scraped": 5,
    "success_rate": 0.42,
    "scraper_version": "modular-v1.1"
  }
}
```

## Files to Modify

### 1. Core Files

#### 1.1 `src/journalist/core/file_manager.py`
**Changes needed:**
- Add method `save_source_specific_session_data(domain: str, session_data: dict)`
- Add method `load_source_specific_session_data(domain: str) -> dict`
- Add method `list_source_session_files() -> List[str]`
- Add method `get_source_session_filename(domain: str) -> str`
- Add utility method `sanitize_domain_for_filename(domain: str) -> str`

**New methods to implement:**
```python
def sanitize_domain_for_filename(self, domain: str) -> str:
    """Convert domain to safe filename format"""
    # www.fanatik.com.tr -> www_fanatik_com_tr
    
def get_source_session_filename(self, domain: str) -> str:
    """Generate session filename for specific domain"""
    # Returns: session_data_www_fanatik_com_tr.json
    
def save_source_specific_session_data(self, domain: str, session_data: dict) -> bool:
    """Save session data for specific source domain"""
    
def load_source_specific_session_data(self, domain: str) -> Optional[dict]:
    """Load session data for specific source domain"""
    
def list_source_session_files(self) -> List[str]:
    """List all source-specific session data files"""
    
def load_all_source_session_data(self) -> List[dict]:
    """Load all source session data files and return as list"""
```

#### 1.2 `src/journalist/core/web_scraper.py`
**Changes needed:**
- Modify `execute_scraping_for_session()` to group articles by source domain
- Return source-segregated data instead of unified session_data
- Add source domain extraction logic

**New method structure:**
```python
async def execute_scraping_for_session(self, session_id: str, keywords: List[str], 
                                     sites: Optional[List[str]] = None, scrape_depth: int = 1) -> Dict[str, Any]:
    # ... existing logic ...
    
    # NEW: Group articles by source domain
    articles_by_source = self._group_articles_by_source(scraped_articles, sites or [])
    
    # NEW: Create source-specific session data
    source_session_data = {}
    for domain, articles in articles_by_source.items():
        source_session_data[domain] = {
            'source_domain': domain,
            'source_url': self._get_original_url_for_domain(domain, sites or []),
            'articles': articles,
            'session_metadata': self._create_source_session_metadata(
                session_id, session_start, domain, articles
            )
        }
    
    return {
        'source_session_data': source_session_data,
        'unified_articles': scraped_articles,  # For backward compatibility
        'session_metadata': self._create_session_metadata(session_id, session_start, len(processed_links), len(scraped_articles))
    }
```

**New helper methods to add:**
```python
def _group_articles_by_source(self, articles: List[dict], original_urls: List[str]) -> Dict[str, List[dict]]:
    """Group articles by their source domain"""
    
def _get_original_url_for_domain(self, domain: str, original_urls: List[str]) -> str:
    """Get the original URL that corresponds to a domain"""
    
def _create_source_session_metadata(self, session_id: str, start_time: datetime, 
                                   domain: str, articles: List[dict]) -> dict:
    """Create session metadata for a specific source"""
```

#### 1.3 `src/journalist/journalist.py`
**Changes needed:**
- Modify the session data saving logic in the `read()` method
- Instead of saving unified `session_data.json`, save multiple source-specific files
- Update the return structure to include source-specific data

**Key changes in `read()` method:**
```python
# OLD CODE (around line 242):
session_file = os.path.join(self.file_manager.base_data_dir, "session_data.json")
session_payload = {
    'saved_at': datetime.now().isoformat(),
    'articles_count': len(filtered_articles),
    **filtered_result
}
self.file_manager.save_json_data(session_file, session_payload, data_type="session")

# NEW CODE:
if self.persist:
    # Save source-specific session data
    source_session_data = result.get('source_session_data', {})
    saved_source_files = []
    
    for domain, source_data in source_session_data.items():
        # Filter articles by date for this source
        source_articles = source_data.get('articles', [])
        filtered_source_articles = self._filter_articles_by_date(source_articles)
        
        # Update source data with filtered articles
        source_data_filtered = source_data.copy()
        source_data_filtered['articles'] = filtered_source_articles
        source_data_filtered['saved_at'] = datetime.now().isoformat()
        source_data_filtered['articles_count'] = len(filtered_source_articles)
        
        # Save source-specific session data
        success = self.file_manager.save_source_specific_session_data(domain, source_data_filtered)
        if success:
            filename = self.file_manager.get_source_session_filename(domain)
            saved_source_files.append(filename)
```

### 2. Utility Functions

#### 2.1 New utility in `src/journalist/core/network_utils.py`
**Add domain extraction helper:**
```python
def extract_domain_from_url(url: str) -> str:
    """Extract clean domain name for filename purposes"""
    # https://www.fanatik.com.tr -> www.fanatik.com.tr
    
def sanitize_domain_for_filename(domain: str) -> str:
    """Convert domain to filename-safe format"""
    # www.fanatik.com.tr -> www_fanatik_com_tr
```

### 3. Return Value Changes

#### 3.1 Updated Return Structure
The `journalist.read()` method will return:
```python
{
    'articles': [...],  # All articles (for backward compatibility)
    'source_session_files': [
        'session_data_www_fanatik_com_tr.json',
        'session_data_www_fotomac_com_tr.json'
    ],
    'source_session_data': {
        'www.fanatik.com.tr': { ... },
        'www.fotomac.com.tr': { ... }
    },
    'extraction_summary': {
        'urls_processed': 2,
        'articles_extracted': 10,
        'sources_processed': 2,
        'extraction_time_seconds': 45.67
    }
}
```

## Implementation Steps

### Phase 1: Core Infrastructure
1. **Add domain utilities** to `network_utils.py`
2. **Extend FileManager** with source-specific methods
3. **Create unit tests** for new FileManager methods

### Phase 2: Web Scraper Updates
1. **Modify WebScraper** to group articles by source
2. **Update session metadata creation** for source-specific data
3. **Test with multiple sources**

### Phase 3: Journalist Class Updates
1. **Update Journalist.read()** method to handle source-specific saving
2. **Modify return structure** to include source information
3. **Ensure backward compatibility** with existing API

### Phase 4: Testing & Documentation
1. **Update test scripts** (especially `test_turkish_sports.py`)
2. **Update documentation** to reflect new structure
3. **Add examples** showing source-specific data access

## Backward Compatibility

### Maintaining Compatibility
- Keep existing `articles` field in return value
- Add new fields without breaking existing consumers
- Provide method to get unified session data if needed

### Migration Path
- Old code will continue to work with the `articles` field
- New code can access source-specific data via new fields
- Add utility method to convert source-specific data back to unified format

## Benefits

### Advantages of This Approach
1. **Source Isolation**: Each news source's data is stored separately
2. **Better Organization**: Easier to analyze performance per source
3. **Scalability**: Can handle many sources without massive single files
4. **Debugging**: Easier to identify issues with specific sources
5. **Flexibility**: Can process sources independently

### Use Cases Enabled
1. **Source-specific analysis**: Performance metrics per news site
2. **Selective reprocessing**: Re-run only failed sources
3. **Source comparison**: Compare article quality across sources
4. **Incremental processing**: Process new sources without affecting existing data

## Files to Create/Modify Summary

### New Files
- None (all changes in existing files)

### Modified Files
1. `src/journalist/core/file_manager.py` - Add source-specific session methods
2. `src/journalist/core/web_scraper.py` - Add source grouping logic
3. `src/journalist/journalist.py` - Update session saving and return structure
4. `src/journalist/core/network_utils.py` - Add domain utilities
5. `test_turkish_sports.py` - Update to demonstrate new functionality
6. Documentation files in `docs/` - Update API reference

### Test Files to Update
1. `tests/unit/test_journalist.py` - Add tests for source-specific functionality
2. `tests/unit/test_config.py` - Update configuration tests if needed
3. Add new test file `tests/unit/test_source_segregation.py`

## Risk Assessment

### Low Risk
- All changes are additive to existing functionality
- Backward compatibility maintained
- Existing tests should continue to pass

### Medium Risk
- File system structure changes (but in isolated session directories)
- Return value structure changes (but backward compatible)

### Mitigation Strategies
- Comprehensive testing with multiple sources
- Gradual rollout starting with non-persistent mode
- Fallback to unified format if source-specific fails

---

*This plan ensures a clean separation of session data by source while maintaining full backward compatibility and providing enhanced functionality for source-specific analysis.*
