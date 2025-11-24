"""Tavily search tool - Primary web search."""

import os
from typing import List, Dict, Any, Optional
from tavily import AsyncTavilyClient


class TavilySearchTool:
    """Wrapper for Tavily search API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Tavily client.
        
        Args:
            api_key: Tavily API key (defaults to TAVILY_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        
        self.client = AsyncTavilyClient(api_key=self.api_key)
    
    async def search(
        self,
        query: str,
        max_results: int = 5,
        include_raw_content: bool = True,
        topic: str = "general",
        days: Optional[int] = None
    ) -> Dict[str, Any]:
        """Execute a search query.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            include_raw_content: Whether to include full page content
            topic: Search topic (general or news)
            days: Limit results to last N days (optional)
            
        Returns:
            Dictionary with search results
        """
        try:
            result = await self.client.search(
                query=query,
                max_results=max_results,
                include_raw_content=include_raw_content,
                topic=topic,
                days=days
            )
            return result
        except Exception as e:
            print(f"[TavilySearch] Error: {e}")
            return {"results": [], "error": str(e)}
    
    async def search_news(
        self,
        query: str,
        max_results: int = 5,
        days: int = 30
    ) -> Dict[str, Any]:
        """Search for recent news articles.
        
        Args:
            query: Search query
            max_results: Maximum results
            days: Limit to last N days
            
        Returns:
            News search results
        """
        return await self.search(
            query=query,
            max_results=max_results,
            include_raw_content=True,
            topic="news",
            days=days
        )
    
    def format_results(self, results: Dict[str, Any]) -> str:
        """Format search results into readable text.
        
        Args:
            results: Raw search results from Tavily
            
        Returns:
            Formatted text string
        """
        if "error" in results:
            return f"Search error: {results['error']}"
        
        formatted = ""
        for item in results.get("results", []):
            url = item.get("url", "")
            title = item.get("title", "")
            content = item.get("content", "")[:1000]  # Limit content
            
            formatted += f"\n--- SOURCE: {url} ---\n"
            formatted += f"Title: {title}\n"
            formatted += f"Content: {content}\n\n"
        
        return formatted
