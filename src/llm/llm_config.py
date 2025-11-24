"""LLM configuration - Google Gemini."""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.rate_limiters import InMemoryRateLimiter


def get_configured_llms() -> Dict[str, Any]:
    """
    Get optimized multi-model LLM configuration.
    
    Uses different Gemini models strategically:
    - Fast models (high RPM) for query generation
    - Live models (unlimited RPM) for data extraction  
    - Quality models for gap detection
    - Premium models for final synthesis
    
    Returns:
        Dictionary with LLM instances for different tasks
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError(
            "GOOGLE_API_KEY not found in environment variables. "
            "Please set GOOGLE_API_KEY in .env file"
        )
    
    print("✅ Using Google Gemini Multi-Model Configuration")
    print("   - Query Generation: gemini-2.0-flash (9 RPM)")
    print("   - Data Extraction: gemini-2.0-flash (9 RPM)")
    print("   - Gap Detection: gemini-2.5-flash (10 RPM)")
    print("   - Report Synthesis: gemini-2.5-pro (2 RPM)")
    
    # Query Generation: Standard flash model
    # Note: gemini-2.0-flash-lite not available in standard API
    query_llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.3,
        rate_limiter=InMemoryRateLimiter(
            requests_per_second=0.15,  # 9 RPM
            check_every_n_seconds=0.5,
            max_bucket_size=5,
        )
    )
    
    # Data Extraction: Standard flash model
    # Note: gemini-2.0-flash-live only available in Live API, not standard API
    extraction_llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2,
        rate_limiter=InMemoryRateLimiter(
            requests_per_second=0.15,  # 9 RPM
            check_every_n_seconds=0.5,
            max_bucket_size=5,
        )
    )
    
    # Gap Detection: Quality model for better reasoning
    gap_detection_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        rate_limiter=InMemoryRateLimiter(
            requests_per_second=0.15,  # 10 RPM
            check_every_n_seconds=0.5,
            max_bucket_size=5,
        )
    )
    
    # Report Synthesis: Premium model for highest quality
    synthesis_llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.4,
        rate_limiter=InMemoryRateLimiter(
            requests_per_second=0.03,  # 2 RPM
            check_every_n_seconds=1.0,
            max_bucket_size=2,
        )
    )
    
    return {
        "query_llm": query_llm,              # Fast: 30 RPM
        "extraction_llm": extraction_llm,    # Unlimited RPM
        "gap_detection_llm": gap_detection_llm,  # Quality: 10 RPM
        "synthesis_llm": synthesis_llm,      # Premium: 2 RPM
        "report_llm": synthesis_llm,         # Alias for compatibility
        "provider": "google"
    }


def get_llm_for_task(task: str) -> Any:
    """
    Get LLM for specific task.
    
    Args:
        task: Task type (query, extraction, report)
        
    Returns:
        LLM instance
    """
    llms = get_configured_llms()
    
    task_map = {
        "query": "query_llm",
        "extraction": "extraction_llm",
        "report": "report_llm"
    }
    
    return llms.get(task_map.get(task, "extraction_llm"))
