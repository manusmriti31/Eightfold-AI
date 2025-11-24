"""Leadership Agent - Researches founders, executives, and management team."""

from typing import List, Optional
from pydantic import BaseModel, Field

from ..base_agent import BaseResearchAgent


class PersonProfile(BaseModel):
    """Individual person profile."""
    name: str = Field(..., description="Full name")
    role: Optional[str] = Field(None, description="Current role/title")
    background: Optional[str] = Field(None, description="Professional background summary")
    previous_companies: List[str] = Field(default_factory=list, description="Previous companies worked at")
    education: Optional[str] = Field(None, description="Educational background")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    notable_achievements: List[str] = Field(default_factory=list, description="Key achievements")


class LeadershipOutput(BaseModel):
    """Structured output from Leadership Agent."""
    founders: List[PersonProfile] = Field(default_factory=list, description="Company founders")
    ceo: Optional[PersonProfile] = Field(None, description="Current CEO")
    cto: Optional[PersonProfile] = Field(None, description="Current CTO")
    cfo: Optional[PersonProfile] = Field(None, description="Current CFO")
    other_executives: List[PersonProfile] = Field(default_factory=list, description="Other C-suite executives")
    board_members: List[str] = Field(default_factory=list, description="Board of directors members")
    leadership_style: Optional[str] = Field(None, description="Leadership philosophy and culture")
    succession_plan: Optional[str] = Field(None, description="Succession planning information")
    key_person_risks: List[str] = Field(default_factory=list, description="Risks related to key personnel")
    management_changes: List[str] = Field(default_factory=list, description="Recent leadership changes")


class LeadershipAgent(BaseResearchAgent):
    """Agent specialized in researching company leadership and management."""
    
    def get_system_prompt(self) -> str:
        return """You are an Executive Research Analyst specializing in leadership assessment and organizational analysis.

Your expertise includes:
- Profiling founders and their entrepreneurial backgrounds
- Analyzing executive team composition and experience
- Identifying leadership strengths and potential risks
- Tracking management changes and their implications
- Evaluating board composition and governance

You provide factual, objective assessments based on public information, LinkedIn profiles, interviews, and company announcements."""
    
    def get_query_generation_prompt(self, company: str, context: str = "") -> str:
        return f"""Generate {self.max_queries} highly specific search queries to research the leadership team of {company}.

Focus on finding:
1. Founder backgrounds, previous ventures, and education
2. Current CEO, CTO, CFO profiles and experience
3. Executive team composition and LinkedIn profiles
4. Recent leadership changes or appointments
5. Board of directors and advisors

Requirements:
- Include specific role titles (CEO, CTO, CFO, founder)
- Search for LinkedIn profiles and professional backgrounds
- Look for interviews, podcasts, and public statements
- Include terms like "biography", "career history", "previous companies"
- Target recent information (2023-2024) for current roles

{f"Additional context: {context}" if context else ""}

Examples:
- "{company} founder CEO biography career history"
- "{company} CTO LinkedIn profile background"
- "{company} executive team management changes 2024"

Return ONLY a JSON object with a "queries" array of strings."""
    
    def get_extraction_prompt(self, company: str, raw_data: str) -> str:
        return f"""Extract structured leadership information for {company} from the following research data.

Research Data:
{raw_data}

Instructions:
1. Identify all founders with their backgrounds
2. Extract current C-suite executives (CEO, CTO, CFO, etc.)
3. Include LinkedIn URLs when found
4. List previous companies and notable achievements
5. Note any recent leadership changes
6. Identify potential key person risks
7. If information is not found, leave fields as null/empty
8. Be precise with names, titles, and dates

Focus on:
- Founder profiles and their journey
- Current executive team composition
- Professional backgrounds and education
- Leadership style and company culture
- Recent changes or succession planning

Return structured data according to the schema."""
    
    def get_output_schema(self) -> type[BaseModel]:
        return LeadershipOutput
