"""Multi-Agent LangGraph - Orchestrates all 5 research agents."""

import os
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

from tavily import AsyncTavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.rate_limiters import InMemoryRateLimiter
from langgraph.graph import StateGraph, START, END

from src.graph.state import (
    InputState,
    MultiAgentState,
    OutputState,
    ProfileData,
    LeadershipData,
    FinancialData,
    MarketData,
    SignalsData,
)
from src.agents.research.profile_agent import ProfileAgent
from src.agents.research.leadership_agent import LeadershipAgent
from src.agents.research.financial_agent import FinancialAgent
from src.agents.research.market_agent import MarketAgent
from src.agents.research.signals_agent import SignalsAgent


# --- CONFIGURATION ---
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.15,
    check_every_n_seconds=0.5,
    max_bucket_size=5,
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    rate_limiter=rate_limiter,
)

tavily_client = AsyncTavilyClient()

# Initialize all 5 research agents
profile_agent = ProfileAgent(
    name="ProfileAgent",
    llm=llm,
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

leadership_agent = LeadershipAgent(
    name="LeadershipAgent",
    llm=llm,
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

financial_agent = FinancialAgent(
    name="FinancialAgent",
    llm=llm,
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

market_agent = MarketAgent(
    name="MarketAgent",
    llm=llm,
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

signals_agent = SignalsAgent(
    name="SignalsAgent",
    llm=llm,
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)


# --- GRAPH NODES ---

async def run_profile_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Run Profile Agent research."""
    print(f"\n🏢 Profile Agent researching {state.company}...")
    
    result = await profile_agent.research(state.company)
    
    profile_data = ProfileData(
        company_name=result['data'].company_name,
        founded=result['data'].founded,
        ownership_type=result['data'].ownership_type,
        business_model=result['data'].business_model.model_dump() if result['data'].business_model else None,
        products_services=result['data'].products_services,
        revenue_streams=result['data'].business_model.revenue_streams if result['data'].business_model else [],
        confidence_score=result['confidence_score'],
        sources=result['sources']
    )
    
    return {"profile_data": profile_data}


async def run_leadership_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Run Leadership Agent research."""
    print(f"\n👥 Leadership Agent researching {state.company}...")
    
    result = await leadership_agent.research(state.company)
    
    leadership_data = LeadershipData(
        founders=[f.model_dump() for f in result['data'].founders],
        executives=[],  # Combine CEO, CTO, CFO, others
        leadership_style=result['data'].leadership_style,
        key_risks=result['data'].key_person_risks,
        confidence_score=result['confidence_score'],
        sources=result['sources']
    )
    
    # Add executives
    if result['data'].ceo:
        leadership_data.executives.append(result['data'].ceo.model_dump())
    if result['data'].cto:
        leadership_data.executives.append(result['data'].cto.model_dump())
    if result['data'].cfo:
        leadership_data.executives.append(result['data'].cfo.model_dump())
    leadership_data.executives.extend([e.model_dump() for e in result['data'].other_executives])
    
    return {"leadership_data": leadership_data}


async def run_financial_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Run Financial Agent research."""
    print(f"\n💰 Financial Agent researching {state.company}...")
    
    result = await financial_agent.research(state.company)
    
    financial_data = FinancialData(
        revenue=result['data'].revenue.model_dump() if result['data'].revenue else None,
        profitability=result['data'].profitability.model_dump() if result['data'].profitability else None,
        funding=result['data'].funding.model_dump() if result['data'].funding else None,
        financial_ratios=result['data'].financial_ratios.model_dump() if result['data'].financial_ratios else None,
        financial_health_score=result['data'].financial_health_score or 0.0,
        confidence_score=result['confidence_score'],
        sources=result['sources']
    )
    
    return {"financial_data": financial_data}


async def run_market_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Run Market Agent research."""
    print(f"\n📊 Market Agent researching {state.company}...")
    
    result = await market_agent.research(state.company)
    
    market_data = MarketData(
        market=result['data'].market.model_dump() if result['data'].market else None,
        competitors=[c.model_dump() for c in result['data'].competitors],
        swot=result['data'].swot.model_dump() if result['data'].swot else None,
        market_position=result['data'].market_position,
        confidence_score=result['confidence_score'],
        sources=result['sources']
    )
    
    return {"market_data": market_data}


async def run_signals_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Run Signals Agent research."""
    print(f"\n🚨 Signals Agent researching {state.company}...")
    
    result = await signals_agent.research(state.company)
    
    signals_data = SignalsData(
        recent_news=[n.model_dump() for n in result['data'].recent_news],
        employee_sentiment=result['data'].employee_sentiment.model_dump() if result['data'].employee_sentiment else None,
        risks=[r.model_dump() for r in result['data'].risks],
        hiring_trends=result['data'].hiring_trends.model_dump() if result['data'].hiring_trends else None,
        social_sentiment=result['data'].social_sentiment.model_dump() if result['data'].social_sentiment else None,
        confidence_score=result['confidence_score'],
        sources=result['sources']
    )
    
    return {"signals_data": signals_data}


def aggregate_data(state: MultiAgentState) -> Dict[str, Any]:
    """Aggregate all research data."""
    print("\n📦 Aggregating all research data...")
    
    # Collect all sources
    all_sources = []
    if state.profile_data:
        all_sources.extend(state.profile_data.sources)
    if state.leadership_data:
        all_sources.extend(state.leadership_data.sources)
    if state.financial_data:
        all_sources.extend(state.financial_data.sources)
    if state.market_data:
        all_sources.extend(state.market_data.sources)
    if state.signals_data:
        all_sources.extend(state.signals_data.sources)
    
    # Remove duplicates
    all_sources = list(set(all_sources))
    
    # Create aggregated data dictionary
    aggregated = {
        "profile": state.profile_data.__dict__ if state.profile_data else None,
        "leadership": state.leadership_data.__dict__ if state.leadership_data else None,
        "financial": state.financial_data.__dict__ if state.financial_data else None,
        "market": state.market_data.__dict__ if state.market_data else None,
        "signals": state.signals_data.__dict__ if state.signals_data else None,
    }
    
    return {
        "aggregated_data": aggregated,
        "all_sources": all_sources,
        "research_complete": True
    }


async def synthesize_report(state: MultiAgentState) -> Dict[str, Any]:
    """Synthesize final report from all agent data."""
    print("\n📝 Synthesizing final report...")
    
    # Build comprehensive prompt with all data
    prompt = f"""You are a Senior Research Analyst creating a comprehensive company report.

Company: {state.company}

You have research data from 5 specialized agents. Create a professional, well-structured report.

=== PROFILE DATA ===
{state.profile_data.__dict__ if state.profile_data else "No data"}

=== LEADERSHIP DATA ===
{state.leadership_data.__dict__ if state.leadership_data else "No data"}

=== FINANCIAL DATA ===
{state.financial_data.__dict__ if state.financial_data else "No data"}

=== MARKET DATA ===
{state.market_data.__dict__ if state.market_data else "No data"}

=== SIGNALS & RISKS DATA ===
{state.signals_data.__dict__ if state.signals_data else "No data"}

Create a comprehensive report with these sections:
1. Executive Summary (2-3 paragraphs)
2. Company Overview
3. Leadership & Management
4. Financial Performance
5. Market Position & Competition
6. Recent Developments & Risks
7. Key Insights & Recommendations

Use markdown formatting. Be specific with numbers, dates, and facts.
"""
    
    response = llm.invoke(prompt)
    final_report = response.content
    
    # Create executive summary
    summary_prompt = f"""Create a concise 3-sentence executive summary of this company report:

{final_report}

Focus on: What the company does, their market position, and key highlights/concerns."""
    
    summary_response = llm.invoke(summary_prompt)
    executive_summary = summary_response.content
    
    # Calculate overall confidence
    confidences = []
    if state.profile_data:
        confidences.append(state.profile_data.confidence_score)
    if state.leadership_data:
        confidences.append(state.leadership_data.confidence_score)
    if state.financial_data:
        confidences.append(state.financial_data.confidence_score)
    if state.market_data:
        confidences.append(state.market_data.confidence_score)
    if state.signals_data:
        confidences.append(state.signals_data.confidence_score)
    
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    
    return {
        "final_report": final_report,
        "executive_summary": executive_summary,
        "report_metadata": {
            "company": state.company,
            "agents_used": 5,
            "total_sources": len(state.all_sources),
            "average_confidence": avg_confidence,
            "report_type": state.report_type if isinstance(state.report_type, str) else state.report_type.value
        }
    }


# --- BUILD GRAPH ---

def create_multi_agent_graph():
    """Create and compile the multi-agent research graph."""
    
    builder = StateGraph(MultiAgentState, input=InputState, output=OutputState)
    
    # Add all research agent nodes
    builder.add_node("profile", run_profile_agent)
    builder.add_node("leadership", run_leadership_agent)
    builder.add_node("financial", run_financial_agent)
    builder.add_node("market", run_market_agent)
    builder.add_node("signals", run_signals_agent)
    
    # Add processing nodes
    builder.add_node("aggregate", aggregate_data)
    builder.add_node("synthesize", synthesize_report)
    
    # Parallel execution: All 5 agents start simultaneously
    builder.add_edge(START, "profile")
    builder.add_edge(START, "leadership")
    builder.add_edge(START, "financial")
    builder.add_edge(START, "market")
    builder.add_edge(START, "signals")
    
    # All agents must complete before aggregation
    builder.add_edge(["profile", "leadership", "financial", "market", "signals"], "aggregate")
    
    # Sequential processing after aggregation
    builder.add_edge("aggregate", "synthesize")
    builder.add_edge("synthesize", END)
    
    return builder.compile()


# Create the graph instance
graph = create_multi_agent_graph()


# --- CONVENIENCE FUNCTION ---

async def research_company(
    company: str,
    report_type: str = "investment_memo"
) -> Dict[str, Any]:
    """
    Research a company using all 5 agents.
    
    Args:
        company: Company name to research
        report_type: Type of report to generate
        
    Returns:
        Complete research results with final report
    """
    print(f"\n{'='*60}")
    print(f"🚀 Starting Multi-Agent Research: {company}")
    print(f"{'='*60}")
    
    result = await graph.ainvoke({
        "company": company,
        "report_type": report_type
    })
    
    print(f"\n{'='*60}")
    print(f"✅ Research Complete!")
    print(f"{'='*60}")
    print(f"📊 Total Sources: {len(result['all_sources'])}")
    print(f"📈 Average Confidence: {result['report_metadata']['average_confidence']:.2f}")
    print(f"\n")
    
    return result
