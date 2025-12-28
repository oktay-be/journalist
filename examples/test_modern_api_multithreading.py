#!/usr/bin/env python3
"""
Test to verify the modern API works with multiple journalist instances running simultaneously
"""

import sys
import os
import asyncio

# Add the src directory to the path so we can import our package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_multithreading_api():
    """Test multiple journalist instances running simultaneously"""
    try:
        from journalist import Journalist
        
        print("🚀 Starting multithreading test with two journalist instances...")
        print("📋 Both instances will use same keywords but different URLs")
          # Create journalist instances
        keywords = ["sports", "soccer"]
        urls1 = ["https://www.espn.com/", "https://ajansspor.com/"]
        urls2 = ["https://www.reuters.com/", "https://www.bbc.com/news"]
        
        print("🔧 Creating journalist instances...")
        journalist1 = Journalist(persist=True, scrape_depth=1)
        print(f"   Journalist 1 session path: {journalist1.session_path}")
        
        # Add small delay to avoid race condition in session path creation
        await asyncio.sleep(0.001)
        
        journalist2 = Journalist(persist=True, scrape_depth=1)
        print(f"   Journalist 2 session path: {journalist2.session_path}")
        
        print(f"✅ Journalist instances initialized")
        print(f"   Journalist 1 - URLs: {urls1}")
        print(f"   Journalist 2 - URLs: {urls2}")
        print(f"   Keywords (both): {keywords}")
          # Create asyncio tasks directly from the read methods
        print("🚀 Creating asyncio tasks...")
        task1 = asyncio.create_task(journalist1.read(urls=urls1, keywords=keywords), name="journalist1")
        task2 = asyncio.create_task(journalist2.read(urls=urls2, keywords=keywords), name="journalist2")
        
        print(f"   Task 1 (journalist1): {task1.get_name()}")
        print(f"   Task 2 (journalist2): {task2.get_name()}")
        
        print("\n⏳ Running both journalists simultaneously...")
        
        # Execute both tasks simultaneously using asyncio.gather
        results = await asyncio.gather(task1, task2, return_exceptions=True)
        
        print("\n📊 Results Summary:")
        success_count = 0
        
        for i, result in enumerate(results, 1):
            task_name = f"journalist{i}"
            if isinstance(result, Exception):
                print(f"❌ {task_name} failed with exception: {result}")
                print(f"   Exception type: {type(result).__name__}")
                import traceback
                print(f"   Traceback: {traceback.format_exception(type(result), result, result.__traceback__)}")
            else:
                print(f"✅ {task_name}: SUCCESS")
                print(f"   Result type: {type(result)}")
                if isinstance(result, dict) and 'articles' in result:
                    articles_count = len(result.get('articles', []))
                    print(f"   Articles found: {articles_count}")
                elif isinstance(result, (list, tuple, dict, str)) and hasattr(result, '__len__'):
                    print(f"   Result length: {len(result)}")
                success_count += 1
        
        print(f"\n📈 Summary: {success_count}/2 journalists completed successfully")
        
        # Additional debugging - check if session folders exist
        print(f"\n🔍 Session folder verification:")
        if journalist1.session_path:
            print(f"   Journalist 1 session: {journalist1.session_path}")
            print(f"   Exists: {os.path.exists(journalist1.session_path)}")
        else:
            print(f"   Journalist 1 session: None")
            
        if journalist2.session_path:
            print(f"   Journalist 2 session: {journalist2.session_path}")  
            print(f"   Exists: {os.path.exists(journalist2.session_path)}")
        else:
            print(f"   Journalist 2 session: None")
        
        return success_count == 2
        
    except Exception as e:
        print(f"❌ Multithreading test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing modern API with multithreading...")
    print("🎯 Goal: Run 2 journalist instances simultaneously with same keywords, different URLs")
    print("📋 Configuration:")
    print("   Journalist 1: espn.com + ajansspor.com")
    print("   Journalist 2: reuters.com + bbc.com")
    print("   Keywords (both): sports, soccer")
    
    success = asyncio.run(test_multithreading_api())
    
    if success:
        print("\n🎉 Multithreading API test successful!")
        print("✅ Both journalist instances completed successfully")
        print("✅ Asyncio tasks and gather worked correctly")
        print("✅ Modern API supports concurrent operations")
    else:
        print("⚠️ Multithreading API test failed!")
