# Example Scenarios: Before & After Nexus

**Document Purpose**: Provide concrete, relatable scenarios showing how Nexus transforms daily work for Sales and Solutions teams.

**Audience**: Workshop participants (dual-audience: Sales + Solutions teams)

**Usage**: Reference these scenarios during presentation (Slides 8-9) and facilitator talking points.

---

## Sales Team Example: Client Proposal Workflow

### Scenario Overview

**Character**: Sarah, Senior Sales Rep at AI Agent Company
**Task**: Create proposal for new enterprise prospect (Healthcare SaaS company)
**Timeline**: 2-day turnaround requested by prospect

---

### Before Nexus: Manual Template Hunting & Copy-Paste Chaos

#### Monday 9:00 AM - Discovery Call Complete

Sarah just finished a discovery call with the prospect. Great fit! They want a proposal by Wednesday morning.

**What Sarah needs to do**:
1. Find the last proposal she sent (where did she save it?)
2. Hunt for pricing info (is it in Slack? Email? Google Drive?)
3. Copy-paste discovery notes from ChatGPT (if she can find the conversation)
4. Customize messaging for Healthcare industry
5. Get legal to review (find the latest template version)

#### Monday 10:00 AM - The Search Begins

Sarah opens Google Drive and searches "proposal"...

