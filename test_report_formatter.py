"""Test script for Phase 2: Report Formatting."""

import asyncio
from pathlib import Path
from src.graph.intelligent_graph import research_company_intelligent
from src.agents.intelligence.report_formatter import ReportFormatter


async def test_report_formatting():
    """Test the report formatting system."""
    
    print("\n" + "="*80)
    print("TESTING PHASE 2: REPORT FORMATTING")
    print("="*80)
    
    # Run research first
    print("\n🔍 Step 1: Running intelligent research...")
    result = await research_company_intelligent(
        company="Tesla",
        max_refinement_iterations=1  # Quick test
    )
    
    print("✓ Research complete!")
    
    # Initialize formatter
    formatter = ReportFormatter()
    
    # Create output directory
    output_dir = Path("test_reports")
    output_dir.mkdir(exist_ok=True)
    
    print("\n📝 Step 2: Formatting reports...")
    
    # Helper function to convert dataclass to dict
    def to_dict(obj):
        """Convert dataclass or dict to dict."""
        if obj is None:
            return None
        if isinstance(obj, dict):
            return obj
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return obj
    
    # Debug: Print what we got
    print(f"\n🔍 Debug: Result keys: {list(result.keys())}")
    print(f"   - Has financial_data: {result.get('financial_data') is not None}")
    print(f"   - Has leadership_data: {result.get('leadership_data') is not None}")
    print(f"   - Has market_data: {result.get('market_data') is not None}")
    
    # Format Financial Report
    financial_data = to_dict(result.get('financial_data'))
    if financial_data:
        print("\n   Formatting Financial Report...")
        try:
            financial_report = formatter.format_financial_report(
                company_name=result['report_metadata']['company'],
                financial_data=financial_data,
                profile_data=to_dict(result.get('profile_data'))
            )
            
            # Save to file
            output_file = output_dir / "financial_report.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(financial_report.html_content)
            
            print(f"   ✓ Financial Report saved: {output_file}")
            print(f"      - Has charts: {financial_report.has_charts}")
            print(f"      - Has tables: {financial_report.has_tables}")
            print(f"      - Sections: {', '.join(financial_report.sections)}")
        except Exception as e:
            print(f"   ✗ Error formatting financial report: {e}")
    else:
        print("\n   ⚠️  No financial data available")
    
    # Format Leadership Report
    leadership_data = to_dict(result.get('leadership_data'))
    if leadership_data:
        print("\n   Formatting Leadership Report...")
        try:
            leadership_report = formatter.format_leadership_report(
                company_name=result['report_metadata']['company'],
                leadership_data=leadership_data
            )
            
            # Save to file
            output_file = output_dir / "leadership_report.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(leadership_report.html_content)
            
            print(f"   ✓ Leadership Report saved: {output_file}")
            print(f"      - Has tables: {leadership_report.has_tables}")
            print(f"      - Sections: {', '.join(leadership_report.sections)}")
        except Exception as e:
            print(f"   ✗ Error formatting leadership report: {e}")
    else:
        print("\n   ⚠️  No leadership data available")
    
    # Format Market Report
    market_data = to_dict(result.get('market_data'))
    if market_data:
        print("\n   Formatting Market Report...")
        try:
            market_report = formatter.format_market_report(
                company_name=result['report_metadata']['company'],
                market_data=market_data
            )
            
            # Save to file
            output_file = output_dir / "market_report.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(market_report.html_content)
            
            print(f"   ✓ Market Report saved: {output_file}")
            print(f"      - Has charts: {market_report.has_charts}")
            print(f"      - Has tables: {market_report.has_tables}")
            print(f"      - Sections: {', '.join(market_report.sections)}")
        except Exception as e:
            print(f"   ✗ Error formatting market report: {e}")
    else:
        print("\n   ⚠️  No market data available")
    
    print("\n" + "="*80)
    print("✅ PHASE 2 TEST COMPLETE")
    print("="*80)
    
    print(f"\n📁 Reports saved in: {output_dir.absolute()}")
    print("\n🌐 Open the HTML files in your browser to view the formatted reports!")
    
    print("\n📊 Summary:")
    print(f"   - Financial Report: {'✓' if financial_data else '✗'}")
    print(f"   - Leadership Report: {'✓' if leadership_data else '✗'}")
    print(f"   - Market Report: {'✓' if market_data else '✗'}")
    
    return result


if __name__ == "__main__":
    asyncio.run(test_report_formatting())
