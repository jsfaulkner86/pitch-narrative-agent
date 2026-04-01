# 🎤 Pitch Narrative & Storytelling Agent

Analyzes successful women's health pitch decks, monitors investor language resonance, and helps founders continuously refine their fundraising narrative as the market evolves.

Delivers **bi-weekly narrative intelligence** and **on-demand pitch critique**.

*Built by The Faulkner Group — Agentic AI for Women's Health Founders*

---

## What It Does

Women's health founders are pitching into a market where investor language, funding thesis framing, and clinical evidence standards shift every quarter. This agent monitors what's actually landing right now — and tells you where your narrative is falling short.

**Every run produces a 5-section briefing:**

| Section | What You Get |
|---|---|
| 📊 Market Language Update | Investor phrases resonating in recently funded deals |
| 🛡️ Objection Playbook | Top 3 current objections with tested founder responses |
| 📝 Pitch Critique | Rubric-scored critique with replacement language |
| ✏️ Narrative Refreshes | Specific before/after rewrites for your weakest slides |
| 📊 Funding Context | Recent raises and the story framing that got them funded |

---

## Agent Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   CrewAI Pipeline                       │
│                                                         │
│  ┌──────────────────────┐   ┌───────────────────────┐  │
│  │  Market Language     │   │   Objection Agent     │  │
│  │  Agent               │   │                       │  │
│  │  • Perplexity search │   │  • Top 3 objections   │  │
│  │  • Recent raise lang │   │  • Founder rebuttals  │  │
│  └──────────┬───────────┘   └──────────┬────────────┘  │
│             │                          │                │
│             ▼                          ▼                │
│       ┌─────────────────────────────────────┐          │
│       │     Narrative Critique Agent        │          │
│       │  • 5-dimension rubric (0–100 pts)   │          │
│       │  • Per-dimension replacement lang   │          │
│       └──────────────────┬──────────────────┘          │
│                          ▼                              │
│       ┌─────────────────────────────────────┐          │
│       │    Narrative Synthesizer Agent      │          │
│       │  • Structured bi-weekly briefing    │          │
│       │  • Before/after narrative rewrites  │          │
│       └─────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
```

### Critique Rubric (100 points total)

| Dimension | Points | What It Measures |
|---|---|---|
| Problem Urgency | 0–20 | Emotional + clinical weight |
| Market Size Credibility | 0–20 | TAM/SAM/SOM defensibility |
| Solution Differentiation | 0–20 | Specificity of the "why us" |
| Evidence Confidence | 0–20 | Clinical evidence staged appropriately |
| Business Model Clarity | 0–20 | Path to revenue and scale |

---

## Project Structure

```
pitch-narrative-agent/
├── agents/
│   ├── market_language_agent.py       # Perplexity-powered investor language monitor
│   ├── narrative_critique_agent.py    # 5-dimension rubric scorer
│   ├── objection_agent.py             # Investor objection + rebuttal generator
│   └── narrative_synthesizer_agent.py # Briefing synthesizer
├── pipelines/                         # CrewAI crew definitions
├── tools/
│   └── perplexity_tool.py             # Perplexity search integration
├── profiles/                          # Founder pitch profiles
├── delivery/                          # Output delivery handlers
├── scheduler/                         # Bi-weekly run scheduler
├── db/                                # Persistence layer
├── config/                            # Agent configuration
├── .env.example
└── requirements.txt
```

---

## Setup

### Prerequisites

- Python 3.11+
- OpenAI API key
- Perplexity API key

### Installation

```bash
git clone https://github.com/jsfaulkner86/pitch-narrative-agent.git
cd pitch-narrative-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables

```bash
# .env
OPENAI_API_KEY=your_openai_key
PERPLEXITY_API_KEY=your_perplexity_key
```

---

## Usage

### On-Demand Pitch Critique

```bash
python pipelines/run_critique.py \
  --founder "Your Company Name" \
  --summary "Your current pitch summary paragraph here"
```

### Run Full Bi-Weekly Briefing

```bash
python pipelines/run_briefing.py --profile profiles/your_founder.json
```

### Scheduled Run

```bash
python scheduler/schedule.py  # Runs on configured cadence
```

---

## Output Example

```markdown
## 📊 Market Language Update
Investors funding maternal health in Q1 2026 are responding to:
"closing the 40-week gap" over "improving maternal outcomes"...

## 🛡️ Objection Playbook
**Objection:** "The market is too fragmented for institutional scale."
**Response:** "We're not solving fragmentation — we're the layer that makes
fragmentation irrelevant by sitting above EHR and payer workflows..."

## 📝 Pitch Critique
- Problem Urgency: 14/20 — Clinical framing strong, emotional resonance missing.
  → Replace "affects 1 in 8 women" with "1 in 8 women leave their OB
    appointment without a next step — we built the next step."
...
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | CrewAI |
| LLM | GPT-4o (OpenAI) |
| Market Research | Perplexity API |
| Language | Python 3.11 |
| Scheduling | Native Python scheduler |

---

## Built By

**The Faulkner Group** — Boutique advisory and AI systems firm for leaders solving real operational problems in healthcare.

[thefaulknergroupadvisors.com](https://thefaulknergroupadvisors.com)
