# Workshop Quick Start Guide - Your 30-Day Transformation

**Purpose**: Action-oriented guide for workshop participants to execute their Nexus transformation
**Audience**: Solutions Engineers who just completed the 90-minute workshop
**Timeline**: 30 days from workshop → measurable 2x capacity impact

---

## 🎯 WORKSHOP RECAP - What You Just Learned

You completed the 90-minute Nexus Product Introduction Workshop. Here's what you have now:

✅ **Nexus workspace set up** (5-folder system: system, memory, projects, skills, workspace)
✅ **goals.md created** with your current client context
✅ **roadmap.md created** with 4 milestones
✅ **1-3 Skills identified** from your actual work (time savings estimated)
✅ **Understanding achieved**: Projects vs Skills, 4-folder pattern, team multiplier vision

---

## 📋 YOUR 30-DAY ROADMAP - Week by Week

### WEEK 1: ORGANIZE YOUR CLIENT LIFECYCLE (Foundation)

**Goal**: Get your current client fully organized in Nexus using the phase-based project model

**Why Phase-Based Projects?**
- 1 client = 7 separate phase projects (not 1 monolithic project)
- Each phase is a reusable template for next client
- Clone entire lifecycle for Client #2 → 70% head start!

**What to Do**:

#### Day 1-2: Import Your Current Client Work
```
04-workspace/
└── input/
    └── current-client-[name]/
        ├── requirements/
        ├── discovery-notes/
        ├── test-results/
        ├── email-templates/
        └── deliverables/
```

Copy ALL files related to your current client into `input/` folder. Don't organize yet - just gather everything.

**Where to find files**:
- Desktop (scattered notes, drafts)
- Downloads (PDFs, specs, diagrams)
- Email (saved attachments)
- Linear (exported notes)
- Notion (client docs)

---

#### Day 3-4: Organize Into Phase Projects

**Create 7 phase projects** for your client:

```
02-projects/
├── [client]-phase-1-pre-contract/
│   ├── 01-planning/    # Lead qualification, SE sign-off
│   ├── 02-resources/   # Sales notes, requirements
│   ├── 03-working/     # Feasibility assessment
│   └── 04-outputs/     # GO/NO-GO decision, scope doc
│
├── [client]-phase-2-project-setup/
│   ├── 01-planning/    # Kickoff agenda, roadmap
│   ├── 02-resources/   # Client context
│   ├── 03-working/     # Notion/Linear setup
│   └── 04-outputs/     # Kickoff deck
│
├── [client]-phase-3-discovery/
│   ├── 01-planning/    # Discovery session guide
│   ├── 02-resources/   # API docs, workflow diagrams
│   ├── 03-working/     # Deep dive notes
│   └── 04-outputs/     # Scope document, test cases
│
├── [client]-phase-4-build/
│   ├── 01-planning/    # Build roadmap
│   ├── 02-resources/   # Code libraries, integration docs
│   ├── 03-working/     # Agent code, configs
│   └── 04-outputs/     # Working agent
│
├── [client]-phase-5-testing/
│   ├── 01-planning/    # Test plan
│   ├── 02-resources/   # Test case templates
│   ├── 03-working/     # Airtable evals, test runs
│   └── 04-outputs/     # Test reports
│
├── [client]-phase-6-go-live/
│   ├── 01-planning/    # Go-live checklist
│   ├── 02-resources/   # Runbooks, user guides
│   ├── 03-working/     # Production config
│   └── 04-outputs/     # Launch report
│
└── [client]-phase-7-maintenance/
    ├── 01-planning/    # Maintenance schedule
    ├── 02-resources/   # Runbooks, escalation paths
    ├── 03-working/     # Incident logs
    └── 04-outputs/     # Performance reports
```

**How to organize** (ask AI during session):
> "Help me organize my imported files into phase projects for [client-name]"

AI will:
1. Analyze your imported files
2. Detect which phase each file belongs to
3. Move files into appropriate phase project folders
4. Generate missing artifacts (scope docs, checklists, etc.)

---

#### Day 5: Experience Instant Context

**Test the power of Nexus**:

**Morning**:
1. Work on your client (add notes, update test results, edit docs)
2. At end of session: `close-session`
   - AI saves session report
   - All work organized
   - Context preserved

**Afternoon**:
1. Reload Nexus (new session)
2. Say: "continue [client-name]"
3. AI instantly knows:
   - Where you left off
   - What you were working on
   - What needs to be done next
   - Where every file lives

