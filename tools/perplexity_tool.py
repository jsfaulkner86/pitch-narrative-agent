import os
import httpx
from crewai.tools import tool


@tool("research_narrative")
def research_narrative(query: str) -> str:
    """Research investor language trends, objection responses, and pitch narrative strategies
    using the Perplexity Sonar API. Use this for any research task related to fundraising
    narratives, investor language, market sizing, or objection handling."""
    api_key = os.getenv("PERPLEXITY_API_KEY", "")
    if not api_key:
        return "Error: PERPLEXITY_API_KEY not set."
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a pitch narrative strategist for women's health tech founders. "
                    "Research: successful women's health fundraising narratives, investor language that resonates, "
                    "common objections investors raise and how top founders address them, "
                    "market sizing language that lands, and recent women's health funding announcements "
                    "that reveal what story investors funded. Always cite sources."
                ),
            },
            {"role": "user", "content": query},
        ],
    }
    resp = httpx.post(
        "https://api.perplexity.ai/chat/completions",
        json=payload,
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
