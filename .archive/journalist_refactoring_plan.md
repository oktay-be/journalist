# Journalist.py Refactoring Plan - Article Processing Extraction

## Overview
Extract the article processing logic (starting from line 211) into a separate `process_articles` method that handles both persistence modes and creates source-specific session data files.

## Current State Analysis

### Current Code Structure (Lines 211-289)
The current code in the `read()` method handles:
1. Processing task results from web scraping
2. Filtering articles by date 
3. Saving individual articles to files (if persist=True)
4. Saving unified session data to `session_data.json` (if persist=True)
5. Storing articles in memory (if persist=False)
6. Preparing final result structure

### Problems with Current Structure
1. **Single Responsibility Violation**: The `read()` method is doing too much
2. **Unified Session Data**: Only one `session_data.json` file regardless of source
3. **Code Duplication**: Similar logic for persist=True and persist=False cases
4. **Inconsistent Return Data**: Different data structures depending on persistence mode

## Proposed Refactoring

### New Method: `process_articles`

#### Method Signature
```python
def process_articles(
    self, 
    scraped_articles: List[Dict[str, Any]], 
    original_urls: List[str],
    session_metadata: Dict[str, Any]
) -> List[Dict[str, Any]]:
```

#### Parameters
- `scraped_articles`: Raw articles from web scraper
- `original_urls`: Original URLs provided by user for source identification
- `session_metadata`: Metadata from scraping session

#### Return Value
- **Always returns the same structure regardless of persist mode**
- List of source-specific session data dictionaries (content of session_data_<url_sanitized>.json files)

### Implementation Plan

#### Step 1: Extract Domain Utility Functions
```python
def _sanitize_url_for_filename(self, url: str) -> str:
    """Convert URL to filename-safe string"""
    # Remove protocol, replace special chars with underscores
    # Example: https://www.fanatik.com.tr -> www_fanatik_com_tr
    
def _extract_domain_from_url(self, url: str) -> str:
    """Extract domain from URL"""
    # Example: https://www.fanatik.com.tr/path -> www.fanatik.com.tr
```

#### Step 2: Article Grouping Logic
```python
def _group_articles_by_source(self, articles: List[Dict], original_urls: List[str]) -> Dict[str, Dict]:
    """Group articles by source URL and create source-specific data"""
    # Returns: {
    #   'www.fanatik.com.tr': {
    #     'source_url': 'https://www.fanatik.com.tr',
    #     'source_domain': 'www.fanatik.com.tr', 
    #     'articles': [...],
    #     'articles_count': 5
    #   }
    # }
```

#### Step 3: Source Session Data Creation
```python
def _create_source_session_data(self, grouped_articles: Dict, session_metadata: Dict) -> List[Dict]:
    """Create source-specific session data structures"""
    # Creates the final data structure that will be:
    # 1. Saved as session_data_<url_sanitized>.json files (if persist=True)
    # 2. Returned regardless of persistence mode
```

#### Step 4: Main Process Articles Method
```python
def process_articles(
    self, 
    scraped_articles: List[Dict[str, Any]], 
    original_urls: List[str],
    session_metadata: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Process articles with filtering, saving, and source segregation.
    
    Always returns the same data structure regardless of persistence mode.
    """
    # 1. Filter articles by date
    filtered_articles = self._filter_articles_by_date(scraped_articles)
    
    # 2. Group articles by source
    grouped_articles = self._group_articles_by_source(filtered_articles, original_urls)
    
    # 3. Create source-specific session data
    source_session_data_list = self._create_source_session_data(grouped_articles, session_metadata)
    
    # 4. Handle persistence (if enabled)
    if self.persist and self.file_manager:
        # Save individual articles
        self._save_individual_articles(filtered_articles)
        
        # Save source-specific session data files
        self._save_source_session_files(source_session_data_list)
    else:
        # Store in memory for non-persistent mode
        self.memory_articles.extend(filtered_articles)
    
    # 5. Always return the same structure
    return source_session_data_list
```

#### Step 5: Supporting Methods
```python
def _save_individual_articles(self, articles: List[Dict]) -> None:
    """Save individual articles to files"""
    # Extract current article saving logic
    
def _save_source_session_files(self, source_session_data_list: List[Dict]) -> None:
    """Save source-specific session data files"""
    # For each source in source_session_data_list:
    #   - Generate filename: session_data_<sanitized_url>.json  
    #   - Save using file_manager.save_json_data()
```

