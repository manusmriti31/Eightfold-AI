"""Report viewer component - Display research results."""

import streamlit as st
from typing import Dict, Any, List
import base64


class ReportViewer:
    """Component for viewing research reports."""
    
    def __init__(self):
        """Initialize report viewer."""
        pass
    
    def _clean_markdown(self, content: str) -> str:
        """
        Clean markdown content by removing code block wrappers.
        
        Args:
            content: Raw markdown content
            
        Returns:
            Cleaned markdown content
        """
        # Remove markdown code block wrappers if present
        content = content.strip()
        if content.startswith("```markdown"):
            content = content[len("```markdown"):].strip()
        elif content.startswith("```"):
            content = content[3:].strip()
        
        if content.endswith("```"):
            content = content[:-3].strip()
        
        return content
    
    def render(self, results: Dict[str, Any]):
        """
        Render complete report.
        
        Args:
            results: Research results from multi-agent graph
        """
        company = results.get("company", results.get("report_metadata", {}).get("company", "Company"))
        
        st.markdown(f"# 📄 Research Report: {company}")
        
        # Check if we have individual reports (new format) or consolidated report (old format)
        individual_reports = results.get("individual_reports", {})
        
        if individual_reports:
            # New format: Individual reports per agent
            self._render_individual_reports(results, individual_reports)
        else:
            # Old format: Consolidated report
            self._render_consolidated_report(results)
    
    def _render_individual_reports(self, results: Dict[str, Any], individual_reports: Dict[str, str]):
        """Render individual reports from each agent."""
        # Create tabs for each agent report
        agent_tabs = []
        agent_names = []
        
        if "profile" in individual_reports:
            agent_tabs.append("🏢 Business Profile")
            agent_names.append("profile")
        if "leadership" in individual_reports:
            agent_tabs.append("👥 Leadership Team")
            agent_names.append("leadership")
        if "financial" in individual_reports:
            agent_tabs.append("💰 Financial Analysis")
            agent_names.append("financial")
        if "market" in individual_reports:
            agent_tabs.append("📊 Market & Competition")
            agent_names.append("market")
        if "signals" in individual_reports:
            agent_tabs.append("🚨 News & Risks")
            agent_names.append("signals")
        
        tabs = st.tabs(agent_tabs)
        
        for idx, (tab, agent_name) in enumerate(zip(tabs, agent_names)):
            with tab:
                # Clean markdown (remove code block wrappers if present)
                report_content = self._clean_markdown(individual_reports[agent_name])
                st.markdown(report_content)
                
                # Download button for individual report
                st.download_button(
                    label=f"📥 Download {agent_tabs[idx]} Report",
                    data=report_content,
                    file_name=f"{results.get('company', 'company')}_{agent_name}_report.md",
                    mime="text/markdown",
                    key=f"download_{agent_name}"
                )
    
    def _render_consolidated_report(self, results: Dict[str, Any]):
        """Render old consolidated report format."""
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs([
            "📝 Executive Summary",
            "📊 Full Report",
            "🔗 Sources"
        ])
        
        with tab1:
            self._render_executive_summary(results)
        
        with tab2:
            self._render_full_report(results)
        
        with tab3:
            self._render_sources(results)
        
        # Download buttons
        self._render_download_buttons(results)
    
    def _render_executive_summary(self, results: Dict[str, Any]):
        """Render executive summary tab."""
        summary = results.get("executive_summary", "No summary available.")
        
        st.markdown("### 📋 Executive Summary")
        st.info(summary)
        
        # Key metrics
        metadata = results.get("report_metadata", {})
        
        st.markdown("### 📊 Key Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Confidence Score",
                f"{metadata.get('average_confidence', 0):.0%}"
            )
        
        with col2:
            st.metric(
                "Sources Used",
                metadata.get("total_sources", 0)
            )
        
        with col3:
            st.metric(
                "Agents",
                metadata.get("agents_used", 0)
            )
    
    def _render_full_report(self, results: Dict[str, Any]):
        """Render full report tab."""
        report = results.get("final_report", "No report available.")
        
        st.markdown(report)
    
    def _render_sources(self, results: Dict[str, Any]):
        """Render sources tab."""
        sources = results.get("all_sources", [])
        
        if not sources:
            st.info("No sources available.")
            return
        
        st.markdown(f"### 🔗 Sources ({len(sources)} total)")
        
        # Group sources by domain
        from urllib.parse import urlparse
        sources_by_domain = {}
        
        for url in sources:
            try:
                domain = urlparse(url).netloc
                if domain not in sources_by_domain:
                    sources_by_domain[domain] = []
                sources_by_domain[domain].append(url)
            except:
                if "other" not in sources_by_domain:
                    sources_by_domain["other"] = []
                sources_by_domain["other"].append(url)
        
        # Display sources by domain
        for domain, urls in sorted(sources_by_domain.items()):
            with st.expander(f"📌 {domain} ({len(urls)} sources)"):
                for idx, url in enumerate(urls, 1):
                    st.markdown(f"{idx}. [{url}]({url})")
    
    def _render_download_buttons(self, results: Dict[str, Any]):
        """Render download buttons."""
        st.markdown("---")
        st.markdown("### 💾 Export Report")
        
        col1, col2, col3 = st.columns(3)
        
        # Markdown download
        with col1:
            report_md = results.get("final_report", "")
            st.download_button(
                label="📄 Download Markdown",
                data=report_md,
                file_name=f"{results.get('report_metadata', {}).get('company', 'report')}_report.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        # Text download
        with col2:
            report_text = self._markdown_to_text(report_md)
            st.download_button(
                label="📝 Download Text",
                data=report_text,
                file_name=f"{results.get('report_metadata', {}).get('company', 'report')}_report.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        # JSON download
        with col3:
            import json
            report_json = json.dumps(results, indent=2, default=str)
            st.download_button(
                label="📊 Download JSON",
                data=report_json,
                file_name=f"{results.get('report_metadata', {}).get('company', 'report')}_data.json",
                mime="application/json",
                use_container_width=True
            )
    
    def _markdown_to_text(self, markdown: str) -> str:
        """
        Convert markdown to plain text.
        
        Args:
            markdown: Markdown content
            
        Returns:
            Plain text content
        """
        import re
        
        # Remove markdown formatting
        text = re.sub(r'#{1,6}\s', '', markdown)  # Headers
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)  # Italic
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # Links
        
        return text
    
    def render_error(self, error: Exception):
        """
        Render error message.
        
        Args:
            error: Exception that occurred
        """
        st.error("❌ An error occurred during research")
        
        with st.expander("🔍 Error Details"):
            st.code(str(error))
            
            import traceback
            st.code(traceback.format_exc())
        
        st.info("💡 Try again with a different company or check your API keys.")
