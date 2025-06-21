#!/usr/bin/env python3
"""
Test script for Turkish sports news extraction
Testing with Fenerbahçe and Galatasaray keywords on Turkish sports sites
"""

import asyncio
import sys
import os

# Add the src directory to Python path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from journalist import Journalist


async def main():
    """Main test function for Turkish sports news extraction"""
    print("🚀 Starting Turkish Sports News Extraction Test")
    print("=" * 60)
    
    # Create journalist instance with persistence and depth 1
    journalist = Journalist(persist=False, scrape_depth=1)
    
    # Define test parameters
    urls = [
        "https://www.fanatik.com.tr",
        "https://www.ntvspor.net"

    ]
    
    keywords = ["fenerbahce"]
    
    print(f"📰 Target URLs: {urls}")
    print(f"🔍 Keywords: {keywords}")
    print("-" * 60)
    
    try:
        # Extract content from Turkish sports news sites
        print("⏳ Starting content extraction...")
        result = await journalist.read(
            urls=urls,
            keywords=keywords
        )
        
        print("✅ Content extraction completed!")
        print("=" * 60)
        
        # Display extracted articles
        articles = result.get('articles', [])
        print(f"📄 Found {len(articles)} articles:")
        print("-" * 60)
        
        for i, article in enumerate(articles, 1):
            print(f"\n🏆 Article {i}:")
            print(f"   Title: {article.get('title', 'N/A')}")
            print(f"   URL: {article.get('url', 'N/A')}")
            print(f"   Published: {article.get('published_date', 'N/A')}")
            print(f"   Content Preview: {article.get('content', '')[:200]}...")
            if article.get('matched_keywords'):
                print(f"   Matched Keywords: {article.get('matched_keywords')}")
            print("-" * 40)
          # Display extraction summary
        summary = result.get('extraction_summary', {})
        print(f"\n📊 Extraction Summary:")
        print(f"   URLs Processed: {summary.get('urls_processed', 0)}")
        print(f"   Articles Extracted: {summary.get('articles_extracted', 0)}")
        print(f"   Sources Processed: {summary.get('sources_processed', 0)}")
        print(f"   Extraction Time: {summary.get('extraction_time_seconds', 0):.2f} seconds")
        
        # Display source-specific information if available
        source_session_files = result.get('source_session_files', [])
        if source_session_files:
            print(f"\n📂 Source Session Files:")
            for filename in source_session_files:
                print(f"   - {filename}")
        
        source_session_data = result.get('source_session_data', [])
        if source_session_data:
            print(f"\n🌐 Source-Specific Results:")
            print("-" * 60)
            for i, source_data in enumerate(source_session_data, 1):
                domain = source_data.get('source_domain', 'Unknown')
                source_url = source_data.get('source_url', 'N/A')
                source_articles = source_data.get('articles', [])
                
                print(f"\n📍 Source {i}: {domain}")
                print(f"   Original URL: {source_url}")
                print(f"   Articles Found: {len(source_articles)}")
                
                # Show first few articles from this source
                for j, article in enumerate(source_articles[:3], 1):
                    print(f"   📄 Article {j}:")
                    print(f"      Title: {article.get('title', 'N/A')[:60]}...")
                    print(f"      URL: {article.get('url', 'N/A')}")
                
                if len(source_articles) > 3:
                    print(f"   ... and {len(source_articles) - 3} more articles")
                print("-" * 40)
        
        # Display any errors if occurred
        errors = result.get('errors', [])
        if errors:
            print(f"\n⚠️  Errors encountered:")
            for error in errors:
                print(f"   - {error}")
        
        print("\n🎉 Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during extraction: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())