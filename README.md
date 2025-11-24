# 🔍 Multi-Agent Company Research System

An intelligent multi-agent system that researches companies using 5 specialized AI agents working in parallel. Built with LangGraph and Google Gemini, it generates comprehensive research reports with visualizations and interactive UI.

## ✨ Features

- **5 Specialized AI Agents** - Profile, Leadership, Financial, Market, and Signals agents working in parallel
- **Interactive Web UI** - Streamlit-based interface with real-time agent monitoring
- **Comprehensive Reports** - HTML reports with charts, tables, and visualizations
- **Multiple Report Types** - Executive summary, detailed analysis, or investor reports
- **High Confidence** - Average 85%+ confidence scores with source tracking
- **Flexible Architecture** - Run all agents or select specific ones based on your needs

## 🏗️ Architecture

The system uses **5 specialized AI agents** that work in parallel:

### Research Agents

1. **🏢 Profile Agent** - Business model, products, revenue streams
2. **👥 Leadership Agent** - Founders, executives, management team
3. **💰 Financial Agent** - Revenue, profitability, funding, financial ratios
4. **📊 Market Agent** - Market size, competitors, SWOT analysis
5. **🚨 Signals Agent** - News, sentiment, risks, hiring trends

### Processing Pipeline

```
START → [5 Agents in Parallel] → Aggregate → Synthesize → Generate Report
```

**Benefits:**
- ⚡ 2.5x faster than sequential execution
- 🎯 85%+ average confidence scores
- 📊 45+ sources per company
- 📝 Comprehensive reports with visualizations

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key
- Tavily API key (for web search)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/company-researcher.git
cd company-researcher
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install as a package:

```bash
pip install -e .
```

### Step 4: Configure API Keys

1. Copy the example environment file:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
```

2. Edit `.env` and add your API keys:

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Optional (for enhanced data)
ALPHA_VANTAGE_API_KEY=your_key_here
FMP_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

**Get API Keys:**
- **Google Gemini**: https://ai.google.dev/
- **Tavily**: https://tavily.com/
- **Alpha Vantage** (optional): https://www.alphavantage.co/
- **Financial Modeling Prep** (optional): https://financialmodelingprep.com/

## 🎯 Usage

### Option 1: Web UI (Recommended)

Launch the interactive Streamlit interface:

```bash
streamlit run ui.py
```

Then open your browser to `http://localhost:8501`

**Features:**
- Select which agents to run
- Choose report type (executive, detailed, investor)
- Real-time agent monitoring
- Interactive HTML reports with charts
- Export reports

### Option 2: Python API

Use the system programmatically:

```python
import asyncio
from src.graph.multi_agent_graph import research_company

async def main():
    # Research a company
    result = await research_company("Tesla")
    
    # Access results
    print(result['final_report'])
    print(f"Confidence: {result['report_metadata']['average_confidence']:.2%}")
    print(f"Sources: {len(result['all_sources'])}")

asyncio.run(main())
```

### Option 3: Selective Agents

Run only specific agents:

```python
from src.graph.selective_graph import research_selective

# Run only financial and market agents
result = await research_selective(
    company="Apple",
    selected_agents=["financial", "market"],
    report_type="executive"
)
```

### Option 4: Command Line Testing

Test individual agents:

```bash
python test_intelligent_graph.py
```

Quick test:

```bash
python test_intelligent_graph_quick.py
```

## 📊 Report Types

### Executive Summary
- High-level overview
- Key metrics and insights
- 1-2 page format
- Perfect for quick briefings

### Detailed Analysis
- Comprehensive research
- All agent findings
- Charts and visualizations
- 5-10 page format

### Investor Report
- Financial focus
- Market analysis
- Risk assessment
- Investment recommendations

## 📁 Project Structure

```
company-researcher/
├── src/
│   ├── agent/          # LangGraph agent configuration
│   ├── agents/         # Individual research agents
│   │   ├── intelligence/  # Intelligent routing
│   │   └── research/      # Research agents
│   ├── graph/          # Multi-agent orchestration
│   ├── llm/            # LLM configuration
│   ├── tools/          # Search and data tools
│   │   ├── analysis/   # Data analysis tools
│   │   ├── data/       # Financial data APIs
│   │   ├── search/     # Web search tools
│   │   └── visualization/  # Charts and tables
│   ├── ui/             # Streamlit web interface
│   └── voice/          # Voice interface (future)
├── docs/               # Documentation
├── eval/               # Evaluation scripts
├── test_reports/       # Generated reports
├── .env.example        # Environment template
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Package configuration
└── ui.py              # Main UI entry point
```

## 🔧 Configuration

### Adjust Research Depth

Edit `src/graph/multi_agent_graph.py`:

```python
# More queries = more depth
max_queries=5,

# More results = more sources
max_results_per_query=3
```

### Adjust Rate Limiting

```python
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.15,  # Adjust for your API limits
    check_every_n_seconds=60,
    max_bucket_size=10
)
```

### Change LLM Model

Edit `src/llm/llm_config.py`:

```python
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",  # or "gemini-1.5-pro"
    temperature=0.7
)
```

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed installation instructions
- **[Quick Start](docs/QUICKSTART.md)** - Get started quickly
- **[Architecture](docs/ARCHITECTURE.md)** - System design and workflow
- **[Agents](docs/AGENTS.md)** - Agent specifications and capabilities
- **[Tools](docs/TOOLS.md)** - Available tools and integrations
- **[API Keys](docs/API_KEYS.md)** - API keys setup guide

## 🧪 Testing

Run the test suite:

```bash
# Test intelligent graph
python test_intelligent_graph.py

# Quick test
python test_intelligent_graph_quick.py

# Test report formatter
python test_report_formatter.py
```

## 📈 Performance

- **Speed**: 2.5x faster than sequential execution
- **Confidence**: 85%+ average across all agents
- **Sources**: 45+ unique sources per company
- **Time**: ~3-4 minutes per company (rate limited)

## 🛠️ Troubleshooting

### Rate Limit Errors

If you see `429 You exceeded your current quota`:

1. Wait 1 minute for rate limit to reset
2. Reduce `requests_per_second` in configuration
3. Consider upgrading your API plan

### Low Quality Results

Increase research depth:
- Increase `max_queries` (more search queries)
- Increase `max_results_per_query` (more sources per query)
- Add optional API keys for better data

### Import Errors

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [Google Gemini](https://ai.google.dev/)
- Search by [Tavily](https://tavily.com/)

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check the [documentation](docs/README.md)
- Review existing issues for solutions

---

**Made with ❤️ using LangGraph and Google Gemini**
