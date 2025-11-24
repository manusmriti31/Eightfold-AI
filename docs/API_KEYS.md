# API Keys Required for Multi-Agent Research System

## ✅ Currently Configured

You already have these keys set up in your `.env` file:

1. **Google Gemini API** ✅
   - Variable: `GOOGLE_API_KEY`
   - Status: Configured
   - Used by: All agents (LLM reasoning)

2. **Tavily Search API** ✅
   - Variable: `TAVILY_API_KEY`
   - Status: Configured
   - Used by: All agents (web search)

## 🔧 Required for Full Functionality

### Core Search & Data (Required)

These are **essential** for the agents to work:

#### 1. Tavily API (Already have ✅)
- **Purpose**: Primary web search for all agents
- **Cost**: Free tier: 1,000 searches/month, Paid: $0.005/search
- **Sign up**: https://tavily.com/
- **Variable**: `TAVILY_API_KEY`

#### 2. Google Gemini API (Already have ✅)
- **Purpose**: LLM for reasoning, query generation, extraction
- **Cost**: Gemini 2.0 Flash is free (2M tokens/day), Pro is paid
- **Sign up**: https://ai.google.dev/
- **Variable**: `GOOGLE_API_KEY`

## 📊 Optional but Highly Recommended

These will significantly improve data quality for specific agents:

### Financial Agent Enhancement

#### 3. Alpha Vantage API (Free)
- **Purpose**: Stock prices, financial ratios, company fundamentals
- **Cost**: Free tier: 25 requests/day, Premium: $50/month
- **Sign up**: https://www.alphavantage.co/support/#api-key
- **Variable**: `ALPHA_VANTAGE_API_KEY`
- **Agents**: Financial Agent
- **Data**: Revenue, market cap, P/E ratio, financial statements

#### 4. Financial Modeling Prep API (Free tier available)
- **Purpose**: Financial statements, ratios, company profiles
- **Cost**: Free tier: 250 requests/day, Paid: $15-$200/month
- **Sign up**: https://site.financialmodelingprep.com/developer/docs/
- **Variable**: `FMP_API_KEY`
- **Agents**: Financial Agent
- **Data**: Income statements, balance sheets, cash flow

### News & Signals Agent Enhancement

#### 5. NewsAPI (Free tier available)
- **Purpose**: Recent news articles and headlines
- **Cost**: Free tier: 100 requests/day, Paid: $449/month
- **Sign up**: https://newsapi.org/register
- **Variable**: `NEWS_API_KEY`
- **Agents**: Signals Agent
- **Data**: Recent news, sentiment, press releases

#### 6. Serper API (Alternative search)
- **Purpose**: Google search results (backup for Tavily)
- **Cost**: Free tier: 2,500 searches, Paid: $50/month for 10k
- **Sign up**: https://serper.dev/
- **Variable**: `SERPER_API_KEY`
- **Agents**: All agents (fallback search)

### Market & Competitive Intelligence

#### 7. Crunchbase API (Paid)
- **Purpose**: Funding data, investors, company profiles
- **Cost**: $29-$99/month (no free tier)
- **Sign up**: https://data.crunchbase.com/docs
- **Variable**: `CRUNCHBASE_API_KEY`
- **Agents**: Financial Agent, Profile Agent
- **Data**: Funding rounds, investors, valuations

## 🌐 Web Scraping (No API Key Needed)

These don't require API keys but may need setup:

#### 8. LinkedIn Scraping
- **Purpose**: Executive profiles, company pages, job postings
- **Method**: Web scraping (use with caution - rate limits)
- **Agents**: Leadership Agent, Signals Agent
- **Note**: Consider using Bright Data or ScraperAPI for reliable access

#### 9. Glassdoor Scraping
- **Purpose**: Employee reviews, ratings, sentiment
- **Method**: Web scraping or third-party services
- **Agents**: Signals Agent
- **Note**: Glassdoor has anti-scraping measures

