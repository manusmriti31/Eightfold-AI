"""Gap Detector Agent - Identifies missing data and generates refinement queries."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage


class GapPriority(str, Enum):
    """Priority levels for data gaps."""
    CRITICAL = "critical"  # Essential data (e.g., revenue, CEO name)
    HIGH = "high"          # Important data (e.g., funding, market size)
    MEDIUM = "medium"      # Useful data (e.g., employee count, subsidiaries)
    LOW = "low"            # Nice-to-have (e.g., mission statement)


@dataclass
class Gap:
    """Represents a missing or incomplete data field."""
    field_name: str
    agent_name: str
    priority: GapPriority
    field_type: str  # e.g., "revenue", "person_profile", "market_data"
    context: Optional[str] = None  # Additional context about what's missing
    attempted_queries: List[str] = None
    filled: bool = False
    
    def __post_init__(self):
        if self.attempted_queries is None:
            self.attempted_queries = []


class GapDetectorAgent:
    """Agent that detects data gaps and generates targeted refinement queries."""
    
    # Critical fields by agent type
    CRITICAL_FIELDS = {
        "profile": ["company_name", "business_model", "products_services"],
        "leadership": ["founders", "ceo"],
        "financial": ["revenue", "profitability"],
        "market": ["market", "competitors"],
        "signals": ["recent_news", "risks"]
    }
    
    HIGH_PRIORITY_FIELDS = {
        "profile": ["founded", "ownership_type", "revenue_streams"],
        "leadership": ["cto", "cfo", "leadership_style"],
        "financial": ["funding", "financial_health_score"],
        "market": ["swot", "market_position"],
        "signals": ["employee_sentiment", "hiring_trends"]
    }
    
    def __init__(self, llm: BaseChatModel):
        """Initialize gap detector.
        
        Args:
            llm: Language model for generating refinement queries
        """
        self.llm = llm
    
    def analyze_gaps(
        self,
        agent_name: str,
        structured_data: BaseModel,
        company: str
    ) -> List[Gap]:
        """Analyze structured data to find missing or incomplete fields.
        
        Args:
            agent_name: Name of the agent (profile, leadership, etc.)
            structured_data: Extracted structured data
            company: Company name being researched
            
        Returns:
            List of identified gaps with priorities
        """
        gaps = []
        data_dict = structured_data.model_dump()
        
        # Check critical fields
        for field in self.CRITICAL_FIELDS.get(agent_name, []):
            if self._is_field_empty(data_dict.get(field)):
                gaps.append(Gap(
                    field_name=field,
                    agent_name=agent_name,
                    priority=GapPriority.CRITICAL,
                    field_type=field,
                    context=f"Missing critical {field} data for {company}"
                ))
        
        # Check high priority fields
        for field in self.HIGH_PRIORITY_FIELDS.get(agent_name, []):
            if self._is_field_empty(data_dict.get(field)):
                gaps.append(Gap(
                    field_name=field,
                    agent_name=agent_name,
                    priority=GapPriority.HIGH,
                    field_type=field,
                    context=f"Missing {field} data for {company}"
                ))
        
        # Check for incomplete nested data
        gaps.extend(self._check_nested_gaps(agent_name, data_dict, company))
        
        return gaps
    
    def _is_field_empty(self, value: Any) -> bool:
        """Check if a field is empty or missing."""
        if value is None:
            return True
        if isinstance(value, (list, dict)) and len(value) == 0:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        return False
    
    def _check_nested_gaps(
        self,
        agent_name: str,
        data_dict: Dict[str, Any],
        company: str
    ) -> List[Gap]:
        """Check for incomplete nested data structures."""
        gaps = []
        
        if agent_name == "financial":
            # Check revenue data completeness
            revenue = data_dict.get("revenue")
            if revenue and isinstance(revenue, dict):
                if not revenue.get("current_revenue"):
                    gaps.append(Gap(
                        field_name="revenue.current_revenue",
                        agent_name=agent_name,
                        priority=GapPriority.CRITICAL,
                        field_type="revenue",
                        context=f"Missing current revenue amount for {company}"
                    ))
                if not revenue.get("yoy_growth_rate"):
                    gaps.append(Gap(
                        field_name="revenue.yoy_growth_rate",
                        agent_name=agent_name,
                        priority=GapPriority.HIGH,
                        field_type="revenue",
                        context=f"Missing revenue growth rate for {company}"
                    ))
            
            # Check profitability data
            profitability = data_dict.get("profitability")
            if profitability and isinstance(profitability, dict):
                if profitability.get("is_profitable") is None:
                    gaps.append(Gap(
                        field_name="profitability.is_profitable",
                        agent_name=agent_name,
                        priority=GapPriority.CRITICAL,
                        field_type="profitability",
                        context=f"Missing profitability status for {company}"
                    ))
        
        elif agent_name == "leadership":
            # Check if CEO profile is incomplete
            ceo = data_dict.get("ceo")
            if ceo and isinstance(ceo, dict):
                if not ceo.get("background"):
                    gaps.append(Gap(
                        field_name="ceo.background",
                        agent_name=agent_name,
                        priority=GapPriority.HIGH,
                        field_type="person_profile",
                        context=f"Missing CEO background for {company}"
                    ))
        
        elif agent_name == "market":
            # Check market data completeness
            market = data_dict.get("market")
            if market and isinstance(market, dict):
                if not market.get("tam"):
                    gaps.append(Gap(
                        field_name="market.tam",
                        agent_name=agent_name,
                        priority=GapPriority.HIGH,
                        field_type="market_size",
                        context=f"Missing TAM (Total Addressable Market) for {company}"
                    ))
        
        return gaps
    
    def prioritize_gaps(self, gaps: List[Gap]) -> List[Gap]:
        """Sort gaps by priority for refinement.
        
        Args:
            gaps: List of identified gaps
            
        Returns:
            Sorted list with critical gaps first
        """
        priority_order = {
            GapPriority.CRITICAL: 0,
            GapPriority.HIGH: 1,
            GapPriority.MEDIUM: 2,
            GapPriority.LOW: 3
        }
        
        return sorted(gaps, key=lambda g: priority_order[g.priority])
    
    async def generate_refinement_queries(
        self,
        gap: Gap,
        company: str,
        previous_queries: List[str] = None
    ) -> List[str]:
        """Generate targeted search queries to fill a specific gap.
        
        Args:
            gap: The gap to fill
            company: Company name
            previous_queries: Queries already attempted (to avoid duplicates)
            
        Returns:
            List of 3-5 highly specific search queries
        """
        previous_queries = previous_queries or []
        
        # Build prompt for query generation
        # Handle both enum and string priority
        priority_str = gap.priority.value if hasattr(gap.priority, 'value') else gap.priority
        
        prompt = f"""You are a research query specialist. Generate 5 highly specific search queries to find missing data.

