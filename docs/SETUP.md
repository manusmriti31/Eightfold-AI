# Setup Guide

## Prerequisites

- Python 3.11+
- pip or uv package manager

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/langchain-ai/company-researcher.git
cd company-researcher
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

## Configuration

### 1. API Keys

Copy the example environment file:

```bash
cp .env.example .env
```

### 2. Required API Keys

Edit `.env` and add your API keys:

```bash
# Required
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Optional (enhances data quality)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
FMP_API_KEY=your_fmp_key
NEWS_API_KEY=your_news_api_key
SERPER_API_KEY=your_serper_key
```

### 3. Get API Keys

**Google Gemini API** (Required)
- Sign up: https://ai.google.dev/
- Free tier: 10 RPM, 4M TPM

**Tavily API** (Required)
- Sign up: https://tavily.com/
- Free tier: 1,000 searches/month

**Optional APIs:**
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key (Free: 25 req/day)
- **FMP**: https://site.financialmodelingprep.com/developer/docs/ (Free: 250 req/day)
- **NewsAPI**: https://newsapi.org/register (Free: 100 req/day)
- **Serper**: https://serper.dev/ (Free: 2,500 searches)

## Verification

Test your setup:

```bash
python test_agents.py
```

Expected output:
```
✅ Required APIs:
GOOGLE_API_KEY            ✅ SET
TAVILY_API_KEY            ✅ SET
```

## Next Steps

- [Quick Start Guide](QUICKSTART.md)
- [Architecture Overview](ARCHITECTURE.md)
- [API Keys Details](API_KEYS.md)
