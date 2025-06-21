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
        print(f"✅ Result is dict: {isinstance(result_persist, dict)}")
        
        if isinstance(result_persist, dict):
            print(f"✅ Result keys: {list(result_persist.keys())}")
            print(f"✅ Articles count: {len(result_persist.get('articles', []))}")
            print(f"✅ Has extraction_summary: {'extraction_summary' in result_persist}")
            print(f"✅ Has source_sessions: {'source_sessions' in result_persist}")
            
            # Check source sessions
            source_sessions = result_persist.get('source_sessions', [])
            print(f"✅ Source sessions count: {len(source_sessions)}")
            
            for i, session in enumerate(source_sessions):
                print(f"  📊 Session {i+1}: domain={session.get('source_domain')}, articles={session.get('articles_count', 0)}")
        
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
        print(f"✅ Result is dict: {isinstance(result_memory, dict)}")
        
        if isinstance(result_memory, dict):
            print(f"✅ Result keys: {list(result_memory.keys())}")
            print(f"✅ Articles count: {len(result_memory.get('articles', []))}")
            print(f"✅ Has source_sessions: {'source_sessions' in result_memory}")
        
        print(f"📋 Memory articles: {len(journalist_memory.memory_articles)}")
        
    except Exception as e:
        print(f"❌ Error in memory test: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Refactored system test completed!")

if __name__ == "__main__":
    asyncio.run(test_refactored_journalist())
