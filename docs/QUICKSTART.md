# Quick Start Guide

## Test Individual Agents

Test a single agent:

```bash
python test_agents.py
```

Test all 5 agents:

```bash
python test_agents.py --full
```

## Use Multi-Agent Graph

Test the complete system:

```bash
python test_multi_agent_graph.py
```

## Use in Your Code

### Simple Usage

```python
from src.graph.multi_agent_graph import research_company

# Research a company
result = await research_company("Tesla")

# Access results
print(result['final_report'])
print(result['executive_summary'])
print(f"Confidence: {result['report_metadata']['average_confidence']:.2%}")
```

### Advanced Usage

```python
from src.graph.multi_agent_graph import graph

# Stream events for real-time updates
async for event in graph.astream_events(
    {"company": "OpenAI"},
    version="v1"
):
    if event["event"] == "on_chain_start":
        print(f"Starting: {event['name']}")
```

## Expected Output

### Individual Agent Test

```
🧪 Testing Profile Agent...
   Company: OpenAI
[ProfileAgent] Starting research for OpenAI
[ProfileAgent] Generated 5 queries
[ProfileAgent] Found 15 sources
[ProfileAgent] Extracted structured data
[ProfileAgent] Confidence score: 0.85
   ✅ Success!
```

### Multi-Agent Graph Test

```
============================================================
🚀 Starting Multi-Agent Research: Tesla
============================================================

🏢 Profile Agent researching Tesla...
👥 Leadership Agent researching Tesla...
💰 Financial Agent researching Tesla...
📊 Market Agent researching Tesla...
🚨 Signals Agent researching Tesla...

📦 Aggregating all research data...
📝 Synthesizing final report...

============================================================
✅ Research Complete!
============================================================
📊 Total Sources: 45
📈 Average Confidence: 0.85
```

## Performance

**Timing:**
- Individual agent: ~15-20 seconds
- All 5 agents (parallel): ~3-4 minutes (rate limited)

**Rate Limiting:**
- Gemini 2.0 Flash: 10 RPM limit
- Configured: 9 RPM (safe margin)

## Troubleshooting

### Rate Limit Errors

If you see `429 You exceeded your current quota`:

1. Wait 1 minute for rate limit to reset
2. Reduce `requests_per_second` in `src/graph/multi_agent_graph.py`

### Low Quality Results

Increase research depth:

```python
# In multi_agent_graph.py
max_queries=7,  # More queries
max_results_per_query=5  # More sources
```

## Next Steps

- [Architecture Guide](ARCHITECTURE.md)
- [Agent Details](AGENTS.md)
- [Tools Documentation](TOOLS.md)
