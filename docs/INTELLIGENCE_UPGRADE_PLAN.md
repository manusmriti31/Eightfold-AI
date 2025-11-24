# Intelligence Upgrade Plan - Multi-Agent Research System

## Executive Summary

This document outlines the plan to upgrade the multi-agent research system from a basic search-and-report tool to an intelligent, self-refining research platform with rich, specialized report formats.

**Current Issues:**
1. Reports contain "no data available" for missing information
2. All reports look generic (plain text/markdown)
3. No follow-up research when data is incomplete
4. No visual elements (tables, charts, images)

**Solution:**
Add 3 intelligence layers that make agents more persistent, intelligent, and produce professional-looking reports.

---

## Architecture Overview

### Current Flow
```
START → [5 Agents Parallel] → Aggregate → Synthesize → END
```

### New Flow
```
START 
  ↓
[5 Agents in Parallel]
  ↓
Aggregate Data
  ↓
Gap Detection ←─────┐
  ↓                 │
Targeted Re-search ─┘ (2-3 iterations)
  ↓
Format Reports (type-specific)
  ↓
Verification (optional)
  ↓
END
```

---

## Priority 1: Gap Detection & Refinement (PHASE 1)

**Timeline:** 2-3 hours  
**Impact:** HIGH - Eliminates "no data available" issues  
**Status:** 🚧 IN PROGRESS

### What It Does

1. **Analyzes extracted data** for missing/incomplete fields
2. **Generates targeted queries** specifically for gaps
3. **Re-runs searches** with different strategies
4. **Fills gaps** with newly found data
5. **Tracks attempts** to distinguish "not found" from "not available"

### Implementation Steps

#### Step 1.1: Create Gap Detector Agent
**File:** `src/agents/intelligence/gap_detector.py`

**Responsibilities:**
- Analyze structured data for null/empty fields
- Identify critical vs. optional gaps
- Generate hyper-specific refinement queries
- Track refinement attempts and success rate

**Key Methods:**
```python
- analyze_gaps(data: BaseModel) -> List[Gap]
- prioritize_gaps(gaps: List[Gap]) -> List[Gap]
- generate_refinement_queries(gap: Gap, company: str) -> List[str]
- should_continue_refining(iteration: int, gaps_filled: int) -> bool
```

#### Step 1.2: Add Refinement Logic to Base Agent
**File:** `src/agents/base_agent.py`

**New Methods:**
```python
- refine_research(company: str, gaps: List[Gap]) -> Dict[str, Any]
- execute_searches_with_fallback(queries: List[str]) -> Dict[str, Any]
- merge_data(original: BaseModel, new_data: Dict) -> BaseModel
```

#### Step 1.3: Update Graph with Refinement Loop
**File:** `src/graph/multi_agent_graph.py` or new `src/graph/intelligent_graph.py`

**Changes:**
- Add `gap_detection` node
- Add `refinement` node
- Add conditional edge for iteration control
- Update state to track refinement metadata

#### Step 1.4: Update State Management
**File:** `src/graph/state.py`

**New Fields:**
```python
@dataclass
class MultiAgentState:
    # ... existing fields ...
    
    # Refinement tracking
    gaps_detected: List[Gap] = field(default_factory=list)
    refinement_iteration: int = 0
    max_refinement_iterations: int = 2
    gaps_filled: int = 0
    gaps_remaining: int = 0
```

### Success Metrics

- **Before:** 30-40% of fields have "no data available"
- **After:** <10% of fields remain empty after refinement
- **Target:** 2-3 refinement iterations per agent
- **Quality:** Higher confidence scores (85%+ average)

### Example Scenario

**Initial Search:**
```
Financial Agent → Tesla
Result: Revenue = None, Profitability = None
```

**Gap Detection:**
```
Gaps Found:
1. Revenue data missing (CRITICAL)
2. Profitability metrics missing (CRITICAL)
3. Funding history incomplete (MEDIUM)
```

**Refinement Queries:**
```
Iteration 1:
- "Tesla 10-K SEC filing 2024 annual revenue"
- "Tesla Q4 2024 earnings report financial results"
- "Tesla investor presentation 2024 revenue breakdown"

Iteration 2 (if still missing):
- "Tesla total revenue 2024 automotive energy"
- "Tesla GAAP revenue fiscal year 2024"
- "Tesla annual report 2024 consolidated statements"
```

**Final Result:**
```
Revenue: $96.8B (2024, from 10-K filing)
Profitability: EBITDA $12.3B, 12.7% margin
Confidence: 0.92 (up from 0.45)
```

---

## Priority 2: Report Formatting & Visualization (PHASE 2)

**Timeline:** 3-4 hours  
**Impact:** HIGH - Professional, specialized reports  
**Status:** 📋 PLANNED

### What It Does

1. **Transforms structured data** into rich HTML reports
2. **Generates visualizations** (charts, tables, graphs)
3. **Fetches images** (leader photos, logos, products)
4. **Applies report-specific formatting** based on agent type
5. **Exports to multiple formats** (HTML, PDF, JSON)

