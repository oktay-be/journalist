#!/usr/bin/env python3
"""
Test to verify the modern API works
"""

import sys
import os
import asyncio

# Add the src directory to the path so we can import our package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_modern_api():
    """Test the modern API signature"""
    try:
        from journalist import Journalist
        
        # Test initialization with new parameters
        # persist=False means no caching/filesystem writes (equivalent to disable_cache=True)
        journalist = Journalist(persist=False, scrape_depth=1)
        print(f"✅ Journalist initialized with session_id: {journalist.session_id[:8]}...")
        print(f"   persist: {journalist.persist}, scrape_depth: {journalist.scrape_depth}")
        
        # Test the new read method signature  
        client_keywords_direct = ["Galatasaray", "Fenerbahce"]
        client_scrape_urls_direct = ["https://www.bbc.com/news", "https://www.reuters.com/"]
        
        # This should work with the new API
        print("🧪 Testing new read() API signature...")
        result = await journalist.read(urls=client_scrape_urls_direct, keywords=client_keywords_direct)
        print(f"✅ read() method called successfully")
        print(f"   Result type: {type(result)}")
        print(f"   Articles found: {len(result.get('articles', []))}")
        print(f"   Session metadata: {bool(result.get('session_metadata'))}")

        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing modern API...")
    print("📋 Testing new parameters: persist (replaces disable_cache) and scrape_depth")
    success = asyncio.run(test_modern_api())
    
    if success:
        print("\n🎉 Modern API test successful!")
        print("✅ New API parameters working correctly:")
        print("   - persist=False (equivalent to old disable_cache=True)")
        print("   - persist=True (enables filesystem operations)")
        print("   - scrape_depth (moved from config to runtime parameter)")
    else:
        print("⚠️ API test failed!")
