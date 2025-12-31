# Workspace Map

> Last updated: 2025-12-31

## Folder Structure

```
04-workspace/
│
├── 01-hypotheses/                    # Hypothesis tracking (D/F/V categories)
│   ├── desirability/                 # Customer pain & demand hypotheses
│   ├── feasibility/                  # Technical feasibility hypotheses
│   └── viability/                    # Business model hypotheses
│
├── 02-experiments/                   # Validation experiments
│   └── NNN-experiment-name/          # Each experiment gets numbered folder
│       ├── experiment-plan.md        # Experiment design & success criteria
│       └── input/                    # Raw data for this experiment
│
├── 03-interviews/                    # Interview data warehouse
│   ├── raw-transcripts/              # Unprocessed interview transcripts
│   ├── analyzed/                     # Processed interviews with insights
│   └── synthesis/                    # Cross-interview patterns & themes
│
├── 04-icp/                           # ICP definition
│   ├── segments/                     # Customer segment definitions
│   └── personas/                     # Validated buyer personas
│
├── 05-prospect-research/             # Lead research
│   ├── target-companies/             # Company profiles & research
│   ├── target-contacts/              # Individual contact research
│   └── lead-lists/                   # Curated outreach lists
│
├── 06-outbound/                      # Outbound campaigns
│   ├── campaigns/                    # Individual campaign folders
│   ├── sequences/                    # Email/LinkedIn sequences
│   ├── assets/                       # Scripts, templates, copy
│   └── results/                      # Campaign performance data
│
├── 07-insights/                      # Strategic synthesis
│   ├── patterns/                     # Recurring themes from research
│   ├── decisions/                    # Key decisions & rationale
│   ├── slack-extracts/               # Slack channel extractions
│   └── core-papers/                  # Curated foundational papers
│       ├── _index.md                 # Paper index with tiers
│       ├── context-engineering/      # Context management papers
│       ├── agent-memory/             # Memory & learning papers
│       ├── multi-agent/              # Orchestration papers
│       └── evaluation-safety/        # Eval & safety papers
│
├── 08-strategy/                      # Business foundations
│   └── [strategy documents]          # BMC, VPC, company context, team alignment
│
└── templates/                        # Reusable frameworks & templates
```

---

## Workflow

```
RESEARCH → OUTBOUND → INTERVIEW → ANALYZE → VALIDATE → DECIDE

05-prospect-research/    Find target companies & contacts
        ↓
06-outbound/             Run campaigns to book interviews
        ↓
03-interviews/           Conduct & store interviews
        ↓
02-experiments/          Analyze per experiment design
        ↓
01-hypotheses/           Update hypothesis status
        ↓
07-insights/             Synthesize patterns & decisions
        ↓
04-icp/                  Refine ICP based on evidence
```

---

## Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Experiments | `NNN-descriptive-name/` | `002-pricing-validation/` |
| Campaigns | `NNN-channel-target/` | `001-linkedin-cto-saas/` |
| Transcripts | `YYYY-MM-DD-company.md` | `2025-01-15-stripe.md` |
| Hypotheses | `X##-short-name.md` | `D1-root-cause-blindness.md` |

---

## Key Files Reference

| When you need... | Go to... |
|------------------|----------|
| Full company strategy | `08-strategy/company-context.md` |
| Hypotheses | `01-hypotheses/` |
| Experiment data | `02-experiments/` |
| Target customer profile | `08-strategy/value-proposition-canvas.md` |
| Team roles & risks | `08-strategy/team-alignment-map.md` |
| Core research papers | `07-insights/core-papers/_index.md` |
| Slack extractions | `07-insights/slack-extracts/` |
