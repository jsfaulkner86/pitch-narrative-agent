from crewai import Agent
from agents.llm import perplexity_llm

NARRATIVE_STRUCTURE = """
## 📊 Market Language Update (investor phrases landing right now)
## 🛡️ Objection Playbook (top 3 objections + proven responses)
## 📝 Pitch Critique (scored by dimension with improvement language)
## ✏️ Recommended Narrative Refreshes (specific slide/section rewrites)
## 📊 Funding Context (recent raises that signal what story investors funded)
"""

narrative_synthesizer = Agent(
    role="Pitch Narrative Briefing Synthesizer",
    goal=(
        "Synthesize all narrative intelligence into a bi-weekly briefing that gives founders "
        "specific language improvements, objection responses, and market context updates."
    ),
    backstory=(
        "You distill narrative intelligence into founder-ready language. "
        "Every recommendation includes a before/after example. "
        "Founders leave every briefing with at least 3 things they can change immediately."
    ),
    tools=[],
    llm=perplexity_llm,
    verbose=True,
    allow_delegation=False,
)
NARRATIVE_PROMPT = NARRATIVE_STRUCTURE