## 📝 Updated .env File Template

Here's what your complete `.env` file should look like:

```bash
# ===== CORE (Required) =====
GOOGLE_API_KEY=AIzaSyCNgGdiOBMBETzv9tf-C_04Lu5Ipx_zBqk
TAVILY_API_KEY=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

# ===== FINANCIAL DATA (Optional but recommended) =====
ALPHA_VANTAGE_API_KEY=your_key_here
FMP_API_KEY=your_key_here

# ===== NEWS & SIGNALS (Optional) =====
NEWS_API_KEY=your_key_here
SERPER_API_KEY=your_key_here

# ===== COMPANY DATA (Optional - Paid) =====
CRUNCHBASE_API_KEY=your_key_here

# ===== LANGSMITH (For monitoring) =====
LANGSMITH_API_KEY=your_key_here
LANGSMITH_PROJECT=company-researcher
```

## 🚀 Quick Start - Minimum Viable Setup

**You can start RIGHT NOW with just what you have:**

✅ Google Gemini API (for LLM)
✅ Tavily API (for web search)

This is enough to run all 5 agents! They will:
- Generate intelligent search queries
- Search the web via Tavily
- Extract structured data from results

**The optional APIs just add:**
- More accurate financial data (Alpha Vantage, FMP)
- More news sources (NewsAPI)
- Funding data (Crunchbase)

## 💰 Cost Estimate

### Free Tier (What you have now)
- **Google Gemini 2.0 Flash**: Free (2M tokens/day)
- **Tavily**: Free (1,000 searches/month)
- **Total**: $0/month

### Recommended Setup
- **Google Gemini**: Free
- **Tavily**: $25/month (5,000 searches)
- **Alpha Vantage**: Free (25 requests/day)
- **NewsAPI**: Free (100 requests/day)
- **Total**: $25/month

### Premium Setup
- **Google Gemini Pro**: ~$50/month
- **Tavily**: $50/month (10,000 searches)
- **Alpha Vantage Premium**: $50/month
- **NewsAPI**: $449/month
- **Crunchbase**: $99/month
- **Total**: $698/month

## 🔑 How to Add API Keys

1. **Get the API keys** from the links above
2. **Add to `.env` file**:
   ```bash
   ALPHA_VANTAGE_API_KEY=your_actual_key_here
   NEWS_API_KEY=your_actual_key_here
   ```
3. **Restart your application** to load new environment variables

## 🧪 Testing Your Setup

Run this command to test which APIs are configured:

```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

apis = {
    'Google Gemini': 'GOOGLE_API_KEY',
    'Tavily': 'TAVILY_API_KEY',
    'Alpha Vantage': 'ALPHA_VANTAGE_API_KEY',
    'NewsAPI': 'NEWS_API_KEY',
    'Serper': 'SERPER_API_KEY',
    'Crunchbase': 'CRUNCHBASE_API_KEY',
}

print('API Configuration Status:')
print('-' * 50)
for name, var in apis.items():
    status = '✅ Configured' if os.getenv(var) else '❌ Not set'
    print(f'{name:20} {status}')
"
```

## 📊 Agent-Specific Requirements

| Agent | Required APIs | Optional APIs |
|-------|--------------|---------------|
| **Profile Agent** | Tavily, Gemini | Crunchbase |
| **Leadership Agent** | Tavily, Gemini | LinkedIn API |
| **Financial Agent** | Tavily, Gemini | Alpha Vantage, FMP, Crunchbase |
| **Market Agent** | Tavily, Gemini | - |
| **Signals Agent** | Tavily, Gemini | NewsAPI, Serper |

## 🎯 Recommendation

**Start with what you have** (Gemini + Tavily) and add optional APIs based on:

1. **If researching public companies**: Add Alpha Vantage (free)
2. **If need recent news**: Add NewsAPI (free tier)
3. **If researching startups**: Consider Crunchbase (paid)

Your current setup is **fully functional** for all 5 agents!