**Result**: Zero time hunting for files, zero "what was I doing?" moments

---

#### Week 1 Success Metrics
- ✅ All current client work organized into 7 phase projects
- ✅ Experience instant context switching (close-session → reload → continue)
- ✅ Zero "where did I put that?" moments
- ✅ AI knows your complete client context

---

### WEEK 2-3: BUILD YOUR FIRST SKILLS (The Multiplier Kicks In)

**Goal**: Build 2-3 Skills from your most painful repetitive tasks

**Why Skills?**
- Your best process → shared with team → everyone faster
- Client #1 pain → Client #2 automation
- "10 people automating each other's work" - Dorian

---

#### Day 8-10: Pick Your First Skill (Highest ROI)

**Use the Skills Ideas Catalog** ([skills-ideas-catalog.md](skills-ideas-catalog.md)) to pick from Quick Wins:

**Option 1: Weekly Client Update Automation** ⭐ **HIGHEST ROI**
- **Pain**: Manual status emails every Friday take 4 hours
- **Time Savings**: 4 hours → 30 minutes (87.5% reduction)
- **Best for**: If you spend Friday afternoons compiling updates from Linear, Airtable, email, Slack

**Option 2: Test Report Generation** ⭐ **HIGH ROI**
- **Pain**: Manual test report creation from Airtable eval data takes 3 hours
- **Time Savings**: 3 hours → 20 minutes (89% reduction)
- **Best for**: If you have Airtable evals and manually create PowerPoint reports

