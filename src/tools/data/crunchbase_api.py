"""Crunchbase API tool - Funding and investor data."""

import os
import aiohttp
from typing import Dict, Any, Optional, List


class CrunchbaseTool:
    """Wrapper for Crunchbase API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Crunchbase client.
        
        Args:
            api_key: Crunchbase API key (defaults to CRUNCHBASE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("CRUNCHBASE_API_KEY")
        self.base_url = "https://api.crunchbase.com/api/v4"
    
    async def get_organization(self, permalink: str) -> Dict[str, Any]:
        """Get organization details.
        
        Args:
            permalink: Organization permalink (e.g., 'openai')
            
        Returns:
            Organization data
        """
        if not self.api_key:
            return {"error": "CRUNCHBASE_API_KEY not configured"}
        
        url = f"{self.base_url}/entities/organizations/{permalink}"
        headers = {"X-cb-user-key": self.api_key}
        params = {
            "card_ids": "fields,funding_rounds,investors,founders"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        return {"error": f"HTTP {response.status}: {error_text}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def search_organizations(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for organizations.
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of matching organizations
        """
        if not self.api_key:
            return []
        
        url = f"{self.base_url}/searches/organizations"
        headers = {"X-cb-user-key": self.api_key}
        payload = {
            "field_ids": ["identifier", "name", "short_description"],
            "query": [
                {
                    "type": "predicate",
                    "field_id": "name",
                    "operator_id": "contains",
                    "values": [query]
                }
            ],
            "limit": limit
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("entities", [])
                    else:
                        return []
        except Exception as e:
            print(f"[Crunchbase] Search error: {e}")
            return []
    
    def extract_funding_data(self, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract funding information from organization data.
        
        Args:
            org_data: Raw organization data from Crunchbase
            
        Returns:
            Formatted funding data
        """
        if "error" in org_data:
            return org_data
        
        properties = org_data.get("properties", {})
        cards = org_data.get("cards", {})
        
        funding_rounds = []
        if "funding_rounds" in cards:
            for round_data in cards["funding_rounds"]:
                funding_rounds.append({
                    "round_type": round_data.get("identifier", {}).get("value"),
                    "announced_on": round_data.get("announced_on", {}).get("value"),
                    "money_raised": round_data.get("money_raised", {}).get("value"),
                    "currency": round_data.get("money_raised", {}).get("currency")
                })
        
        investors = []
        if "investors" in cards:
            for investor in cards["investors"]:
                investors.append(investor.get("identifier", {}).get("value"))
        
        return {
            "total_funding": properties.get("total_funding_usd", {}).get("value"),
            "last_funding_type": properties.get("last_funding_type"),
            "num_funding_rounds": properties.get("num_funding_rounds"),
            "funding_rounds": funding_rounds,
            "investors": investors[:10],  # Limit to top 10
            "valuation": properties.get("valuation", {}).get("value")
        }
