"""Serper search tool - Google search API backup."""

import os
import aiohttp
from typing import List, Dict, Any, Optional


class SerperSearchTool:
    """Wrapper for Serper.dev Google search API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Serper client.
        
        Args:
            api_key: Serper API key (defaults to SERPER_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        self.base_url = "https://google.serper.dev"
    
    async def search(
        self,
        query: str,
        max_results: int = 5,
        search_type: str = "search"
    ) -> Dict[str, Any]:
        """Execute a Google search via Serper.
        
        Args:
            query: Search query string
            max_results: Maximum number of results
            search_type: Type of search (search, news, images)
            
        Returns:
            Dictionary with search results
        """
        if not self.api_key:
            return {
                "results": [],
                "error": "SERPER_API_KEY not configured"
            }
        
        url = f"{self.base_url}/{search_type}"
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": max_results
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_response(data)
                    else:
                        error_text = await response.text()
                        return {
                            "results": [],
                            "error": f"HTTP {response.status}: {error_text}"
                        }
        except Exception as e:
            print(f"[SerperSearch] Error: {e}")
            return {"results": [], "error": str(e)}
    
    def _format_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format Serper response to match Tavily format.
        
        Args:
            data: Raw Serper response
            
        Returns:
            Formatted results
        """
        results = []
        
        # Extract organic results
        for item in data.get("organic", []):
            results.append({
                "url": item.get("link", ""),
                "title": item.get("title", ""),
                "content": item.get("snippet", ""),
                "raw_content": None  # Serper doesn't provide full content
            })
        
        return {"results": results}
    
    async def search_news(
        self,
        query: str,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """Search for news articles.
        
        Args:
            query: Search query
            max_results: Maximum results
            
        Returns:
            News search results
        """
        return await self.search(
            query=query,
            max_results=max_results,
            search_type="news"
        )
