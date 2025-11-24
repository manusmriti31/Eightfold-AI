import asyncio
import json
from typing import cast, Any, List, Optional, Literal

from dotenv import load_dotenv
load_dotenv()

from tavily import AsyncTavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel, Field

# --- CONFIGURATION ---
# Gemini 2.0 Flash has 10 RPM limit, so we limit to ~0.15 requests/sec (9 per minute)
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.15,  # 9 requests per minute (safe margin)
    check_every_n_seconds=0.5,
    max_bucket_size=5, 
)

# Use Gemini 2.0 Flash stable (10 RPM limit on free tier)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Stable version, 10 RPM limit
    temperature=0.3,
    rate_limiter=rate_limiter,
)

tavily_async_client = AsyncTavilyClient()

# --- STATE MODELS ---
class InputState(BaseModel):
    company: str
    topics: List[str]

class OutputState(BaseModel):
    final_report: str
    sources: List[str]

class OverallState(InputState):
    search_queries: List[str] = []
    raw_research: str = ""
    draft_report: str = ""
    critique: str = ""
    iteration_count: int = 0
    final_report: str = ""
    sources: List[str] = []

# --- NODES ---

def generate_deep_research_plan(state: OverallState) -> dict:
    """Step 1: Create a forensic research plan."""
    topics_str = ", ".join(state.topics)
    
    # Prompt Engineering: Force specific, hard-hitting queries
    prompt = f"""
    You are a Lead Equity Analyst. 
    Target: {state.company}
    Focus Areas: {topics_str}
    
    Generate 5 distinct, highly technical search queries to uncover hidden details.
    
    CRITICAL: Do NOT use generic terms like "overview" or "history".
    Instead, search for:
    - "Annual Report 2024 risk factors"
    - "EBITDA margins vs competitors"
    - "CEO interview transcript 2024"
    - "Regulatory lawsuits"
    """
    
    class Queries(BaseModel):
        queries: List[str]
        
    structured_llm = llm.with_structured_output(Queries)
    result = structured_llm.invoke(prompt)
    
    return {"search_queries": result.queries}

async def execute_research(state: OverallState) -> dict:
    """Step 2: Execute parallel search with raw content extraction."""
    tasks = []
    for q in state.search_queries:
        tasks.append(
            tavily_async_client.search(
                q, max_results=2, include_raw_content=True, topic="general"
            )
        )
    
    results = await asyncio.gather(*tasks)
    
    raw_text = ""
    sources = []
    for group in results:
        for result in group.get("results", []):
            # Limit content length to avoid context window overflow
            content = result.get('content', '')[:3000] 
            raw_text += f"\n--- SOURCE: {result['url']} ---\n{content}\n"
            sources.append(result['url'])
            
    return {"raw_research": raw_text, "sources": list(set(sources))}

def write_initial_draft(state: OverallState) -> dict:
    """Step 3: Write the first pass."""
    prompt = f"""
    Role: Senior Investment Banker.
    Task: Write a comprehensive internal memo on {state.company}.
    Focus: {", ".join(state.topics)}.
    
    Raw Data:
    {state.raw_research}
    
    Requirements:
    - Use a professional, objective tone.
    - CITE SPECIFIC NUMBERS and DATES.
    - Do not be generic. If data is missing, state "Data not found in public filings".
    """
    result = llm.invoke(prompt)
    return {"draft_report": result.content, "iteration_count": 1}

def critique_and_refine(state: OverallState) -> dict:
    """Step 4: The Loop. Critique and Rewrite."""
    
    # Critique
    critique_prompt = f"""
    Critique this draft report on {state.company}:
    {state.draft_report}
    
    Identify 3 areas where it is too vague. 
    (e.g., "Revenue grew" -> Needs exact % and $ amount).
    """
    critique = llm.invoke(critique_prompt).content
    
    # Refine
    refine_prompt = f"""
    Rewrite the report to be denser and more factual.
    Original Draft: {state.draft_report}
    Critique: {critique}
    Raw Data: {state.raw_research}
    
    Action: Incorporate the missing details. Remove fluff. 
    """
    new_draft = llm.invoke(refine_prompt).content
    
    return {
        "draft_report": new_draft, 
        "iteration_count": state.iteration_count + 1,
        "critique": critique
    }

def check_quality(state: OverallState) -> Literal["critique_and_refine", END]:
    if state.iteration_count < 2:
        return "critique_and_refine"
    return END

def finalize_output(state: OverallState) -> dict:
    return {"final_report": state.draft_report}

# --- GRAPH BUILD ---
builder = StateGraph(OverallState, input=InputState, output=OutputState)

builder.add_node("plan", generate_deep_research_plan)
builder.add_node("research", execute_research)
builder.add_node("draft", write_initial_draft)
builder.add_node("critique_and_refine", critique_and_refine)
builder.add_node("finalize", finalize_output)

builder.add_edge(START, "plan")
builder.add_edge("plan", "research")
builder.add_edge("research", "draft")
builder.add_edge("draft", "critique_and_refine")
builder.add_conditional_edges("critique_and_refine", check_quality)
builder.add_edge("finalize", END)

graph = builder.compile()