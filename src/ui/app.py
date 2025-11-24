"""Main Streamlit application for multi-agent company research."""

import streamlit as st
import asyncio
from typing import Dict, Any, List

from src.ui.components import AgentMonitor, ReportViewer, InputForm
from src.ui.styles import apply_custom_styles
from src.ui.utils import run_async


def initialize_session_state():
    """Initialize session state variables."""
    if "research_results" not in st.session_state:
        st.session_state.research_results = None
    if "research_in_progress" not in st.session_state:
        st.session_state.research_in_progress = False
    if "current_company" not in st.session_state:
        st.session_state.current_company = None


def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Multi-Agent Company Research",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )


async def run_research_async(
    company: str,
    report_type: str,
    selected_agents: List[str],
    monitor: AgentMonitor
) -> Dict[str, Any]:
    """
    Run multi-agent research with real-time monitoring.
    
    Args:
        company: Company name to research
        report_type: Type of report to generate
        selected_agents: List of agents to run
        monitor: Agent monitor instance
        
    Returns:
        Research results
    """
    from src.graph.selective_graph import research_selective
    
    # Clear previous logs
    monitor.clear_logs()
    
    # Initialize only selected agents
    all_agents = ["profile", "leadership", "financial", "market", "signals"]
    for agent in all_agents:
        if agent in selected_agents:
            monitor.update_status(agent, "Waiting to start...", 0)
        else:
            monitor.update_status(agent, "Not selected", 0)
    
    monitor.add_log("system", f"Starting research for {company}", "info")
    monitor.add_log("system", f"Selected agents: {', '.join(selected_agents)}", "info")
    
    # Set selected agents to in progress
    for agent in selected_agents:
        monitor.update_status(agent, "Researching...", 50)
        monitor.add_log(agent, "Research in progress", "info")
    
    # Run research
    result = await research_selective(company, selected_agents, report_type)
    
    # Mark selected agents as complete
    for agent in selected_agents:
        monitor.update_status(agent, "Complete", 100)
        monitor.add_log(agent, "Completed successfully", "success")
    
    monitor.add_log("system", "Research complete!", "success")
    
    return result


def run_research(
    company: str,
    report_type: str,
    selected_agents: List[str],
    monitor: AgentMonitor
) -> Dict[str, Any]:
    """
    Synchronous wrapper for research execution.
    
    Args:
        company: Company name to research
        report_type: Type of report to generate
        selected_agents: List of agents to run
        monitor: Agent monitor instance
        
    Returns:
        Research results
    """
    return run_async(run_research_async(company, report_type, selected_agents, monitor))


def render_sidebar():
    """Render sidebar with information and settings."""
    with st.sidebar:
        st.markdown("# 🔍 Multi-Agent Research")
        st.markdown("---")
        
        st.markdown("### 📊 System Status")
        st.success("✅ All agents operational")
        
        st.markdown("### 🤖 Available Agents")
        agents = [
            ("🏢", "Profile Agent", "Business model & products"),
            ("👥", "Leadership Agent", "Founders & executives"),
            ("💰", "Financial Agent", "Revenue & funding"),
            ("📊", "Market Agent", "Competitors & SWOT"),
            ("🚨", "Signals Agent", "News & risks")
        ]
        
        for icon, name, description in agents:
            st.markdown(f"**{icon} {name}**")
            st.caption(description)
        
        st.markdown("---")
        
        st.markdown("### ℹ️ About")
        st.info(
            "This system uses 5 specialized AI agents working in parallel "
            "to research companies and generate comprehensive reports."
        )
        
        st.markdown("### 📚 Resources")
        st.markdown("- [Documentation](../docs/README.md)")
        st.markdown("- [GitHub](https://github.com/langchain-ai/company-researcher)")


def main():
    """Main application entry point."""
    # Configure page
    configure_page()
    
    # Apply custom styles
    apply_custom_styles()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Initialize components
    input_form = InputForm()
    monitor = AgentMonitor()
    report_viewer = ReportViewer()
    
    # Main content area
    if st.session_state.research_in_progress:
        # Show research in progress
        st.markdown(f"# 🔍 Researching: {st.session_state.current_company}")
        
        # Create two columns for monitoring
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Progress bars
            monitor.render_progress_bars()
        
        with col2:
            # Activity log
            monitor.render_activity_log()
        
        # Run research
        try:
            with st.spinner("Running research..."):
                results = run_research(
                    st.session_state.current_company,
                    st.session_state.report_type,
                    st.session_state.selected_agents,
                    monitor
                )
            
            # Store results and update state
            st.session_state.research_results = results
            st.session_state.research_in_progress = False
            st.rerun()
            
        except Exception as e:
            st.session_state.research_in_progress = False
            st.error(f"❌ Research failed: {str(e)}")
            report_viewer.render_error(e)
            
            if st.button("🔄 Try Again"):
                st.session_state.research_results = None
                st.session_state.current_company = None
                st.rerun()
    
    elif st.session_state.research_results is not None:
        # Show results
        results = st.session_state.research_results
        
        # Render summary
        monitor.render_summary(results)
        
        st.markdown("---")
        
        # Render report
        report_viewer.render(results)
        
        # New research button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 New Research", use_container_width=True, type="primary"):
                st.session_state.research_results = None
                st.session_state.current_company = None
                st.session_state.research_in_progress = False
                monitor.clear_logs()
                st.rerun()
    
    else:
        # Show input form
        st.markdown("# 🔍 Multi-Agent Company Research System")
        st.markdown(
            "Generate comprehensive company research reports using 5 specialized AI agents "
            "working in parallel."
        )
        
        # Render input form
        form_data = input_form.render()
        
        # Show examples
        input_form.render_examples()
        
        # Start research if form submitted
        if form_data:
            st.session_state.research_in_progress = True
            st.session_state.current_company = form_data["company"]
            st.session_state.report_type = form_data["report_type"]
            st.session_state.selected_agents = form_data["selected_agents"]
            st.rerun()


if __name__ == "__main__":
    main()
