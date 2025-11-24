"""Base agent class for all research agents."""

import asyncio
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel


@dataclass
class ResearchQuery:
    """A single research query."""
    query: str
    priority: int = 1
    category: str = "general"


class BaseResearchAgent(ABC):
    """Abstract base class for all research agents."""
    
    def __init__(
        self,
        name: str,
        llm: BaseChatModel,
        search_tool: Any,
        max_queries: int = 5,
        max_results_per_query: int = 3
    ):
        """Initialize the agent.
        
        Args:
            name: Agent name for logging
            llm: Language model for reasoning
            search_tool: Tool for web search (e.g., Tavily)
            max_queries: Maximum search queries to generate
            max_results_per_query: Maximum results per query
        """
        self.name = name
        self.llm = llm
        self.search_tool = search_tool
        self.max_queries = max_queries
        self.max_results_per_query = max_results_per_query
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass
    
    @abstractmethod
    def get_query_generation_prompt(self, company: str, context: str = "") -> str:
        """Return prompt for generating search queries."""
        pass
    
    @abstractmethod
    def get_extraction_prompt(self, company: str, raw_data: str) -> str:
        """Return prompt for extracting structured data."""
        pass
    
    @abstractmethod
    def get_output_schema(self) -> type[BaseModel]:
        """Return Pydantic model for structured output."""
        pass
    
    async def generate_queries(
        self, 
        company: str, 
        context: str = ""
    ) -> List[ResearchQuery]:
        """Generate targeted search queries.
        
        Args:
            company: Company name to research
            context: Additional context or requirements
            
        Returns:
            List of research queries
        """
        prompt = self.get_query_generation_prompt(company, context)
        
        class QueryList(BaseModel):
            queries: List[str]
        
        structured_llm = self.llm.with_structured_output(QueryList)
        result = structured_llm.invoke([
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=prompt)
        ])
        
        # Convert to ResearchQuery objects
        queries = [
            ResearchQuery(query=q, priority=i+1, category=self.name)
            for i, q in enumerate(result.queries[:self.max_queries])
        ]
        
        return queries
    
    async def execute_searches(
        self, 
        queries: List[ResearchQuery]
    ) -> Dict[str, Any]:
        """Execute all search queries in parallel.
        
        Args:
            queries: List of queries to execute
            
        Returns:
            Dictionary with raw search results
        """
        tasks = []
        for query in queries:
            tasks.append(
                self.search_tool.search(
                    query.query,
                    max_results=self.max_results_per_query,
                    include_raw_content=True
                )
            )
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate results
        raw_data = ""
        sources = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"[{self.name}] Query failed: {queries[i].query} - {result}")
                continue
            
            for item in result.get("results", []):
                content = item.get("content", "")[:3000]  # Limit content
                url = item.get("url", "")
                
                raw_data += f"\n--- SOURCE: {url} ---\n{content}\n"
                sources.append(url)
        
        return {
            "raw_data": raw_data,
            "sources": list(set(sources)),
            "query_count": len(queries),
            "result_count": len(sources)
        }
    
    async def extract_structured_data(
        self,
        company: str,
        raw_data: str
    ) -> BaseModel:
        """Extract structured data from raw search results.
        
        Args:
            company: Company name
            raw_data: Raw text from searches
            
        Returns:
            Structured data according to agent's schema
        """
        prompt = self.get_extraction_prompt(company, raw_data)
        schema = self.get_output_schema()
        
        structured_llm = self.llm.with_structured_output(schema)
        result = structured_llm.invoke([
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=prompt)
        ])
        
        return result
    
    def calculate_confidence_score(
        self,
        extracted_data: BaseModel,
        search_results: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for extracted data.
        
        Args:
            extracted_data: Structured data extracted
            search_results: Raw search results metadata
            
        Returns:
            Confidence score between 0 and 1
        """
        score = 0.0
        
        # Factor 1: Number of sources (max 0.4)
        source_count = search_results.get("result_count", 0)
        score += min(source_count / 10, 0.4)
        
        # Factor 2: Data completeness (max 0.4)
        filled_fields = sum(
            1 for field, value in extracted_data.model_dump().items()
            if value is not None and value != [] and value != {}
        )
        total_fields = len(extracted_data.model_dump())
        score += (filled_fields / total_fields) * 0.4 if total_fields > 0 else 0
        
        # Factor 3: Query success rate (max 0.2)
        query_count = search_results.get("query_count", 1)
        result_count = search_results.get("result_count", 0)
        score += (result_count / (query_count * self.max_results_per_query)) * 0.2
        
        return min(score, 1.0)
    
    async def refine_research(
        self,
        company: str,
        gaps: List[str],
        previous_data: BaseModel,
        previous_sources: List[str]
    ) -> Dict[str, Any]:
        """Targeted re-search for specific data gaps.
        
        Args:
            company: Company name
            gaps: List of specific gaps to fill (as query strings)
            previous_data: Previously extracted data
            previous_sources: Sources already used
            
        Returns:
            Dictionary with updated data, new sources, and metadata
        """
        print(f"[{self.name}] Refining research for {len(gaps)} gaps...")
        
        # Execute targeted searches for gaps
        tasks = []
        for gap_query in gaps:
            tasks.append(
                self.search_tool.search(
                    gap_query,
                    max_results=self.max_results_per_query,
                    include_raw_content=True
                )
            )
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate new results
        raw_data = ""
        new_sources = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"[{self.name}] Refinement query failed: {gaps[i]} - {result}")
                continue
            
            for item in result.get("results", []):
                content = item.get("content", "")[:3000]
                url = item.get("url", "")
                
                # Skip sources we already have
                if url not in previous_sources:
                    raw_data += f"\n--- SOURCE: {url} ---\n{content}\n"
                    new_sources.append(url)
        
        if not raw_data:
            print(f"[{self.name}] No new data found during refinement")
            return {
                "data": previous_data,
                "sources": previous_sources,
                "new_sources": [],
                "gaps_filled": 0
            }
        
        # Extract data from new sources
        extraction_prompt = f"""You are refining previous research for {company}.

PREVIOUS DATA (may have gaps):
{previous_data.model_dump()}

NEW RESEARCH DATA:
{raw_data}

Instructions:
1. Extract any NEW information that fills gaps in the previous data
2. Keep all existing data that was already found
3. Only update fields that were null/empty before
4. Be precise with numbers, dates, and facts
5. If new data contradicts old data, prefer the newer source

Return the COMPLETE updated data structure with gaps filled."""
        
        schema = self.get_output_schema()
        structured_llm = self.llm.with_structured_output(schema)
        
        updated_data = structured_llm.invoke([
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=extraction_prompt)
        ])
        
        # Count how many gaps were filled
        gaps_filled = self._count_filled_gaps(previous_data, updated_data)
        
        print(f"[{self.name}] Filled {gaps_filled} gaps with {len(new_sources)} new sources")
        
        return {
            "data": updated_data,
            "sources": previous_sources + new_sources,
            "new_sources": new_sources,
            "gaps_filled": gaps_filled
        }
    
    def _count_filled_gaps(self, old_data: BaseModel, new_data: BaseModel) -> int:
        """Count how many previously empty fields were filled."""
        old_dict = old_data.model_dump()
        new_dict = new_data.model_dump()
        
        filled = 0
        for key, old_value in old_dict.items():
            new_value = new_dict.get(key)
            
            # Check if field was empty before and filled now
            if self._is_empty(old_value) and not self._is_empty(new_value):
                filled += 1
        
        return filled
    
    def _is_empty(self, value: Any) -> bool:
        """Check if a value is considered empty."""
        if value is None:
            return True
        if isinstance(value, (list, dict)) and len(value) == 0:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        return False
    
    async def research(
        self,
        company: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """Main research method - orchestrates the full workflow.
        
        Args:
            company: Company name to research
            context: Additional context or requirements
            
        Returns:
            Dictionary with structured data, sources, and confidence
        """
        print(f"[{self.name}] Starting research for {company}")
        
        # Step 1: Generate queries
        queries = await self.generate_queries(company, context)
        print(f"[{self.name}] Generated {len(queries)} queries")
        
        # Step 2: Execute searches
        search_results = await self.execute_searches(queries)
        print(f"[{self.name}] Found {search_results['result_count']} sources")
        
        # Step 3: Extract structured data
        structured_data = await self.extract_structured_data(
            company,
            search_results["raw_data"]
        )
        print(f"[{self.name}] Extracted structured data")
        
        # Step 4: Calculate confidence
        confidence = self.calculate_confidence_score(
            structured_data,
            search_results
        )
        print(f"[{self.name}] Confidence score: {confidence:.2f}")
        
        return {
            "data": structured_data,
            "sources": search_results["sources"],
            "confidence_score": confidence,
            "metadata": {
                "agent": self.name,
                "query_count": len(queries),
                "source_count": search_results["result_count"]
            }
        }
