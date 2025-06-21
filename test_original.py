#!/usr/bin/env python3

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from journalist import Journalist

async def simple_test():
    print("🔍 Testing original working version...")
    
    try:
        # Create journalist instance
        journalist = Journalist(persist=False, scrape_depth=1)
        print("✅ Journalist created successfully")
        
        # Test with a single URL
        test_urls = ["https://www.fanatik.com.tr/futbol"]
        print(f"📰 Testing with URL: {test_urls[0]}")
        
        # Call the read method
        print("🔄 Calling read method...")
        result = await journalist.read(test_urls, ["mourinho"])
        print("✅ Read method completed")
        
        print(f"📊 Result type: {type(result)}")
        print(f"📊 Result structure: {f'List with {len(result)} sources' if isinstance(result, list) else 'Not a list'}")
        
        if isinstance(result, list):
            # Extract all articles from all sources
            all_articles = []
            print(f"📊 Source sessions: {len(result)}")
            
            for i, source_data in enumerate(result):
                domain = source_data.get('source_domain', 'unknown')
                articles_count = source_data.get('articles_count', 0)
                source_url = source_data.get('source_url', 'N/A')
                source_articles = source_data.get('articles', [])
                all_articles.extend(source_articles)
                
                print(f"  📍 Source {i+1}: {domain} ({articles_count} articles)")
                print(f"      URL: {source_url}")
            
            print(f"📊 Total articles found: {len(all_articles)}")
        else:
            # Fallback for old format (shouldn't happen)
            if isinstance(result, dict):
                articles = result.get('articles', [])
                print(f"📊 Articles found: {len(articles)}")
                
                summary = result.get('extraction_summary', {})
                print(f"📊 Extraction summary: {summary}")
            else:
                print(f"❌ Unexpected result type: {type(result)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(simple_test())
