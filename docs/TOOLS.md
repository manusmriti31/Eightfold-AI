# Tools Guide - Multi-Agent Research System

## 📁 Complete Tools Structure

```
src/tools/
├── __init__.py
├── search/                      # Search tools
│   ├── __init__.py
│   ├── tavily_search.py        # ✅ Primary web search
│   ├── serper_search.py        # ✅ Backup Google search
│   └── news_api.py             # ✅ News articles
├── data/                        # Data APIs
│   ├── __init__.py
│   ├── financial_api.py        # ✅ Alpha Vantage, FMP
│   ├── crunchbase_api.py       # ✅ Funding data
│   ├── linkedin_scraper.py     # ⚠️  Placeholder (ToS issues)
│   └── glassdoor_scraper.py    # ⚠️  Placeholder (ToS issues)
└── analysis/                    # Analysis tools
    ├── __init__.py
    ├── sentiment_analyzer.py   # ✅ Sentiment analysis
    └── fact_checker.py         # ✅ Cross-verification
```

## 🔍 Search Tools

### 1. Tavily Search (Primary)

**File**: `src/tools/search/tavily_search.py`

**Purpose**: Primary web search tool with full content extraction

**Usage**:
```python
from src.tools.search import TavilySearchTool

tool = TavilySearchTool()
results = await tool.search(
    query="OpenAI revenue 2024",
    max_results=5,
    include_raw_content=True
)
```

**Features**:
- Full page content extraction
- News-specific search
- Date filtering
- High-quality results

**API Key**: `TAVILY_API_KEY` (Required)

---

### 2. Serper Search (Backup)

**File**: `src/tools/search/serper_search.py`

**Purpose**: Google search API as backup for Tavily

**Usage**:
```python
from src.tools.search import SerperSearchTool

tool = SerperSearchTool()
results = await tool.search(
    query="Tesla competitors",
    max_results=5
)
```

**Features**:
- Google search results
- News search
- Fast and reliable

**API Key**: `SERPER_API_KEY` (Optional)

---

### 3. NewsAPI

**File**: `src/tools/search/news_api.py`

**Purpose**: Dedicated news article search

**Usage**:
```python
from src.tools.search import NewsAPITool

tool = NewsAPITool()
results = await tool.search(
    query="Microsoft AI",
    max_results=5,
    days=30  # Last 30 days
)
```

**Features**:
- Recent news articles
- Date range filtering
- Source filtering
- Top headlines

**API Key**: `NEWS_API_KEY` (Optional)

---

## 💰 Data Tools

### 4. Financial Data Tool

**File**: `src/tools/data/financial_api.py`

**Purpose**: Financial data from Alpha Vantage and FMP

**Usage**:
```python
from src.tools.data import FinancialDataTool

tool = FinancialDataTool()

# Get company overview
overview = await tool.get_company_overview("TSLA")

# Get income statement
income = await tool.get_income_statement("TSLA")

# Search for ticker
ticker = await tool.search_ticker("Tesla")
```

**Features**:
- Company fundamentals
- Income statements
- Financial ratios
- Ticker search

**API Keys**: 
- `ALPHA_VANTAGE_API_KEY` (Optional)
- `FMP_API_KEY` (Optional)

---

### 5. Crunchbase Tool

**File**: `src/tools/data/crunchbase_api.py`

**Purpose**: Funding rounds, investors, valuations

**Usage**:
```python
from src.tools.data import CrunchbaseTool

tool = CrunchbaseTool()

# Get organization data
org = await tool.get_organization("openai")

# Extract funding info
funding = tool.extract_funding_data(org)
```

**Features**:
- Funding rounds
- Investor lists
- Valuations
- Company profiles

**API Key**: `CRUNCHBASE_API_KEY` (Optional - Paid)

---

### 6. LinkedIn Scraper (Placeholder)

**File**: `src/tools/data/linkedin_scraper.py`

**Status**: ⚠️ Placeholder only

**Why**: LinkedIn has strict anti-scraping policies

**Alternative**: Use `LinkedInSearchHelper` to generate search queries:
```python
from src.tools.data.linkedin_scraper import LinkedInSearchHelper

queries = LinkedInSearchHelper.generate_search_queries(
    person_name="Sam Altman",
    company="OpenAI",
    title="CEO"
)
# Returns: ["Sam Altman OpenAI LinkedIn", ...]
```

**Recommendation**: Use web search to find LinkedIn profiles instead

---

### 7. Glassdoor Scraper (Placeholder)

**File**: `src/tools/data/glassdoor_scraper.py`

**Status**: ⚠️ Placeholder only

**Why**: Glassdoor has anti-scraping measures

**Alternative**: Use `GlassdoorSearchHelper`:
```python
from src.tools.data.glassdoor_scraper import GlassdoorSearchHelper

queries = GlassdoorSearchHelper.generate_search_queries("Tesla")
# Returns: ["Tesla Glassdoor reviews rating", ...]
```

**Recommendation**: Use web search to find Glassdoor data

---

## 🧠 Analysis Tools

### 8. Sentiment Analyzer

**File**: `src/tools/analysis/sentiment_analyzer.py`

**Purpose**: Analyze sentiment of text (news, reviews, etc.)

**Usage**:
```python
from src.tools.analysis import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# Analyze single text
result = analyzer.analyze("Great company with strong growth")
# Returns: {"sentiment": "Positive", "score": 0.5, ...}

# Analyze multiple texts
results = analyzer.analyze_batch([text1, text2, text3])
# Returns: {"overall_sentiment": "Positive", ...}
```

