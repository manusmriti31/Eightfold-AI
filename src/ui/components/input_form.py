"""Input form component - Company research input."""

import streamlit as st
from typing import Dict, Any, Union


class InputForm:
    """Component for research input form."""
    
    REPORT_TYPES = {
        "investment_memo": "📈 Investment Memo",
        "due_diligence": "🔍 Due Diligence Report",
        "sales_account_plan": "💼 Sales Account Plan",
        "competitive_intelligence": "⚔️ Competitive Intelligence"
    }
    
    def __init__(self):
        """Initialize input form."""
        if "company_name" not in st.session_state:
            st.session_state.company_name = ""
        if "report_type" not in st.session_state:
            st.session_state.report_type = "investment_memo"
    
    def render(self) -> Union[Dict[str, Any], None]:
        """
        Render input form.
        
        Returns:
            Dictionary with form data if submitted, None otherwise
        """
        st.markdown("## 🔍 Company Research")
        st.markdown("Enter a company name and select which areas to research.")
        
        with st.form("research_form"):
            # Company name input
            company = st.text_input(
                "Company Name",
                value=st.session_state.company_name,
                placeholder="e.g., Tesla, Microsoft, OpenAI",
                help="Enter the full company name"
            )
            
            # Agent selection
            st.markdown("### 📊 Select Research Areas")
            st.markdown("Choose which aspects of the company you want to research:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                profile_selected = st.checkbox(
                    "🏢 Business Profile",
                    value=True,
                    help="Business model, products, revenue streams"
                )
                leadership_selected = st.checkbox(
                    "👥 Leadership Team",
                    value=True,
                    help="Founders, executives, management"
                )
                financial_selected = st.checkbox(
                    "💰 Financial Analysis",
                    value=True,
                    help="Revenue, profitability, funding"
                )
            
            with col2:
                market_selected = st.checkbox(
                    "📊 Market & Competition",
                    value=True,
                    help="Market size, competitors, SWOT"
                )
                signals_selected = st.checkbox(
                    "🚨 News & Risk Signals",
                    value=False,
                    help="Recent news, sentiment, risks"
                )
            
            # Report type selection
            report_type = st.selectbox(
                "Report Type",
                options=list(self.REPORT_TYPES.keys()),
                format_func=lambda x: self.REPORT_TYPES[x],
                index=list(self.REPORT_TYPES.keys()).index(st.session_state.report_type),
                help="Select the type of report to generate"
            )
            
            # Advanced options (collapsible)
            with st.expander("⚙️ Advanced Options"):
                max_queries = st.slider(
                    "Queries per Agent",
                    min_value=3,
                    max_value=10,
                    value=5,
                    help="Number of search queries each agent will generate"
                )
                
                max_results = st.slider(
                    "Results per Query",
                    min_value=2,
                    max_value=5,
                    value=3,
                    help="Number of search results to retrieve per query"
                )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submitted = st.form_submit_button(
                    "🚀 Start Research",
                    use_container_width=True,
                    type="primary"
                )
            
            if submitted:
                if not company.strip():
                    st.error("Please enter a company name")
                    return None
                
                # Build selected agents list
                selected_agents = []
                if profile_selected:
                    selected_agents.append("profile")
                if leadership_selected:
                    selected_agents.append("leadership")
                if financial_selected:
                    selected_agents.append("financial")
                if market_selected:
                    selected_agents.append("market")
                if signals_selected:
                    selected_agents.append("signals")
                
                if not selected_agents:
                    st.error("Please select at least one research area")
                    return None
                
                # Update session state
                st.session_state.company_name = company
                st.session_state.report_type = report_type
                
                return {
                    "company": company.strip(),
                    "report_type": report_type,
                    "selected_agents": selected_agents,
                    "max_queries": max_queries,
                    "max_results": max_results
                }
        
        return None
    
    def render_examples(self):
        """Render example companies."""
        st.markdown("### 💡 Example Companies")
        
        examples = [
            ("Tesla", "investment_memo"),
            ("Microsoft", "due_diligence"),
            ("OpenAI", "competitive_intelligence"),
            ("Stripe", "sales_account_plan")
        ]
        
        cols = st.columns(len(examples))
        
        for idx, (company, report_type) in enumerate(examples):
            with cols[idx]:
                if st.button(
                    company,
                    key=f"example_{company}",
                    use_container_width=True
                ):
                    st.session_state.company_name = company
                    st.session_state.report_type = report_type
                    st.rerun()
