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
        print(f"📊 Result structure: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        
        if isinstance(result, dict):
            articles = result.get('articles', [])
            print(f"📊 Articles found: {len(articles)}")
            
            summary = result.get('extraction_summary', {})
            print(f"📊 Extraction summary: {summary}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(simple_test())
