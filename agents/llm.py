"""Shared LLM instance for all CrewAI agents — Perplexity Sonar.

Uses LiteLLM (bundled with crewai) with the perplexity/ provider prefix.
No additional dependencies required beyond crewai.

Import in every agent:
    from agents.llm import perplexity_llm
"""
import os
from crewai import LLM


def get_perplexity_llm() -> LLM:
    api_key = os.getenv("PERPLEXITY_API_KEY", "")
    if not api_key:
        raise EnvironmentError(
            "PERPLEXITY_API_KEY is not set. "
            "Add it to your Streamlit secrets or .env file."
        )
    return LLM(
        model="perplexity/sonar",
        api_key=api_key,
        temperature=0.1,
    )


perplexity_llm = get_perplexity_llm()
