"""Shared LLM instance for all CrewAI agents — Perplexity Sonar.

Fix: litellm.drop_params = True silently strips unsupported parameters
(including CrewAI's injected stop=["\\nObservation"]) before the request
reaches Perplexity, preventing the 400 unsupported_parameter error.

Import in every agent:
    from agents.llm import perplexity_llm
"""
import os
import litellm
from crewai import LLM

# Strip any parameter Perplexity doesn't support (including CrewAI stop words)
litellm.drop_params = True


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
        stop=[],
    )


perplexity_llm = get_perplexity_llm()
