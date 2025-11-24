"""Financial data tools - Alpha Vantage, Yahoo Finance, FMP."""

import os
import aiohttp
from typing import Dict, Any, Optional


class FinancialDataTool:
    """Unified financial data tool supporting multiple providers."""
    
    def __init__(
        self,
        alpha_vantage_key: Optional[str] = None,
        fmp_key: Optional[str] = None
    ):
        """Initialize financial data clients.
        
        Args:
            alpha_vantage_key: Alpha Vantage API key
            fmp_key: Financial Modeling Prep API key
        """
        self.alpha_vantage_key = alpha_vantage_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        self.fmp_key = fmp_key or os.getenv("FMP_API_KEY")
        
        self.av_base_url = "https://www.alphavantage.co/query"
        self.fmp_base_url = "https://financialmodelingprep.com/api/v3"
    
    async def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """Get company overview from Alpha Vantage.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Company overview data
        """
        if not self.alpha_vantage_key:
            return {"error": "ALPHA_VANTAGE_API_KEY not configured"}
        
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.alpha_vantage_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.av_base_url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_income_statement(self, symbol: str) -> Dict[str, Any]:
        """Get income statement from Alpha Vantage.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Income statement data
        """
        if not self.alpha_vantage_key:
            return {"error": "ALPHA_VANTAGE_API_KEY not configured"}
        
        params = {
            "function": "INCOME_STATEMENT",
            "symbol": symbol,
            "apikey": self.alpha_vantage_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.av_base_url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_fmp_profile(self, symbol: str) -> Dict[str, Any]:
        """Get company profile from Financial Modeling Prep.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Company profile data
        """
        if not self.fmp_key:
            return {"error": "FMP_API_KEY not configured"}
        
        url = f"{self.fmp_base_url}/profile/{symbol}"
        params = {"apikey": self.fmp_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data[0] if data else {}
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def get_fmp_ratios(self, symbol: str) -> Dict[str, Any]:
        """Get financial ratios from FMP.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Financial ratios
        """
        if not self.fmp_key:
            return {"error": "FMP_API_KEY not configured"}
        
        url = f"{self.fmp_base_url}/ratios/{symbol}"
        params = {"apikey": self.fmp_key, "limit": 1}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data[0] if data else {}
                    else:
                        return {"error": f"HTTP {response.status}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def search_ticker(self, company_name: str) -> Optional[str]:
        """Search for stock ticker by company name.
        
        Args:
            company_name: Company name to search
            
        Returns:
            Stock ticker symbol or None
        """
        if not self.alpha_vantage_key:
            return None
        
        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": company_name,
            "apikey": self.alpha_vantage_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.av_base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        matches = data.get("bestMatches", [])
                        if matches:
                            return matches[0].get("1. symbol")
        except Exception as e:
            print(f"[FinancialData] Ticker search error: {e}")
        
        return None