### Implementation Steps

#### Step 2.1: Create Report Formatter Agent
**File:** `src/agents/intelligence/report_formatter.py`

**Responsibilities:**
- Format reports by type (financial, leadership, market)
- Generate HTML with embedded charts
- Create tables and visual elements
- Handle image embedding

#### Step 2.2: Build Visualization Tools
**Files:**
- `src/tools/visualization/chart_generator.py`
- `src/tools/visualization/table_builder.py`

**Charts Needed:**
- Revenue growth line chart
- Profitability metrics dashboard
- Market share pie chart
- Competitive positioning matrix
- Funding timeline

#### Step 2.3: Create HTML Templates
**Files:**
- `src/templates/financial_report.html`
- `src/templates/leadership_report.html`
- `src/templates/market_report.html`
- `src/templates/signals_report.html`

**Template Engine:** Jinja2

#### Step 2.4: Add Image Fetching
**Files:**
- `src/tools/media/image_fetcher.py`
- `src/tools/media/logo_fetcher.py`

**Image Sources:**
- LinkedIn profile photos
- Company press kits
- Google Images (with face detection)
- Fallback to avatar generation

### Report-Specific Formats

#### Financial Report Components
- **Revenue Table:** Year-over-year comparison
- **Profitability Dashboard:** Margins, net income, EBITDA
- **Funding Timeline:** Visual timeline of rounds
- **Financial Ratios:** Comparison with industry benchmarks
- **Health Score:** 0-100 with color coding

#### Leadership Report Components
- **Executive Cards:** Photo, name, role, background
- **Quote Boxes:** Recent public statements
- **Career Timeline:** Visual journey
- **LinkedIn Integration:** Live profile links
- **Org Chart:** Visual hierarchy

#### Market Report Components
- **Competitive Matrix:** 2x2 positioning
- **Market Share Chart:** Pie/bar chart
- **SWOT Grid:** Color-coded quadrants
- **Competitor Table:** Side-by-side comparison
- **Market Size Funnel:** TAM/SAM/SOM visualization

### Dependencies

**Python Packages:**
```bash
pip install plotly matplotlib jinja2 pillow beautifulsoup4
```

### Success Metrics

- **Before:** Plain text markdown reports
- **After:** Rich HTML with 5+ visual elements per report
- **Target:** <2 seconds to generate formatted report
- **Quality:** Professional, presentation-ready output

---

## Priority 3: Polish & Enhancement (PHASE 3)

**Timeline:** 2-3 hours  
**Impact:** MEDIUM - Quality improvements  
**Status:** 📋 PLANNED

### Features

#### 3.1: Verification Agent
**File:** `src/agents/intelligence/verifier.py`

**Purpose:**
- Cross-check facts across sources
- Flag contradictions between agents
- Adjust confidence scores
- Identify outdated information

#### 3.2: Enhanced Image Fetching
**Improvements:**
- Better LinkedIn scraping
- Face detection for leader photos
- Image quality validation
- Caching for performance

#### 3.3: Interactive Charts
**Enhancements:**
- Plotly interactive charts
- Zoom, pan, hover tooltips
- Export chart as PNG/SVG
- Responsive design

#### 3.4: Export Options
**Formats:**
- HTML (rich, interactive)
- PDF (print-ready)
- JSON (API integration)
- Markdown (legacy support)

---

## Technical Architecture

### New Directory Structure

```
src/
├── agents/
│   ├── research/              # Existing research agents
│   │   ├── profile_agent.py
│   │   ├── leadership_agent.py
│   │   ├── financial_agent.py
│   │   ├── market_agent.py
│   │   └── signals_agent.py
│   └── intelligence/          # NEW: Intelligence layer
│       ├── __init__.py
│       ├── gap_detector.py    # Phase 1
│       ├── report_formatter.py # Phase 2
│       └── verifier.py        # Phase 3
├── tools/
│   ├── search/                # Existing search tools
│   ├── data/                  # Existing data tools
│   ├── analysis/              # Existing analysis tools
│   ├── visualization/         # NEW: Charts and tables
│   │   ├── __init__.py
│   │   ├── chart_generator.py
│   │   └── table_builder.py
│   └── media/                 # NEW: Image handling
│       ├── __init__.py
│       ├── image_fetcher.py
│       └── logo_fetcher.py
├── templates/                 # NEW: HTML templates
│   ├── base.html
│   ├── financial_report.html
│   ├── leadership_report.html
│   ├── market_report.html
│   └── signals_report.html
└── graph/
    ├── multi_agent_graph.py   # Existing
    ├── selective_graph.py     # Existing
    └── intelligent_graph.py   # NEW: With refinement loop
```

### State Management Updates

