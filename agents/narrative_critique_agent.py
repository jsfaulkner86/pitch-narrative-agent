from crewai import Agent
from agents.llm import perplexity_llm

CRITIQUE_RUBRIC = """
Evaluate the founder's current pitch summary against these dimensions:

1. Problem urgency (0-20): Is the problem framed with emotional + clinical weight?
2. Market size credibility (0-20): Is the TAM/SAM/SOM grounded in defensible data?
3. Solution differentiation (0-20): Is the 'why us' specific and defensible?
4. Evidence confidence (0-20): Is clinical evidence positioned appropriately for stage?
5. Business model clarity (0-20): Is the path to revenue and scale clear?

For each dimension: score, 1-sentence critique, and 1-sentence improvement recommendation.
"""

narrative_critique_agent = Agent(
    role="Pitch Narrative Critic & Coach",
    goal=(
        "Evaluate the founder's current pitch narrative against a structured rubric. "
        "Identify the weakest narrative dimensions and provide specific, actionable language improvements."
    ),
    backstory=(
        "You are a pitch coach who has helped women's health companies raise over $500M combined. "
        "You are direct, specific, and always replace weak language with stronger alternatives "
        "rather than just flagging problems."
    ),
    tools=[],
    llm=perplexity_llm,
    verbose=True,
    allow_delegation=False,
)
CRITIQUE_PROMPT = CRITIQUE_RUBRIC
