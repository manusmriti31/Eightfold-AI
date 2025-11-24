"""Market Agent - Researches market size, competitors, and competitive positioning."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from ..base_agent import BaseResearchAgent


class MarketSize(BaseModel):
    """Market size information."""
    tam: Optional[float] = Field(None, description="Total Addressable Market in USD")
    sam: Optional[float] = Field(None, description="Serviceable Addressable Market in USD")
    som: Optional[float] = Field(None, description="Serviceable Obtainable Market in USD")
    market_growth_rate: Optional[float] = Field(None, description="Annual market growth rate as percentage")
    market_year: Optional[int] = Field(None, description="Year of market data")
    industry: Optional[str] = Field(None, description="Primary industry/sector")
    sub_industry: Optional[str] = Field(None, description="Sub-industry or niche")


class Competitor(BaseModel):
    """Competitor information."""
    name: str = Field(..., description="Competitor name")
    market_share: Optional[float] = Field(None, description="Market share as percentage")
    revenue: Optional[float] = Field(None, description="Competitor revenue in USD")
    differentiation: Optional[str] = Field(None, description="How they differ from target company")
    strengths: List[str] = Field(default_factory=list, description="Competitor strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Competitor weaknesses")


class SWOTAnalysis(BaseModel):
    """SWOT analysis."""
    strengths: List[str] = Field(default_factory=list, description="Company strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Company weaknesses")
    opportunities: List[str] = Field(default_factory=list, description="Market opportunities")
    threats: List[str] = Field(default_factory=list, description="External threats")


class PortersFiveForces(BaseModel):
    """Porter's Five Forces analysis."""
    competitive_rivalry: Optional[str] = Field(None, description="Level of competitive rivalry (High/Medium/Low)")
    supplier_power: Optional[str] = Field(None, description="Bargaining power of suppliers")
    buyer_power: Optional[str] = Field(None, description="Bargaining power of buyers")
    threat_of_substitutes: Optional[str] = Field(None, description="Threat of substitute products")
    threat_of_new_entrants: Optional[str] = Field(None, description="Threat of new entrants")


class MarketOutput(BaseModel):
    """Structured output from Market Agent."""
    market: Optional[MarketSize] = Field(None, description="Market size and growth")
    competitors: List[Competitor] = Field(default_factory=list, description="Main competitors")
    market_position: Optional[str] = Field(None, description="Company's market position (Leader/Challenger/Niche)")
    market_share: Optional[float] = Field(None, description="Company's market share as percentage")
    competitive_advantages: List[str] = Field(default_factory=list, description="Key competitive advantages")
    barriers_to_entry: List[str] = Field(default_factory=list, description="Barriers protecting the business")
    swot: Optional[SWOTAnalysis] = Field(None, description="SWOT analysis")
    porters_five_forces: Optional[PortersFiveForces] = Field(None, description="Porter's Five Forces")
    market_trends: List[str] = Field(default_factory=list, description="Key market trends")
    target_customers: List[str] = Field(default_factory=list, description="Target customer segments")
    geographic_markets: List[str] = Field(default_factory=list, description="Geographic markets served")


class MarketAgent(BaseResearchAgent):
    """Agent specialized in market analysis and competitive intelligence."""
    
    def get_system_prompt(self) -> str:
        return """You are a Market Research Analyst specializing in competitive intelligence and industry analysis.

Your expertise includes:
- Sizing markets (TAM, SAM, SOM) and growth projections
- Competitive landscape mapping and positioning
- SWOT and Porter's Five Forces analysis
- Identifying competitive advantages and moats
- Analyzing market trends and dynamics

You extract data from market research reports, industry analyses, competitor websites, and business intelligence sources.
You provide objective assessments of competitive positioning and market opportunities."""
    
    def get_query_generation_prompt(self, company: str, context: str = "") -> str:
        return f"""Generate {self.max_queries} highly specific search queries to research the market and competitive landscape for {company}.

Focus on finding:
1. Market size (TAM, SAM) and growth rates for their industry
2. Main competitors and competitive positioning
3. Market share data and rankings
4. SWOT analysis and competitive advantages
5. Industry trends and market dynamics

Requirements:
- Include market research terms (TAM, market size, industry analysis)
- Search for competitor comparisons and rankings
- Look for analyst reports and market research
- Include industry-specific terminology
- Target recent data (2023-2024)

{f"Additional context: {context}" if context else ""}

Examples:
- "{company} industry market size TAM SAM 2024"
- "{company} competitors comparison market share"
- "{company} vs [competitor] competitive analysis"
- "{company} SWOT analysis competitive advantages"
- "[industry] market trends growth forecast 2024"

Return ONLY a JSON object with a "queries" array of strings."""
    
    def get_extraction_prompt(self, company: str, raw_data: str) -> str:
        return f"""Extract structured market and competitive information for {company} from the following research data.

Research Data:
{raw_data}

Instructions:
1. Extract market size figures (TAM, SAM) with year and source
2. Identify top 3-5 competitors with details
3. Determine company's market position (Leader/Challenger/Niche Player)
4. Conduct SWOT analysis based on available information
5. List competitive advantages and barriers to entry
6. Note market trends affecting the industry
7. If data is missing, leave as null/empty
8. Be specific with numbers and percentages

Focus on:
- Market size and growth projections
- Competitive landscape and key players
- Company's market share and positioning
- Strengths, weaknesses, opportunities, threats
- Competitive advantages and moats
- Industry trends and dynamics

Market Position Definitions:
- Leader: Top 3 player, >20% market share, sets industry standards
- Challenger: Top 10 player, 5-20% share, growing rapidly
- Niche Player: Specialized focus, <5% share, strong in segment
- Emerging: New entrant, <1% share, high growth potential

Return structured data according to the schema."""
    
    def get_output_schema(self) -> type[BaseModel]:
        return MarketOutput
