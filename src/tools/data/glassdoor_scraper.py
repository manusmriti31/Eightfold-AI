"""Glassdoor scraper - Employee reviews and sentiment.

NOTE: Glassdoor has strict anti-scraping policies. This is a placeholder.
Consider using web search to find Glassdoor data instead.
"""

from typing import Dict, Any, List


class GlassdoorScraper:
    """Placeholder for Glassdoor data extraction."""
    
    def __init__(self):
        """Initialize Glassdoor scraper."""
        self.warning_shown = False
    
    def _show_warning(self):
        """Show warning about Glassdoor scraping."""
        if not self.warning_shown:
            print("⚠️  WARNING: Glassdoor scraping is against their ToS.")
            print("   Use web search to find Glassdoor reviews instead.")
            self.warning_shown = True
    
    async def get_company_reviews(self, company: str) -> Dict[str, Any]:
        """Get company reviews from Glassdoor.
        
        Args:
            company: Company name
            
        Returns:
            Reviews data (placeholder)
        """
        self._show_warning()
        
        return {
            "error": "Glassdoor scraping not implemented",
            "recommendation": "Use web search with queries like:",
            "example_queries": [
                f"{company} Glassdoor reviews",
                f"{company} employee reviews rating",
                f'site:glassdoor.com "{company}" reviews'
            ]
        }


class GlassdoorSearchHelper:
    """Helper to find Glassdoor data via web search."""
    
    @staticmethod
    def generate_search_queries(company: str) -> List[str]:
        """Generate search queries to find Glassdoor data.
        
        Args:
            company: Company name
            
        Returns:
            List of search queries
        """
        return [
            f"{company} Glassdoor reviews rating",
            f"{company} employee reviews Glassdoor",
            f'site:glassdoor.com "{company}" reviews',
            f"{company} CEO approval rating Glassdoor",
            f"{company} work culture reviews"
        ]
