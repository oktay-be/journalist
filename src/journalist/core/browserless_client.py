"""
Browserless client for JavaScript-heavy page rendering.

This module provides integration with a self-hosted Browserless (headless Chrome) service
for extracting content from pages that require JavaScript execution (e.g., infinite scroll).

IMPORTANT: This is an opt-in feature. Users must explicitly provide:
- browserless_url: The URL of the Browserless service
- browserless_token: Authentication token for the Browserless API

Without both parameters, this client will not be used and all requests
will fall back to the standard aiohttp client.
"""

import asyncio
import logging
import aiohttp
from typing import Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class BrowserlessClient:
    """
    Client for interacting with a Browserless (headless Chrome) service.
    
    Browserless provides a Chrome browser as a service, allowing JavaScript
    execution and dynamic content rendering that aiohttp cannot handle.
    
    Usage:
        client = BrowserlessClient(
            browserless_url="https://your-browserless-service.run.app",
            browserless_token="your-secret-token",
            max_scrolls=20
        )
        html = await client.fetch("https://example.com/foto-galeri/123")
    """
    
    # Default timeout for Browserless requests (accounts for cold start + rendering)
    DEFAULT_TIMEOUT = 30
    
    # Default number of scroll iterations for infinite scroll pages
    DEFAULT_MAX_SCROLLS = 20
    
    # Wait time between scrolls (milliseconds) to allow content loading
    SCROLL_WAIT_MS = 500
    
    def __init__(
        self, 
        browserless_url: str, 
        browserless_token: str,
        max_scrolls: int = DEFAULT_MAX_SCROLLS,
        timeout: int = DEFAULT_TIMEOUT
    ):
        """
        Initialize the Browserless client.
        
        Args:
            browserless_url: Base URL of the Browserless service (required)
            browserless_token: Authentication token for the API (required)
            max_scrolls: Maximum number of scroll iterations (default: 20)
            timeout: Request timeout in seconds (default: 30)
        
        Raises:
            ValueError: If browserless_url or browserless_token is not provided
        """
        if not browserless_url:
            raise ValueError("browserless_url is required for BrowserlessClient")
        if not browserless_token:
            raise ValueError("browserless_token is required for BrowserlessClient")
        
        self.browserless_url = browserless_url.rstrip('/')
        self.browserless_token = browserless_token
        self.max_scrolls = max_scrolls
        self.timeout = timeout
        
        logger.info(
            "BrowserlessClient initialized (url=%s, max_scrolls=%d, timeout=%ds)",
            self.browserless_url, self.max_scrolls, self.timeout
        )
    
    def _build_scroll_script(self, max_scrolls: Optional[int] = None) -> str:
        """
        Build JavaScript code to scroll down the page and trigger infinite scroll.
        
        Args:
            max_scrolls: Override default max_scrolls for this request
            
        Returns:
            JavaScript code as a string
        """
        scrolls = max_scrolls if max_scrolls is not None else self.max_scrolls
        wait_ms = self.SCROLL_WAIT_MS
        
        return f"""
        async function scrollPage() {{
            const maxScrolls = {scrolls};
            const waitTime = {wait_ms};
            let lastHeight = document.body.scrollHeight;
            let scrollCount = 0;
            
            while (scrollCount < maxScrolls) {{
                // Scroll to bottom
                window.scrollTo(0, document.body.scrollHeight);
                
                // Wait for content to load
                await new Promise(resolve => setTimeout(resolve, waitTime));
                
                // Check if new content was loaded
                const newHeight = document.body.scrollHeight;
                if (newHeight === lastHeight) {{
                    // No new content, try a few more times then stop
                    scrollCount += 3;
                }} else {{
                    scrollCount += 1;
                }}
                lastHeight = newHeight;
            }}
            
            // Final scroll to ensure we're at the bottom
            window.scrollTo(0, document.body.scrollHeight);
            await new Promise(resolve => setTimeout(resolve, waitTime));
            
            return document.documentElement.outerHTML;
        }}
        scrollPage();
        """
    
    async def fetch(self, url: str, max_scrolls: Optional[int] = None) -> Optional[str]:
        """
        Fetch a URL using Browserless with JavaScript execution and scrolling.
        
        This method:
        1. Opens the URL in a headless Chrome browser
        2. Executes scroll script to trigger infinite scroll loading
        3. Returns the fully rendered HTML after all content loads
        
        Args:
            url: The URL to fetch
            max_scrolls: Override default max_scrolls for this request
            
        Returns:
            The fully rendered HTML content, or None if fetch failed
        """
        logger.info("Browserless: Fetching URL with JS rendering: %s", url)
        
        try:
            # Build the Browserless /content endpoint URL
            # See: https://www.browserless.io/docs/content
            content_endpoint = f"{self.browserless_url}/content"
            
            # Build request payload
            payload = {
                "url": url,
                "gotoOptions": {
                    "waitUntil": "networkidle2",
                    "timeout": (self.timeout - 5) * 1000  # Leave 5s buffer, convert to ms
                },
                # Execute scroll script after page loads
                "addScriptTag": [
                    {
                        "content": self._build_scroll_script(max_scrolls)
                    }
                ],
                # Wait for scroll script to complete
                "waitForFunction": {
                    "fn": "() => true",  # Simple wait after script execution
                    "timeout": self.timeout * 1000
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.browserless_token}"
            }
            
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    content_endpoint,
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        logger.info(
                            "Browserless: Successfully fetched %s (content length: %d)",
                            url, len(html_content)
                        )
                        return html_content
                    else:
                        error_text = await response.text()
                        logger.error(
                            "Browserless: Failed to fetch %s - Status %d: %s",
                            url, response.status, error_text[:500]
                        )
                        return None
                        
        except asyncio.TimeoutError:
            logger.error("Browserless: Timeout fetching %s (timeout=%ds)", url, self.timeout)
            return None
        except aiohttp.ClientError as e:
            logger.error("Browserless: Client error fetching %s: %s", url, str(e))
            return None
        except Exception as e:
            logger.error("Browserless: Unexpected error fetching %s: %s", url, str(e))
            return None
    
    async def fetch_with_fallback(
        self, 
        url: str, 
        fallback_fetcher,
        max_scrolls: Optional[int] = None
    ) -> Optional[str]:
        """
        Fetch a URL using Browserless, falling back to another fetcher on failure.
        
        Args:
            url: The URL to fetch
            fallback_fetcher: Async callable that takes URL and returns HTML
            max_scrolls: Override default max_scrolls for this request
            
        Returns:
            HTML content from Browserless or fallback, or None if both fail
        """
        # Try Browserless first
        html = await self.fetch(url, max_scrolls)
        
        if html:
            return html
        
        # Browserless failed, try fallback
        logger.warning(
            "Browserless: Falling back to standard fetcher for %s", url
        )
        
        try:
            return await fallback_fetcher(url)
        except Exception as e:
            logger.error("Browserless: Fallback fetcher also failed for %s: %s", url, str(e))
            return None
    
    def is_available(self) -> bool:
        """
        Check if the Browserless client is properly configured.
        
        Returns:
            True if client has URL and token configured
        """
        return bool(self.browserless_url and self.browserless_token)
