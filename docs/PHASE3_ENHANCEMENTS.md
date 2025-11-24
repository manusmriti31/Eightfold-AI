# Phase 3: Advanced Enhancements - Implementation Plan

## Overview

Phase 3 adds advanced features to make reports more comprehensive and detailed:
1. PDF document downloading (financial reports, investor presentations)
2. Stock market performance tracking
3. Enhanced targeted search strategies
4. Optimized multi-model usage

---

## 1. PDF Document Downloading

### Goal
Download and extract text from professional PDFs available on the web (10-K filings, investor presentations, annual reports).

### Implementation

**New Tool:** `src/tools/data/pdf_downloader.py`

**Capabilities:**
- Search for company PDFs (10-K, 10-Q, investor presentations)
- Download PDFs from SEC EDGAR, company investor relations pages
- Extract text from PDFs using PyPDF2 or pdfplumber
- Cache downloaded PDFs to avoid re-downloading

**APIs/Sources:**
- SEC EDGAR API (free, official financial filings)
- Company investor relations pages
- Direct PDF URLs from search results

**Example Usage:**
```python
pdf_tool = PDFDownloader()

# Download 10-K filing
filing = await pdf_tool.download_sec_filing(
    company="Tesla",
    filing_type="10-K",
    year=2024
)

# Extract financial data from PDF
text = pdf_tool.extract_text(filing.pdf_path)
```

---

## 2. Stock Market Performance

### Goal
Add real-time stock data and financial news for publicly traded companies.

### Implementation

**New Tool:** `src/tools/data/stock_market.py`

**Data Sources:**
- **Yahoo Finance API** (free, real-time quotes)
- **Alpha Vantage** (already configured, stock data)
- **Financial Modeling Prep** (already configured, financial statements)
- **News API** (already configured, financial news)

**Features:**
- Current stock price and change
- 52-week high/low
- Market cap, P/E ratio, dividend yield
- Recent price chart (6 months)
- Latest financial news headlines
- Analyst ratings and price targets

**Example Output:**
```
Stock Performance (TSLA):
- Current Price: $242.50 (+2.3%)
- 52-Week Range: $138.80 - $299.29
- Market Cap: $770B
- P/E Ratio: 65.4
- Recent News: "Tesla reports Q4 earnings beat..."
```

---

## 3. Enhanced Targeted Search

### Goal
Generate more specific, targeted queries to get deeper, more detailed information.

### Current Issue
- Queries are too broad: "Tesla revenue 2024"
- Results are generic and surface-level

### Solution: Multi-Level Search Strategy

**Level 1: Broad Discovery (Current)**
- General queries to understand the company
- 5 queries per agent

**Level 2: Deep Dive (NEW)**
- Specific queries based on Level 1 findings
- Target specific documents (10-K, investor decks)
- 10 additional targeted queries per agent

**Level 3: Gap Filling (Existing - Phase 1)**
- Refinement queries for missing data
- 5 queries per gap

**Example Progression:**

**Level 1 (Broad):**
```
"Tesla financial performance 2024"
```

**Level 2 (Targeted):**
```
"Tesla 10-K SEC filing 2024 revenue breakdown by segment"
"Tesla Q4 2024 earnings call transcript gross margin discussion"
"Tesla investor presentation 2024 automotive vs energy revenue"
"Tesla Form 8-K material events 2024"
```

**Level 3 (Gap Filling):**
```
"Tesla GAAP revenue fiscal year 2024 consolidated statements"
```

### Implementation

**Update:** `src/agents/base_agent.py`

Add new parameter: `search_depth` (shallow, medium, deep)

```python
class BaseResearchAgent:
    def __init__(
        self,
        max_queries: int = 5,
        max_results_per_query: int = 3,
        search_depth: str = "medium"  # NEW
    ):
        self.search_depth = search_depth
        
    async def research_deep(self, company: str):
        # Level 1: Broad discovery
        broad_results = await self.research(company)
        
        # Level 2: Targeted deep dive
        if self.search_depth in ["medium", "deep"]:
            targeted_queries = self.generate_targeted_queries(
                company, 
                broad_results
            )
            deep_results = await self.execute_searches(targeted_queries)
            
        # Merge results
        return self.merge_results(broad_results, deep_results)
```

---

## 4. Multi-Model Optimization

### Goal
Use different Gemini models strategically to maximize quality while respecting rate limits.

### Model Strategy (Based on Your Rate Limits)

#### Available Models & Limits:

**Fast Models (High RPM):**
- `gemini-2.0-flash`: 9 RPM, 27.45K TPM (currently using)
- `gemini-2.0-flash-lite`: 30 RPM, 1M TPM
- `gemma-3-12b`: 30 RPM, 15K TPM

**Quality Models (Low RPM):**
- `gemini-2.5-flash`: 10 RPM, 250K TPM
- `gemini-2.5-pro`: 2 RPM, 125K TPM (highest quality)

**Live Models (Unlimited RPM):**
- `gemini-2.0-flash-live`: Unlimited RPM, 1M TPM
- `gemini-2.5-flash-live`: Unlimited RPM, 1M TPM

### Recommended Model Assignment

**Task Distribution:**

1. **Query Generation** (Many calls, simple task)
   - Model: `gemini-2.0-flash-lite` (30 RPM)
   - Why: Fast, high rate limit, simple task
   - Usage: ~50 calls per research

2. **Data Extraction** (Many calls, medium complexity)
   - Model: `gemini-2.0-flash-live` (Unlimited RPM)
   - Why: Unlimited calls, good quality
   - Usage: ~25 calls per research

