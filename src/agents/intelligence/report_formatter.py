"""Report Formatter Agent - Creates rich, specialized reports with visualizations."""

from typing import Dict, Any, Optional
from dataclasses import dataclass

from src.tools.visualization.chart_generator import ChartGenerator
from src.tools.visualization.table_builder import TableBuilder


@dataclass
class FormattedReport:
    """Container for formatted report with HTML and metadata."""
    html_content: str
    report_type: str
    has_charts: bool
    has_tables: bool
    has_images: bool
    sections: list


class ReportFormatter:
    """Formats research data into rich HTML reports with visualizations."""
    
    def __init__(self):
        """Initialize report formatter with visualization tools."""
        self.chart_generator = ChartGenerator()
        self.table_builder = TableBuilder()
    
    def format_financial_report(
        self,
        company_name: str,
        financial_data: Optional[Dict[str, Any]],
        profile_data: Optional[Dict[str, Any]] = None
    ) -> FormattedReport:
        """Format financial data into professional document-style report.
        
        Args:
            company_name: Company name
            financial_data: Financial data from agent
            profile_data: Optional profile data for context
            
        Returns:
            FormattedReport with HTML content
        """
        sections = []
        has_charts = False
        has_tables = False
        
        # Professional document styling
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{company_name} - Financial Analysis Report</title>
            <style>
                body {{
                    font-family: Georgia, 'Times New Roman', serif;
                    line-height: 1.8;
                    color: #2c3e50;
                    max-width: 900px;
                    margin: 40px auto;
                    padding: 40px;
                    background-color: #ffffff;
                }}
                h1 {{
                    font-size: 28px;
                    color: #1a1a1a;
                    border-bottom: 3px solid #2c3e50;
                    padding-bottom: 15px;
                    margin-bottom: 10px;
                    font-weight: 600;
                }}
                .subtitle {{
                    font-size: 14px;
                    color: #7f8c8d;
                    margin-bottom: 40px;
                    font-style: italic;
                }}
                h2 {{
                    font-size: 22px;
                    color: #2c3e50;
                    margin-top: 40px;
                    margin-bottom: 20px;
                    font-weight: 600;
                }}
                h3 {{
                    font-size: 18px;
                    color: #34495e;
                    margin-top: 30px;
                    margin-bottom: 15px;
                    font-weight: 600;
                }}
                p {{
                    margin-bottom: 15px;
                    text-align: justify;
                }}
                .chart-container {{
                    margin: 30px 0;
                    padding: 20px 0;
                    text-align: center;
                }}
                .chart-caption {{
                    font-size: 13px;
                    color: #7f8c8d;
                    font-style: italic;
                    margin-top: 10px;
                    text-align: center;
                }}
                .table-container {{
                    margin: 25px 0;
                }}
            </style>
        </head>
        <body>
            <h1>{company_name}</h1>
            <div class="subtitle">Financial Analysis Report</div>
        """
        
        if not financial_data:
            html += """
            <h2>Executive Summary</h2>
            <p>Insufficient financial data available for comprehensive analysis of this company.</p>
            </body>
            </html>
            """
            return FormattedReport(
                html_content=html,
                report_type="financial",
                has_charts=False,
                has_tables=False,
                has_images=False,
                sections=["header", "no_data"]
            )
        
        # Executive Summary
        html += '<h2>Executive Summary</h2>'
        revenue_data = financial_data.get('revenue')
        profitability_data = financial_data.get('profitability')
        
        # Build narrative summary
        summary_parts = []
        if revenue_data and revenue_data.get('current_revenue'):
            revenue_val = revenue_data['current_revenue']
            revenue_str = f"${revenue_val / 1e9:.1f} billion" if revenue_val >= 1e9 else f"${revenue_val / 1e6:.0f} million"
            year = revenue_data.get('revenue_year', 2024)
            growth = revenue_data.get('yoy_growth_rate', 0)
            summary_parts.append(f"{company_name} reported annual revenue of {revenue_str} for fiscal year {year}")
            if growth:
                summary_parts.append(f"representing a year-over-year growth rate of {growth:+.1f}%")
        
        if profitability_data:
            is_profitable = profitability_data.get('is_profitable')
            if is_profitable is not None:
                if is_profitable:
                    summary_parts.append(f"The company is currently profitable")
                    if profitability_data.get('net_margin'):
                        summary_parts.append(f"with a net profit margin of {profitability_data['net_margin']:.1f}%")
                else:
                    summary_parts.append(f"The company is not yet profitable")
        
        if summary_parts:
            html += f'<p>{", ".join(summary_parts)}.</p>'
        
        # Revenue Analysis Section
        if revenue_data:
            sections.append("revenue")
            html += '<h2>Revenue Analysis</h2>'
            
            # Narrative text
            current_revenue = revenue_data.get('current_revenue')
            if current_revenue:
                revenue_str = f"${current_revenue / 1e9:.2f} billion" if current_revenue >= 1e9 else f"${current_revenue / 1e6:.0f} million"
                year = revenue_data.get('revenue_year', 2024)
                html += f'<p>{company_name} generated {revenue_str} in revenue during fiscal year {year}. '
                
                growth_rate = revenue_data.get('yoy_growth_rate')
                if growth_rate:
                    if growth_rate > 0:
                        html += f'This represents a strong year-over-year growth rate of {growth_rate:.1f}%, indicating robust business expansion and market demand. '
                    else:
                        html += f'Revenue declined by {abs(growth_rate):.1f}% year-over-year, suggesting challenges in market conditions or competitive pressures. '
                
                html += 'The revenue performance is illustrated in Figure 1 below.</p>'
            
            # Revenue chart embedded in text
            revenue_chart = self.chart_generator.create_revenue_chart(revenue_data, company_name)
            if revenue_chart:
                html += '<div class="chart-container">'
                html += revenue_chart
                html += '<div class="chart-caption">Figure 1: Revenue Growth Trend</div>'
                html += '</div>'
                has_charts = True
            
            # Revenue table embedded in text
            html += '<p>Table 1 provides a detailed breakdown of the revenue metrics:</p>'
            html += '<div class="table-container">'
            revenue_table = self.table_builder.create_revenue_table(revenue_data)
            if revenue_table:
                html += revenue_table
                has_tables = True
            html += '</div>'
        
        # Profitability Analysis Section
        if profitability_data:
            sections.append("profitability")
            html += '<h2>Profitability Analysis</h2>'
            
            # Narrative analysis
            is_profitable = profitability_data.get('is_profitable')
            if is_profitable is not None:
                if is_profitable:
                    html += f'<p>{company_name} has achieved profitability, demonstrating effective cost management and operational efficiency. '
                else:
                    html += f'<p>{company_name} is currently operating at a loss as it invests in growth and market expansion. '
            
            # Discuss margins
            gross_margin = profitability_data.get('gross_margin')
            ebitda_margin = profitability_data.get('ebitda_margin')
            net_margin = profitability_data.get('net_margin')
            
            if gross_margin or ebitda_margin or net_margin:
                html += 'The company\'s margin profile reveals important insights into operational efficiency: '
                margin_comments = []
                if gross_margin:
                    if gross_margin > 40:
                        margin_comments.append(f'a strong gross margin of {gross_margin:.1f}% indicating pricing power and efficient production')
                    elif gross_margin > 20:
                        margin_comments.append(f'a healthy gross margin of {gross_margin:.1f}%')
                    else:
                        margin_comments.append(f'a gross margin of {gross_margin:.1f}% suggesting competitive pricing pressures')
                
                if ebitda_margin:
                    margin_comments.append(f'EBITDA margin of {ebitda_margin:.1f}%')
                
                if net_margin:
                    margin_comments.append(f'net profit margin of {net_margin:.1f}%')
                
                html += ', '.join(margin_comments) + '. '
            
            html += 'Figure 2 illustrates the profitability margin structure.</p>'
            
            # Profitability chart
            prof_chart = self.chart_generator.create_profitability_dashboard(profitability_data, company_name)
            if prof_chart:
                html += '<div class="chart-container">'
                html += prof_chart
                html += '<div class="chart-caption">Figure 2: Profitability Margins</div>'
                html += '</div>'
                has_charts = True
            
            # Profitability table
            html += '<p>Table 2 summarizes the key profitability metrics:</p>'
            html += '<div class="table-container">'
            prof_table = self.table_builder.create_profitability_table(profitability_data)
            if prof_table:
                html += prof_table
                has_tables = True
            html += '</div>'
        
        # Funding & Capital Structure Section
        funding_data = financial_data.get('funding')
        if funding_data:
            sections.append("funding")
            html += '<h2>Funding & Capital Structure</h2>'
            
            # Narrative about funding
            total_raised = funding_data.get('total_raised')
            if total_raised:
                raised_str = f"${total_raised / 1e9:.1f} billion" if total_raised >= 1e9 else f"${total_raised / 1e6:.0f} million"
                html += f'<p>{company_name} has raised {raised_str} in total funding. '
                
                last_round = funding_data.get('last_round_type')
                if last_round:
                    html += f'The most recent funding round was a {last_round}'
                    last_amount = funding_data.get('last_round_amount')
                    if last_amount:
                        amount_str = f"${last_amount / 1e9:.1f} billion" if last_amount >= 1e9 else f"${last_amount / 1e6:.0f} million"
                        html += f' of {amount_str}'
                    last_date = funding_data.get('last_round_date')
                    if last_date:
                        html += f' completed in {last_date}'
                    html += '. '
                
                valuation = funding_data.get('valuation')
                if valuation:
                    val_str = f"${valuation / 1e9:.1f} billion" if valuation >= 1e9 else f"${valuation / 1e6:.0f} million"
                    html += f'The company is currently valued at approximately {val_str}. '
                
                html += 'Table 3 provides detailed funding information.</p>'
            
            # Funding table
            html += '<div class="table-container">'
            funding_table = self.table_builder.create_funding_table(funding_data)
            if funding_table:
                html += funding_table
                has_tables = True
            html += '</div>'
        
        # Financial Health Assessment Section
        health_score = financial_data.get('financial_health_score', 0)
        if health_score:
            sections.append("health")
            html += '<h2>Financial Health Assessment</h2>'
            
            # Narrative assessment
            if health_score >= 80:
                assessment = f'{company_name} demonstrates excellent financial health with strong fundamentals across revenue growth, profitability, and capital efficiency.'
            elif health_score >= 60:
                assessment = f'{company_name} shows good financial health with solid performance in key metrics, though some areas may benefit from improvement.'
            elif health_score >= 40:
                assessment = f'{company_name} exhibits moderate financial health. While the company shows promise, there are notable areas requiring attention and improvement.'
            else:
                assessment = f'{company_name} faces financial health challenges that require strategic intervention and operational improvements.'
            
            html += f'<p>{assessment} The overall financial health score of {health_score:.0f}/100 is derived from a comprehensive analysis of revenue stability, profitability metrics, capital structure, and growth trajectory. Figure 3 visualizes this assessment.</p>'
            
            # Health gauge
            health_gauge = self.chart_generator.create_financial_health_gauge(health_score, company_name)
            if health_gauge:
                html += '<div class="chart-container">'
                html += health_gauge
                html += '<div class="chart-caption">Figure 3: Financial Health Score</div>'
                html += '</div>'
                has_charts = True
        
        # Conclusion
        html += '<h2>Conclusion</h2>'
        html += f'<p>Based on the financial analysis presented, {company_name} '
        if profitability_data and profitability_data.get('is_profitable'):
            html += 'demonstrates strong financial performance with sustainable profitability. '
        else:
            html += 'is in a growth phase with focus on market expansion. '
        
        if revenue_data and revenue_data.get('yoy_growth_rate', 0) > 10:
            html += 'The company exhibits robust revenue growth, indicating strong market demand and effective business execution. '
        
        html += 'Continued monitoring of key financial metrics will be essential for assessing long-term sustainability and growth potential.</p>'
        
        html += """
        </body>
        </html>
        """
        
        return FormattedReport(
            html_content=html,
            report_type="financial",
            has_charts=has_charts,
            has_tables=has_tables,
            has_images=False,
            sections=sections
        )
    
    def format_leadership_report(
        self,
        company_name: str,
        leadership_data: Optional[Dict[str, Any]]
    ) -> FormattedReport:
        """Format leadership data into rich HTML report.
        
        Args:
            company_name: Company name
            leadership_data: Leadership data from agent
            
        Returns:
            FormattedReport with HTML content
        """
        sections = []
        has_tables = False
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{company_name} - Leadership Team</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .report-header {{
                    background: linear-gradient(135deg, #2ca02c 0%, #98df8a 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .report-header h1 {{
                    margin: 0;
                    font-size: 32px;
                }}
                .section {{
                    background: white;
                    padding: 25px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .section h2 {{
                    color: #2ca02c;
                    border-bottom: 2px solid #2ca02c;
                    padding-bottom: 10px;
                    margin-top: 0;
                }}
                .executive-card {{
                    background: #f8f9fa;
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 8px;
                    border-left: 4px solid #2ca02c;
                }}
                .executive-card h3 {{
                    margin: 0 0 5px 0;
                    color: #2ca02c;
                }}
                .executive-card .role {{
                    color: #666;
                    font-style: italic;
                    margin-bottom: 10px;
                }}
                .executive-card .background {{
                    color: #333;
                    line-height: 1.6;
                }}
            </style>
        </head>
        <body>
            <div class="report-header">
                <h1>{company_name}</h1>
                <p>Leadership Team Analysis</p>
            </div>
        """
        
        if not leadership_data:
            html += """
            <div class="section">
                <h2>⚠️ Limited Leadership Data</h2>
                <p>Insufficient leadership data available for comprehensive analysis.</p>
            </div>
            </body>
            </html>
            """
            return FormattedReport(
                html_content=html,
                report_type="leadership",
                has_charts=False,
                has_tables=False,
                has_images=False,
                sections=["header", "no_data"]
            )
        
        # Founders Section
        founders = leadership_data.get('founders', [])
        if founders:
            sections.append("founders")
            html += '<div class="section"><h2>🚀 Founders</h2>'
            
            for founder in founders:
                name = founder.get('name', 'Unknown')
                role = founder.get('role', 'Founder')
                background = founder.get('background', 'No background information available.')
                previous_companies = founder.get('previous_companies', [])
                
                html += f"""
                <div class="executive-card">
                    <h3>{name}</h3>
                    <div class="role">{role}</div>
                    <div class="background">{background}</div>
                """
                
                if previous_companies:
                    html += f'<p><strong>Previous:</strong> {", ".join(previous_companies)}</p>'
                
                html += '</div>'
            
            html += '</div>'
        
        # Executive Team Section
        executives = leadership_data.get('executives', [])
        if executives:
            sections.append("executives")
            html += '<div class="section"><h2>👥 Executive Team</h2>'
            
            # Executive table
            exec_table = self.table_builder.create_executive_table(executives)
            if exec_table:
                html += exec_table
                has_tables = True
            else:
                # Fallback to cards
                for exec in executives[:5]:
                    name = exec.get('name', 'Unknown')
                    role = exec.get('role', 'Executive')
                    background = exec.get('background', 'No background information available.')
                    
                    html += f"""
                    <div class="executive-card">
                        <h3>{name}</h3>
                        <div class="role">{role}</div>
                        <div class="background">{background}</div>
                    </div>
                    """
            
            html += '</div>'
        
        # Leadership Style Section
        leadership_style = leadership_data.get('leadership_style')
        if leadership_style:
            sections.append("style")
            html += f"""
            <div class="section">
                <h2>🎯 Leadership Style & Culture</h2>
                <p>{leadership_style}</p>
            </div>
            """
        
        # Key Risks Section
        key_risks = leadership_data.get('key_risks', [])
        if key_risks:
            sections.append("risks")
            html += '<div class="section"><h2>⚠️ Key Person Risks</h2><ul>'
            for risk in key_risks:
                html += f'<li>{risk}</li>'
            html += '</ul></div>'
        
        html += """
        </body>
        </html>
        """
        
        return FormattedReport(
            html_content=html,
            report_type="leadership",
            has_charts=False,
            has_tables=has_tables,
            has_images=False,
            sections=sections
        )
    
    def format_market_report(
        self,
        company_name: str,
        market_data: Optional[Dict[str, Any]]
    ) -> FormattedReport:
        """Format market data into rich HTML report.
        
        Args:
            company_name: Company name
            market_data: Market data from agent
            
        Returns:
            FormattedReport with HTML content
        """
        sections = []
        has_charts = False
        has_tables = False
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{company_name} - Market Analysis</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .report-header {{
                    background: linear-gradient(135deg, #ff7f0e 0%, #ffbb78 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .report-header h1 {{
                    margin: 0;
                    font-size: 32px;
                }}
                .section {{
                    background: white;
                    padding: 25px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .section h2 {{
                    color: #ff7f0e;
                    border-bottom: 2px solid #ff7f0e;
                    padding-bottom: 10px;
                    margin-top: 0;
                }}
            </style>
        </head>
        <body>
            <div class="report-header">
                <h1>{company_name}</h1>
                <p>Market & Competition Analysis</p>
            </div>
        """
        
        if not market_data:
            html += """
            <div class="section">
                <h2>⚠️ Limited Market Data</h2>
                <p>Insufficient market data available for comprehensive analysis.</p>
            </div>
            </body>
            </html>
            """
            return FormattedReport(
                html_content=html,
                report_type="market",
                has_charts=False,
                has_tables=False,
                has_images=False,
                sections=["header", "no_data"]
            )
        
        # Market Size Section
        market = market_data.get('market')
        if market:
            sections.append("market_size")
            html += '<div class="section"><h2>📈 Market Size</h2>'
            
            tam = market.get('tam')
            sam = market.get('sam')
            growth_rate = market.get('growth_rate')
            
            if tam:
                html += f'<p><strong>TAM (Total Addressable Market):</strong> ${tam / 1e9:.1f}B</p>'
            if sam:
                html += f'<p><strong>SAM (Serviceable Addressable Market):</strong> ${sam / 1e9:.1f}B</p>'
            if growth_rate:
                html += f'<p><strong>Market Growth Rate:</strong> {growth_rate:.1f}% annually</p>'
            
            html += '</div>'
        
        # Competitors Section
        competitors = market_data.get('competitors', [])
        if competitors:
            sections.append("competitors")
            html += '<div class="section"><h2>🏆 Competitive Landscape</h2>'
            
            # Competitor table
            comp_table = self.table_builder.create_competitor_table(competitors, company_name)
            if comp_table:
                html += comp_table
                has_tables = True
            
            html += '</div>'
        
        # SWOT Analysis Section
        swot = market_data.get('swot')
        if swot:
            sections.append("swot")
            html += '<div class="section"><h2>🎯 SWOT Analysis</h2>'
            
            # SWOT chart
            swot_chart = self.chart_generator.create_swot_matrix(swot, company_name)
            if swot_chart:
                html += swot_chart
                has_charts = True
            else:
                # Fallback to text
                for category in ['strengths', 'weaknesses', 'opportunities', 'threats']:
                    items = swot.get(category, [])
                    if items:
                        html += f'<h3>{category.title()}</h3><ul>'
                        for item in items:
                            html += f'<li>{item}</li>'
                        html += '</ul>'
            
            html += '</div>'
        
        # Market Position Section
        market_position = market_data.get('market_position')
        if market_position:
            sections.append("position")
            html += f"""
            <div class="section">
                <h2>📍 Market Position</h2>
                <p>{market_position}</p>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return FormattedReport(
            html_content=html,
            report_type="market",
            has_charts=has_charts,
            has_tables=has_tables,
            has_images=False,
            sections=sections
        )
