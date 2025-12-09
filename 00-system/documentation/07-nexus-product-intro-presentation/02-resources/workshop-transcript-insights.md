# Workshop Transcript Insights - Reusable Context

**Source**: Onboarding Workshop (Nexus 2) - November 20, 2024
**Recording**: https://fathom.video/share/Xw_oJ91uAGSxs3Wph1Z7sVRNky-gvssx
**Duration**: 155 minutes
**Participants**: Solutions Engineers team (Dorian, Anas, Muj, Sven, Hassan, Jack, Fahad, Safi, Kilian)

**Purpose**: Extract real language, pain points, and energy from actual Solutions Engineers to inform presentation materials and ensure authentic messaging.

---

## 1. REAL LANGUAGE PATTERNS (Use This Tone!)

### How Solutions Engineers Actually Talk

**Concrete, Direct, No Fluff**:
- "We need to see what is the deterministic path" - Anas
- "Just think of this as your filing cabinet. Each folder has a clear purpose." - Dorian
- "I personally intentionally left some stuff at the end" - Anas (honest, practical)
- "Let's not reinvent the wheel" - Anas (repeated 2x - important!)

**Problem Framing (Specific, Not Abstract)**:
- "47 proposal files" (Jack's real example - use this!)
- "Client provides information on the 20th of November, that's 20 days we lost" - Hassan
- "Every client = rebuild workflows from scratch" - Sven
- "We should have 10+ people to automate each other's work" - Dorian

**Excitement & Energy Markers**:
- "This is where the magic happens" - Dorian (use for Skills library)
- "I'm quite excited" - Anas (genuine enthusiasm)
- "Really, really cool. I'm making my way through the notes. Really, really awesome." - Kilian
- "We have a masterpiece in here" - Dorian

**Cautious Optimism (Not Overpromising)**:
- "Maybe we should..." (tentative suggestions)
- "I think..." (hedging appropriately)
- "Let's try to..." (action-oriented but realistic)

---

## 2. AUTHENTIC PAIN POINTS (Real Quotes from SEs)

### Pre-Contract Assessment Pain

**Hassan** (Critical Gap):
> "We need to differentiate between the kickoff date and when we're receiving the documents. For the client, kickoff is Nov 1st, they think POC is done in 3 months. But they provide info Nov 20th - that's 20 days we lost."

**Application**: Use this exact example in Slide 6 (Phase 1: Pre-Contract Assessment) to show why SE involvement early matters.

---

**Sven** (Feasibility Assessment):
> "We should always identify if this is a use case that we should take or not because some cases are just process automation and don't need agentic capabilities."

**Application**: "Lead Qualification Skill" should include agentic capability assessment, not just technical feasibility.

---

### Discovery & Scoping Pain

**Jack** (Integration Complexity):
> "Client asks for express POC with two integrations. Building agent is not a problem, but building the integration takes time to figure out due to platform limitations and lack of comprehensive documentation."

**Application**: Highlight in Phase 3 that API Documentation Gatherer Skill saves 40% of discovery time.

---

**Muj** (Reverse Planning Insight):
> "The idea of every phase is having prerequisites from the previous phase. Reverse approach: look at what you need in Phase 4, then plan Phase 3 to deliver those prerequisites."

**Application**: This is GENIUS - use this as the mental model for Skills library design. Each Skill outputs what the next phase needs as input.

---

**Fahad** (Prompt Quality):
> "Most of the difficulty we face is due to incorrect prompts. AI cannot understand the context and cannot work properly. We should enhance prompts to get consistent results every time."

**Application**: Solutions Engineers care about CONSISTENCY over speed. Emphasize "Senior-level quality every time" in ROI messaging.

---

### Build & Implement Pain

**Sven** (Scope Creep):
> "If you see additional features being requested, only implement if they are blocking the POC scope. Otherwise document as 'Out of scope' for now. Reinforce this with the client."

**Application**: "Out-of-Scope Tracker Skill" should auto-generate client communication templates, not just track internally.

---

**Hassan** (Data Transfer Hell):
> "Even if we want to go live, there's constant new requirements coming in. We need central repository for versioning. Client has staging environment and production environment - I create one agent for staging, now transfer all data to production where maybe only the API key changes."

**Application**: Phase 7 "Version Rollout Skill" should handle staging → production migrations automatically.

---

### Testing & Optimization Pain

**Dorian** (Reporting Gap):
> "Sending reports to clients on accuracy - I didn't hear this a lot from you guys, but I think this is something we should be doing more often."

**Application**: Phase 5 "Test Report Automation Skill" fills a gap the team isn't currently addressing but knows they should.

---

## 3. NEXUS SYSTEM INSIGHTS (Dorian's Explanation)

### The "Aha Moments" from Dorian's Demo

**Why Nexus Exists** (Dorian, 2:29:31):
> "With plain Claude Code, you generate thousands of documents all over the place. It doesn't know which, where to put documents, how to delete them, how to organize. It gets a mess extremely fast."

**Application**: Use this exact language in Slide 2 (Why This Opportunity Exists NOW) - "From Chaos to Clarity" section.

---

**Best Practice Pattern** (Dorian, 2:29:44):
> "Most people just say 'I want to do this' and let AI implement, but that will not get you best results. Best results come if you use AI to research and plan. Once your plan has been done well, you don't need to look at execution - AI will execute perfectly. I'm constantly planning with AI collaboratively, I'm not implementing anymore."

**Application**: This is the CORE METHODOLOGY. Add to Slide 7 (How It Works) - "Step 1: Plan (you lead), Step 2: Execute (AI leads), Step 3: Save (automatic)"

---

**Skills = Jobs to Be Done** (Dorian, 2:30:21):
> "Skills is essentially a job to be done. When we need to onboard a new client, we have a sequence of things we need to do: create Linear project, create Notion page, analyze transcripts from sales calls, get data from HubSpot. This is a job - convert it into a skill."

**Application**: Use "Jobs to Be Done" language in Slide 6 - connects directly to Solutions team's workshop vocabulary.

---

**The Sharing Vision** (Dorian, 2:30:44):
> "I can just give you the folder. You put it on your computer, and you also have the graph slicer. Now everybody can build their own skills and share with everybody else. We can build up a library very fast. We essentially have 10 people to automate each other's work."

**Application**: This is the TEAM MULTIPLIER message for Slide 9. Use exact phrasing: "10 people automating each other's work."

---

## 4. SPECIFIC EXAMPLES TO USE IN SLIDES

### Example 1: The "20 Days Lost" Story (Hassan)

**Scenario**: Client kickoff Nov 1st, documents arrive Nov 20th
**Current State**: Client expects 3-month POC timeline from Nov 1st
**Reality**: SE can't start until Nov 20th (20 days lost)
**Solution**: Pre-Contract Assessment Skill flags documentation requirements BEFORE kickoff date is set

**Use In**: Slide 6, Phase 1 example

---

### Example 2: The "Staging vs Production" Nightmare (Hassan)

**Scenario**: Built agent in staging environment, client reports "account not found"
**Root Cause**: Client was testing in production, not staging
**Current Manual Fix**: SE has to duplicate entire agent, change API keys, transfer all data
**Solution**: Version Rollout Skill handles environment migrations automatically

**Use In**: Slide 6, Phase 7 example or Slide 7 (Real JTBD Quotes)

---

### Example 3: The "Express POC with 2 Integrations" Trap (Jack)

**Scenario**: Sales closes deal for "express POC" with 2 integrations
**Current State**: "Building agent is not a problem, but integration takes time due to platform limitations and lack of docs"
**Time Lost**: 40% of discovery phase spent on integration R&D
**Solution**: API Documentation Gatherer Skill pre-loads common integration patterns

**Use In**: Slide 6, Phase 3 example

---

### Example 4: The "Reverse Planning" Insight (Muj)

**Mental Model**: "Look at Phase 4 requirements, then plan Phase 3 to deliver those prerequisites"
**Application**: Skills library should be designed with dependency mapping
**Example**: Phase 4 needs test cases → Phase 3 Skill must output structured test case templates

**Use In**: Slide 6 intro or Slide 7 (Real JTBD Quotes)

---

### Example 5: The "Out of Scope" Communication Gap (Sven)

**Scenario**: Client requests additional features mid-project
**Current Manual Process**: SE manually documents, emails client, logs in feature backlog
**Pain**: "Client can request additional functionality without context that this is an 'additional feature'"
**Solution**: Out-of-Scope Tracker Skill auto-generates client communication + logs to backlog + forwards to sales for upsell

**Use In**: Slide 6, Phase 4 example

---

## 5. TEAM ENERGY & CULTURE MARKERS

### What Motivates This Team

**Learning-Oriented**:
- "Really nice work" (Dorian, multiple times)
- "I love that" (Anas, responding to Muj's reverse planning)
- "Very good point" (Anas, validating Hassan's staging/production issue)

**Collaborative Problem-Solving**:
- "Let's do this quickly in the sense that..." (Anas, time-boxing)
- "Does anyone have questions?" (Anas, multiple check-ins)
- "Please just raise your hand and add to this" (Anas, inclusive)

**Pragmatic, Not Perfectionist**:
- "Let's not reinvent the wheel" (Anas, 2x)
- "We can use AI at the end of the day to construct the format" (Dorian, pragmatic shortcut)
- "Let's just focus on the problems and keep the how for later" (Anas, scope management)

**Time-Conscious**:
- "Let's be mindful of time" (Anas, 3x)
- "Running out of time" (multiple participants)
- "Four more minutes" (Anas, adding time when needed)

---

## 6. IMPLEMENTATION GUIDELINES FOR SLIDES

### Language Checklist - Use This Vocabulary

✅ **DO USE** (Resonates with SEs):
- "Skills library" (not "template library" or "workflow library")
- "Jobs to be done" (workshop vocabulary)
- "Deterministic path" (Anas's framing)
- "Prerequisites" (Muj's mental model)
- "Reverse planning" (Muj's insight)
- "10 people automating each other's work" (Dorian's vision)
- "Research and plan collaboratively" (Dorian's methodology)
- "Filing cabinet" metaphor (Dorian's explanation)
- "Masterpiece" (Dorian's excitement marker)

❌ **AVOID** (Doesn't match team language):
- "Workflow templates" (too generic)
- "Best practices" (overused, vague)
- "Productivity hacks" (too casual)
- "Game-changer" (marketing speak)
- "Revolutionary" (overpromising)

---

### Tone Calibration

**Balance Two Modes**:

1. **Facilitator Anas Mode** (Structured, Neutral, Inclusive):
   - "Let me actually go back..."
   - "Does that sound good?"
   - "If anyone has questions, please share them"
   - Use for: Workshop guide, facilitator scripts

2. **Visionary Dorian Mode** (Excited, Concrete, Demo-Focused):
   - "This is where the magic happens"
   - "Let me show you one example"
   - "This is what we're doing"
   - Use for: Slide content, demo moments, vision statements

---

## 7. SPECIFIC SLIDE APPLICATIONS

### Slide 1: The Breakthrough Opportunity
**Add Real Quote**:
> "We essentially have 10 people to automate each other's work." - Dorian

**Reframe Opportunity #4**:
From: "Client #10: Nearly automatic"
To: "Client #10: Nearly automatic (10 people automating each other)"

---

### Slide 2: Why This Opportunity Exists NOW
**Add Dorian's Insight to "From Chaos to Clarity" section**:
> "With plain Claude Code, you generate thousands of documents all over the place. Without a system, it gets a mess extremely fast. Nexus creates a map for AI so it knows what files are where."

---

### Slide 4: Your AI Partner That Actually Remembers You
**Update "My Superpowers (Growing)" section with real example from Fahad**:
```markdown
## My Superpowers (Growing)
✅ Deep dive discovery sessions (mastered)
✅ Consistent prompt engineering (confident)
🔄 API integration patterns (learning)
```

---

### Slide 6: Skills Library - The 7-Phase Lifecycle ROI
**Add Real Examples Under Each Phase**:

**Phase 1 Example** (Hassan's 20-day gap):
"WITHOUT: Kickoff Nov 1st, docs arrive Nov 20th → 20 days lost"
"WITH: Pre-Contract Assessment Skill → docs required BEFORE kickoff date set"

**Phase 3 Example** (Jack's integration pain):
"WITHOUT: 40% of discovery time spent on integration R&D"
"WITH: API Documentation Gatherer Skill → common patterns pre-loaded"

**Phase 7 Example** (Hassan's staging/production):
"WITHOUT: Manually duplicate agent, change API keys, transfer all data"
"WITH: Version Rollout Skill → automated environment migration"

---

### Slide 7: Real JTBD Quotes → Nexus Skills Mapping
**Add Muj's Reverse Planning Quote**:

```
QUOTE #6 (Mentioned by Muj)
"The idea of every phase is having prerequisites from the previous
 phase. Reverse approach: look at what you need in Phase 4, then
 plan Phase 3 to deliver it."

✅ SOLUTION: Dependency-Mapped Skills Architecture
   • Each Skill outputs prerequisites for next phase
   • Phase 3 Deep Dive Skill → structured test cases for Phase 5
   • Phase 5 Test Report Skill → sign-off criteria for Phase 6
```

---

### Slide 9: Your Transformation Journey
**Add Dorian's Planning Methodology to "YOUR WORK EXPERIENCE" section**:

```
Planning: From reactive implementation → Collaborative research & planning
Execution: From manual coding → AI executes your crystal-clear plan
Quality: From variable results → Consistent senior-level output every time
```

---

### Slide 10: Your 90-Day Transformation
**Update WEEK 3-4 section with Fahad's consistency focus**:

```
⚡ WEEK 3-4: YOUR FIRST SKILL (The Multiplier Unlocks)

Pick your biggest time sink:
💡 Inconsistent prompts? → Prompt Engineering Skill (variable → consistent)
💡 Weekly client updates? → Update Automation Skill (4 hours → 30 minutes)
💡 Test report generation? → Report Builder Skill (3 hours → 20 minutes)

Build it once → Get consistent results every time → Share with team!
```

---

## 8. METADATA FOR FUTURE REFERENCE

**Workshop Context**:
- **Team Size**: 8-10 Solutions Engineers
- **Experience Level**: Mix of senior (Dorian, Muj, Sven) and mid-level (Hassan, Jack, Fahad, Safi)
- **Workshop Format**: Collaborative Jobs-to-be-Done mapping exercise
- **Output**: 7-phase lifecycle with pain points and solution ideas at each phase
- **Follow-Up**: Scheduled next session to review solutions and assign skill owners

**Key Takeaways**:
1. Team values **concrete examples** over abstract concepts
2. Team language is **pragmatic, time-conscious, collaborative**
3. Team energy is **learning-oriented, not blame-oriented**
4. Team cares about **consistency and quality**, not just speed
5. Team already thinks in "Skills" vocabulary (Jobs to Be Done framework)

---

## 9. REUSABLE QUOTE LIBRARY

### Pain Point Quotes (Use Sparingly, For Credibility)

> "20 days lost because client provided docs late" - Hassan

> "Building agent is not a problem, but integration takes time" - Jack

> "Most difficulty we face is due to incorrect prompts" - Fahad

> "Every client = rebuild from scratch, no learning curve" - Sven

> "Staging vs production data transfer is manual nightmare" - Hassan

---

### Vision Quotes (Use for Inspiration)

> "10 people to automate each other's work" - Dorian

> "Research and plan collaboratively, then AI executes perfectly" - Dorian

> "Reverse planning: look at what Phase 4 needs, then build Phase 3 to deliver it" - Muj

> "Let's not reinvent the wheel - build on what we already have" - Anas

---

### Methodology Quotes (Use for "How It Works")

> "You don't need to look at execution anymore - you're only overseeing the planning" - Dorian

> "Prerequisites from previous phase - that's the mental model" - Muj

> "Define clear tickets and milestones by understanding what you need beforehand" - Muj

---

## 10. ANTI-PATTERNS (What NOT to Say)

Based on team language, **AVOID**:

❌ "We'll solve all your problems" (team is pragmatic, not utopian)
❌ "This is revolutionary" (team doesn't use hype language)
❌ "Never worry about X again" (team knows edge cases exist)
❌ "Guaranteed results" (team values honesty over promises)
❌ "One-size-fits-all solution" (team knows context matters)

**Instead, USE**:
✅ "This handles 80% of the common cases"
✅ "We can build on what already works"
✅ "Let's not reinvent the wheel"
✅ "Here's what we've seen work in practice"
✅ "Your mileage may vary, but here's the pattern"

---

## 11. NEXT STEPS FOR USING THIS CONTEXT

### When Creating New Materials

1. **Before writing slides**: Re-read sections 1-3 (Language Patterns, Pain Points, Nexus Insights)
2. **When stuck on messaging**: Check section 6 (Language Checklist) for approved vocabulary
3. **When needing examples**: Pull from section 4 (Specific Examples to Use)
4. **When checking tone**: Compare against section 7 (Tone Calibration)

### When Revising Existing Materials

1. **Find abstract language** → Replace with concrete examples from section 4
2. **Find marketing speak** → Replace with team vocabulary from section 6
3. **Find generic pain points** → Replace with real quotes from section 9
4. **Find overpromising** → Reframe using anti-patterns guide (section 10)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-25
**Source Workshop**: November 20, 2024
**Next Update**: After next Solutions team workshop or feedback session

**Usage Notes**:
- This document is a living resource - update after each workshop or team conversation
- Real quotes are gold - preserve exact wording and attribution
- Team language evolves - retire outdated vocabulary and add new patterns
- Examples should be anonymized if used in external materials, but keep raw internally for authenticity
