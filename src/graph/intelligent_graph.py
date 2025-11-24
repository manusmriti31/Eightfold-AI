"""Intelligent Multi-Agent Graph with Gap Detection and Refinement."""

import os
from typing import Dict, Any, List, Literal
from dotenv import load_dotenv

load_dotenv()

from tavily import AsyncTavilyClient
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
    Gap,
    RefinementMetadata,
)
from src.agents.research.profile_agent import ProfileAgent
from src.agents.research.leadership_agent import LeadershipAgent
from src.agents.research.financial_agent import FinancialAgent
from src.agents.research.market_agent import MarketAgent
from src.agents.research.signals_agent import SignalsAgent
from src.agents.intelligence.gap_detector import GapDetectorAgent, GapPriority
from src.llm.llm_config import get_configured_llms


# --- CONFIGURATION ---
llm_config = get_configured_llms()
query_llm = llm_config["query_llm"]
extraction_llm = llm_config["extraction_llm"]
gap_detection_llm = llm_config["gap_detection_llm"]  # NEW: Quality model for gap detection
synthesis_llm = llm_config["synthesis_llm"]  # NEW: Premium model for synthesis
report_llm = llm_config["report_llm"]  # Alias for synthesis_llm

print(f"🤖 Using {llm_config['provider'].upper()} Multi-Model Configuration for Intelligent Graph")

tavily_client = AsyncTavilyClient()

