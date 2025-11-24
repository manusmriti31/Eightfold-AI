"""Selective multi-agent graph - runs only selected agents."""

import os
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

from tavily import AsyncTavilyClient
from langgraph.graph import StateGraph, START, END

from src.graph.state import MultiAgentState, InputState
from src.agents.research.profile_agent import ProfileAgent
from src.agents.research.leadership_agent import LeadershipAgent
from src.agents.research.financial_agent import FinancialAgent
from src.agents.research.market_agent import MarketAgent
from src.agents.research.signals_agent import SignalsAgent
from src.llm.llm_config import get_configured_llms


# --- CONFIGURATION ---
# Get LLMs (Google Gemini)
llm_config = get_configured_llms()
query_llm = llm_config["query_llm"]
extraction_llm = llm_config["extraction_llm"]
report_llm = llm_config["report_llm"]

print(f"🤖 Using {llm_config['provider'].upper()} API for LLM calls")

tavily_client = AsyncTavilyClient()

# Initialize all agents with extraction LLM
profile_agent = ProfileAgent(
    name="ProfileAgent",
    llm=extraction_llm,
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

leadership_agent = LeadershipAgent(
    name="LeadershipAgent",
    llm=extraction_llm,
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

financial_agent = FinancialAgent(
    name="FinancialAgent",
    llm=extraction_llm,
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

market_agent = MarketAgent(
    name="MarketAgent",
    llm=extraction_llm,
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

signals_agent = SignalsAgent(
    name="SignalsAgent",
    llm=extraction_llm,
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)


# --- AGENT RUNNERS ---

async def run_profile_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Run Profile Agent and generate report."""
    print(f"\n🏢 Profile Agent researching {state.company}...")
    
    result = await profile_agent.research(state.company)
    
    # Generate individual report
    report_prompt = f"""Create a comprehensive Business Profile report for {state.company}.

Data from research:
{result['data'].model_dump()}

Create a well-structured markdown report with:
1. Company Overview
2. Business Model
3. Products & Services
4. Revenue Streams
5. Key Insights

Be specific with facts and numbers."""
    
    report_response = report_llm.invoke(report_prompt)
    
    return {
        "profile_data": result['data'],
        "individual_reports": {
            "profile": report_response.content
        }
    }


async def run_leadership_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Run Leadership Agent and generate report."""
    print(f"\n👥 Leadership Agent researching {state.company}...")
    
    result = await leadership_agent.research(state.company)
    
    # Generate individual report
    report_prompt = f"""Create a comprehensive Leadership Team report for {state.company}.

Data from research:
{result['data'].model_dump()}

Create a well-structured markdown report with:
1. Founders & Their Background
2. Executive Team
3. Leadership Style & Culture
4. Key Person Risks
5. Management Insights

Be specific with names, roles, and backgrounds."""
    
    report_response = report_llm.invoke(report_prompt)
    
    return {
        "leadership_data": result['data'],
        "individual_reports": {
            "leadership": report_response.content
        }
    }


async def run_financial_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Run Financial Agent and generate report."""
    print(f"\n💰 Financial Agent researching {state.company}...")
    
    result = await financial_agent.research(state.company)
    
    # Generate individual report
    report_prompt = f"""Create a comprehensive Financial Analysis report for {state.company}.

Data from research:
{result['data'].model_dump()}

Create a well-structured markdown report with:
1. Revenue & Growth
2. Profitability Metrics
3. Funding History
4. Financial Health Assessment
5. Key Financial Insights

Be specific with numbers, percentages, and dates."""
    
    report_response = report_llm.invoke(report_prompt)
    
    return {
        "financial_data": result['data'],
        "individual_reports": {
            "financial": report_response.content
        }
    }


async def run_market_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Run Market Agent and generate report."""
    print(f"\n📊 Market Agent researching {state.company}...")
    
    result = await market_agent.research(state.company)
    
    # Generate individual report
    report_prompt = f"""Create a comprehensive Market & Competition report for {state.company}.

Data from research:
{result['data'].model_dump()}

Create a well-structured markdown report with:
1. Market Size & Growth
2. Competitive Landscape
3. SWOT Analysis
4. Market Position
5. Strategic Insights

Be specific with market data, competitor names, and analysis."""
    
    report_response = report_llm.invoke(report_prompt)
    
    return {
        "market_data": result['data'],
        "individual_reports": {
            "market": report_response.content
        }
    }


async def run_signals_agent(state: MultiAgentState) -> Dict[str, Any]:
    """Run Signals Agent and generate report."""
    print(f"\n🚨 Signals Agent researching {state.company}...")
    
    result = await signals_agent.research(state.company)
    
    # Generate individual report
    report_prompt = f"""Create a comprehensive News & Risk Signals report for {state.company}.

Data from research:
{result['data'].model_dump()}

Create a well-structured markdown report with:
1. Recent News & Developments
2. Employee Sentiment
3. Risk Factors
4. Hiring Trends
5. Key Signals & Alerts

Be specific with dates, sources, and risk assessments."""
    
    report_response = report_llm.invoke(report_prompt)
    
    return {
        "signals_data": result['data'],
        "individual_reports": {
            "signals": report_response.content
        }
    }


# --- GRAPH BUILDER ---

async def research_selective(
    company: str,
    selected_agents: List[str],
    report_type: str = "investment_memo"
) -> Dict[str, Any]:
    """
    Research company using only selected agents.
    
    Args:
        company: Company name
        selected_agents: List of agent names to run
        report_type: Type of report
        
    Returns:
        Individual reports from each selected agent
    """
    print(f"\n{'='*60}")
    print(f"🚀 Starting Selective Research: {company}")
    print(f"Selected Agents: {', '.join(selected_agents)}")
    print(f"{'='*60}")
    
    # Initialize results
    results = {
        "company": company,
        "report_type": report_type,
        "selected_agents": selected_agents,
        "individual_reports": {},
        "all_sources": [],
        "metadata": {
            "agents_used": len(selected_agents),
            "total_sources": 0,
            "average_confidence": 0.0
        }
    }
    
    confidences = []
    
    # Run selected agents
    if "profile" in selected_agents:
        profile_result = await run_profile_agent(
            type('State', (), {'company': company})()
        )
        results["individual_reports"]["profile"] = profile_result["individual_reports"]["profile"]
        confidences.append(0.85)  # Placeholder
    
    if "leadership" in selected_agents:
        leadership_result = await run_leadership_agent(
            type('State', (), {'company': company})()
        )
        results["individual_reports"]["leadership"] = leadership_result["individual_reports"]["leadership"]
        confidences.append(0.85)
    
    if "financial" in selected_agents:
        financial_result = await run_financial_agent(
            type('State', (), {'company': company})()
        )
        results["individual_reports"]["financial"] = financial_result["individual_reports"]["financial"]
        confidences.append(0.85)
    
    if "market" in selected_agents:
        market_result = await run_market_agent(
            type('State', (), {'company': company})()
        )
        results["individual_reports"]["market"] = market_result["individual_reports"]["market"]
        confidences.append(0.85)
    
    if "signals" in selected_agents:
        signals_result = await run_signals_agent(
            type('State', (), {'company': company})()
        )
        results["individual_reports"]["signals"] = signals_result["individual_reports"]["signals"]
        confidences.append(0.85)
    
    # Calculate metadata
    results["metadata"]["average_confidence"] = sum(confidences) / len(confidences) if confidences else 0.0
    results["metadata"]["total_sources"] = len(selected_agents) * 15  # Approximate
    
    print(f"\n{'='*60}")
    print(f"✅ Research Complete!")
    print(f"{'='*60}")
    
    return results
