"""Financial Agent - Researches revenue, profitability, funding, and financial health."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from ..base_agent import BaseResearchAgent
from src.tools.data.stock_market import StockMarketTool


class RevenueData(BaseModel):
    """Revenue information."""
    current_revenue: Optional[float] = Field(None, description="Most recent annual revenue in USD")
    revenue_year: Optional[int] = Field(None, description="Year of revenue data")
    yoy_growth_rate: Optional[float] = Field(None, description="Year-over-year growth rate as percentage")
    revenue_breakdown: Optional[Dict[str, Any]] = Field(None, description="Revenue by segment/product")
    currency: str = Field(default="USD", description="Currency of revenue figures")
    is_estimated: bool = Field(False, description="Whether revenue is estimated or official")


class ProfitabilityData(BaseModel):
    """Profitability metrics."""
    is_profitable: Optional[bool] = Field(None, description="Whether company is profitable")
    net_income: Optional[float] = Field(None, description="Net income in USD")
    ebitda: Optional[float] = Field(None, description="EBITDA in USD")
    ebitda_margin: Optional[float] = Field(None, description="EBITDA margin as percentage")
    net_margin: Optional[float] = Field(None, description="Net profit margin as percentage")
    gross_margin: Optional[float] = Field(None, description="Gross margin as percentage")
    burn_rate: Optional[float] = Field(None, description="Monthly cash burn rate for unprofitable companies")


class FundingData(BaseModel):
    """Funding and investment information."""
    total_raised: Optional[float] = Field(None, description="Total funding raised in USD")
    last_round_type: Optional[str] = Field(None, description="Type of last funding round (Seed, Series A, etc.)")
    last_round_amount: Optional[float] = Field(None, description="Amount raised in last round")
    last_round_date: Optional[str] = Field(None, description="Date of last funding round")
    valuation: Optional[float] = Field(None, description="Company valuation in USD")
    investors: List[str] = Field(default_factory=list, description="List of investors")
    is_bootstrapped: bool = Field(False, description="Whether company is bootstrapped")


class FinancialRatios(BaseModel):
    """Key financial ratios."""
    pe_ratio: Optional[float] = Field(None, description="Price-to-earnings ratio")
    ps_ratio: Optional[float] = Field(None, description="Price-to-sales ratio")
    debt_to_equity: Optional[float] = Field(None, description="Debt-to-equity ratio")
    current_ratio: Optional[float] = Field(None, description="Current ratio (liquidity)")
    quick_ratio: Optional[float] = Field(None, description="Quick ratio")


class FinancialOutput(BaseModel):
    """Structured output from Financial Agent."""
    revenue: Optional[RevenueData] = Field(None, description="Revenue information")
    profitability: Optional[ProfitabilityData] = Field(None, description="Profitability metrics")
    funding: Optional[FundingData] = Field(None, description="Funding history")
    financial_ratios: Optional[FinancialRatios] = Field(None, description="Key financial ratios")
    market_cap: Optional[float] = Field(None, description="Market capitalization for public companies")
    stock_ticker: Optional[str] = Field(None, description="Stock ticker symbol if public")
    fiscal_year_end: Optional[str] = Field(None, description="Fiscal year end date")
    financial_health_score: Optional[float] = Field(None, description="Overall financial health score 0-100")
    key_financial_risks: List[str] = Field(default_factory=list, description="Identified financial risks")
    financial_highlights: List[str] = Field(default_factory=list, description="Key financial highlights")
    
    # Stock market data (Phase 3)
    stock_data: Optional[Dict[str, Any]] = Field(None, description="Real-time stock market data")
    financial_news: Optional[List[Dict[str, Any]]] = Field(None, description="Latest financial news")


class FinancialAgent(BaseResearchAgent):
    """Agent specialized in financial research and analysis."""
    
    def __init__(self, *args, **kwargs):
        """Initialize financial agent with stock market tool."""
        super().__init__(*args, **kwargs)
        self.stock_tool = StockMarketTool()
    
    def get_system_prompt(self) -> str:
        return """You are a Financial Analyst specializing in corporate finance and investment analysis.

Your expertise includes:
- Analyzing revenue, profitability, and growth metrics
- Evaluating funding history and investor profiles
- Calculating and interpreting financial ratios
- Assessing financial health and sustainability
- Identifying financial risks and opportunities

You extract precise financial data from SEC filings, investor presentations, financial databases, and credible news sources.
You distinguish between official figures and estimates, and always note the source and date of financial data."""
    
    def get_query_generation_prompt(self, company: str, context: str = "") -> str:
        return f"""Generate {self.max_queries} highly specific search queries to research the financial performance of {company}.

Focus on finding:
1. Annual revenue, growth rates, and revenue breakdown
2. Profitability metrics (EBITDA, net income, margins)
3. Funding history, investors, and valuation
4. Financial ratios and health indicators
5. SEC filings, investor presentations, or financial reports

Requirements:
- Include specific financial terms (revenue, EBITDA, funding, valuation)
- Search for official sources (10-K, investor decks, earnings reports)
- Include year (2024, 2023) for recent data
- Look for both official figures and analyst estimates
- Target financial databases and business news

{f"Additional context: {context}" if context else ""}

Examples:
- "{company} annual revenue 2024 growth rate"
- "{company} EBITDA margin profitability 2023"
- "{company} Series B funding round investors valuation"
- "{company} 10-K SEC filing financial statements"

Return ONLY a JSON object with a "queries" array of strings."""
    
    def get_extraction_prompt(self, company: str, raw_data: str) -> str:
        return f"""Extract structured financial information for {company} from the following research data.

Research Data:
{raw_data}

Instructions:
1. Extract EXACT numbers with currency and year
2. Distinguish between official figures and estimates
3. Include growth rates as percentages
4. List all investors found
5. Note the source and date of financial data
6. Calculate financial health score based on available data
7. If data is missing, leave as null - DO NOT estimate
8. Be precise with financial terminology

Focus on:
- Revenue figures and growth trends
- Profitability metrics (margins, net income, EBITDA)
- Funding rounds, amounts, and investors
- Financial ratios and health indicators
- Market cap and valuation for public/private companies

Financial Health Scoring (0-100):
- 80-100: Strong (profitable, growing, well-funded)
- 60-79: Healthy (positive trajectory, adequate funding)
- 40-59: Moderate (break-even or path to profitability)
- 20-39: Concerning (high burn, funding needed)
- 0-19: Critical (financial distress)

Return structured data according to the schema."""
    
    def get_output_schema(self) -> type[BaseModel]:
        return FinancialOutput

    
    async def research(self, company: str, context: str = "") -> Dict[str, Any]:
        """Enhanced research method with stock market data integration."""
        # Run base research
        result = await super().research(company, context)
        
        # Try to get stock market data
        try:
            ticker = self.stock_tool.get_stock_ticker(company)
            if ticker:
                print(f"[{self.name}] Fetching stock data for {ticker}...")
                stock_data = self.stock_tool.get_stock_data(ticker)
                financial_news = self.stock_tool.get_financial_news(ticker, limit=5)
                
                if stock_data:
                    # Add stock data to result
                    result['data'].stock_data = stock_data
                    result['data'].financial_news = financial_news
                    result['data'].stock_ticker = ticker
                    if stock_data.get('market_cap'):
                        result['data'].market_cap = stock_data['market_cap']
                    
                    print(f"[{self.name}] Added stock data: ${stock_data['current_price']:.2f}, Market Cap: ${stock_data['market_cap']/1e9:.1f}B")
        except Exception as e:
            print(f"[{self.name}] Could not fetch stock data: {e}")
        
        return result
