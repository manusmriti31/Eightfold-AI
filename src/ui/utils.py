"""Utility functions for Streamlit app."""

import asyncio
from typing import Any, Coroutine


def run_async(coro: Coroutine) -> Any:
    """
    Run an async coroutine in Streamlit.
    
    Args:
        coro: Async coroutine to run
        
    Returns:
        Result of the coroutine
    """
    try:
        # Try to get existing event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        # No event loop exists, create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(coro)
    finally:
        # Don't close the loop as it might be needed again
        pass


def format_number(num: float, decimals: int = 2) -> str:
    """
    Format number with commas and decimals.
    
    Args:
        num: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted number string
    """
    return f"{num:,.{decimals}f}"


def format_percentage(num: float, decimals: int = 1) -> str:
    """
    Format number as percentage.
    
    Args:
        num: Number to format (0-1 range)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{num * 100:.{decimals}f}%"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
