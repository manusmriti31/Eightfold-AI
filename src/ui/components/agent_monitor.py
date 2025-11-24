"""Agent monitoring component - Real-time agent status display."""

import streamlit as st
from typing import Dict, Any, List
from datetime import datetime


class AgentMonitor:
    """Component for monitoring agent execution in real-time."""
    
    AGENT_ICONS = {
        "profile": "🏢",
        "leadership": "👥",
        "financial": "💰",
        "market": "📊",
        "signals": "🚨"
    }
    
    AGENT_NAMES = {
        "profile": "Profile Agent",
        "leadership": "Leadership Agent",
        "financial": "Financial Agent",
        "market": "Market Agent",
        "signals": "Signals Agent"
    }
    
    def __init__(self):
        """Initialize agent monitor."""
        if "agent_status" not in st.session_state:
            st.session_state.agent_status = {}
        if "agent_logs" not in st.session_state:
            st.session_state.agent_logs = []
    
    def update_status(self, agent: str, status: str, progress: float = 0.0):
        """
        Update agent status.
        
        Args:
            agent: Agent name (profile, leadership, etc.)
            status: Status message
            progress: Progress percentage (0-100)
        """
        st.session_state.agent_status[agent] = {
            "status": status,
            "progress": progress,
            "timestamp": datetime.now()
        }
    
    def add_log(self, agent: str, message: str, log_type: str = "info"):
        """
        Add log entry.
        
        Args:
            agent: Agent name
            message: Log message
            log_type: Type of log (info, success, warning, error)
        """
        icon_map = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }
        
        st.session_state.agent_logs.append({
            "agent": agent,
            "message": message,
            "type": log_type,
            "icon": icon_map.get(log_type, "ℹ️"),
            "timestamp": datetime.now()
        })
    
    def render_progress_bars(self):
        """Render progress bars for all agents."""
        st.markdown("### 🤖 Agent Progress")
        
        for agent_key, agent_name in self.AGENT_NAMES.items():
            icon = self.AGENT_ICONS[agent_key]
            status_data = st.session_state.agent_status.get(agent_key, {})
            
            progress = status_data.get("progress", 0.0) / 100.0
            status = status_data.get("status", "Waiting...")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(progress, text=f"{icon} {agent_name}")
            with col2:
                if progress >= 1.0:
                    st.success("✓ Done")
                elif progress > 0:
                    st.info(f"{int(progress * 100)}%")
                else:
                    st.text("⏳ Waiting")
            
            if status != "Waiting...":
                st.caption(f"   {status}")
    
    def render_activity_log(self, max_entries: int = 10):
        """
        Render activity log.
        
        Args:
            max_entries: Maximum number of log entries to display
        """
        st.markdown("### 📋 Activity Log")
        
        if not st.session_state.agent_logs:
            st.info("No activity yet. Start a research to see logs.")
            return
        
        # Show most recent logs first
        recent_logs = st.session_state.agent_logs[-max_entries:][::-1]
        
        for log in recent_logs:
            agent_icon = self.AGENT_ICONS.get(log["agent"], "🔹")
            timestamp = log["timestamp"].strftime("%H:%M:%S")
            
            with st.container():
                st.markdown(
                    f"{log['icon']} **{timestamp}** - {agent_icon} {log['message']}"
                )
    
    def render_summary(self, results: Dict[str, Any]):
        """
        Render research summary.
        
        Args:
            results: Research results from multi-agent graph
        """
        st.markdown("### 📊 Research Summary")
        
        metadata = results.get("report_metadata", {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Agents Used",
                metadata.get("agents_used", 0),
                delta=None
            )
        
        with col2:
            st.metric(
                "Total Sources",
                metadata.get("total_sources", 0),
                delta=None
            )
        
        with col3:
            confidence = metadata.get("average_confidence", 0.0)
            st.metric(
                "Avg Confidence",
                f"{confidence:.0%}",
                delta=None
            )
        
        with col4:
            st.metric(
                "Report Type",
                metadata.get("report_type", "N/A"),
                delta=None
            )
    
    def clear_logs(self):
        """Clear all logs and status."""
        st.session_state.agent_logs = []
        st.session_state.agent_status = {}