### Updated read() Method Structure

#### Before (Lines 211-289)
```python
# Process results based on task type
for i, (task_type, _) in enumerate(tasks):
    # ... 60+ lines of processing logic
    
# Prepare final result
result = {
    'articles': articles,
    # ... rest of result
}
```

#### After
```python
# Process results based on task type  
for i, (task_type, _) in enumerate(tasks):
    result = results[i]
    
    if isinstance(result, Exception):
        logger.error("Session [%s]: Error in %s task: %s", session_id, task_type, result, exc_info=True)
    else:
        if task_type == 'web_scrape' and result and isinstance(result, dict):
            # Extract data from scraper result
            scraped_articles = result.get('articles', [])
            session_metadata = result.get('session_metadata', {})
            
            # Process articles through new method
            source_session_data_list = self.process_articles(
                scraped_articles=scraped_articles,
                original_urls=scrape_urls_for_session, 
                session_metadata=session_metadata
            )
            
            articles.extend(source_session_data_list)

# Prepare final result with source-specific data
result = {
    'source_session_data': source_session_data_list,
    'session_id': session_id,
    'extraction_summary': {
        # ... existing fields
        'sources_processed': len(source_session_data_list)
    }
}
```

## File Structure Changes

### Current Structure
```
session_folder/
├── articles/
│   ├── article_1.json
│   └── article_2.json  
└── session_data.json  # Single unified file
```

### New Structure
```
session_folder/
├── articles/
│   ├── article_1.json
│   └── article_2.json
├── session_data_www_fanatik_com_tr.json    # Source-specific
├── session_data_www_fotomac_com_tr.json    # Source-specific  
└── session_data_www_ntvspor_net.json       # Source-specific
```

### Source Session Data File Content
```json
{
  "source_url": "https://www.fanatik.com.tr",
  "source_domain": "www.fanatik.com.tr", 
  "saved_at": "2025-06-21T14:30:55.123456",
  "articles_count": 5,
  "articles": [
    {
      "title": "Fenerbahçe transfer haberi...",
      "url": "https://www.fanatik.com.tr/...",
      "content": "...",
      "published_at": "2025-06-21T10:00:00"
    }
  ],
  "session_metadata": {
    "session_id": "20250621_143055_123456",
    "source_specific": true,
    "articles_scraped": 5,
    "scraper_version": "modular-v1.1"
  }
}
```

## Benefits of This Refactoring

### 1. Single Responsibility
- `read()` method focuses on orchestration
- `process_articles()` handles all article processing logic

### 2. Consistent Return Data
- Same data structure returned regardless of persistence mode
- Source-specific information always available

### 3. Source Segregation
- Each news source gets its own session data file
- Easier to analyze performance per source
- Better organization for multiple sources

### 4. Maintainability
- Cleaner, more focused methods
- Easier to test individual components
- Reduced code duplication

### 5. Extensibility  
- Easy to add new processing steps
- Source-specific processing can be added
- Different storage backends can be supported

## Implementation Steps

1. **Create utility methods** (`_sanitize_url_for_filename`, `_extract_domain_from_url`)
2. **Implement article grouping** (`_group_articles_by_source`)
3. **Create session data builder** (`_create_source_session_data`)
4. **Extract file saving logic** (`_save_individual_articles`, `_save_source_session_files`)
5. **Implement main process_articles method**
6. **Update read() method** to use new process_articles method
7. **Update return structure** to include source-specific data
8. **Test with Turkish sports URLs** to verify source segregation

## Testing Strategy

### Test Cases
1. **Single Source**: One URL (e.g., fanatik.com.tr)
2. **Multiple Sources**: Two URLs (fanatik.com.tr, fotomac.com.tr)  
3. **Persist=True**: Verify files are created correctly
4. **Persist=False**: Verify same data structure returned
5. **No Articles**: Handle empty results gracefully
6. **Mixed Results**: Some sources succeed, others fail

### Validation Points
1. Source session data files created with correct naming
2. Articles properly grouped by source domain
3. Same data structure returned for both persistence modes
4. Individual article files still saved correctly
5. Final result includes source-specific data structure

---

*This refactoring implements source-specific functionality with improved code organization.*
