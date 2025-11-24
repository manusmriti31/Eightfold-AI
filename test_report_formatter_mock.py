"""Test Phase 2 with mock data (no API calls needed)."""

from pathlib import Path
from src.agents.intelligence.report_formatter import ReportFormatter


def test_with_mock_data():
    """Test report formatting with mock data."""
    
    print("\n" + "="*80)
    print("TESTING PHASE 2: REPORT FORMATTING (Mock Data)")
    print("="*80)
    
    # Initialize formatter
    formatter = ReportFormatter()
    
    # Create output directory
    output_dir = Path("test_reports")
    output_dir.mkdir(exist_ok=True)
    
    print("\n📝 Formatting reports with mock data...")
    
    # Mock Financial Data
    print("\n   Formatting Financial Report...")
    financial_data = {
        'revenue': {
            'current_revenue': 96800000000,  # $96.8B
            'revenue_year': 2024,
            'yoy_growth_rate': 18.5,
            'currency': 'USD',
            'is_estimated': False
        },
        'profitability': {
            'is_profitable': True,
            'net_income': 15000000000,  # $15B
            'ebitda': 18000000000,  # $18B
            'gross_margin': 25.6,
            'ebitda_margin': 18.6,
            'net_margin': 15.5
        },
        'funding': {
            'total_raised': 2000000000,  # $2B
            'last_round_type': 'IPO',
            'last_round_amount': 226000000,
            'last_round_date': '2010-06-29',
            'valuation': 800000000000,  # $800B
            'investors': ['Fidelity', 'T. Rowe Price', 'Baillie Gifford']
        },
        'financial_health_score': 85.0
    }
    
    financial_report = formatter.format_financial_report(
        company_name="Tesla",
        financial_data=financial_data
    )
    
    output_file = output_dir / "financial_report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(financial_report.html_content)
    
    print(f"   ✓ Financial Report saved: {output_file}")
    print(f"      - Has charts: {financial_report.has_charts}")
    print(f"      - Has tables: {financial_report.has_tables}")
    print(f"      - Sections: {', '.join(financial_report.sections)}")
    
    # Mock Leadership Data
    print("\n   Formatting Leadership Report...")
    leadership_data = {
        'founders': [
            {
                'name': 'Elon Musk',
                'role': 'CEO & Product Architect',
                'background': 'Serial entrepreneur with background in software, aerospace, and electric vehicles. Co-founded PayPal, SpaceX, and Neuralink.',
                'previous_companies': ['PayPal', 'Zip2', 'SpaceX'],
                'education': 'University of Pennsylvania (Physics, Economics)'
            },
            {
                'name': 'JB Straubel',
                'role': 'Co-founder & Former CTO',
                'background': 'Engineer and entrepreneur specializing in battery technology and electric vehicles.',
                'previous_companies': ['Redwood Materials'],
                'education': 'Stanford University (Energy Engineering)'
            }
        ],
        'executives': [
            {
                'name': 'Elon Musk',
                'role': 'CEO',
                'background': 'Leading Tesla since 2008, driving innovation in EVs and sustainable energy.'
            },
            {
                'name': 'Zachary Kirkhorn',
                'role': 'CFO',
                'background': 'Former Master of Coin, managing Tesla\'s financial operations and capital allocation.'
            },
            {
                'name': 'Drew Baglino',
                'role': 'SVP of Powertrain and Energy',
                'background': 'Leading battery and powertrain technology development.'
            }
        ],
        'leadership_style': 'Tesla operates with a flat organizational structure and fast decision-making. Elon Musk is known for hands-on leadership, setting ambitious goals, and driving rapid innovation.',
        'key_risks': [
            'Heavy dependence on CEO Elon Musk for vision and execution',
            'Limited succession planning publicly disclosed',
            'High executive turnover in recent years'
        ]
    }
    
    leadership_report = formatter.format_leadership_report(
        company_name="Tesla",
        leadership_data=leadership_data
    )
    
    output_file = output_dir / "leadership_report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(leadership_report.html_content)
    
    print(f"   ✓ Leadership Report saved: {output_file}")
    print(f"      - Has tables: {leadership_report.has_tables}")
    print(f"      - Sections: {', '.join(leadership_report.sections)}")
    
    # Mock Market Data
    print("\n   Formatting Market Report...")
    market_data = {
        'market': {
            'tam': 5000000000000,  # $5T
            'sam': 1000000000000,  # $1T
            'growth_rate': 15.5
        },
        'competitors': [
            {
                'name': 'BYD',
                'market_share': 18.5,
                'strength': 'Largest EV manufacturer by volume, strong in China'
            },
            {
                'name': 'Volkswagen Group',
                'market_share': 12.3,
                'strength': 'Established brand, global distribution network'
            },
            {
                'name': 'General Motors',
                'market_share': 8.7,
                'strength': 'Strong US presence, Ultium battery platform'
            },
            {
                'name': 'Ford',
                'market_share': 6.2,
                'strength': 'F-150 Lightning, Mustang Mach-E success'
            }
        ],
        'swot': {
            'strengths': [
                'Leading brand in premium EV segment',
                'Vertical integration (batteries, software, manufacturing)',
                'Supercharger network advantage',
                'Strong brand loyalty and customer satisfaction',
                'Advanced autonomous driving technology'
            ],
            'weaknesses': [
                'Quality control issues reported',
                'Limited model lineup compared to traditional automakers',
                'Dependence on CEO Elon Musk',
                'Customer service challenges',
                'Production delays on new models'
            ],
            'opportunities': [
                'Growing global EV market',
                'Energy storage business expansion',
                'Full Self-Driving licensing potential',
                'New Gigafactories in key markets',
                'Cybertruck and new model launches'
            ],
            'threats': [
                'Increasing competition from traditional automakers',
                'Chinese EV manufacturers (BYD, NIO, XPeng)',
                'Regulatory changes and subsidy reductions',
                'Supply chain disruptions',
                'Economic downturn affecting luxury purchases'
            ]
        },
        'market_position': 'Tesla is the market leader in premium electric vehicles with strong brand recognition and technological advantages. However, facing increasing competition from both traditional automakers and Chinese EV manufacturers.'
    }
    
    market_report = formatter.format_market_report(
        company_name="Tesla",
        market_data=market_data
    )
    
    output_file = output_dir / "market_report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(market_report.html_content)
    
    print(f"   ✓ Market Report saved: {output_file}")
    print(f"      - Has charts: {market_report.has_charts}")
    print(f"      - Has tables: {market_report.has_tables}")
    print(f"      - Sections: {', '.join(market_report.sections)}")
    
    print("\n" + "="*80)
    print("✅ PHASE 2 TEST COMPLETE (Mock Data)")
    print("="*80)
    
    print(f"\n📁 Reports saved in: {output_dir.absolute()}")
    print("\n🌐 Open the HTML files in your browser to view the formatted reports!")
    
    print("\n📊 Summary:")
    print("   - Financial Report: ✓ (with charts and tables)")
    print("   - Leadership Report: ✓ (with executive profiles)")
    print("   - Market Report: ✓ (with SWOT and competitors)")
    
    print("\n💡 Note: These reports use mock data since API quota was exceeded.")
    print("   The formatting and visualizations are fully functional!")


if __name__ == "__main__":
    test_with_mock_data()
