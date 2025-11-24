"""Chart generator for financial and market visualizations."""

from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class ChartGenerator:
    """Generates interactive charts using Plotly."""
    
    def __init__(self):
        """Initialize chart generator with default styling."""
        self.default_colors = {
            'primary': '#1f77b4',
            'success': '#2ca02c',
            'warning': '#ff7f0e',
            'danger': '#d62728',
            'info': '#17becf'
        }
    
    def create_revenue_chart(
        self,
        revenue_data: Dict[str, Any],
        company_name: str
    ) -> Optional[str]:
        """Create revenue growth chart.
        
        Args:
            revenue_data: Revenue information
            company_name: Company name for title
            
        Returns:
            HTML string of the chart or None if insufficient data
        """
        if not revenue_data or not revenue_data.get('current_revenue'):
            return None
        
        current_revenue = revenue_data.get('current_revenue', 0)
        year = revenue_data.get('revenue_year', 2024)
        growth_rate = revenue_data.get('yoy_growth_rate', 0)
        
        # Calculate previous year revenue
        if growth_rate:
            previous_revenue = current_revenue / (1 + growth_rate / 100)
        else:
            previous_revenue = current_revenue * 0.85  # Estimate
        
        # Create data
        years = [year - 1, year]
        revenues = [previous_revenue / 1e9, current_revenue / 1e9]  # Convert to billions
        
        # Create bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=years,
            y=revenues,
            text=[f'${r:.1f}B' for r in revenues],
            textposition='outside',
            marker_color=self.default_colors['primary'],
            name='Revenue'
        ))
        
        fig.update_layout(
            title=f'{company_name} Revenue Growth',
            xaxis_title='Year',
            yaxis_title='Revenue (Billions USD)',
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='revenue_chart')
    
    def create_profitability_dashboard(
        self,
        profitability_data: Dict[str, Any],
        company_name: str
    ) -> Optional[str]:
        """Create profitability metrics dashboard.
        
        Args:
            profitability_data: Profitability information
            company_name: Company name for title
            
        Returns:
            HTML string of the dashboard or None if insufficient data
        """
        if not profitability_data:
            return None
        
        # Extract margins
        margins = {}
        if profitability_data.get('gross_margin'):
            margins['Gross Margin'] = profitability_data['gross_margin']
        if profitability_data.get('ebitda_margin'):
            margins['EBITDA Margin'] = profitability_data['ebitda_margin']
        if profitability_data.get('net_margin'):
            margins['Net Margin'] = profitability_data['net_margin']
        
        if not margins:
            return None
        
        # Create horizontal bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=list(margins.keys()),
            x=list(margins.values()),
            orientation='h',
            text=[f'{v:.1f}%' for v in margins.values()],
            textposition='outside',
            marker_color=[
                self.default_colors['success'] if v > 20 else
                self.default_colors['warning'] if v > 10 else
                self.default_colors['danger']
                for v in margins.values()
            ]
        ))
        
        fig.update_layout(
            title=f'{company_name} Profitability Margins',
            xaxis_title='Margin (%)',
            template='plotly_white',
            height=300,
            showlegend=False
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='profitability_chart')
    
    def create_funding_timeline(
        self,
        funding_data: Dict[str, Any],
        company_name: str
    ) -> Optional[str]:
        """Create funding timeline visualization.
        
        Args:
            funding_data: Funding information
            company_name: Company name for title
            
        Returns:
            HTML string of the timeline or None if insufficient data
        """
        if not funding_data or not funding_data.get('total_raised'):
            return None
        
        total_raised = funding_data.get('total_raised', 0)
        last_round = funding_data.get('last_round_amount', 0)
        last_round_type = funding_data.get('last_round_type', 'Unknown')
        
        # Create simple visualization
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=total_raised / 1e6,  # Convert to millions
            title={'text': f"{company_name} Total Funding"},
            delta={'reference': last_round / 1e6 if last_round else 0},
            number={'suffix': 'M', 'prefix': '$'},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        
        fig.update_layout(
            height=250,
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='funding_chart')
    
    def create_market_share_chart(
        self,
        competitors: List[Dict[str, Any]],
        company_name: str
    ) -> Optional[str]:
        """Create market share pie chart.
        
        Args:
            competitors: List of competitor data
            company_name: Company name for title
            
        Returns:
            HTML string of the chart or None if insufficient data
        """
        if not competitors or len(competitors) < 2:
            return None
        
        # Extract market shares
        names = [company_name] + [c.get('name', 'Unknown') for c in competitors[:4]]
        shares = [30] + [20, 15, 15, 20][:len(competitors)]  # Placeholder data
        
        fig = go.Figure(data=[go.Pie(
            labels=names,
            values=shares,
            hole=0.3,
            marker_colors=[self.default_colors['primary']] + 
                         [self.default_colors['info']] * len(competitors)
        )])
        
        fig.update_layout(
            title=f'{company_name} Market Position',
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='market_share_chart')
    
    def create_swot_matrix(
        self,
        swot_data: Dict[str, List[str]],
        company_name: str
    ) -> Optional[str]:
        """Create SWOT analysis matrix visualization.
        
        Args:
            swot_data: SWOT analysis data
            company_name: Company name for title
            
        Returns:
            HTML string of the matrix or None if insufficient data
        """
        if not swot_data:
            return None
        
        # Create 2x2 subplot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Strengths', 'Weaknesses', 'Opportunities', 'Threats'),
            specs=[[{'type': 'table'}, {'type': 'table'}],
                   [{'type': 'table'}, {'type': 'table'}]]
        )
        
        # Add tables for each quadrant
        quadrants = [
            ('strengths', 1, 1, self.default_colors['success']),
            ('weaknesses', 1, 2, self.default_colors['danger']),
            ('opportunities', 2, 1, self.default_colors['info']),
            ('threats', 2, 2, self.default_colors['warning'])
        ]
        
        for key, row, col, color in quadrants:
            items = swot_data.get(key, [])[:5]  # Top 5 items
            if items:
                fig.add_trace(
                    go.Table(
                        cells=dict(
                            values=[items],
                            fill_color=color,
                            font=dict(color='white', size=11),
                            align='left',
                            height=30
                        )
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(
            title=f'{company_name} SWOT Analysis',
            height=600,
            showlegend=False
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='swot_chart')
    
    def create_financial_health_gauge(
        self,
        health_score: float,
        company_name: str
    ) -> Optional[str]:
        """Create financial health gauge chart.
        
        Args:
            health_score: Health score 0-100
            company_name: Company name for title
            
        Returns:
            HTML string of the gauge or None if no score
        """
        if not health_score:
            return None
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            title={'text': f"{company_name} Financial Health Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': self.default_colors['danger']},
                    {'range': [40, 70], 'color': self.default_colors['warning']},
                    {'range': [70, 100], 'color': self.default_colors['success']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            template='plotly_white'
        )
        
        return fig.to_html(include_plotlyjs='cdn', div_id='health_gauge')
