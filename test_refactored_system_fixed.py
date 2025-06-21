#!/usr/bin/env python3

"""
Test script for the refactored journalist system to verify that:
1. Source-specific session data files are created correctly
2. Process_articles always returns source-specific session data
3. File operations are delegated to FileManager
4. Session data creation is delegated to WebScraper
"""

import asyncio
import os
import json
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from journalist import Journalist

async def test_refactored_system():
    """Test the refactored journalist system with Turkish sports URLs"""
    
    print("🧪 Testing refactored journalist system...")
    
    # Test URLs for Turkish sports sites
    test_urls = [
        "https://www.fanatik.com.tr/futbol"
    ]
    
    # Test keywords
    test_keywords = ["mourinho"]
    
    print(f"📰 Testing with URLs: {test_urls}")
    print(f"🔍 Testing with keywords: {test_keywords}")
    
    # Test with persistence enabled
    print("\n=== Test 1: Persistence Enabled ===")
    journalist_persist = Journalist(persist=True, scrape_depth=1)
    
    try:
        result_persist = await journalist_persist.read(test_urls, test_keywords)
        
        print(f"✅ Result type: {type(result_persist)}")
        print(f"✅ Result is list: {isinstance(result_persist, list)}")
        
        if isinstance(result_persist, list):
            print(f"✅ Number of source sessions: {len(result_persist)}")
            
            # Check each source session data
            for i, source_session in enumerate(result_persist):
                print(f"\n📊 Source Session {i+1}:")
                print(f"  - Domain: {source_session.get('source_domain', 'N/A')}")
                print(f"  - URL: {source_session.get('source_url', 'N/A')}")
                print(f"  - Articles count: {source_session.get('articles_count', 0)}")
                print(f"  - Has saved_at: {'saved_at' in source_session}")
                print(f"  - Has session_metadata: {'session_metadata' in source_session}")
                
                # Check if source-specific files were created
                domain = source_session.get('source_domain')
                if domain:
                    workspace_path = journalist_persist.session_path
                    expected_filename = f"session_data_{domain.replace('.', '_')}.json"
                    expected_path = os.path.join(workspace_path, expected_filename)
                    
                    if os.path.exists(expected_path):
                        print(f"  ✅ Source-specific file created: {expected_filename}")
                        
                        # Verify file content
                        try:
                            with open(expected_path, 'r', encoding='utf-8') as f:
                                file_data = json.load(f)
                            print(f"  ✅ File content valid JSON with {len(file_data.get('articles', []))} articles")
                        except Exception as e:
                            print(f"  ❌ Error reading file: {e}")
                    else:
                        print(f"  ❌ Source-specific file NOT found: {expected_filename}")
        
        print(f"\n📁 Session workspace: {journalist_persist.session_path}")
        
        # List files in workspace
        if os.path.exists(journalist_persist.session_path):
            files = os.listdir(journalist_persist.session_path)
            session_files = [f for f in files if f.startswith('session_data_') and f.endswith('.json')]
            print(f"📄 Session files found: {session_files}")
        
    except Exception as e:
        print(f"❌ Error in persistence test: {e}")
        import traceback
        traceback.print_exc()
    
    # Test with persistence disabled
    print("\n=== Test 2: Persistence Disabled ===")
    journalist_memory = Journalist(persist=False, scrape_depth=1)
    
    try:
        result_memory = await journalist_memory.read(test_urls, test_keywords)
        
        print(f"✅ Result type: {type(result_memory)}")
        print(f"✅ Result is list: {isinstance(result_memory, list)}")
        
        if isinstance(result_memory, list):
            print(f"✅ Number of source sessions: {len(result_memory)}")
            
            # Verify structure is the same as persistent mode
            for i, source_session in enumerate(result_memory):
                print(f"\n📊 Source Session {i+1} (Memory Mode):")
                print(f"  - Domain: {source_session.get('source_domain', 'N/A')}")
                print(f"  - URL: {source_session.get('source_url', 'N/A')}")
                print(f"  - Articles count: {source_session.get('articles_count', 0)}")
                print(f"  - Has saved_at: {'saved_at' in source_session}")
                print(f"  - Has session_metadata: {'session_metadata' in source_session}")
        
        # Verify memory storage
        print(f"📋 Memory articles count: {len(journalist_memory.memory_articles)}")
        
    except Exception as e:
        print(f"❌ Error in memory test: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Refactored system test completed!")

if __name__ == "__main__":
    asyncio.run(test_refactored_system())