**Features**:
- Positive/Negative/Neutral classification
- Sentiment scoring
- Batch analysis
- Overall sentiment aggregation

**API Key**: None (built-in)

---

### 9. Fact Checker

**File**: `src/tools/analysis/fact_checker.py`

**Purpose**: Cross-check facts across multiple sources

**Usage**:
```python
from src.tools.analysis import FactChecker

checker = FactChecker()

# Check consistency across sources
result = checker.check_consistency([
    {"revenue": 2000000000, "founded": 2015},
    {"revenue": 2100000000, "founded": 2015},
    {"revenue": 1950000000, "founded": 2015}
])

# Returns contradictions and verified facts
```

**Features**:
- Cross-source verification
- Contradiction detection
- Consistency scoring
- Outlier identification

**API Key**: None (built-in)

---

## 🎯 Tool Usage by Agent

| Agent | Primary Tools | Optional Tools |
|-------|--------------|----------------|
| **Profile** | Tavily | Crunchbase |
| **Leadership** | Tavily | LinkedIn Search Helper |
| **Financial** | Tavily | Alpha Vantage, FMP, Crunchbase |
| **Market** | Tavily | Serper |
| **Signals** | Tavily, NewsAPI | Glassdoor Search Helper |

---

## 🔧 Integration with Agents

### Current Setup (Base Agent)

The `BaseResearchAgent` currently uses Tavily directly:

```python
from tavily import AsyncTavilyClient

tavily_client = AsyncTavilyClient()

agent = ProfileAgent(
    name="ProfileAgent",
    llm=llm,
    search_tool=tavily_client,  # Uses Tavily
    max_queries=5
)
```

### Enhanced Setup (Multiple Tools)

You can extend agents to use multiple tools:

```python
from src.tools.search import TavilySearchTool, NewsAPITool
from src.tools.data import FinancialDataTool

# Initialize tools
tavily = TavilySearchTool()
news = NewsAPITool()
financial = FinancialDataTool()

# Pass to agent (requires agent modification)
agent = FinancialAgent(
    name="FinancialAgent",
    llm=llm,
    search_tool=tavily,
    financial_tool=financial,  # Additional tool
    max_queries=5
)
```

---

## 📊 Tool Comparison

### Search Tools

| Tool | Speed | Quality | Cost | Content |
|------|-------|---------|------|---------|
| **Tavily** | Fast | High | $0.005/search | Full page |
| **Serper** | Very Fast | High | $0.005/search | Snippets |
| **NewsAPI** | Fast | Medium | Free tier | Articles |

### Financial Tools

| Tool | Coverage | Accuracy | Cost | Best For |
|------|----------|----------|------|----------|
| **Alpha Vantage** | Public companies | High | Free tier | Stock data |
| **FMP** | Public companies | High | Free tier | Financials |
| **Crunchbase** | Startups | High | $29-99/mo | Funding |

---

## 🚀 Quick Start

### Minimum Setup (Works Now)

```python
from tavily import AsyncTavilyClient

# Only Tavily needed
tavily = AsyncTavilyClient()
```

### Recommended Setup

```python
from src.tools.search import TavilySearchTool, NewsAPITool
from src.tools.data import FinancialDataTool
from src.tools.analysis import SentimentAnalyzer, FactChecker

# Initialize all tools
tavily = TavilySearchTool()
news = NewsAPITool()
financial = FinancialDataTool()
sentiment = SentimentAnalyzer()
fact_checker = FactChecker()
```

### Premium Setup

```python
from src.tools.search import TavilySearchTool, SerperSearchTool, NewsAPITool
from src.tools.data import FinancialDataTool, CrunchbaseTool

# All tools including paid ones
tavily = TavilySearchTool()
serper = SerperSearchTool()
news = NewsAPITool()
financial = FinancialDataTool()
crunchbase = CrunchbaseTool()
```

---

## 🧪 Testing Tools

Create a test script:

```python
import asyncio
from src.tools.search import TavilySearchTool

async def test_tools():
    # Test Tavily
    tavily = TavilySearchTool()
    results = await tavily.search("OpenAI", max_results=2)
    print(f"Found {len(results.get('results', []))} results")

asyncio.run(test_tools())
```

---

## 💡 Best Practices

1. **Fallback Strategy**: Use Serper as backup if Tavily fails
2. **Rate Limiting**: Respect API rate limits
3. **Error Handling**: Always check for errors in responses
4. **Caching**: Cache results to reduce API calls
5. **Cost Optimization**: Use free tiers first, upgrade as needed

---

## 🔐 Security Notes

1. **Never commit API keys** to version control
2. **Use environment variables** for all keys
3. **Respect ToS** of all services
4. **Avoid scraping** LinkedIn and Glassdoor directly
5. **Use official APIs** when available

---

## 📚 Additional Resources

- **Tavily Docs**: https://docs.tavily.com/
- **Serper Docs**: https://serper.dev/docs
- **NewsAPI Docs**: https://newsapi.org/docs
- **Alpha Vantage Docs**: https://www.alphavantage.co/documentation/
- **FMP Docs**: https://site.financialmodelingprep.com/developer/docs/

---

**All tools are now ready to use!** 🎉

The agents can leverage these tools for comprehensive company research.
