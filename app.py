"""Streamlit demo app for Pitch Narrative Agent — The Faulkner Group.

DEMO MODE: Accepts a single synthetic founder profile via form input.
Runs the 4-agent CrewAI crew and renders output in-browser.
No Supabase writes, no email delivery, no Notion push in demo mode.
The production bi-weekly pipeline is in pipelines/biweekly_narrative_run.py.
"""
import os
import sys
import streamlit as st
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Pitch Narrative Agent · The Faulkner Group",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Brand CSS ───────────────────────────────────────────────────
# Brand: Blue #6E93B0 (primary/actions/accents), Gold #D4AE48 (highlights/tags)
st.markdown("""
<style>
/* ─ Layout ──────────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
    background: #f4f3ef;
}
[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    padding-top: 2rem;
    max-width: 900px;
}

/* ─ Form ──────────────────────────────────────────────────── */
[data-testid="stForm"] {
    background: #ffffff;
    border: 1.5px solid #c8c5be;
    border-radius: 10px;
    padding: 1.5rem 1.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* ─ Input labels ─────────────────────────────────────────── */
.stTextInput label,
.stTextArea label,
[data-baseweb="form-control-label"] {
    color: #1a1916 !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.01em;
}

/* ─ Text inputs & textareas ───────────────────────────────── */
.stTextInput input,
.stTextArea textarea {
    background: #fafaf8 !important;
    border: 1.5px solid #b0ada6 !important;
    border-radius: 6px !important;
    color: #1a1916 !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 0.75rem !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #6E93B0 !important;
    box-shadow: 0 0 0 3px rgba(110,147,176,0.18) !important;
    outline: none !important;
    background: #ffffff !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #9c9890 !important;
}

/* ─ Primary button ─────────────────────────────────────────── */
.stButton > button,
[data-testid="stFormSubmitButton"] > button,
[data-testid="stBaseButton-primary"] {
    background: #6E93B0 !important;
    color: #ffffff !important;
    border: none !important;
    padding: 0.6rem 1.5rem !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em;
    transition: background 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover,
[data-testid="stBaseButton-primary"]:hover {
    background: #4e7799 !important;
    box-shadow: 0 2px 8px rgba(110,147,176,0.30) !important;
}

/* ─ Download button ────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #6E93B0 !important;
    border: 1.5px solid #6E93B0 !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    padding: 0.45rem 1.25rem !important;
    transition: background 0.15s ease, color 0.15s ease;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #6E93B0 !important;
    color: #ffffff !important;
}

/* ─ Output card ───────────────────────────────────────────── */
.output-card {
    background: #ffffff;
    border: 1.5px solid #c8c5be;
    border-radius: 10px;
    padding: 1.5rem 1.75rem;
    margin-top: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    color: #1a1916;
    line-height: 1.7;
}

/* ─ Tags ────────────────────────────────────────────────────── */
.tag {
    display: inline-block;
    background: rgba(212,174,72,0.18);
    color: #8a6a00;
    border: 1px solid rgba(212,174,72,0.45);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 999px;
    margin-right: 4px;
    letter-spacing: 0.02em;
}

/* ─ Info / warning / success / error ─────────────────────────── */
[data-testid="stInfo"] {
    background: #eef3f7 !important;
    border-left: 4px solid #6E93B0 !important;
    color: #1a1916 !important;
    border-radius: 6px !important;
}
[data-testid="stWarning"] {
    background: #fdf3e3 !important;
    border-left: 4px solid #c87d00 !important;
    color: #1a1916 !important;
    border-radius: 6px !important;
}
[data-testid="stSuccess"] {
    background: #edf6ed !important;
    border-left: 4px solid #2e7d32 !important;
    color: #1a1916 !important;
    border-radius: 6px !important;
}
[data-testid="stError"] {
    background: #fdecea !important;
    border-left: 4px solid #c62828 !important;
    color: #1a1916 !important;
    border-radius: 6px !important;
}

/* ─ Status box ────────────────────────────────────────────── */
[data-testid="stStatusWidget"] {
    border: 1.5px solid #c8c5be !important;
    border-radius: 8px !important;
    background: #ffffff !important;
}

/* ─ Typography ─────────────────────────────────────────── */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #1a1916 !important;
    font-weight: 700;
}
.stMarkdown p, .stMarkdown li {
    color: #2c2b28;
}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown("## 🎯 Pitch Narrative Agent")
st.markdown(
    """<p style='color:#7a7974; margin-top:-0.5rem; margin-bottom:1.5rem;'>
    AI-powered investor narrative briefings &nbsp;·&nbsp;
    <a href='https://thefaulknergroupadvisors.com' target='_blank' style='color:#6E93B0; font-weight:600;'>The Faulkner Group</a>
    </p>""",
    unsafe_allow_html=True,
)

# ── API key guard ───────────────────────────────────────────────
PERPLEXITY_KEY = os.getenv("PERPLEXITY_API_KEY") or st.secrets.get("PERPLEXITY_API_KEY", "")

if not PERPLEXITY_KEY:
    st.error(
        "**PERPLEXITY_API_KEY not configured.** "
        "Add it under App Settings → Secrets in Streamlit Cloud."
    )
    st.stop()

os.environ["PERPLEXITY_API_KEY"] = PERPLEXITY_KEY

# ── Imports (after env vars set) ─────────────────────────────────
try:
    from crewai import Crew, Task
    from agents.market_language_agent import market_language_agent
    from agents.objection_agent import objection_agent
    from agents.narrative_critique_agent import narrative_critique_agent, CRITIQUE_PROMPT
    from agents.narrative_synthesizer_agent import narrative_synthesizer, NARRATIVE_PROMPT
except ImportError as e:
    st.error(f"Import error — check requirements.txt: {e}")
    st.stop()

# ── Sample profile defaults ───────────────────────────────────────────
DEFAULT_PROFILE = {
    "founder_name": "Dr. Sarah Chen",
    "indication": "Post-acute care coordination for complex Medicare populations",
    "stage": "Series A ($8M target)",
    "investor_types_targeting": "healthcare-focused VCs and strategic payers",
    "known_objections": (
        "Reimbursement risk in value-based models, "
        "long sales cycles with health systems, "
        "competitive pressure from larger care management platforms"
    ),
    "current_pitch_summary": (
        "We reduce 30-day readmissions by 40% for high-risk Medicare patients "
        "through AI-driven care coordination. Our platform connects discharge planners, "
        "SNFs, and home health agencies in a single workflow. "
        "Currently live in 3 health systems, $1.2M ARR, growing 20% MoM."
    ),
}

# ── Input form ───────────────────────────────────────────────────
with st.form("narrative_form"):
    st.markdown("### Founder Profile")
    st.caption("Fill in a real or hypothetical profile. Pre-populated with a sample healthcare founder.")

    col1, col2 = st.columns(2)
    with col1:
        founder_name = st.text_input("Founder Name", value=DEFAULT_PROFILE["founder_name"])
        stage = st.text_input("Raise Stage & Target", value=DEFAULT_PROFILE["stage"])
    with col2:
        indication = st.text_input("Indication / Focus Area", value=DEFAULT_PROFILE["indication"])
        investor_types = st.text_input(
            "Investor Types Targeting", value=DEFAULT_PROFILE["investor_types_targeting"]
        )

    known_objections = st.text_area(
        "Known Objections",
        value=DEFAULT_PROFILE["known_objections"],
        height=100,
        help="Comma-separated list of objections investors typically raise.",
    )
    current_pitch = st.text_area(
        "Current Pitch Summary",
        value=DEFAULT_PROFILE["current_pitch_summary"],
        height=130,
        help="Paste your current elevator pitch or executive summary.",
    )

    submitted = st.form_submit_button("▶ Run Narrative Analysis", type="primary", use_container_width=True)

# ── Agent run ───────────────────────────────────────────────────
if submitted:
    if not founder_name or not indication or not current_pitch:
        st.warning("Founder name, indication, and pitch summary are required.")
        st.stop()

    profile = {
        "founder_name": founder_name,
        "indication": indication,
        "stage": stage,
        "investor_types_targeting": investor_types,
        "known_objections": known_objections,
        "current_pitch_summary": current_pitch,
    }

    period = datetime.now().strftime("%B %d, %Y")

    status_box = st.status("Running 4-agent CrewAI pipeline...", expanded=True)
    with status_box:
        st.write("**Agent 1/4** — Market Language Researcher: scanning investor language trends...")
        st.write("**Agent 2/4** — Objection Analyst: researching counter-narratives...")
        st.write("**Agent 3/4** — Narrative Critic: scoring pitch dimensions...")
        st.write("**Agent 4/4** — Narrative Synthesizer: assembling briefing...")
        st.caption("This typically takes 60–120 seconds depending on LLM response times.")

    try:
        tasks = [
            Task(
                description=(
                    f"Research current investor language trends for a "
                    f"{profile['indication']} company doing a {profile['stage']} raise "
                    f"targeting {profile['investor_types_targeting']}. "
                    f"Identify phrases, frameworks, and narrative structures that resonate "
                    f"with this investor cohort right now."
                ),
                agent=market_language_agent,
                expected_output="Current investor language patterns with examples and sources.",
            ),
            Task(
                description=(
                    f"Research evidence-based objection responses for these known objections: "
                    f"{profile['known_objections']}.\n"
                    f"Stage: {profile['stage']}, Indication: {profile['indication']}."
                ),
                agent=objection_agent,
                expected_output="Each objection paired with a proven counter-narrative and supporting data.",
            ),
            Task(
                description=(
                    f"Critique this pitch summary using the scoring rubric below.\n\n"
                    f"PITCH:\n'{profile['current_pitch_summary']}'\n\n"
                    f"RUBRIC:\n{CRITIQUE_PROMPT}"
                ),
                agent=narrative_critique_agent,
                expected_output="Scored critique with specific improvement language for each dimension.",
            ),
            Task(
                description=(
                    f"Synthesize a full narrative briefing for {profile['founder_name']}.\n"
                    f"Period: {period}\n\n"
                    f"{NARRATIVE_PROMPT}"
                ),
                agent=narrative_synthesizer,
                expected_output="Structured narrative briefing covering investor language, objections, critique, and refined pitch.",
            ),
        ]

        crew = Crew(
            agents=[market_language_agent, objection_agent, narrative_critique_agent, narrative_synthesizer],
            tasks=tasks,
            verbose=False,
        )

        result = crew.kickoff()
        result_str = result if isinstance(result, str) else str(result)

        status_box.update(label="Analysis complete", state="complete", expanded=False)

        # ── Output rendering ────────────────────────────────────────────────
        st.markdown("---")
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:0.75rem;margin-bottom:0.25rem'>"
            f"<h3 style='margin:0;color:#1a1916;'>Narrative Briefing</h3>"
            f"<span class='tag'>{founder_name}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
        st.caption(f"Generated {period} · Demo mode (no delivery integrations active)")

        if result_str.strip().startswith("<"):
            st.markdown(
                f'<div class="output-card">{result_str}</div>',
                unsafe_allow_html=True,
            )
        else:
            with st.container(border=True):
                st.markdown(result_str)

        st.download_button(
            label="⬇ Download Briefing (.txt)",
            data=result_str,
            file_name=f"narrative_briefing_{founder_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
        )

    except Exception as e:
        status_box.update(label="Pipeline error", state="error", expanded=True)
        st.error(f"**Agent error:** {e}")
        st.caption("Check that your API keys are valid and all agent modules import correctly.")
        if st.checkbox("Show full traceback"):
            import traceback
            st.code(traceback.format_exc())

# ── Footer ───────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='color:#bab9b4; font-size:0.8rem;'>Production pipeline runs bi-weekly via scheduled job. "
    "This demo does not write to Supabase, Notion, or send email. "
    "<a href='https://github.com/jsfaulkner86/pitch-narrative-agent' target='_blank' style='color:#6E93B0;font-weight:600;'>GitHub →</a></p>",
    unsafe_allow_html=True,
)
