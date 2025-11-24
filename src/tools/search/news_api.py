"""NewsAPI tool - News articles search."""

import os
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


class NewsAPITool:
    """Wrapper for NewsAPI.org."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize NewsAPI client.
        
        Args:
            api_key: NewsAPI key (defaults to NEWS_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    async def search(
        self,
        query: str,
        max_results: int = 5,
        days: int = 30,
        language: str = "en",
        sort_by: str = "relevancy"
    ) -> Dict[str, Any]:
        """Search for news articles.
        
        Args:
            query: Search query
            max_results: Maximum results
            days: Search last N days
            language: Language code (en, es, fr, etc.)
            sort_by: Sort by relevancy, popularity, or publishedAt
            
        Returns:
            Dictionary with news results
        """
        if not self.api_key:
            return {
                "results": [],
                "error": "NEWS_API_KEY not configured"
            }
        
        # Calculate date range
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)
        
        url = f"{self.base_url}/everything"
        params = {
            "q": query,
            "apiKey": self.api_key,
            "pageSize": max_results,
            "language": language,
            "sortBy": sort_by,
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d")
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
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
            print(f"[NewsAPI] Error: {e}")
            return {"results": [], "error": str(e)}
    
    def _format_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format NewsAPI response to match Tavily format.
        
        Args:
            data: Raw NewsAPI response
            
        Returns:
            Formatted results
        """
        results = []
        
        for article in data.get("articles", []):
            results.append({
                "url": article.get("url", ""),
                "title": article.get("title", ""),
                "content": article.get("description", ""),
                "raw_content": article.get("content", ""),
                "published_at": article.get("publishedAt", ""),
                "source": article.get("source", {}).get("name", ""),
                "author": article.get("author", "")
            })
        
        return {"results": results}
    
    async def get_top_headlines(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        country: str = "us",
        max_results: int = 5
    ) -> Dict[str, Any]:
        """Get top headlines.
        
        Args:
            query: Search query (optional)
            category: Category (business, technology, etc.)
            country: Country code (us, gb, etc.)
            max_results: Maximum results
            
        Returns:
            Top headlines
        """
        if not self.api_key:
            return {
                "results": [],
                "error": "NEWS_API_KEY not configured"
            }
        
        url = f"{self.base_url}/top-headlines"
        params = {
            "apiKey": self.api_key,
            "pageSize": max_results,
            "country": country
        }
        
        if query:
            params["q"] = query
        if category:
            params["category"] = category
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_response(data)
                    else:
                        return {"results": [], "error": f"HTTP {response.status}"}
        except Exception as e:
            return {"results": [], "error": str(e)}
