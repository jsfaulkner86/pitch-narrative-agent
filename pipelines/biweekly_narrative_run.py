from crewai import Crew, Task
from agents.market_language_agent import market_language_agent
from agents.objection_agent import objection_agent
from agents.narrative_critique_agent import narrative_critique_agent, CRITIQUE_PROMPT
from agents.narrative_synthesizer_agent import narrative_synthesizer, NARRATIVE_PROMPT
from delivery.email_briefing import send_narrative_briefing
from delivery.notion_push import push_to_notion
from db.supabase_client import save_briefing
from profiles.founder_profiles import FOUNDER_PROFILES
from datetime import datetime

def run_pipeline():
    period = datetime.now().strftime("%B %d, %Y")
    for profile in FOUNDER_PROFILES:
        tasks = [
            Task(description=f"Research investor language trends for {profile['indication']} {profile['stage']} raise targeting {profile['investor_types_targeting']}.", agent=market_language_agent, expected_output="Current investor language patterns with examples and sources."),
            Task(description=f"Research objection responses for: {profile['known_objections']}. Stage: {profile['stage']}, Indication: {profile['indication']}.", agent=objection_agent, expected_output="Objection + proven counter-narrative for each."),
            Task(description=f"Critique this pitch summary:\n'{profile['current_pitch_summary']}'\n\nRubric:\n{CRITIQUE_PROMPT}", agent=narrative_critique_agent, expected_output="Scored critique with improvement language per dimension."),
            Task(description=f"Synthesize narrative briefing for {profile['founder_name']}.\n{NARRATIVE_PROMPT}", agent=narrative_synthesizer, expected_output="Structured HTML narrative briefing."),
        ]
        crew = Crew(agents=[market_language_agent, objection_agent, narrative_critique_agent, narrative_synthesizer], tasks=tasks, verbose=True)
        result = crew.kickoff()
        result_str = result if isinstance(result, str) else str(result)
        save_briefing({"client_id": profile["client_id"], "period": period, "briefing": result_str})
        push_to_notion(profile["client_id"], profile["founder_name"], result_str, period)
        send_narrative_briefing(profile["email"], profile["founder_name"], result_str, period)
    print("[PitchNarrativeAgent] Bi-weekly run complete.")

if __name__ == "__main__":
    run_pipeline()
