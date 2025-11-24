# LLM Configuration - Google Gemini

## Overview

This system uses **Google Gemini 2.0 Flash** as the LLM provider for all AI operations.

---

## Configuration

### API Key Setup

Add your Google API key to `.env`:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### Get Your API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy and paste into `.env` file

---

## LLM Settings

```python
Model: gemini-2.0-flash
Temperature: 0.3
Rate Limit: 0.15 requests/second
Max Bucket Size: 5
```

---

## Features

### Fast & Reliable
- Gemini 2.0 Flash is optimized for speed
- Consistent, high-quality responses
- Proven in production environments

### Structured Output
- Supports JSON schema validation
- Works seamlessly with Pydantic models
- Reliable parsing for all agent outputs

### Rate Limiting
- Built-in rate limiter prevents API throttling
- Conservative limits ensure stability
- Automatic retry on transient failures

---

## Usage in Code

### Get Configured LLM

```python
from src.llm import get_configured_llms

llms = get_configured_llms()

query_llm = llms["query_llm"]
extraction_llm = llms["extraction_llm"]
report_llm = llms["report_llm"]
```

### All Tasks Use Same Model

For simplicity and reliability, all tasks use the same Gemini model:
- Query generation
- Data extraction
- Report synthesis

This ensures consistent behavior across all agents.

---

## Benefits

### Simplicity
- Single LLM provider
- No complex configuration
- Easy to understand and maintain

### Reliability
- Proven track record
- Stable API
- Good error handling

### Performance
- Fast response times
- High-quality outputs
- Efficient token usage

### Cost-Effective
- Competitive pricing
- Free tier available
- Pay-as-you-go model

---

## Troubleshooting

### Error: "GOOGLE_API_KEY not found"

**Solution:** Add your API key to `.env` file:
```bash
GOOGLE_API_KEY=your_actual_key_here
```

### Error: "Rate limit exceeded"

**Solution:** The system has built-in rate limiting. If you still hit limits:
1. Wait a few minutes
2. Check your API quota at https://console.cloud.google.com/
3. Consider upgrading your plan

### Error: "Invalid API key"

**Solution:** 
1. Verify your API key is correct
2. Check it's not expired
3. Ensure it has the necessary permissions
4. Generate a new key if needed

---

## API Limits

### Free Tier
- 60 requests per minute
- 1,500 requests per day
- Sufficient for testing and small-scale use

### Paid Tier
- Higher rate limits
- More requests per day
- Better for production use

---

## Code Structure

```
src/llm/
├── __init__.py          # Package exports
└── llm_config.py        # Gemini configuration
```

### llm_config.py

Main configuration file that:
- Loads API key from environment
- Creates Gemini LLM instance
- Configures rate limiting
- Returns LLM for all tasks

---

## Best Practices

### 1. Environment Variables
Always use `.env` file for API keys - never hardcode them.

### 2. Rate Limiting
Keep the conservative rate limits to avoid API throttling.

### 3. Error Handling
The system handles errors gracefully and provides clear messages.

### 4. Temperature
Temperature of 0.3 provides good balance between creativity and consistency.

---

## Future Enhancements

If needed, the system can be extended to:
- Support multiple LLM providers
- Use different models for different tasks
- Implement caching for repeated queries
- Add fallback providers

For now, Gemini provides excellent performance for all use cases.

---

## Summary

✅ **Simple** - Single LLM provider  
✅ **Reliable** - Proven and stable  
✅ **Fast** - Optimized for speed  
✅ **Cost-effective** - Competitive pricing  
✅ **Production-ready** - Battle-tested  

**Your system is configured and ready to use!** 🚀
