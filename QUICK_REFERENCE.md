# Quick Reference Guide

## 🚀 Quick Start

### Windows
```bash
start.bat
```

### macOS/Linux
```bash
chmod +x start.sh
./start.sh
```

### Manual Start
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run UI
streamlit run ui.py
```

## 📋 Common Commands

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Verify setup
python verify_setup.py
```

### Testing
```bash
# Quick test
python test_intelligent_graph_quick.py

# Full test
python test_intelligent_graph.py

# Test report formatter
python test_report_formatter.py
```

### Development
```bash
# Lint code
ruff check .

# Format code
ruff format .

# Type check
mypy src/
```

## 🔑 Required API Keys

1. **Google Gemini** (Required)
   - Get: https://ai.google.dev/
   - Free tier: 60 requests/minute

2. **Tavily** (Required)
   - Get: https://tavily.com/
   - Free tier: 1,000 searches/month

## 📊 Report Types

- **Executive**: Quick overview, 1-2 pages
- **Detailed**: Comprehensive analysis, 5-10 pages
- **Investor**: Financial focus with recommendations

## 🤖 Available Agents

- **Profile**: Business model, products, revenue
- **Leadership**: Founders, executives, team
- **Financial**: Revenue, funding, ratios
- **Market**: Competitors, SWOT, market size
- **Signals**: News, sentiment, risks

## 🔧 Configuration Files

- `.env` - API keys and secrets
- `pyproject.toml` - Package configuration
- `requirements.txt` - Python dependencies
- `langgraph.json` - LangGraph configuration

## 📁 Important Directories

- `src/agents/` - Research agents
- `src/graph/` - Multi-agent orchestration
- `src/tools/` - Search and data tools
- `src/ui/` - Streamlit interface
- `docs/` - Documentation
- `test_reports/` - Generated reports

## 🐛 Troubleshooting

### Rate Limit Error
```
Wait 1 minute, then reduce requests_per_second in:
src/graph/multi_agent_graph.py
```

### Import Error
```bash
pip install -r requirements.txt
```

### Missing .env
```bash
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux
# Then edit .env with your API keys
```

## 📚 Documentation

- [README.md](README.md) - Full documentation
- [docs/SETUP.md](docs/SETUP.md) - Installation guide
- [docs/QUICKSTART.md](docs/QUICKSTART.md) - Quick start
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guide

## 💡 Tips

- Start with executive reports for quick results
- Use selective agents for faster research
- Add optional API keys for better data quality
- Check test_reports/ for example outputs
- Monitor agent progress in the UI

## 🆘 Getting Help

1. Check [docs/](docs/) folder
2. Run `python verify_setup.py`
3. Review [CONTRIBUTING.md](CONTRIBUTING.md)
4. Open an issue on GitHub