**Search results**: 47 files
- "Proposal_Final_v3.docx" (which prospect was this?)
- "Proposal_REALLY_FINAL.docx" (no indication of what's inside)
- "Enterprise_Proposal_Template_2023.docx" (is this current?)
- "Acme_Corp_Proposal.pdf" (this was a different industry)

Sarah spends 30 minutes opening files, trying to find the best starting point.

#### Monday 11:00 AM - Copy-Paste Marathon

Sarah finds a decent template (from 6 months ago). Now she needs to:
- Manually copy discovery notes from ChatGPT (hopes the tab is still open)
- Oh no, she closed ChatGPT yesterday. Notes are gone.
- Reconstructs notes from memory (misses 3 key requirements)
- Copy-paste pricing from Slack conversation with sales ops
- Realizes pricing changed last month
- Messages sales ops: "What's current pricing?"
- Waits for response...

#### Monday 2:00 PM - Customization Chaos

Sales ops responds with new pricing. Sarah updates the proposal.

Now she needs to customize for Healthcare:
- Searches email for "Healthcare case studies"
- Finds 2 case studies, but they're in PDF format
- Copy-paste content into proposal (formatting breaks)
- Spends 20 minutes fixing formatting
- Realizes she forgot to update the client name in section 3 (still says "Acme Corp")

#### Monday 4:30 PM - Legal Review Bottleneck

Sarah sends proposal to legal for review.

Legal responds: "This template is outdated. Use the new one from last month."

Sarah groans. She needs to:
- Find the new template
- Copy her work into the new template
- Re-do formatting
- Send back to legal

#### Tuesday 10:00 AM - Version Control Nightmare

Legal approves v2. Sarah makes final edits.

**Current files on her computer**:
- Prospect_Proposal_v1.docx
- Prospect_Proposal_v2_legal.docx
- Prospect_Proposal_v2_legal_FINAL.docx
- Prospect_Proposal_v2_legal_FINAL_REALLY.docx

Which one is the actual final version? Sarah isn't sure.

#### Tuesday 3:00 PM - Sent!

Sarah sends the proposal. **Total time: 2 days, ~12 hours of work.**

#### Wednesday 9:00 AM - The Follow-Up

Prospect responds: "Can you add information about HIPAA compliance?"

Sarah realizes she forgot to include compliance info (it wasn't in her template).

She now needs to:
- Hunt for HIPAA compliance language
- Create a v3 of the proposal
- Send follow-up

**Additional time: 2 hours**

#### The Problems

❌ **Lost work**: Discovery notes lost when ChatGPT tab closed
❌ **No reuse**: Had to manually find and adapt old proposals
❌ **Scattered files**: 47 proposal files, no naming convention
❌ **Outdated templates**: Using old template caused rework
❌ **Version chaos**: 4+ versions of same file, unclear which is final
❌ **Missing content**: Forgot compliance info (not in checklist)
❌ **Wasted time**: 14 hours total for one proposal

---

### After Nexus: Load Proposal-Builder Skill, Reuse Structure

#### Monday 9:00 AM - Discovery Call Complete

Sarah just finished the same discovery call. She opens Claude Code (her Nexus workspace).

**What Sarah does**:
```
Sarah: "Load proposal-builder skill for enterprise Healthcare prospect"
```

#### Monday 9:05 AM - Context Loaded Automatically

Claude loads:
- ✅ Sarah's goals (knows she's focused on enterprise healthcare)
- ✅ Latest proposal template (automatically uses current version)
- ✅ Pricing info (pulled from sales ops Airtable base)
- ✅ Healthcare case studies (from shared knowledge base)
- ✅ HIPAA compliance language (included in Healthcare template)

#### Monday 9:10 AM - Skill Guides Her Through

The `proposal-builder` skill asks Sarah structured questions:

**Skill**: "Let's build this proposal together. I need some info:"

1. **Client name**: [Sarah types: "HealthCo"]
2. **Industry**: Healthcare SaaS (auto-detected from call notes)
3. **Key pain points** (from discovery):
   - Manual patient data entry
   - Compliance reporting overhead
   - Staff burnout
4. **Proposed solution**: AI agent for patient intake automation
5. **Timeline**: 3-month POC
6. **Decision makers**: CTO, Head of Compliance

**Time spent**: 5 minutes answering questions

#### Monday 9:15 AM - Proposal Generated

The skill generates:
- ✅ Customized proposal with HealthCo's name throughout
- ✅ Problem statement matching their pain points
- ✅ Healthcare case studies auto-inserted
- ✅ HIPAA compliance section included
- ✅ Current pricing (pulled from Airtable)
- ✅ Timeline with milestones
- ✅ Next steps section

**Sarah reviews**: 30 minutes (reading, minor tweaks)

#### Monday 9:45 AM - Legal Review (Streamlined)

Sarah sends to legal. Legal responds in 1 hour:

"Looks good! This is the current template. Approved."

(No rework needed because skill used current template)

#### Monday 11:00 AM - Sent!

Sarah sends the proposal. **Total time: 2 hours.**

#### Monday 2:00 PM - Prospect Responds

Prospect: "This is exactly what we need! Can we schedule a demo?"

Sarah celebrates. The proposal included all necessary info (HIPAA compliance, case studies, pricing) from the start.

**Follow-up time: 0 hours (no missing content)**

#### The Transformation

✅ **Memory works**: Discovery notes saved in Nexus, never lost
✅ **Template reuse**: Skill uses current template automatically
✅ **Organized files**: Proposal saved in `02-projects/healthco-proposal/04-outputs/`
✅ **Version control**: One source of truth, no "FINAL_FINAL" files
✅ **Complete content**: Skill includes compliance checklist (nothing forgotten)
✅ **Time saved**: 14 hours → 2 hours (85% faster)

#### Sarah's Next Prospect

**Prospect #2** (next week): Enterprise FinTech company

Sarah: "Load proposal-builder skill for enterprise FinTech prospect"

**Time**: 1.5 hours (faster because skill is refined from HealthCo usage)

**Pattern**: Second time is faster than first. Tenth time is nearly automatic.

---

## Solutions Team Example: Client Implementation Tracking

### Scenario Overview

**Character**: Marcus, Solutions Engineer at AI Agent Company
**Current load**: Managing 3 concurrent client projects (Client A, B, C)
**Challenge**: Keep all 3 projects on track without dropping balls

---

### Before Nexus: Scattered Docs, Manual Status Updates, Lost Work

#### Week 1 - Context Switching Chaos

Marcus starts his week trying to remember where each project stands.

**Client A** (Week 8 of implementation):
- Where are the test results? (Checks email, Slack, Google Drive)
- What tasks are blocked? (Has to re-read Notion board)
- Did client send API docs? (Searches inbox for 10 minutes)

**Client B** (Week 3 of implementation):
- What was decided in last week's meeting? (Notes are in personal Google Doc)
- Opens Google Doc: "Meeting notes - ClientB_3_15" (which meeting was this?)
- Realizes he took notes in ChatGPT, not Google Doc
- ChatGPT conversation is gone (context limit reached)

**Client C** (Week 1 - just starting):
- Needs to create project plan
- Copies Client A's project plan
- Manually updates all client names, dates, milestones
- Takes 3 hours

**Morning spent**: 4 hours just context switching and finding info

#### Week 2 - Manual Status Update Hell

It's Monday. Marcus needs to send weekly status updates to all 3 clients.

**Client A status update**:
- Manually checks Linear for completed tasks (23 tasks this week)
- Manually summarizes each task in email
- Pulls test results from Airtable (copy-paste into email)
- Formats email to look professional
- **Time**: 90 minutes

**Client B status update**:
- Repeats same process
- **Time**: 90 minutes

**Client C status update**:
- Repeats same process
- **Time**: 60 minutes (fewer tasks, still ramp-up phase)

**Total**: 4 hours/week on status updates alone

#### Week 4 - The Dropped Ball

Marcus gets a Slack message from Client A:

> "We didn't receive the test results you mentioned last week. Is everything okay?"

Marcus panics. He forgot to send the results.

**Root cause**: No system to track deliverables across 3 projects.

Marcus scrambles:
- Finds test results in Airtable
- Formats report manually
- Apologizes to client for delay
- **Time wasted**: 2 hours + damaged client trust

#### Week 8 - Knowledge Loss Incident

Marcus's colleague (who helped with Client B discovery) leaves the company.

**What's lost**:
- Discovery session notes (were in colleague's personal Notion)
- Client's edge case examples (were in colleague's head)
- Detailed API integration requirements (were in verbal conversations)

Marcus now needs to:
- Re-interview client for missing requirements
- Rebuild edge case list
- **Time wasted**: 8 hours + client frustration ("Didn't we already cover this?")

#### Week 12 - The Overwhelm

Marcus is burning out.

**Current state**:
- Working 60+ hours/week
- Constantly context switching
- Missing deliverables
- Client satisfaction dropping
- No bandwidth for new clients

**Team capacity**: 3 clients/year per SE (could be 6 with better tools)

#### The Problems

❌ **Lost work**: ChatGPT notes disappear, colleague's knowledge gone
❌ **No reuse**: Manually rebuilding project plans for each client
❌ **Scattered docs**: Project info in 5+ tools (Notion, Linear, Airtable, Drive, Email)
❌ **Manual updates**: 4 hours/week on status reports
❌ **Dropped deliverables**: No system to track what's due
❌ **Slow onboarding**: New SEs take 8 weeks to ramp up
❌ **Team capacity**: 3 clients/year max per SE

---

### After Nexus: 7-Phase Skills Library, Automated Dashboards, Project Templates

#### Week 1 - Structured Project Setup

Marcus starts Client C implementation. He opens Nexus:

```
Marcus: "Create new project for Client C implementation using client-implementation template"
```

**Nexus loads**:
- ✅ 7-phase project structure (Pre-Contract → Maintenance)
- ✅ All standard tasks pre-populated in steps.md
- ✅ Timeline template with milestones
- ✅ Checklist for each phase (nothing forgotten)

**Time**: 30 minutes (vs 3 hours manually)

#### Week 2 - Automated Weekly Status Updates

Monday morning. Marcus needs status updates for all 3 clients.

```
Marcus: "Generate weekly status updates for all in-progress projects"
```

**Nexus `weekly-status-update` skill**:
1. Pulls completed tasks from Linear (all 3 projects)
2. Pulls test results from Airtable (all 3 projects)
3. Formats professional status reports (customized per client)
4. Generates 3 separate emails

**Marcus reviews**: 15 minutes (quick scan of all 3 reports)

**Time**: 15 minutes total (vs 4 hours manually)
**Savings**: 3 hours 45 minutes every week

#### Week 4 - No Dropped Deliverables

Marcus runs daily check:

```
Marcus: "Show me all overdue deliverables across projects"
```

**Nexus shows**:
- Client A: Test results due today (not yet sent)
- Client B: API docs needed by Thursday
- Client C: Kickoff slides due Friday

Marcus immediately sends Client A test results (no dropped ball).

**Deliverable tracking**: Automated (nothing falls through cracks)

#### Week 8 - Knowledge Captured, Not Lost

A colleague who helped with Client B leaves the company.

**What happens in Nexus**:
- ✅ Discovery notes: Saved in `02-projects/client-b/02-resources/`
- ✅ Edge cases: Documented in `requirements.md`
- ✅ API details: Captured in `api-integration-notes.md`

**Impact of departure**: **Zero**. All knowledge is in project files.

Marcus continues Client B work without missing a beat.

#### Week 10 - Reusing Skills for Client D

Marcus gets assigned Client D (4th concurrent project).

**Before**: Would be overwhelmed, capacity maxed at 3 clients
**With Nexus**: Uses Skills library built from Clients A, B, C

```
Marcus: "Create new project for Client D using refined client-implementation template"
```

**Nexus loads**:
- ✅ Template refined from 3 previous clients
- ✅ Skills already built (feasibility assessment, scope definition, testing, etc.)
- ✅ Best practices captured from previous projects
- ✅ Common pitfalls flagged automatically

**Setup time**: 20 minutes (vs 30 min for Client C, vs 3 hours manual)

**Pattern**: Each client is faster than the last

#### Week 12 - Sustainable Workload

Marcus's current state:

**Managing**:
- 4 concurrent clients (vs 3 before)
- All projects on track
- No dropped deliverables
- High client satisfaction

**Working hours**: 45 hours/week (vs 60+ before)

**Team capacity**: 6-8 clients/year per SE (was 3/year)

#### The Transformation

✅ **Memory works**: All discovery notes, requirements, decisions saved
✅ **Template reuse**: Project D setup: 20 min (was 3 hours)
✅ **Organized docs**: All project info in one place (`02-projects/client-X/`)
✅ **Automated updates**: 15 min/week (was 4 hours/week)
✅ **No dropped deliverables**: Automated tracking catches everything
✅ **Knowledge captured**: Colleague leaves, zero knowledge loss
✅ **Team capacity**: 6-8 clients/year (was 3/year) = **2x capacity**

---

## Universal Example: Projects as Templates

### The Power of "Create Once, Use Many Times"

This pattern applies to **both** Sales and Solutions teams.

---

### Visual: Template Reuse Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT A (First Time)                        │
├─────────────────────────────────────────────────────────────────┤
│  Build from scratch:                                            │
│    • Create project structure                                   │
│    • Define all tasks                                           │
│    • Build workflows                                            │
│    • Document processes                                         │
│                                                                 │
│  Time: 12 weeks (full manual effort)                           │
│  Learning: Discover what works, what doesn't                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Extract & Template
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT B (First Reuse)                       │
├─────────────────────────────────────────────────────────────────┤
│  Clone Client A project:                                        │
│    • Project structure already defined                          │
│    • Standard tasks pre-populated                               │
│    • Workflows ready to customize                               │
│    • Processes documented                                       │
│                                                                 │
│  Time: 8 weeks (40% faster)                                    │
│  Learning: Refine template, add missing pieces                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Refine Template
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT C (Second Reuse)                      │
├─────────────────────────────────────────────────────────────────┤
│  Clone refined template:                                        │
│    • Best practices from A + B incorporated                     │
│    • Edge cases already handled                                 │
│    • Optimized workflows                                        │
│    • Complete documentation                                     │
│                                                                 │
│  Time: 6 weeks (50% faster than original)                      │
│  Template: Now mature, covers 90% of use cases                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Mature Template
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              CLIENTS D, E, F... (Stable State)                  │
├─────────────────────────────────────────────────────────────────┤
│  Clone mature template:                                         │
│    • 90% of work pre-built                                     │
│    • Only customization needed                                  │
│    • Proven workflows                                           │
│    • Full institutional knowledge                               │
│                                                                 │
│  Time: 6 weeks consistently (stable efficiency)                │
│  Value: Compound returns on initial investment                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Sandbox Pattern: Same Structure, Different Experiments

**Use case**: Testing different approaches without breaking production

**Example - Solutions Team**:

Marcus wants to test a new testing framework for Client implementations.

**With Nexus**:
1. Clone Client A project → "Client A - Testing Framework Experiment"
2. Try new framework in sandbox project
3. If it works better: Update main Client A project + template
4. If it doesn't: Delete sandbox, no harm done

**Key benefit**: Safe experimentation without risking production work

**Example - Sales Team**:

Sarah wants to test a new proposal format for enterprise clients.

**With Nexus**:
1. Clone enterprise-proposal template → "enterprise-proposal-v2-experiment"
2. Try new format with next 2 prospects
3. If conversion rate improves: Make it the new template
4. If not: Revert to original

**Key benefit**: A/B test workflows in real work, keep what works

---

### Team Collaboration Flow: Skills Shared Across Team

**The Multiplier Effect**

```
┌────────────────────────────────────────────────────────────────┐
│                   TEAM MEMBER 1 (Builder)                      │
├────────────────────────────────────────────────────────────────┤
│  Builds "Client Proposal" skill for their work                 │
│  Saves to: 03-skills/client-proposal-builder/                 │
│  Time invested: 4 hours to build skill                        │
└────────────────────────────────────────────────────────────────┘
                              │
                              │ Share with Team
                              ▼
┌────────────────────────────────────────────────────────────────┐
│              TEAM MEMBERS 2, 3, 4, 5 (Users)                   │
├────────────────────────────────────────────────────────────────┤
│  Load "Client Proposal" skill for their work                   │
│  Time per person: 30 min to learn + use                       │
│  Combined time saved: 4 × 3.5 hours = 14 hours                │
└────────────────────────────────────────────────────────────────┘
                              │
                              │ Improvements
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                    TEAM IMPROVEMENT CYCLE                      │
├────────────────────────────────────────────────────────────────┤
│  Member 3 suggests: "Add compliance section to template"      │
│  Member 1 updates skill (15 min)                              │
│  Everyone benefits from improvement                            │
│  Skill gets better over time                                   │
└────────────────────────────────────────────────────────────────┘
```

**ROI Calculation**:
- 1 person builds (4 hours)
- 4 people benefit (14 hours saved)
- **Team ROI**: 250% return on investment
- **Ongoing**: Every new team member benefits (infinite ROI)

---

## Key Takeaways

### For Sales Team

**Before**: 14 hours per proposal, scattered files, inconsistent quality
**After**: 2 hours per proposal, organized structure, consistent best practices

**Bottom line**: **85% time savings** per proposal

**Multiplier**: Share proposal-builder skill with team → Everyone faster

---

### For Solutions Team

**Before**: 3 clients/year max, 60+ hour weeks, knowledge loss when people leave
**After**: 6-8 clients/year, 45 hour weeks, zero knowledge loss

**Bottom line**: **2x team capacity** with same headcount

**Multiplier**: Skills library compounds → 10th client is 10x easier than 1st

---

### Universal Benefits

✅ **Memory**: Never lose work again (everything saved)
✅ **Reuse**: Build once, use forever (templates + skills)
✅ **Sharing**: One person builds, entire team benefits
✅ **Compound**: Work gets faster over time (not linear)
✅ **Institutional**: Knowledge survives team changes

---

**End of Example Scenarios Document**

**Version**: 1.0
**Last Updated**: 2025-11-25
**Next Review**: After first workshop delivery

**Usage**: Reference these scenarios in Slides 8-9 and throughout facilitator talking points to make benefits concrete and relatable.
