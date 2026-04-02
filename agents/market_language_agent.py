from crewai import Agent
from tools.perplexity_tool import research_narrative
from agents.llm import perplexity_llm

market_language_agent = Agent(
    role="Investor Language Intelligence Analyst",
    goal=(
        "Monitor what language, framing, and narrative structures are resonating with investors "
        "funding women's health companies right now. Surface language patterns from recently funded pitches."
    ),
    backstory=(
        "You analyze the language of successful fundraises. When a maternal health company raises $20M, "
        "you study how they framed the problem, market size, and clinical evidence. "
        "You give founders the language that is landing right now, not two years ago."
    ),
    tools=[research_narrative],
    llm=perplexity_llm,
    verbose=True,
    allow_delegation=False,
)
