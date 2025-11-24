"""Table builder for structured data presentation."""

from typing import Dict, Any, List, Optional


class TableBuilder:
    """Builds HTML tables for structured data."""
    
    def __init__(self):
        """Initialize table builder with default styling."""
        self.table_style = """
        <style>
            .data-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 14px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .data-table thead tr {
                background-color: #1f77b4;
                color: white;
                text-align: left;
            }
            .data-table th,
            .data-table td {
                padding: 12px 15px;
            }
            .data-table tbody tr {
                border-bottom: 1px solid #dddddd;
            }
            .data-table tbody tr:nth-of-type(even) {
                background-color: #f3f3f3;
            }
            .data-table tbody tr:last-of-type {
                border-bottom: 2px solid #1f77b4;
            }
            .data-table tbody tr:hover {
                background-color: #e8f4f8;
            }
            .metric-positive {
                color: #2ca02c;
                font-weight: bold;
            }
            .metric-negative {
                color: #d62728;
                font-weight: bold;
            }
            .metric-neutral {
                color: #666;
            }
        </style>
        """
    
    def create_revenue_table(
        self,
        revenue_data: Dict[str, Any]
    ) -> Optional[str]:
        """Create revenue breakdown table.
        
        Args:
            revenue_data: Revenue information
            
        Returns:
            HTML string of the table or None if insufficient data
        """
        if not revenue_data or not revenue_data.get('current_revenue'):
            return None
        
        current_revenue = revenue_data.get('current_revenue', 0)
        year = revenue_data.get('revenue_year', 2024)
        growth_rate = revenue_data.get('yoy_growth_rate', 0)
        currency = revenue_data.get('currency', 'USD')
        is_estimated = revenue_data.get('is_estimated', False)
        
        # Format revenue
        revenue_str = f"${current_revenue / 1e9:.2f}B" if current_revenue >= 1e9 else f"${current_revenue / 1e6:.1f}M"
        growth_class = "metric-positive" if growth_rate > 0 else "metric-negative" if growth_rate < 0 else "metric-neutral"
        
        html = f"""
        {self.table_style}
        <table class="data-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                    <th>Notes</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Annual Revenue</td>
                    <td><strong>{revenue_str}</strong></td>
                    <td>FY {year}</td>
                </tr>
                <tr>
                    <td>YoY Growth Rate</td>
                    <td class="{growth_class}">{growth_rate:+.1f}%</td>
                    <td>Year-over-year change</td>
                </tr>
                <tr>
                    <td>Currency</td>
                    <td>{currency}</td>
                    <td>{'Estimated' if is_estimated else 'Official'}</td>
                </tr>
            </tbody>
        </table>
        """
        
        return html
    
    def create_profitability_table(
        self,
        profitability_data: Dict[str, Any]
    ) -> Optional[str]:
        """Create profitability metrics table.
        
        Args:
            profitability_data: Profitability information
            
        Returns:
            HTML string of the table or None if insufficient data
        """
        if not profitability_data:
            return None
        
        is_profitable = profitability_data.get('is_profitable')
        net_income = profitability_data.get('net_income')
        ebitda = profitability_data.get('ebitda')
        gross_margin = profitability_data.get('gross_margin')
        ebitda_margin = profitability_data.get('ebitda_margin')
        net_margin = profitability_data.get('net_margin')
        
        rows = []
        
        if is_profitable is not None:
            status = "✓ Profitable" if is_profitable else "✗ Not Profitable"
            status_class = "metric-positive" if is_profitable else "metric-negative"
            rows.append(f"""
                <tr>
                    <td>Profitability Status</td>
                    <td class="{status_class}"><strong>{status}</strong></td>
                </tr>
            """)
        
        if net_income is not None:
            income_str = f"${abs(net_income) / 1e9:.2f}B" if abs(net_income) >= 1e9 else f"${abs(net_income) / 1e6:.1f}M"
            if net_income < 0:
                income_str = f"-{income_str}"
            rows.append(f"""
                <tr>
                    <td>Net Income</td>
                    <td>{income_str}</td>
                </tr>
            """)
        
        if ebitda is not None:
            ebitda_str = f"${ebitda / 1e9:.2f}B" if ebitda >= 1e9 else f"${ebitda / 1e6:.1f}M"
            rows.append(f"""
                <tr>
                    <td>EBITDA</td>
                    <td>{ebitda_str}</td>
                </tr>
            """)
        
        if gross_margin is not None:
            rows.append(f"""
                <tr>
                    <td>Gross Margin</td>
                    <td class="metric-positive">{gross_margin:.1f}%</td>
                </tr>
            """)
        
        if ebitda_margin is not None:
            rows.append(f"""
                <tr>
                    <td>EBITDA Margin</td>
                    <td class="metric-positive">{ebitda_margin:.1f}%</td>
                </tr>
            """)
        
        if net_margin is not None:
            margin_class = "metric-positive" if net_margin > 0 else "metric-negative"
            rows.append(f"""
                <tr>
                    <td>Net Margin</td>
                    <td class="{margin_class}">{net_margin:.1f}%</td>
                </tr>
            """)
        
        if not rows:
            return None
        
        html = f"""
        {self.table_style}
        <table class="data-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """
        
        return html
    
    def create_competitor_table(
        self,
        competitors: List[Dict[str, Any]],
        company_name: str
    ) -> Optional[str]:
        """Create competitor comparison table.
        
        Args:
            competitors: List of competitor data
            company_name: Main company name
            
        Returns:
            HTML string of the table or None if insufficient data
        """
        if not competitors:
            return None
        
        rows = []
        for i, comp in enumerate(competitors[:5], 1):  # Top 5 competitors
            name = comp.get('name', 'Unknown')
            market_share = comp.get('market_share', 'N/A')
            strength = comp.get('strength', 'Unknown')
            
            rows.append(f"""
                <tr>
                    <td>{i}</td>
                    <td><strong>{name}</strong></td>
                    <td>{market_share if isinstance(market_share, str) else f'{market_share:.1f}%'}</td>
                    <td>{strength}</td>
                </tr>
            """)
        
        if not rows:
            return None
        
        html = f"""
        {self.table_style}
        <table class="data-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Competitor</th>
                    <th>Market Share</th>
                    <th>Key Strength</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """
        
        return html
    
    def create_executive_table(
        self,
        executives: List[Dict[str, Any]]
    ) -> Optional[str]:
        """Create executive team table.
        
        Args:
            executives: List of executive profiles
            
        Returns:
            HTML string of the table or None if insufficient data
        """
        if not executives:
            return None
        
        rows = []
        for exec in executives[:10]:  # Top 10 executives
            name = exec.get('name', 'Unknown')
            role = exec.get('role', 'N/A')
            background = exec.get('background', 'N/A')
            
            # Truncate background
            if len(background) > 100:
                background = background[:97] + '...'
            
            rows.append(f"""
                <tr>
                    <td><strong>{name}</strong></td>
                    <td>{role}</td>
                    <td>{background}</td>
                </tr>
            """)
        
        if not rows:
            return None
        
        html = f"""
        {self.table_style}
        <table class="data-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Background</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """
        
        return html
    
    def create_funding_table(
        self,
        funding_data: Dict[str, Any]
    ) -> Optional[str]:
        """Create funding history table.
        
        Args:
            funding_data: Funding information
            
        Returns:
            HTML string of the table or None if insufficient data
        """
        if not funding_data:
            return None
        
        total_raised = funding_data.get('total_raised')
        last_round_type = funding_data.get('last_round_type')
        last_round_amount = funding_data.get('last_round_amount')
        last_round_date = funding_data.get('last_round_date')
        valuation = funding_data.get('valuation')
        investors = funding_data.get('investors', [])
        
        rows = []
        
        if total_raised:
            amount_str = f"${total_raised / 1e9:.2f}B" if total_raised >= 1e9 else f"${total_raised / 1e6:.1f}M"
            rows.append(f"""
                <tr>
                    <td>Total Funding Raised</td>
                    <td><strong>{amount_str}</strong></td>
                </tr>
            """)
        
        if last_round_type:
            rows.append(f"""
                <tr>
                    <td>Last Round Type</td>
                    <td>{last_round_type}</td>
                </tr>
            """)
        
        if last_round_amount:
            amount_str = f"${last_round_amount / 1e9:.2f}B" if last_round_amount >= 1e9 else f"${last_round_amount / 1e6:.1f}M"
            rows.append(f"""
                <tr>
                    <td>Last Round Amount</td>
                    <td>{amount_str}</td>
                </tr>
            """)
        
        if last_round_date:
            rows.append(f"""
                <tr>
                    <td>Last Round Date</td>
                    <td>{last_round_date}</td>
                </tr>
            """)
        
        if valuation:
            val_str = f"${valuation / 1e9:.2f}B" if valuation >= 1e9 else f"${valuation / 1e6:.1f}M"
            rows.append(f"""
                <tr>
                    <td>Valuation</td>
                    <td class="metric-positive"><strong>{val_str}</strong></td>
                </tr>
            """)
        
        if investors:
            investor_list = ', '.join(investors[:5])
            if len(investors) > 5:
                investor_list += f' (+{len(investors) - 5} more)'
            rows.append(f"""
                <tr>
                    <td>Key Investors</td>
                    <td>{investor_list}</td>
                </tr>
            """)
        
        if not rows:
            return None
        
        html = f"""
        {self.table_style}
        <table class="data-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """
        
        return html
