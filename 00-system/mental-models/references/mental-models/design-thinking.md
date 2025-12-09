---
name: "Design Thinking"
tier: 2
description: "User-centered iterative problem solving through empathy and rapid prototyping. Load for Build/Content/Process projects with Medium/Complex complexity when facing unclear user needs, innovation challenges, or requiring rapid validation through iteration."
applies_to: ["Build", "Content", "Process"]
complexity: ["Medium", "Complex"]
---

# Design Thinking

## Purpose
Human-centered approach to innovation that integrates user needs, technology possibilities, and business requirements through iterative cycles.

## The 5 Phases

### 1. Empathize
**Goal:** Understand user needs through observation and engagement

**Questions to Ask:**
- Who are the users and what are their pain points?
- What frustrations do they experience with current solutions?
- What unmet needs exist that users may not articulate?
- What context surrounds their use of this solution?
- What emotional states do users experience?

**Activities:**
- User interviews
- Contextual observation
- Journey mapping
- Pain point identification
- Empathy mapping

---

### 2. Define
**Goal:** Frame the core problem from the user's perspective

**Questions to Ask:**
- What is the real problem we're solving (not the symptom)?
- How might we reframe this problem statement?
- What user needs emerged from empathy research?
- What insights did we gain about user behavior?
- What patterns emerged from user research?

**Output:** Point-of-view statement
```
[User] needs [need] because [insight]
```

**Example:**
```
Sales reps need faster lead qualification because 30-minute manual reviews prevent them from focusing on high-value relationships.
```

---

### 3. Ideate
**Goal:** Generate diverse solutions without judgment

**Questions to Ask:**
- How might we solve this problem?
- What would this look like if we removed all constraints?
- What ideas from other domains could we adapt?
- What's the wildest possible solution?
- How would [person/company] approach this?

**Techniques:**
- Brainstorming (quantity over quality)
- SCAMPER (Substitute, Combine, Adapt, Modify, Put to use, Eliminate, Reverse)
- Analogous inspiration (how do other industries solve this?)
- Worst possible idea (then invert it)
- Sketching and rapid visualization

**Rules:**
- Defer judgment (no criticism during ideation)
- Encourage wild ideas
- Build on others' ideas
- Stay focused on topic
- One conversation at a time

---

### 4. Prototype
**Goal:** Build quick, low-fidelity versions to test ideas

**Questions to Ask:**
- What's the fastest way to test this assumption?
- What's the minimum we need to build to learn?
- What hypothesis are we testing?
- What feedback are we seeking?
- How can we fail fast and cheap?

**Types of Prototypes:**
- Paper prototypes (sketches, mockups)
- Wireframes (digital layouts)
- Role-playing (act out the experience)
- Storyboards (visual narrative)
- Clickable mockups
- Minimum Viable Product (MVP)

**Key Principle:** Low fidelity = low commitment = more learning

---

### 5. Test
**Goal:** Gather feedback and iterate

**Questions to Ask:**
- What did we learn that changes our approach?
- Which assumptions were validated? Which were wrong?
- What unexpected insights emerged?
- What should we iterate on next?
- What new questions arose from testing?

**Activities:**
- User testing sessions
- Observation (watch users interact)
- Feedback interviews
- A/B testing
- Analytics review
- Iteration planning

**Critical:** Be prepared to go back to any previous phase based on learnings!

---

## Non-Linear Process

Design Thinking is intentionally iterative:

```
Empathize → Define → Ideate → Prototype → Test
    ↑                                        ↓
    └────────── Learn and iterate ──────────┘
```

You might:
- Test prototype → Learn new user need → Go back to Empathize
- Define problem → Realize you need more empathy research
- Ideate → Discover wrong problem definition

---

## Example Application

**Project:** Lead Qualification Workflow

**Empathize:**
- Interview 5 sales reps about current qualification process
- Shadow 3 reps during lead calls
- Pain point: "30 minutes per lead, can't scale"
- Insight: "We re-ask the same questions because data is scattered"

**Define:**
- POV: Sales reps need consolidated lead data and automated preliminary scoring because scattered information causes repeated research and slows qualification.

**Ideate:**
- Idea 1: AI analyzes LinkedIn + website + form data → preliminary score
- Idea 2: Chatbot pre-qualifies leads before sales contact
- Idea 3: Smart form that adapts questions based on responses
- Idea 4: Browser extension that surfaces lead data during calls
- Selected: Combine Ideas 1 + 4 for hybrid approach

**Prototype:**
- Week 1: Paper mockup of browser extension UI
- Week 2: Airtable form + simple GPT-4 scoring script
- Week 3: Chrome extension (non-functional) to test UX
- Week 4: Working MVP with 10 sample leads

**Test:**
- Test MVP with 2 sales reps for 1 week
- Feedback: "AI score helpful but doesn't explain reasoning"
- Iteration: Add "reasoning" field to AI output
- Re-test: "Much better - now I trust the scores"

**Result:** Ship v1.0 with explanation feature based on user feedback

---

## When to Use

**Best For:**
- ✅ User-facing products or services
- ✅ Problems requiring innovation
- ✅ Situations where user needs are unclear
- ✅ Projects with high uncertainty
- ✅ Cross-functional collaboration
- ✅ Building MVPs

**Not Ideal For:**
- ❌ Well-defined technical problems
- ❌ Pure backend architecture (no users)
- ❌ Time-critical emergencies
- ❌ Situations with no user involvement possible

**Combines Well With:**
- **MVP Thinking** - Align prototype phase with MVP principles
- **Jobs to Be Done** - User needs analysis before empathy
- **Stakeholder Mapping** - Identify all affected parties
- **Prototyping** - Core to Design Thinking methodology

---

**Remember:** Design Thinking is iterative - expect to cycle through phases multiple times as you learn!