3. **Gap Detection** (Few calls, medium complexity)
   - Model: `gemini-2.5-flash` (10 RPM)
   - Why: Better reasoning for gap analysis
   - Usage: ~5 calls per research

4. **Final Report Synthesis** (Few calls, high complexity)
   - Model: `gemini-2.5-pro` (2 RPM)
   - Why: Highest quality for final output
   - Usage: ~2 calls per research

5. **Report Formatting** (Few calls, simple task)
   - Model: `gemini-2.0-flash` (9 RPM)
   - Why: Current model, adequate for formatting
   - Usage: ~3 calls per research

### Implementation

**Update:** `src/llm/llm_config.py`

```python
def get_multi_model_config():
    """Get optimized multi-model configuration."""
    
    return {
        # Fast model for query generation
        "query_llm": ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-lite",
            temperature=0.3,
            rate_limiter=InMemoryRateLimiter(
                requests_per_second=0.5,  # 30 RPM
            )
        ),
        
        # Live model for data extraction (unlimited)
        "extraction_llm": ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-live",
            temperature=0.2,
            # No rate limiter needed - unlimited
        ),
        
        # Quality model for gap detection
        "gap_detection_llm": ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            rate_limiter=InMemoryRateLimiter(
                requests_per_second=0.15,  # 10 RPM
            )
        ),
        
        # Premium model for final synthesis
        "synthesis_llm": ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.4,
            rate_limiter=InMemoryRateLimiter(
                requests_per_second=0.03,  # 2 RPM
            )
        ),
        
        # Standard model for formatting
        "format_llm": ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3,
            rate_limiter=InMemoryRateLimiter(
                requests_per_second=0.15,  # 9 RPM
            )
        )
    }
```

### Expected Improvements

**Before (Single Model):**
- All tasks use `gemini-2.0-flash`
- Hit rate limits quickly (9 RPM)
- Medium quality output
- ~200 API calls per research
- Frequent quota errors

**After (Multi-Model):**
- Query generation: 30 RPM (3.3x faster)
- Data extraction: Unlimited (no limits!)
- Gap detection: Better quality
- Final synthesis: Highest quality
- ~200 API calls distributed across models
- Rare quota errors

### Rate Limit Math

**Single Model (Current):**
```
200 calls / 9 RPM = 22 minutes (with waits)
```

**Multi-Model (Optimized):**
```
Query (50 calls): 50 / 30 RPM = 1.7 minutes
Extraction (25 calls): 25 / unlimited = instant
Gap Detection (5 calls): 5 / 10 RPM = 0.5 minutes
Synthesis (2 calls): 2 / 2 RPM = 1 minute
Formatting (3 calls): 3 / 9 RPM = 0.3 minutes

Total: ~3.5 minutes (6x faster!)
```

---

## 5. Financial News Integration

### Goal
Add latest financial news and market sentiment for the company.

### Implementation

**Enhance:** `src/agents/research/signals_agent.py`

**New Section:** Stock Market Performance & News

**Data Sources:**
- News API (already configured)
- Yahoo Finance news
- Financial news from Tavily search

**Features:**
- Latest 10 news headlines
- News sentiment analysis (positive/negative/neutral)
- Stock price reaction to news
- Analyst upgrades/downgrades

---

## Implementation Priority

### Phase 3A: Core Enhancements (Week 1)
1. ✅ Multi-model optimization (highest impact)
2. ✅ Enhanced targeted search (deeper data)
3. ✅ Stock market performance tool

### Phase 3B: Advanced Features (Week 2)
4. ✅ PDF downloader for financial documents
5. ✅ Financial news integration
6. ✅ Report quality improvements

---

## Expected Results

### Report Quality
**Before:**
- 5-10 pages
- Surface-level information
- Generic insights
- Missing data: 30-40%

**After:**
- 15-25 pages
- Deep, detailed analysis
- Specific insights from SEC filings
- Missing data: <5%
- Real-time stock data
- Latest financial news

### Performance
**Before:**
- 5-10 minutes per research
- Frequent rate limit errors
- Medium quality output

**After:**
- 3-5 minutes per research
- Rare rate limit errors
- High quality output
- 6x faster with multi-model

---

## Technical Requirements

### New Dependencies
```bash
pip install yfinance          # Yahoo Finance data
pip install PyPDF2            # PDF text extraction
pip install pdfplumber        # Advanced PDF parsing
pip install sec-edgar-downloader  # SEC filings
```

### API Keys (Already Have)
- ✅ Google Gemini API
- ✅ Tavily Search
- ✅ Alpha Vantage
- ✅ Financial Modeling Prep
- ✅ News API

---

## Next Steps

1. **Implement multi-model configuration** (30 min)
2. **Add stock market tool** (1 hour)
3. **Enhance search depth** (1 hour)
4. **Add PDF downloader** (2 hours)
5. **Integrate financial news** (1 hour)
6. **Test and optimize** (1 hour)

**Total Time:** ~6-7 hours

---

## Success Metrics

### Quality Metrics
- Report length: 15-25 pages (vs 5-10)
- Data completeness: >95% (vs 60-70%)
- Source diversity: SEC filings, PDFs, news
- Real-time data: Stock prices, latest news

### Performance Metrics
- Research time: 3-5 min (vs 5-10 min)
- Rate limit errors: <5% (vs 30%)
- API calls distributed: 5 models (vs 1)
- Quality score: 9/10 (vs 6/10)

---

**Phase 3 Status:** 📋 PLANNED  
**Ready to implement:** Yes  
**Expected completion:** 1-2 days
