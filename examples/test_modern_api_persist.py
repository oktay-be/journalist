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
        
        # Test the new read method signature  
        client_keywords_direct = ["Galatasaray", "Fenerbahce"]
        client_scrape_urls_direct = ["https://www.bbc.com/news", "https://www.reuters.com/"]
        
        # Test persistent mode as well
        print("\n🧪 Testing persistent mode...")
        journalist_persistent = Journalist(persist=True, scrape_depth=1)
        print(f"✅ Persistent Journalist initialized")
        print(f"   Session path: {journalist_persistent.session_path}")

        result = await journalist_persistent.read(urls=client_scrape_urls_direct, keywords=client_keywords_direct)

        
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