# Initialize research agents with query_llm for query generation, extraction_llm for data extraction
profile_agent = ProfileAgent(
    name="profile",
    llm=extraction_llm,  # Uses gemini-2.0-flash-live (Unlimited RPM)
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

leadership_agent = LeadershipAgent(
    name="leadership",
    llm=extraction_llm,  # Uses gemini-2.0-flash-live (Unlimited RPM)
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

financial_agent = FinancialAgent(
    name="financial",
    llm=extraction_llm,  # Uses gemini-2.0-flash-live (Unlimited RPM)
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

market_agent = MarketAgent(
    name="market",
    llm=extraction_llm,  # Uses gemini-2.0-flash-live (Unlimited RPM)
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

signals_agent = SignalsAgent(
    name="signals",
    llm=extraction_llm,  # Uses gemini-2.0-flash-live (Unlimited RPM)
    search_tool=tavily_client,
    max_queries=5,
    max_results_per_query=3
)

# Initialize gap detector with quality model
gap_detector = GapDetectorAgent(llm=gap_detection_llm)  # Uses gemini-2.5-flash (10 RPM)

# Agent mapping
AGENTS = {
    "profile": profile_agent,
    "leadership": leadership_agent,
    "financial": financial_agent,
    "market": market_agent,
    "signals": signals_agent,
}


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
        executives=[],
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
        sources=result['sources'],
        # Stock market data (Phase 3)
        stock_data=result['data'].stock_data if hasattr(result['data'], 'stock_data') else None,
        financial_news=result['data'].financial_news if hasattr(result['data'], 'financial_news') else None,
        stock_ticker=result['data'].stock_ticker if hasattr(result['data'], 'stock_ticker') else None
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
    
    return {
        "all_sources": all_sources,
        "research_complete": True
    }


async def detect_gaps(state: MultiAgentState) -> Dict[str, Any]:
    """Detect missing data gaps across all agents."""
    print("\n🔍 Detecting data gaps...")
    
    all_gaps = []
    
    # Analyze each agent's data for gaps
    if state.profile_data:
        gaps = gap_detector.analyze_gaps("profile", profile_agent.get_output_schema()(**state.profile_data.__dict__), state.company)
        all_gaps.extend([Gap(
            field_name=g.field_name,
            agent_name=g.agent_name,
            priority=g.priority.value,
            field_type=g.field_type,
            context=g.context,
            attempted_queries=[],
            filled=False
        ) for g in gaps])
    
    if state.leadership_data:
        gaps = gap_detector.analyze_gaps("leadership", leadership_agent.get_output_schema()(**state.leadership_data.__dict__), state.company)
        all_gaps.extend([Gap(
            field_name=g.field_name,
            agent_name=g.agent_name,
            priority=g.priority.value,
            field_type=g.field_type,
            context=g.context,
            attempted_queries=[],
            filled=False
        ) for g in gaps])
    
    if state.financial_data:
        gaps = gap_detector.analyze_gaps("financial", financial_agent.get_output_schema()(**state.financial_data.__dict__), state.company)
        all_gaps.extend([Gap(
            field_name=g.field_name,
            agent_name=g.agent_name,
            priority=g.priority.value,
            field_type=g.field_type,
            context=g.context,
            attempted_queries=[],
            filled=False
        ) for g in gaps])
    
    if state.market_data:
        gaps = gap_detector.analyze_gaps("market", market_agent.get_output_schema()(**state.market_data.__dict__), state.company)
        all_gaps.extend([Gap(
            field_name=g.field_name,
            agent_name=g.agent_name,
            priority=g.priority.value,
            field_type=g.field_type,
            context=g.context,
            attempted_queries=[],
            filled=False
        ) for g in gaps])
    
    if state.signals_data:
        gaps = gap_detector.analyze_gaps("signals", signals_agent.get_output_schema()(**state.signals_data.__dict__), state.company)
        all_gaps.extend([Gap(
            field_name=g.field_name,
            agent_name=g.agent_name,
            priority=g.priority.value,
            field_type=g.field_type,
            context=g.context,
            attempted_queries=[],
            filled=False
        ) for g in gaps])
    
    print(f"🔍 Found {len(all_gaps)} gaps:")
    critical = sum(1 for g in all_gaps if g.priority == "critical")
    high = sum(1 for g in all_gaps if g.priority == "high")
    print(f"   - {critical} CRITICAL")
    print(f"   - {high} HIGH priority")
    
    return {
        "gaps": all_gaps,
        "gap_detection_complete": True
    }


async def refine_research(state: MultiAgentState) -> Dict[str, Any]:
    """Refine research by targeting specific gaps."""
    print(f"\n🔄 Refinement Iteration {state.refinement_iteration + 1}/{state.max_refinement_iterations}")
    
    # Group gaps by agent
    gaps_by_agent = {}
    for gap in state.gaps:
        if not gap.filled:  # Only process unfilled gaps
            if gap.agent_name not in gaps_by_agent:
                gaps_by_agent[gap.agent_name] = []
            gaps_by_agent[gap.agent_name].append(gap)
    
    # Track refinement metadata
    total_queries = 0
    total_new_sources = 0
    gaps_filled_this_iteration = 0
    
    # Refine each agent's data
    updated_data = {}
    
    for agent_name, agent_gaps in gaps_by_agent.items():
        print(f"\n   Refining {agent_name} agent ({len(agent_gaps)} gaps)...")
        
        agent = AGENTS.get(agent_name)
        if not agent:
            continue
        
        # Generate refinement queries for top 3 gaps (prioritize critical/high)
        # Handle both enum and string priority
        def priority_key(g):
            p = g.priority.value if hasattr(g.priority, 'value') else g.priority
            return (p != "critical", p != "high")
        
        sorted_gaps = sorted(agent_gaps, key=priority_key)[:3]
        
        refinement_queries = []
        for gap in sorted_gaps:
            queries = await gap_detector.generate_refinement_queries(gap, state.company, gap.attempted_queries)
            refinement_queries.extend(queries)
            gap.attempted_queries.extend(queries)
            total_queries += len(queries)
        
        if not refinement_queries:
            continue
        
        # Get current data for this agent
        current_data = None
        current_sources = []
        
        if agent_name == "profile" and state.profile_data:
            current_data = profile_agent.get_output_schema()(**state.profile_data.__dict__)
            current_sources = state.profile_data.sources
        elif agent_name == "leadership" and state.leadership_data:
            current_data = leadership_agent.get_output_schema()(**state.leadership_data.__dict__)
            current_sources = state.leadership_data.sources
        elif agent_name == "financial" and state.financial_data:
            current_data = financial_agent.get_output_schema()(**state.financial_data.__dict__)
            current_sources = state.financial_data.sources
        elif agent_name == "market" and state.market_data:
            current_data = market_agent.get_output_schema()(**state.market_data.__dict__)
            current_sources = state.market_data.sources
        elif agent_name == "signals" and state.signals_data:
            current_data = signals_agent.get_output_schema()(**state.signals_data.__dict__)
            current_sources = state.signals_data.sources
        
        if not current_data:
            continue
        
        # Refine research
        refined_result = await agent.refine_research(
            state.company,
            refinement_queries,
            current_data,
            current_sources
        )
        
        total_new_sources += len(refined_result['new_sources'])
        gaps_filled_this_iteration += refined_result['gaps_filled']
        
        # Update state with refined data
        updated_data[agent_name] = refined_result
        
        print(f"   ✓ {agent_name}: Filled {refined_result['gaps_filled']} gaps, found {len(refined_result['new_sources'])} new sources")
    
    # Update state with refined data
    state_updates = {
        "refinement_iteration": state.refinement_iteration + 1,
        "gaps_filled_count": state.gaps_filled_count + gaps_filled_this_iteration,
    }
    
    # Update agent data
    if "profile" in updated_data:
        result = updated_data["profile"]
        state_updates["profile_data"] = ProfileData(
            company_name=result['data'].company_name,
            founded=result['data'].founded,
            ownership_type=result['data'].ownership_type,
            business_model=result['data'].business_model.model_dump() if result['data'].business_model else None,
            products_services=result['data'].products_services,
            revenue_streams=result['data'].business_model.revenue_streams if result['data'].business_model else [],
            confidence_score=result['data'].confidence_score if hasattr(result['data'], 'confidence_score') else 0.85,
            sources=result['sources']
        )
    
    if "financial" in updated_data:
        result = updated_data["financial"]
        state_updates["financial_data"] = FinancialData(
            revenue=result['data'].revenue.model_dump() if result['data'].revenue else None,
            profitability=result['data'].profitability.model_dump() if result['data'].profitability else None,
            funding=result['data'].funding.model_dump() if result['data'].funding else None,
            financial_ratios=result['data'].financial_ratios.model_dump() if result['data'].financial_ratios else None,
            financial_health_score=result['data'].financial_health_score or 0.0,
            confidence_score=result['data'].confidence_score if hasattr(result['data'], 'confidence_score') else 0.85,
            sources=result['sources']
        )
    
    # Add refinement metadata
    metadata = RefinementMetadata(
        iteration=state.refinement_iteration + 1,
        gaps_detected=len([g for g in state.gaps if not g.filled]),
        gaps_filled=gaps_filled_this_iteration,
        queries_generated=total_queries,
        sources_found=total_new_sources
    )
    
    state_updates["refinement_metadata"] = state.refinement_metadata + [metadata]
    
    print(f"\n✓ Refinement complete: {gaps_filled_this_iteration} gaps filled, {total_new_sources} new sources")
    
    return state_updates


def should_refine(state: MultiAgentState) -> Literal["refine", "synthesize"]:
    """Decide whether to continue refinement or move to synthesis."""
    
    # Check if we've reached max iterations
    if state.refinement_iteration >= state.max_refinement_iterations:
        print(f"\n✓ Max refinement iterations reached ({state.max_refinement_iterations})")
        return "synthesize"
    
    # Check if there are any unfilled gaps
    unfilled_gaps = [g for g in state.gaps if not g.filled]
    # Handle both enum and string priority
    critical_gaps = [g for g in unfilled_gaps if (g.priority == "critical" or (hasattr(g.priority, 'value') and g.priority.value == "critical"))]
    
    if not unfilled_gaps:
        print("\n✓ All gaps filled!")
        return "synthesize"
    
    if not critical_gaps and state.refinement_iteration > 0:
        print(f"\n✓ No critical gaps remaining (only {len(unfilled_gaps)} minor gaps)")
        return "synthesize"
    
    print(f"\n→ Continuing refinement ({len(critical_gaps)} critical gaps remaining)")
    return "refine"


async def synthesize_report(state: MultiAgentState) -> Dict[str, Any]:
    """Synthesize final report from all agent data using premium model."""
    print("\n📝 Synthesizing final report with gemini-2.5-pro (premium quality)...")
    
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
    
    # Use premium synthesis model for highest quality
    response = synthesis_llm.invoke(prompt)
    final_report = response.content
    
    # Create executive summary
    summary_prompt = f"""Create a concise 3-sentence executive summary of this company report:

{final_report}

Focus on: What the company does, their market position, and key highlights/concerns."""
    
    summary_response = synthesis_llm.invoke(summary_prompt)
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
    
    # Add refinement summary to metadata
    refinement_summary = gap_detector.get_refinement_summary(state.gaps) if state.gaps else None
    
    # Calculate confidence scores per agent
    confidence_scores = {}
    if state.profile_data:
        confidence_scores['profile'] = state.profile_data.confidence_score
    if state.leadership_data:
        confidence_scores['leadership'] = state.leadership_data.confidence_score
    if state.financial_data:
        confidence_scores['financial'] = state.financial_data.confidence_score
    if state.market_data:
        confidence_scores['market'] = state.market_data.confidence_score
    if state.signals_data:
        confidence_scores['signals'] = state.signals_data.confidence_score
    
    return {
        "final_report": final_report,
        "executive_summary": executive_summary,
        "refinement_complete": True,
        "report_metadata": {
            "company": state.company,
            "agents_used": 5,
            "total_sources": len(state.all_sources),
            "average_confidence": avg_confidence,
            "report_type": state.report_type if isinstance(state.report_type, str) else state.report_type.value,
            "refinement_iterations": state.refinement_iteration,
            "gaps_filled": state.gaps_filled_count,
            "refinement_summary": refinement_summary
        },
        "confidence_scores": confidence_scores,
        # Include agent data for Phase 2 report formatting
        "profile_data": state.profile_data,
        "leadership_data": state.leadership_data,
        "financial_data": state.financial_data,
        "market_data": state.market_data,
        "signals_data": state.signals_data
    }


# --- BUILD GRAPH ---

def create_intelligent_graph():
    """Create and compile the intelligent multi-agent research graph with refinement."""
    
    builder = StateGraph(MultiAgentState, input=InputState, output=OutputState)
    
    # Add research agent nodes
    builder.add_node("profile", run_profile_agent)
    builder.add_node("leadership", run_leadership_agent)
    builder.add_node("financial", run_financial_agent)
    builder.add_node("market", run_market_agent)
    builder.add_node("signals", run_signals_agent)
    
    # Add intelligence nodes
    builder.add_node("aggregate", aggregate_data)
    builder.add_node("detect_gaps", detect_gaps)
    builder.add_node("refine", refine_research)
    builder.add_node("synthesize", synthesize_report)
    
    # Parallel execution: All 5 agents start simultaneously
    builder.add_edge(START, "profile")
    builder.add_edge(START, "leadership")
    builder.add_edge(START, "financial")
    builder.add_edge(START, "market")
    builder.add_edge(START, "signals")
    
    # All agents → aggregate → detect gaps
    builder.add_edge(["profile", "leadership", "financial", "market", "signals"], "aggregate")
    builder.add_edge("aggregate", "detect_gaps")
    
    # Conditional: refine or synthesize
    builder.add_conditional_edges(
        "detect_gaps",
        should_refine,
        {
            "refine": "refine",
            "synthesize": "synthesize"
        }
    )
    
    # After refinement, check again (loop back to detect_gaps)
    builder.add_edge("refine", "detect_gaps")
    
    # Synthesis → end
    builder.add_edge("synthesize", END)
    
    return builder.compile()


# Create the graph instance
intelligent_graph = create_intelligent_graph()


# --- CONVENIENCE FUNCTION ---

async def research_company_intelligent(
    company: str,
    report_type: str = "investment_memo",
    max_refinement_iterations: int = 2
) -> Dict[str, Any]:
    """
    Research a company using intelligent multi-agent system with gap refinement.
    
    Args:
        company: Company name to research
        report_type: Type of report to generate
        max_refinement_iterations: Maximum refinement iterations (default: 2)
        
    Returns:
        Complete research results with final report and refinement metadata
    """
    print(f"\n{'='*60}")
    print(f"🚀 Starting Intelligent Research: {company}")
    print(f"{'='*60}")
    
    result = await intelligent_graph.ainvoke({
        "company": company,
        "report_type": report_type,
        "max_refinement_iterations": max_refinement_iterations
    })
    
    print(f"\n{'='*60}")
    print(f"✅ Intelligent Research Complete!")
    print(f"{'='*60}")
    print(f"📊 Total Sources: {len(result['all_sources'])}")
    print(f"📈 Average Confidence: {result['report_metadata']['average_confidence']:.2f}")
    print(f"🔄 Refinement Iterations: {result['report_metadata']['refinement_iterations']}")
    print(f"✓ Gaps Filled: {result['report_metadata']['gaps_filled']}")
    
    if result['report_metadata'].get('refinement_summary'):
        summary = result['report_metadata']['refinement_summary']
        print(f"\n📋 Gap Analysis:")
        print(f"   - Total gaps detected: {summary['total_gaps']}")
        print(f"   - Gaps filled: {summary['gaps_filled']}")
        print(f"   - Fill rate: {summary['fill_rate']:.1f}%")
        print(f"   - Critical gaps remaining: {summary['critical_gaps_remaining']}")
    
    print(f"\n")
    
    return result
