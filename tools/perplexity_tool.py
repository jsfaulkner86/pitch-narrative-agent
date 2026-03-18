import httpx
from config.settings import settings

def research_narrative(query: str) -> str:
    headers = {"Authorization": f"Bearer {settings.perplexity_api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "You are a pitch narrative strategist for women's health tech founders. Research: successful women's health fundraising narratives, investor language that resonates, common objections investors raise and how top founders address them, market sizing language that lands, and recent women's health funding announcements that reveal what story investors funded. Always cite sources."},
            {"role": "user", "content": query},
        ],
    }
    resp = httpx.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