**New State Fields:**
```python
@dataclass
class Gap:
    """Represents a missing data field."""
    field_name: str
    agent_name: str
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    attempted_queries: List[str] = field(default_factory=list)
    filled: bool = False

@dataclass
class RefinementMetadata:
    """Tracks refinement process."""
    iteration: int
    gaps_detected: int
    gaps_filled: int
    queries_generated: int
    sources_found: int
    confidence_improvement: float

@dataclass
class MultiAgentState:
    # ... existing fields ...
    
    # Refinement tracking
    gaps: List[Gap] = field(default_factory=list)
    refinement_metadata: List[RefinementMetadata] = field(default_factory=list)
    refinement_iteration: int = 0
    max_refinement_iterations: int = 2
    
    # Formatting
    report_format: str = "html"  # html, pdf, json, markdown
    include_visualizations: bool = True
    include_images: bool = True
```

---

## Implementation Timeline

### Week 1: Phase 1 - Gap Detection
- **Day 1-2:** Build Gap Detector Agent
- **Day 2-3:** Add refinement logic to base agent
- **Day 3-4:** Update graph with refinement loop
- **Day 4-5:** Testing and optimization

### Week 2: Phase 2 - Report Formatting
- **Day 1-2:** Build Report Formatter Agent
- **Day 2-3:** Create visualization tools
- **Day 3-4:** Design HTML templates
- **Day 4-5:** Add image fetching

### Week 3: Phase 3 - Polish
- **Day 1-2:** Build Verification Agent
- **Day 2-3:** Enhance image fetching
- **Day 3-4:** Add interactive charts
- **Day 4-5:** Export options and testing

---

## Success Criteria

### Phase 1 Success
- ✅ <10% of fields remain empty after refinement
- ✅ Average confidence score >85%
- ✅ 2-3 refinement iterations per agent
- ✅ Clear tracking of "not found" vs "not available"

### Phase 2 Success
- ✅ All reports have rich HTML format
- ✅ 5+ visual elements per report
- ✅ Leader photos in 80%+ of leadership reports
- ✅ Financial charts in 100% of financial reports

### Phase 3 Success
- ✅ Fact verification on critical data points
- ✅ Interactive charts with hover tooltips
- ✅ Export to PDF working
- ✅ <3 seconds total report generation time

---

## Risk Mitigation

### Risk 1: Refinement Takes Too Long
**Mitigation:**
- Limit to 2-3 iterations max
- Parallel refinement for multiple gaps
- Cache successful query patterns

### Risk 2: Image Fetching Fails
**Mitigation:**
- Multiple fallback sources
- Generate avatar if no image found
- Cache images for reuse

### Risk 3: Charts Slow Down Reports
**Mitigation:**
- Generate charts asynchronously
- Use lightweight chart libraries
- Lazy load images in HTML

### Risk 4: API Rate Limits
**Mitigation:**
- Respect existing rate limiters
- Batch refinement queries
- Cache results aggressively

---

## Testing Strategy

### Unit Tests
- Gap detection logic
- Query generation for gaps
- Data merging functions
- Chart generation

### Integration Tests
- Full refinement loop
- Multi-iteration scenarios
- Report formatting pipeline
- Image fetching with fallbacks

### End-to-End Tests
- Research Tesla with refinement
- Generate all report types
- Export to all formats
- Performance benchmarks

---

## Monitoring & Metrics

### Key Metrics to Track
1. **Gap Fill Rate:** % of gaps filled after refinement
2. **Confidence Improvement:** Average confidence before/after
3. **Refinement Efficiency:** Gaps filled per iteration
4. **Report Generation Time:** Total time including formatting
5. **Image Success Rate:** % of images successfully fetched
6. **User Satisfaction:** Feedback on report quality

### Logging
```python
logger.info(f"Gap Detection: Found {len(gaps)} gaps")
logger.info(f"Refinement Iteration {i}: Filled {filled}/{total} gaps")
logger.info(f"Confidence improved: {old_conf:.2f} → {new_conf:.2f}")
logger.info(f"Report formatted in {duration:.2f}s")
```

---

## Next Steps

1. ✅ Create this implementation plan document
2. 🚧 **START HERE:** Implement Phase 1 - Gap Detection
3. 📋 Implement Phase 2 - Report Formatting
4. 📋 Implement Phase 3 - Polish & Enhancement
5. 📋 Update documentation
6. 📋 Create demo video

---

## Questions & Decisions

### Open Questions
- Should we use Plotly or Matplotlib for charts? (Recommend: Plotly for interactivity)
- How many refinement iterations is optimal? (Recommend: 2-3 max)
- Should we cache images locally? (Recommend: Yes, with expiry)
- PDF generation library? (Recommend: WeasyPrint or Playwright)

### Decisions Made
- ✅ Use Jinja2 for HTML templates
- ✅ Limit refinement to 2-3 iterations
- ✅ Prioritize critical gaps over optional ones
- ✅ Generate avatars as fallback for missing photos

---

## Resources & References

### Documentation
- LangGraph: https://langchain-ai.github.io/langgraph/
- Plotly: https://plotly.com/python/
- Jinja2: https://jinja.palletsprojects.com/

### Similar Systems
- Perplexity AI (search refinement)
- Notion AI (rich formatting)
- Crunchbase (structured company data)

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-24  
**Status:** Phase 1 In Progress  
**Owner:** Development Team
