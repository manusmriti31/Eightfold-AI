"""Profile Agent - Researches business model, products, and revenue streams."""

from typing import List, Optional
from pydantic import BaseModel, Field

from ..base_agent import BaseResearchAgent


class BusinessModel(BaseModel):
    """Business model structure."""
    value_proposition: Optional[str] = Field(None, description="Core value proposition")
    customer_segments: List[str] = Field(default_factory=list, description="Target customer segments")
    revenue_streams: List[str] = Field(default_factory=list, description="How the company makes money")
    key_partnerships: List[str] = Field(default_factory=list, description="Strategic partnerships")
    distribution_channels: List[str] = Field(default_factory=list, description="How products reach customers")


class ProfileOutput(BaseModel):
    """Structured output from Profile Agent."""
    company_name: str = Field(..., description="Official company name")
    founded: Optional[int] = Field(None, description="Year founded")
    ownership_type: Optional[str] = Field(None, description="Public, Private, or Subsidiary")
    headquarters: Optional[str] = Field(None, description="HQ location")
    employee_count: Optional[int] = Field(None, description="Number of employees")
    business_model: Optional[BusinessModel] = Field(None, description="Business model details")
    products_services: List[str] = Field(default_factory=list, description="Main products and services")
    subsidiaries: List[str] = Field(default_factory=list, description="Subsidiary companies")
    parent_company: Optional[str] = Field(None, description="Parent company if applicable")
    mission_vision: Optional[str] = Field(None, description="Company mission and vision")


class ProfileAgent(BaseResearchAgent):
    """Agent specialized in company profile and business model research."""
    
    def get_system_prompt(self) -> str:
        return """You are a Business Model Analyst specializing in understanding how companies operate and generate revenue.

Your expertise includes:
- Identifying business model patterns (B2B, B2C, marketplace, SaaS, etc.)
- Understanding revenue streams and pricing strategies
- Analyzing value propositions and customer segments
- Mapping organizational structures and subsidiaries

You provide factual, structured information based on reliable sources."""
    
    def get_query_generation_prompt(self, company: str, context: str = "") -> str:
        return f"""Generate {self.max_queries} highly specific search queries to research the business profile of {company}.

Focus on finding:
1. Official company information (founding, ownership, structure)
2. Business model and how they make money
3. Products and services offered
4. Revenue streams and pricing models
5. Subsidiaries and parent company relationships

Requirements:
- Use specific terms like "business model", "revenue streams", "products"
- Include year (2024) for recent information
- Avoid generic terms like "overview" or "about"
- Target official sources, investor presentations, and business databases

{f"Additional context: {context}" if context else ""}

Return ONLY a JSON object with a "queries" array of strings."""
    
    def get_extraction_prompt(self, company: str, raw_data: str) -> str:
        return f"""Extract structured business profile information for {company} from the following research data.

Research Data:
{raw_data}

Instructions:
1. Extract factual information only - no speculation
2. Use specific numbers and dates when available
3. If information is not found, leave the field as null/empty
4. For lists, include all relevant items found
5. Prioritize recent information (2023-2024)
6. Be precise with company names and terminology

Focus on:
- Official company details (name, founding year, ownership)
- Business model components (value prop, customers, revenue)
- Products and services
- Corporate structure (subsidiaries, parent company)

Return structured data according to the schema."""
    
    def get_output_schema(self) -> type[BaseModel]:
        return ProfileOutput
