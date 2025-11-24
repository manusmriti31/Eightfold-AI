"""State management for multi-agent research system."""

from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict
from enum import Enum


class ReportType(str, Enum):
    """Types of reports that can be generated."""
    INVESTMENT_MEMO = "investment_memo"
    SALES_ACCOUNT_PLAN = "sales_account_plan"
    DUE_DILIGENCE = "due_diligence"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"


@dataclass
class ProfileData:
    """Output from Profile Agent."""
    company_name: str
    founded: Optional[int] = None
    ownership_type: Optional[str] = None
    business_model: Optional[Dict[str, Any]] = None
    products_services: List[str] = field(default_factory=list)
    revenue_streams: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    sources: List[str] = field(default_factory=list)


@dataclass
class LeadershipData:
    """Output from Leadership Agent."""
    founders: List[Dict[str, Any]] = field(default_factory=list)
    executives: List[Dict[str, Any]] = field(default_factory=list)
    leadership_style: Optional[str] = None
    key_risks: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    sources: List[str] = field(default_factory=list)


@dataclass
class FinancialData:
    """Output from Financial Agent."""
    revenue: Optional[Dict[str, Any]] = None
    profitability: Optional[Dict[str, Any]] = None
    funding: Optional[Dict[str, Any]] = None
    financial_ratios: Optional[Dict[str, Any]] = None
    financial_health_score: float = 0.0
    confidence_score: float = 0.0
    sources: List[str] = field(default_factory=list)
    
    # Stock market data (Phase 3)
    stock_data: Optional[Dict[str, Any]] = None
    financial_news: Optional[List[Dict[str, Any]]] = None
    stock_ticker: Optional[str] = None


@dataclass
class MarketData:
    """Output from Market Agent."""
    market: Optional[Dict[str, Any]] = None
    competitors: List[Dict[str, Any]] = field(default_factory=list)
    swot: Optional[Dict[str, List[str]]] = None
    market_position: Optional[str] = None
    confidence_score: float = 0.0
    sources: List[str] = field(default_factory=list)


@dataclass
class SignalsData:
    """Output from Signals & Risk Agent."""
    recent_news: List[Dict[str, Any]] = field(default_factory=list)
    employee_sentiment: Optional[Dict[str, Any]] = None
    risks: List[Dict[str, Any]] = field(default_factory=list)
    hiring_trends: Optional[Dict[str, Any]] = None
    social_sentiment: Optional[str] = None
    confidence_score: float = 0.0
    sources: List[str] = field(default_factory=list)


@dataclass
class VerificationResult:
    """Output from Verification Agent."""
    contradictions: List[Dict[str, Any]] = field(default_factory=list)
    verified_facts: List[Dict[str, Any]] = field(default_factory=list)
    confidence_adjustments: Dict[str, float] = field(default_factory=dict)
    overall_reliability: float = 0.0


@dataclass
class CritiqueResult:
    """Output from Critic Agent."""
    missing_fields: List[str] = field(default_factory=list)
    vague_statements: List[Dict[str, str]] = field(default_factory=list)
    follow_up_queries: List[str] = field(default_factory=list)
    needs_refinement: bool = False
    quality_score: float = 0.0


@dataclass
class UserInteraction:
    """User questions and answers."""
    questions: List[Dict[str, Any]] = field(default_factory=list)
    answers: Dict[str, Any] = field(default_factory=dict)
    clarifications: List[str] = field(default_factory=list)


@dataclass
class InputState:
    """Input from user."""
    company: str
    report_type: ReportType = ReportType.INVESTMENT_MEMO
    focus_areas: List[str] = field(default_factory=lambda: [
        "profile", "leadership", "financial", "market", "signals"
    ])
    user_requirements: Optional[Dict[str, Any]] = None
    additional_context: Optional[str] = None


@dataclass
class Gap:
    """Represents a missing data field."""
    field_name: str
    agent_name: str
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    field_type: str
    context: Optional[str] = None
    attempted_queries: List[str] = field(default_factory=list)
    filled: bool = False


@dataclass
class RefinementMetadata:
    """Tracks refinement process for one iteration."""
    iteration: int
    gaps_detected: int
    gaps_filled: int
    queries_generated: int
    sources_found: int
    confidence_improvement: float = 0.0


@dataclass
class MultiAgentState(InputState):
    """Complete state flowing through the graph."""
    
    # Research Agent Outputs
    profile_data: Optional[ProfileData] = None
    leadership_data: Optional[LeadershipData] = None
    financial_data: Optional[FinancialData] = None
    market_data: Optional[MarketData] = None
    signals_data: Optional[SignalsData] = None
    
    # Aggregated Data
    aggregated_data: Optional[Dict[str, Any]] = None
    all_sources: List[str] = field(default_factory=list)
    
    # Intelligence Layer Outputs
    verification_result: Optional[VerificationResult] = None
    critique_result: Optional[CritiqueResult] = None
    user_interaction: Optional[UserInteraction] = None
    
    # Refinement Tracking
    gaps: List[Gap] = field(default_factory=list)
    refinement_metadata: List[RefinementMetadata] = field(default_factory=list)
    refinement_iteration: int = 0
    max_refinement_iterations: int = 2
    gaps_filled_count: int = 0
    
    # Processing Metadata
    research_complete: bool = False
    gap_detection_complete: bool = False
    refinement_complete: bool = False
    verification_complete: bool = False
    critique_complete: bool = False
    interaction_complete: bool = False
    
    # Final Output
    final_report: Optional[str] = None
    executive_summary: Optional[str] = None
    report_metadata: Optional[Dict[str, Any]] = None


@dataclass
class OutputState:
    """Final output to user."""
    final_report: str
    executive_summary: str
    report_metadata: Dict[str, Any]
    all_sources: List[str]
    confidence_scores: Dict[str, float]
    
    # Include agent data for report formatting (Phase 2)
    profile_data: Optional[ProfileData] = None
    leadership_data: Optional[LeadershipData] = None
    financial_data: Optional[FinancialData] = None
    market_data: Optional[MarketData] = None
    signals_data: Optional[SignalsData] = None
