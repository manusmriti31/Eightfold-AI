"""Stock market data tool using Yahoo Finance."""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import yfinance as yf


class StockMarketTool:
    """Tool for fetching stock market data and financial news."""
    
    def __init__(self):
        """Initialize stock market tool."""
        self.cache = {}
    
    def get_stock_ticker(self, company_name: str) -> Optional[str]:
        """
        Try to determine stock ticker from company name.
        
        Args:
            company_name: Company name
            
        Returns:
            Stock ticker symbol or None
        """
        # Common mappings
        ticker_map = {
            "tesla": "TSLA",
            "apple": "AAPL",
            "microsoft": "MSFT",
            "google": "GOOGL",
            "alphabet": "GOOGL",
            "amazon": "AMZN",
            "meta": "META",
            "facebook": "META",
            "nvidia": "NVDA",
            "netflix": "NFLX",
            "openai": None,  # Private
            "spacex": None,  # Private
        }
        
        company_lower = company_name.lower().strip()
        return ticker_map.get(company_lower)
    
    def get_stock_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive stock data for a ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., "TSLA")
            
        Returns:
            Dictionary with stock data or None if not found
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get historical data for chart (6 months)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=180)
            hist = stock.history(start=start_date, end=end_date)
            
            # Extract key metrics
            data = {
                "ticker": ticker,
                "company_name": info.get("longName", ticker),
                "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
                "previous_close": info.get("previousClose"),
                "day_change": None,
                "day_change_percent": None,
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "dividend_yield": info.get("dividendYield"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
                "volume": info.get("volume"),
                "avg_volume": info.get("averageVolume"),
                "beta": info.get("beta"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "description": info.get("longBusinessSummary"),
                "website": info.get("website"),
                "employees": info.get("fullTimeEmployees"),
                "historical_data": hist.to_dict() if not hist.empty else None,
            }
            
            # Calculate day change
            if data["current_price"] and data["previous_close"]:
                data["day_change"] = data["current_price"] - data["previous_close"]
                data["day_change_percent"] = (data["day_change"] / data["previous_close"]) * 100
            
            return data
            
        except Exception as e:
            print(f"Error fetching stock data for {ticker}: {e}")
            return None
    
    def get_financial_news(self, ticker: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get latest financial news for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            limit: Maximum number of news items
            
        Returns:
            List of news items
        """
        try:
            stock = yf.Ticker(ticker)
            news = stock.news[:limit] if stock.news else []
            
            formatted_news = []
            for item in news:
                formatted_news.append({
                    "title": item.get("title"),
                    "publisher": item.get("publisher"),
                    "link": item.get("link"),
                    "published": datetime.fromtimestamp(item.get("providerPublishTime", 0)),
                    "type": item.get("type"),
                })
            
            return formatted_news
            
        except Exception as e:
            print(f"Error fetching news for {ticker}: {e}")
            return []
    
    def get_analyst_recommendations(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get analyst recommendations for a ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with analyst data or None
        """
        try:
            stock = yf.Ticker(ticker)
            recommendations = stock.recommendations
            
            if recommendations is None or recommendations.empty:
                return None
            
            # Get most recent recommendations
            recent = recommendations.tail(10)
            
            # Count recommendation types
            rec_counts = recent['To Grade'].value_counts().to_dict()
            
            return {
                "recent_recommendations": recent.to_dict('records'),
                "summary": rec_counts,
                "total_analysts": len(recent)
            }
            
        except Exception as e:
            print(f"Error fetching recommendations for {ticker}: {e}")
            return None
    
    def format_stock_summary(self, ticker: str) -> str:
        """
        Generate a formatted summary of stock performance.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Formatted string summary
        """
        data = self.get_stock_data(ticker)
        if not data:
            return f"Stock data not available for {ticker}"
        
        # Format values with proper None handling
        pe_ratio_str = f"{data['pe_ratio']:.2f}" if data['pe_ratio'] else 'N/A'
        beta_str = f"{data['beta']:.2f}" if data['beta'] else 'N/A'
        dividend_str = f"{data['dividend_yield'] * 100:.2f}%" if data['dividend_yield'] else 'N/A'
        market_cap_str = f"${data['market_cap'] / 1e9:.2f}B" if data['market_cap'] else 'N/A'
        
        summary = f"""
Stock Performance Summary: {data['ticker']}

Current Price: ${data['current_price']:.2f}
Day Change: {data['day_change']:+.2f} ({data['day_change_percent']:+.2f}%)
52-Week Range: ${data['52_week_low']:.2f} - ${data['52_week_high']:.2f}

Market Metrics:
- Market Cap: {market_cap_str}
- P/E Ratio: {pe_ratio_str}
- Beta: {beta_str}
- Dividend Yield: {dividend_str}

Sector: {data['sector']}
Industry: {data['industry']}
"""
        return summary.strip()
    
    def is_publicly_traded(self, company_name: str) -> bool:
        """
        Check if a company is publicly traded.
        
        Args:
            company_name: Company name
            
        Returns:
            True if publicly traded, False otherwise
        """
        ticker = self.get_stock_ticker(company_name)
        if not ticker:
            return False
        
        data = self.get_stock_data(ticker)
        return data is not None and data.get("current_price") is not None
