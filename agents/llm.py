"""Shared LLM instance for all agents — Perplexity Sonar via LangChain.

Import this module in every agent file:
    from agents.llm import perplexity_llm

This ensures CrewAI never falls back to OpenAI.
"""
import os
from langchain_perplexity import ChatPerplexity

def get_perplexity_llm() -> ChatPerplexity:
    """Return a ChatPerplexity instance using the PERPLEXITY_API_KEY env var."""
    api_key = os.getenv("PERPLEXITY_API_KEY", "")
    if not api_key:
        raise EnvironmentError(
            "PERPLEXITY_API_KEY is not set. "
            "Add it to your Streamlit secrets or .env file."
        )
    return ChatPerplexity(
        model="sonar",
        temperature=0.1,
        pplx_api_key=api_key,
    )

# Module-level singleton — imported directly by agent files
perplexity_llm = get_perplexity_llm()
