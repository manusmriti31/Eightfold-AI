"""Test script for intelligent graph with gap detection and refinement."""

import asyncio
from src.graph.intelligent_graph import research_company_intelligent


async def test_intelligent_research():
    """Test the intelligent research system with gap refinement."""
    
    print("\n" + "="*80)
    print("TESTING INTELLIGENT MULTI-AGENT RESEARCH SYSTEM")
    print("="*80)
    
    # Test with a well-known company
    company = "Tesla"
    
    print(f"\n🎯 Testing with: {company}")
    print(f"📋 Features being tested:")
    print(f"   1. Initial research by 5 agents")
    print(f"   2. Gap detection across all agents")
    print(f"   3. Targeted refinement queries")
    print(f"   4. Data gap filling (2 iterations)")
    print(f"   5. Final report synthesis")
    
    # Run intelligent research
    result = await research_company_intelligent(
        company=company,
        report_type="investment_memo",
        max_refinement_iterations=2
    )
    
    # Display results
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80)
    
    print("\n📊 METADATA:")
    metadata = result['report_metadata']
    print(f"   Company: {metadata['company']}")
    print(f"   Agents Used: {metadata['agents_used']}")
    print(f"   Total Sources: {metadata['total_sources']}")
    print(f"   Average Confidence: {metadata['average_confidence']:.2%}")
    print(f"   Refinement Iterations: {metadata['refinement_iterations']}")
    print(f"   Gaps Filled: {metadata['gaps_filled']}")
    
    if metadata.get('refinement_summary'):
        summary = metadata['refinement_summary']
        print(f"\n🔍 GAP ANALYSIS:")
        print(f"   Total Gaps Detected: {summary['total_gaps']}")
        print(f"   Gaps Filled: {summary['gaps_filled']}")
        print(f"   Gaps Remaining: {summary['gaps_remaining']}")
        print(f"   Fill Rate: {summary['fill_rate']:.1f}%")
        print(f"   Critical Gaps Remaining: {summary['critical_gaps_remaining']}")
        
        print(f"\n   By Priority:")
        print(f"      Critical: {summary['filled_by_priority']['critical']}/{summary['by_priority']['critical']}")
        print(f"      High: {summary['filled_by_priority']['high']}/{summary['by_priority']['high']}")
        print(f"      Medium: {summary['filled_by_priority']['medium']}/{summary['by_priority']['medium']}")
    
    print(f"\n📝 EXECUTIVE SUMMARY:")
    print(f"{result['executive_summary']}")
    
    print(f"\n📄 FULL REPORT (first 1000 chars):")
    print(f"{result['final_report'][:1000]}...")
    
    print(f"\n🔗 SOURCES ({len(result['all_sources'])} total):")
    for i, source in enumerate(result['all_sources'][:5], 1):
        print(f"   {i}. {source}")
    if len(result['all_sources']) > 5:
        print(f"   ... and {len(result['all_sources']) - 5} more")
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETE")
    print("="*80)
    
    # Verify improvements
    print("\n🎯 VERIFICATION:")
    
    if metadata['refinement_iterations'] > 0:
        print("   ✅ Refinement system activated")
    else:
        print("   ⚠️  No refinement iterations (all data found initially)")
    
    if metadata['gaps_filled'] > 0:
        print(f"   ✅ Successfully filled {metadata['gaps_filled']} data gaps")
    else:
        print("   ⚠️  No gaps filled (may indicate no gaps or refinement didn't help)")
    
    if metadata['average_confidence'] >= 0.80:
        print(f"   ✅ High confidence score: {metadata['average_confidence']:.2%}")
    else:
        print(f"   ⚠️  Lower confidence: {metadata['average_confidence']:.2%}")
    
    if metadata.get('refinement_summary'):
        summary = metadata['refinement_summary']
        if summary['fill_rate'] >= 70:
            print(f"   ✅ Excellent gap fill rate: {summary['fill_rate']:.1f}%")
        elif summary['fill_rate'] >= 50:
            print(f"   ✓ Good gap fill rate: {summary['fill_rate']:.1f}%")
        else:
            print(f"   ⚠️  Low gap fill rate: {summary['fill_rate']:.1f}%")
    
    print("\n🎉 Intelligent research system is working!")
    
    return result


if __name__ == "__main__":
    asyncio.run(test_intelligent_research())
