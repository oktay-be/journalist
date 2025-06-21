#!/usr/bin/env python3

"""
Test the refactored journalist system to ensure it works correctly
"""

import asyncio
import sys
import os
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from journalist import Journalist

async def test_refactored_journalist():
    """Test the refactored journalist system"""
    
    print("🧪 Testing refactored journalist system...")
    
    # Test URLs
    test_urls = ["https://www.fanatik.com.tr/futbol"]
    test_keywords = ["mourinho"]
    
    print(f"📰 Testing with URL: {test_urls[0]}")
    print(f"🔍 Testing with keywords: {test_keywords}")
    
    # Test with persistence enabled
    print("\n=== Test 1: Persistence Enabled ===")
    journalist_persist = Journalist(persist=True, scrape_depth=1)
    
    try:
        result_persist = await journalist_persist.read(test_urls, test_keywords)
        
        print(f"✅ Result type: {type(result_persist)}")
        print(f"✅ Result is list: {isinstance(result_persist, list)}")
        
        if isinstance(result_persist, list):
            print(f"✅ Source sessions count: {len(result_persist)}")
            
            # Extract all articles from all sources
            all_articles = []
            for source_data in result_persist:
                source_articles = source_data.get('articles', [])
                all_articles.extend(source_articles)
            
            print(f"✅ Total articles count: {len(all_articles)}")
            
            # Check each source session
            for i, source_data in enumerate(result_persist):
                domain = source_data.get('source_domain', 'unknown')
                articles_count = source_data.get('articles_count', 0)
                source_url = source_data.get('source_url', 'N/A')
                print(f"  📊 Source {i+1}: domain={domain}, articles={articles_count}, url={source_url}")
        else:
            print(f"❌ Expected list but got {type(result_persist)}")
        
        # Check if files were created
        if os.path.exists(journalist_persist.session_path):
            files = os.listdir(journalist_persist.session_path)
            session_files = [f for f in files if f.startswith('session_data_')]
            print(f"📄 Session files created: {session_files}")
        
    except Exception as e:
        print(f"❌ Error in persistence test: {e}")
        import traceback
        traceback.print_exc()
    
    # Test with persistence disabled
    print("\n=== Test 2: Memory Mode ===")
    journalist_memory = Journalist(persist=False, scrape_depth=1)
    
    try:
        result_memory = await journalist_memory.read(test_urls, test_keywords)
        
        print(f"✅ Result type: {type(result_memory)}")
        print(f"✅ Result is list: {isinstance(result_memory, list)}")
        
        if isinstance(result_memory, list):
            print(f"✅ Source sessions count: {len(result_memory)}")
            
            # Extract all articles from all sources
            all_articles = []
            for source_data in result_memory:
                source_articles = source_data.get('articles', [])
                all_articles.extend(source_articles)
            
            print(f"✅ Total articles count: {len(all_articles)}")
        else:
            print(f"❌ Expected list but got {type(result_memory)}")
        
        print(f"📋 Memory articles: {len(journalist_memory.memory_articles)}")
        
    except Exception as e:
        print(f"❌ Error in memory test: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Refactored system test completed!")

if __name__ == "__main__":
    asyncio.run(test_refactored_journalist())