**Option 3: Prompt Engineering Templates** ⭐ **CONSISTENCY BOOST**
- **Pain**: "Incorrect prompts → variable results" (Fahad's workshop quote)
- **Time Savings**: Not about time - about consistent quality
- **Best for**: If you iterate on prompts multiple times to get desired output

**Option 4: Pre-Contract Assessment Checklist** ⭐ **DISASTER PREVENTION**
- **Pain**: "Kickoff Nov 1st, docs arrive Nov 20th → 20 days lost" (Hassan's workshop quote)
- **Time Savings**: 20+ days lost → 0 days lost
- **Best for**: If you've experienced late document arrivals or surprise scope gaps

**Option 5: API Documentation Gatherer** ⭐ **DISCOVERY SPEEDUP**
- **Pain**: "Integration takes time... 40% of discovery is integration R&D" (Jack's workshop quote)
- **Time Savings**: 40% of discovery → 10-15% of discovery
- **Best for**: If you spend days researching API integrations during discovery

---

#### Day 11-15: Build Your First Skill

**Step-by-step process**:

1. **Say to AI**: "Create a skill for [workflow name]"
   - Example: "Create a skill for weekly client update automation"

2. **AI will ask**:
   - What are the inputs? (Linear board ID, client name, week ending date)
   - What are the outputs? (Email template, metrics summary)
   - What's the process? (Fetch tasks, generate email, save to outputs)
   - What integrations needed? (Linear, Airtable, Gmail)

3. **AI creates**:
   ```
   03-skills/
   └── weekly-client-update/
       ├── SKILL.md           # Main Skill definition
       ├── references/
       │   └── email-template.md
       └── scripts/
           └── fetch-linear-tasks.py
   ```

4. **Test on current client**:
   - Run the Skill: "Run weekly client update for [client-name]"
   - Review output: Check generated email
   - Iterate: "Update email template to include [X]"

5. **Measure time savings**:
   - Old way: 4 hours (manual compilation)
   - New way: 30 minutes (Skill + review)
   - **Saved**: 3.5 hours this week

---

#### Day 16-20: Build Skills #2 and #3

Repeat the process for 2 more Skills from your pain points.

**Prioritize by**:
1. **Frequency**: How often do you do this task? (daily, weekly, every client)
2. **Pain**: How painful is it? (hours spent, frustration level)
3. **Team reuse**: Would teammates use this Skill?

**Example combinations** (based on workshop participants):

**Hassan's Stack** (Scope + Migration focus):
1. Pre-Contract Assessment (prevent 20-day gaps)
2. Production Migration (staging → production automation)
3. Out-of-Scope Tracker (scope creep communication)

**Jack's Stack** (Discovery + Integration focus):
1. API Doc Gatherer (reduce 40% discovery time)
2. Integration Test Generator (validate integrations faster)
3. Discovery Deep Dive Guide (capture complete requirements)

**Fahad's Stack** (Consistency + Quality focus):
1. Prompt Engineering Templates (consistent results)
2. Code Review Checklist (quality standards)
3. Regression Detector (catch quality drops)

---

#### Week 2-3 Success Metrics
- ✅ 2-3 working Skills built from your actual pain points
- ✅ 80% time savings on those tasks (measured before/after)
- ✅ Skills tested on current client work
- ✅ Skills documented and ready to share

---

### WEEK 4: TEAM MULTIPLIER + CONTINUOUS AGGREGATION

**Goal**: Share Skills with team, start continuous library growth

---

#### Day 21-23: Share with Team

**Step 1: Package Your Skills**
1. Document what each Skill does
2. Add usage examples (how you used it on your client)
3. Include time savings metrics (before/after)

**Step 2: Demo to 1-2 Teammates**
- Show them how you use the Skill
- Let them test on their client work
- Collect feedback: "What would make this more useful?"

**Step 3: Iterate Based on Feedback**
- Update Skill based on teammate feedback
- Generalize for broader use cases
- Add to team Skills library

---

#### Day 24-26: Import Team Skills

**Ask teammates**:
> "What repetitive workflows have you automated?"

**Import their Skills** into your Nexus:
```
03-skills/
├── your-skills/
│   ├── weekly-client-update/
│   ├── test-report-generator/
│   └── prompt-templates/
│
└── team-skills/  (imported from teammates)
    ├── lead-qualification/  (from Sales Engineer)
    ├── kickoff-deck-generator/  (from Senior SE)
    └── incident-runbook/  (from DevOps SE)
```

**Result**: You now have 6+ Skills (yours + team's)

---

#### Day 27-30: Plan Continuous Aggregation

**Set up weekly reflection habit**:

Every Friday (or close-session):
1. **AI asks**: "What task did you do 2+ times this week?"
2. **You answer**: Examples from your work
3. **AI identifies**: Skill opportunities
4. **You decide**: Build now, backlog, or skip

**Track in**:
```
01-memory/
└── weekly-reflections/
    ├── 2025-11-29.md  (Week 1 reflection)
    ├── 2025-12-06.md  (Week 2 reflection)
    └── 2025-12-13.md  (Week 3 reflection)
```

**Skills backlog**:
```
03-skills/
└── backlog.md
    - Skill Idea #1: Automated demo script generator
    - Skill Idea #2: Client feedback summarizer
    - Skill Idea #3: Monthly metrics dashboard
```

**Result**: Continuous library growth (1-2 Skills/week)

---

#### Week 4 Success Metrics
- ✅ Skills shared with 1-2 teammates
- ✅ Feedback collected and Skills improved
- ✅ Team Skills imported into your library (6+ total Skills)
- ✅ Weekly reflection habit established
- ✅ Skills backlog started (ideas for Month 2)

---

## 📊 30-DAY ROI VALIDATION

**At end of Week 4, measure**:

### Time Savings
```
Weekly time saved from Skills:
- Skill #1: _____ hours/week
- Skill #2: _____ hours/week
- Skill #3: _____ hours/week
━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: _____ hours/week saved

Monthly impact:
_____ hours/week × 4 weeks = _____ hours/month
_____ hours/month ÷ 8 hrs/day = _____ days/month
```

**Example** (if you built Quick Wins):
- Weekly Client Update: 3.5 hrs/week
- Test Report: 2.5 hrs/week
- Pre-Contract Assessment: 1 incident prevented (20 days saved)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 6 hrs/week + 20 days disaster prevention

Monthly: 24 hours + 20 days = nearly 1 full month saved!

---

### Quality Improvements
- ✅ Zero "where did I put that?" moments (instant context)
- ✅ Consistent output quality (Prompt Templates)
- ✅ Fewer rework cycles (caught issues earlier)
- ✅ Better handoffs (team using same Skills)

---

### Team Impact
```
Your Skills shared with team:
- Teammate #1 using: [Skill names]
- Teammate #2 using: [Skill names]
- Time saved for team: _____ hours/week

Team Skills you imported:
- [Skill name] from [teammate]: _____ hours/week saved
- [Skill name] from [teammate]: _____ hours/week saved
```

---

### Client Lifecycle Progress
```
Current client organized in Nexus:
✅ Phase 1: Pre-Contract (complete)
✅ Phase 2: Project Setup (complete)
✅ Phase 3: Discovery (complete)
✅ Phase 4: Build (in progress)
□ Phase 5: Testing
□ Phase 6: Go Live
□ Phase 7: Maintenance

Skills built per phase:
- Phase 1: Pre-Contract Assessment
- Phase 3: API Doc Gatherer, Discovery Guide
- Phase 5: Test Report Generator
- Phase 6: (backlog: Production Migration)
- Phase 7: (backlog: Incident Runbook)

Coverage: 3 of 7 phases (43%)
Goal for Month 2: 7 of 7 phases (100%)
```

---

## 🚀 BEYOND 30 DAYS - Your Path to 2x Capacity

### Month 2: Complete Phase Coverage

**Goal**: Build Skills for ALL 7 phases (not just your pain points)

**Why?**
- Client #2 will be 50% faster if you have Skills for entire lifecycle
- Team can reuse your complete phase templates
- You become the "Skill library expert" on the team

**What to Build** (5-7 more Skills):
- Phase 1: Lead Qualification (if not built yet)
- Phase 2: Linear Project Setup, Kickoff Deck Generator
- Phase 4: Code Review Checklist, Integration Testing
- Phase 6: Production Migration, Go-Live Checklist
- Phase 7: Incident Runbook, Monitoring Dashboard

**Reference**: [skills-ideas-catalog.md](skills-ideas-catalog.md) (complete 20-Skill breakdown)

---

### Month 3: Client #2 Speedup

**Goal**: Start second client using Skills from first client, measure 50% speedup

**How**:
1. **Phase 1: Pre-Contract** (1-2 weeks → 3-5 days)
   - Use: Pre-Contract Assessment Skill
   - Clone: phase-1 template from Client #1
   - Result: 50% faster

2. **Phase 2: Project Setup** (1 week → 2-3 days)
   - Use: Linear Setup Skill, Kickoff Deck Generator
   - Clone: phase-2 template from Client #1
   - Result: 50-70% faster

3. **Phase 3: Discovery** (2-3 weeks → 1-1.5 weeks)
   - Use: API Doc Gatherer, Discovery Guide, Prompt Templates
   - Clone: phase-3 template from Client #1
   - Result: 40-50% faster

4. **Continue through all phases** using Skills library

**Track speedup**:
```
Client #1 Timeline (baseline):
- Phase 1: 2 weeks
- Phase 2: 1 week
- Phase 3: 3 weeks
- Phase 4: 6 weeks
- Phase 5: 2 weeks
- Phase 6: 1 week
- Phase 7: ongoing
━━━━━━━━━━━━━━━━
TOTAL: 15 weeks

Client #2 Timeline (with Skills):
- Phase 1: 4 days (75% faster)
- Phase 2: 2 days (80% faster)
- Phase 3: 1.5 weeks (50% faster)
- Phase 4: 4 weeks (33% faster)
- Phase 5: 1 week (50% faster)
- Phase 6: 3 days (60% faster)
- Phase 7: ongoing
━━━━━━━━━━━━━━━━
TOTAL: 8 weeks (47% faster!)

TIME SAVED: 7 weeks
```

**Result**: You just proved the path to 2x capacity!

---

### Month 4+: Exponential Growth

**Goal**: Continuous aggregation, team multiplier effect

**What happens**:
1. **Weekly library growth**: 1-2 new Skills/week (from you + team)
2. **Client #3 even faster**: 8 weeks → 6 weeks (using Client #2 learnings)
3. **Team library**: 50+ Skills (from 10 SEs aggregating)
4. **New SE onboarding**: 6 months → 2 weeks (using Skills library)

**Strategic impact**:
```
Individual SE:
- Old capacity: 3-4 clients/year
- New capacity: 6-8 clients/year (2x)

Team of 10 SEs:
- Old capacity: 30-40 clients/year
- New capacity: 60-80 clients/year (2x)

Revenue impact:
- Old revenue: $700K (3-4 clients × 10 SEs)
- New revenue: $1.4M (6-8 clients × 10 SEs)
- SAME TEAM SIZE!
```

---

## 🎯 COMMON QUESTIONS - Quick Reference

### Q: "I don't have time to build Skills during client work"

**A**: Start with 1 Skill that saves 3+ hours/week. You'll earn back the time investment in Week 1.

**Example**:
- Build Weekly Update Skill: 2 hours investment
- Saves: 3.5 hours/week
- Break even: After 1 use (Friday Week 2)
- ROI by Week 4: 14 hours saved (4 weeks × 3.5 hrs)

---

### Q: "My pain points don't match the catalog examples"

**A**: The catalog provides templates, not prescriptions. Ask AI to customize for YOUR workflow.

**Example**:
> "I need a Skill for [describe your pain point]"
> AI: "I'll create a custom Skill based on [similar catalog Skill]"

---

### Q: "What if my teammates don't want to share Skills?"

**A**: Start by USING their work, not asking them to build for you.

**Example**:
1. Notice teammate has good discovery checklist
2. Ask: "Can I copy your checklist for my client?"
3. Use it, improve it, share improvements back
4. Teammate sees value, starts using your Skills
5. Organic Skills library emerges

---

### Q: "How do I know if I'm building the RIGHT Skills?"

**A**: Build Skills for tasks you do 2+ times (or tasks that hurt most).

**Priority order**:
1. **Highest ROI**: Time savings >3 hours/week
2. **Most frequent**: Daily or weekly tasks
3. **Highest pain**: Tasks you dread or cause errors
4. **Team reuse**: Skills teammates would use too

---

### Q: "What if I fall behind on the 30-day plan?"

**A**: The plan is a guide, not a requirement. Adjust to YOUR pace.

**Flexible approach**:
- Week 1 slow? Extend to 2 weeks (still faster than no system)
- Stuck on Skill #2? Skip it, build Skill #3 instead
- Behind on schedule? Focus on Week 1 (organization) + 1 high-ROI Skill

**Remember**: Even 1 Skill saving 3 hrs/week = 12 hrs/month = 1.5 days/month saved!

---

## 📚 REFERENCE MATERIALS - Where to Find Help

### During Workshop (90 minutes):
- [final-presentation-solutions-version.md](final-presentation-solutions-version.md) - Slides you just saw
- [workshop-facilitator-guide.md](workshop-facilitator-guide.md) - Complete workshop playbook

### After Workshop (Week 1+):
- [skills-ideas-catalog.md](skills-ideas-catalog.md) - 20+ Skill ideas with implementation details
- [skills-library-catalog.md](skills-library-catalog.md) - Complete JTBD research (7-phase lifecycle)
- [workshop-context-system-overview.md](workshop-context-system-overview.md) - How workshop context system works

### MCP Integration Guides:
- Linear MCP: Linear project/issue management
- Airtable MCP: Evaluation data management
- Obsidian MCP: Knowledge base search
- Context7 MCP: Library documentation

---

## ✅ YOUR IMMEDIATE NEXT STEPS (Right After Workshop)

**Before you leave today**:
1. ✅ Import your current client work into `04-workspace/input/`
2. ✅ Read [IMPORT-INSTRUCTIONS.md](../input/IMPORT-INSTRUCTIONS.md) (if exists)
3. ✅ Bookmark this guide for Week 1

**Tomorrow (Day 1)**:
1. ✅ Start organizing imported work into phase projects
2. ✅ Ask AI: "Help me organize my imported files into phase projects for [client-name]"

**This Week (Week 1)**:
1. ✅ Complete client lifecycle organization (7 phase projects)
2. ✅ Experience instant context (close-session → reload → continue)
3. ✅ Identify 1-3 Skills to build in Week 2-3

**Next Week (Week 2)**:
1. ✅ Build your first Skill (pick from Quick Wins)
2. ✅ Test on current client work
3. ✅ Measure time savings

---

## 🎓 REMEMBER THE VISION

**Dorian's Workshop Quote**:
> "We essentially have 10 people to automate each other's work."

**Your transformation**:
- Week 1: Organized (filing cabinet for AI)
- Week 2-3: Automated (2-3 Skills saving 6+ hrs/week)
- Week 4: Multiplied (team using your Skills)
- Month 3: Exponential (Client #2 is 50% faster)

**This isn't just about YOU working faster.**
**This is about YOUR TEAM scaling exponentially.**

**Your best process → shared with team → everyone's work gets faster.**

---

**Ready? Start Week 1 today!**

**Questions?** Ask AI during your sessions or refer back to the reference materials above.

---

**Workshop Quick Start Guide** - v1.0
**Created**: 2025-11-25
**Purpose**: Action-oriented 30-day transformation plan for workshop participants
**Timeline**: Week 1 (Organization) → Week 2-3 (Skills) → Week 4 (Team Multiplier) → Month 2-3 (Exponential Growth)
