"""Signals Agent - Researches news, sentiment, risks, and real-time signals."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

from ..base_agent import BaseResearchAgent


class NewsItem(BaseModel):
    """Individual news item."""
    title: str = Field(..., description="News headline")
    date: Optional[str] = Field(None, description="Publication date")
    summary: str = Field(..., description="Brief summary of the news")
    sentiment: Optional[str] = Field(None, description="Sentiment: Positive/Negative/Neutral")
    source: Optional[str] = Field(None, description="News source")
    url: Optional[str] = Field(None, description="Article URL")
    impact_level: Optional[str] = Field(None, description="Impact level: High/Medium/Low")


class EmployeeSentiment(BaseModel):
    """Employee sentiment data."""
    glassdoor_rating: Optional[float] = Field(None, description="Glassdoor overall rating (1-5)")
    glassdoor_reviews_count: Optional[int] = Field(None, description="Number of Glassdoor reviews")
    recommend_to_friend: Optional[float] = Field(None, description="% who would recommend to a friend")
    ceo_approval: Optional[float] = Field(None, description="CEO approval rating percentage")
    culture_rating: Optional[float] = Field(None, description="Culture and values rating")
    work_life_balance: Optional[float] = Field(None, description="Work-life balance rating")
    common_praises: List[str] = Field(default_factory=list, description="Common positive themes")
    common_complaints: List[str] = Field(default_factory=list, description="Common negative themes")


class RiskItem(BaseModel):
    """Risk or controversy."""
    risk_type: str = Field(..., description="Type: Legal/Financial/Reputational/Operational/Regulatory")
    title: str = Field(..., description="Brief title of the risk")
    description: str = Field(..., description="Detailed description")
    severity: str = Field(..., description="Severity: Critical/High/Medium/Low")
    date_identified: Optional[str] = Field(None, description="When the risk was identified")
    status: Optional[str] = Field(None, description="Status: Active/Resolved/Monitoring")
    potential_impact: Optional[str] = Field(None, description="Potential business impact")


class HiringTrends(BaseModel):
    """Hiring and growth signals."""
    open_positions: Optional[int] = Field(None, description="Number of open job positions")
    hiring_velocity: Optional[str] = Field(None, description="Hiring pace: Aggressive/Moderate/Slow/Frozen")
    top_hiring_roles: List[str] = Field(default_factory=list, description="Most common open roles")
    growth_areas: List[str] = Field(default_factory=list, description="Departments/functions expanding")
    layoffs_recent: Optional[bool] = Field(None, description="Recent layoffs reported")
    headcount_trend: Optional[str] = Field(None, description="Headcount trend: Growing/Stable/Declining")


class SocialSentiment(BaseModel):
    """Social media and public sentiment."""
    twitter_sentiment: Optional[str] = Field(None, description="Twitter sentiment: Positive/Negative/Neutral/Mixed")
    reddit_sentiment: Optional[str] = Field(None, description="Reddit sentiment")
    customer_reviews_rating: Optional[float] = Field(None, description="Average customer review rating")
    brand_perception: Optional[str] = Field(None, description="Overall brand perception summary")
    viral_moments: List[str] = Field(default_factory=list, description="Recent viral moments or PR events")


class SignalsOutput(BaseModel):
    """Structured output from Signals Agent."""
    recent_news: List[NewsItem] = Field(default_factory=list, description="Recent news (last 6 months)")
    employee_sentiment: Optional[EmployeeSentiment] = Field(None, description="Employee reviews and sentiment")
    risks: List[RiskItem] = Field(default_factory=list, description="Identified risks and controversies")
    hiring_trends: Optional[HiringTrends] = Field(None, description="Hiring and growth signals")
    social_sentiment: Optional[SocialSentiment] = Field(None, description="Social media sentiment")
    regulatory_issues: List[str] = Field(default_factory=list, description="Regulatory challenges or investigations")
    partnerships_announced: List[str] = Field(default_factory=list, description="Recent partnerships or deals")
    product_launches: List[str] = Field(default_factory=list, description="Recent product launches")
    overall_momentum: Optional[str] = Field(None, description="Overall momentum: Accelerating/Stable/Declining")
    red_flags: List[str] = Field(default_factory=list, description="Critical red flags identified")


class SignalsAgent(BaseResearchAgent):
    """Agent specialized in real-time signals, news, sentiment, and risk detection."""
    
    def get_system_prompt(self) -> str:
        return """You are a Risk Intelligence Analyst specializing in real-time signals, sentiment analysis, and early warning detection.

Your expertise includes:
- Monitoring recent news and developments
- Analyzing employee sentiment and culture
- Identifying legal, financial, and reputational risks
- Tracking hiring trends and organizational changes
- Assessing social media and public sentiment
- Detecting red flags and warning signs

You extract data from news sources, Glassdoor, LinkedIn, social media, regulatory filings, and public forums.
You provide objective risk assessments and distinguish between minor issues and critical red flags."""
    
    def get_query_generation_prompt(self, company: str, context: str = "") -> str:
        return f"""Generate {self.max_queries} highly specific search queries to research real-time signals and risks for {company}.

Focus on finding:
1. Recent news, announcements, and developments (last 6 months)
2. Employee reviews and sentiment (Glassdoor, Blind)
3. Legal issues, lawsuits, or controversies
4. Hiring trends and job postings
5. Social media sentiment and viral moments

Requirements:
- Include time-bound terms (2024, "last 6 months", recent)
- Search for both positive and negative signals
- Look for Glassdoor reviews and employee feedback
- Include terms like "lawsuit", "controversy", "scandal", "layoffs"
- Search LinkedIn for hiring trends
- Check social media sentiment

{f"Additional context: {context}" if context else ""}

Examples:
- "{company} news 2024 latest developments"
- "{company} Glassdoor reviews employee sentiment"
- "{company} lawsuit legal issues controversy"
- "{company} hiring trends job openings LinkedIn"
- "{company} Twitter Reddit sentiment customer reviews"

Return ONLY a JSON object with a "queries" array of strings."""
    
    def get_extraction_prompt(self, company: str, raw_data: str) -> str:
        return f"""Extract structured signals and risk information for {company} from the following research data.

Research Data:
{raw_data}

Instructions:
1. Extract recent news (last 6 months) with dates and sentiment
2. Gather employee sentiment data from Glassdoor/reviews
3. Identify ALL risks: legal, financial, reputational, operational
4. Note hiring trends and organizational changes
5. Assess social media and public sentiment
6. Flag critical red flags that need immediate attention
7. Classify risk severity objectively
8. Include dates and sources for all items

Focus on:
- Recent news and developments
- Employee satisfaction and culture
- Legal issues, lawsuits, controversies
- Hiring velocity and layoffs
- Social media sentiment
- Regulatory challenges
- Product launches and partnerships

Risk Severity Classification:
- Critical: Existential threat, major lawsuit, fraud allegations
- High: Significant financial impact, regulatory investigation, mass layoffs
- Medium: Moderate reputational damage, minor legal issues, customer complaints
- Low: Minor issues, resolved controversies, normal business challenges

Red Flags (Critical Issues):
- Fraud or financial misconduct
- Major lawsuits or regulatory investigations
- Mass layoffs or executive exodus
- Product failures or safety issues
- Severe reputational damage

Overall Momentum Assessment:
- Accelerating: Positive news, hiring, partnerships, product launches
- Stable: Normal operations, mixed signals
- Declining: Negative news, layoffs, controversies, declining sentiment

Return structured data according to the schema."""
    
    def get_output_schema(self) -> type[BaseModel]:
        return SignalsOutput