Company: {company}
Missing Data: {gap.field_name}
Context: {gap.context}
Priority: {priority_str}

Previous queries that didn't work:
{chr(10).join(f"- {q}" for q in previous_queries) if previous_queries else "None"}

Generate NEW queries that:
1. Use different search terms and angles
2. Target specific sources (SEC filings, press releases, investor decks)
3. Include year (2024, 2023) for recent data
4. Use industry-specific terminology
5. Try alternative phrasings

Examples for financial data:
- "{company} 10-K SEC filing 2024 annual revenue"
- "{company} Q4 2024 earnings call transcript revenue"
- "{company} investor presentation 2024 financial results"

Examples for leadership data:
- "{company} CEO biography career history LinkedIn"
- "{company} founder background previous companies"
- "{company} executive team management bios"

Return ONLY a JSON object with a "queries" array of 5 strings."""
        
        class QueryList(BaseModel):
            queries: List[str]
        
        structured_llm = self.llm.with_structured_output(QueryList)
        result = structured_llm.invoke([
            SystemMessage(content="You are a research query specialist who generates highly targeted search queries."),
            HumanMessage(content=prompt)
        ])
        
        # Filter out queries too similar to previous ones
        new_queries = []
        for query in result.queries:
            if not self._is_similar_to_previous(query, previous_queries):
                new_queries.append(query)
        
        return new_queries[:5]  # Return max 5 queries
    
    def _is_similar_to_previous(self, query: str, previous: List[str]) -> bool:
        """Check if query is too similar to previous queries."""
        query_lower = query.lower()
        for prev in previous:
            prev_lower = prev.lower()
            # Simple similarity check - if >70% of words overlap
            query_words = set(query_lower.split())
            prev_words = set(prev_lower.split())
            if len(query_words & prev_words) / len(query_words | prev_words) > 0.7:
                return True
        return False
    
    def should_continue_refining(
        self,
        iteration: int,
        max_iterations: int,
        gaps_filled: int,
        total_gaps: int
    ) -> bool:
        """Decide whether to continue refinement iterations.
        
        Args:
            iteration: Current iteration number
            max_iterations: Maximum allowed iterations
            gaps_filled: Number of gaps filled so far
            total_gaps: Total number of gaps
            
        Returns:
            True if should continue refining
        """
        # Stop if max iterations reached
        if iteration >= max_iterations:
            return False
        
        # Stop if all gaps filled
        if gaps_filled >= total_gaps:
            return False
        
        # Stop if no progress in last iteration (would need tracking)
        # For now, always continue until max iterations
        return True
    
    def calculate_gap_fill_rate(self, gaps: List[Gap]) -> float:
        """Calculate percentage of gaps that were filled.
        
        Args:
            gaps: List of gaps with filled status
            
        Returns:
            Fill rate as percentage (0-100)
        """
        if not gaps:
            return 100.0
        
        filled = sum(1 for g in gaps if g.filled)
        return (filled / len(gaps)) * 100
    
    def get_refinement_summary(self, gaps: List[Gap]) -> Dict[str, Any]:
        """Generate summary of refinement results.
        
        Args:
            gaps: List of gaps with filled status
            
        Returns:
            Summary dictionary with statistics
        """
        total = len(gaps)
        filled = sum(1 for g in gaps if g.filled)
        by_priority = {
            "critical": sum(1 for g in gaps if g.priority == GapPriority.CRITICAL),
            "high": sum(1 for g in gaps if g.priority == GapPriority.HIGH),
            "medium": sum(1 for g in gaps if g.priority == GapPriority.MEDIUM),
            "low": sum(1 for g in gaps if g.priority == GapPriority.LOW),
        }
        filled_by_priority = {
            "critical": sum(1 for g in gaps if g.priority == GapPriority.CRITICAL and g.filled),
            "high": sum(1 for g in gaps if g.priority == GapPriority.HIGH and g.filled),
            "medium": sum(1 for g in gaps if g.priority == GapPriority.MEDIUM and g.filled),
            "low": sum(1 for g in gaps if g.priority == GapPriority.LOW and g.filled),
        }
        
        return {
            "total_gaps": total,
            "gaps_filled": filled,
            "gaps_remaining": total - filled,
            "fill_rate": self.calculate_gap_fill_rate(gaps),
            "by_priority": by_priority,
            "filled_by_priority": filled_by_priority,
            "critical_gaps_remaining": by_priority["critical"] - filled_by_priority["critical"]
        }
