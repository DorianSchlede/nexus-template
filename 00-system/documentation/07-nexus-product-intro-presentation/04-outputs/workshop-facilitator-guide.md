# Workshop Facilitator Guide: Nexus Product Introduction

**Version**: 1.0
**Duration**: 90 minutes total
**Format**: Hybrid presentation + hands-on onboarding
**Audience**: Sales team + Solutions team (dual-audience)

---

## Section 1: Workshop Overview

### Workshop Objectives

**Primary Goal**: Enable both sales and solutions teams to understand how Nexus solves their specific problems and get hands-on experience with the system.

**By the end of this workshop, participants will**:
- ✅ Understand the 3 core problems Nexus solves (Lost Work, No Reuse, Can't Share)
- ✅ See how Nexus architecture works (5-folder system, memory, skills)
- ✅ Complete their own Nexus setup with goals, workspace, and memory
- ✅ Know how to create projects and skills for their actual work
- ✅ Have a working Nexus instance ready for daily use

**Audience A - Sales Team**:
- Currently: Manual proposal creation, scattered templates, inconsistent messaging
- After Workshop: Can create reusable proposal workflows, share best practices across team
- Key Value: Speed, consistency, team knowledge sharing

**Audience B - Solutions Team**:
- Currently: 12-21 weeks per client, manual work, rebuilding same things
- After Workshop: 7-phase Skills library, 6-10 weeks per client, 2x capacity
- Key Value: Reusability, institutional knowledge, efficiency

---

### Facilitator Role & Responsibilities

**Your role is to**:
- Guide, not lecture (minimize talking, maximize doing)
- Monitor both audiences for comprehension (sales may need simpler explanations)
- Manage timing strictly (90 min hard stop)
- Troubleshoot technical issues quickly (have backup facilitator)
- Celebrate small wins ("Great! Your memory is working!")

**You are NOT expected to**:
- ❌ Be a technical expert on Claude Code internals
- ❌ Debug complex MCP server issues during workshop
- ❌ Answer every "what if" scenario (defer to post-workshop 1:1s)

---

### Required Materials & Pre-Work

**Participant Pre-Work** (send 48 hours before):
- [ ] Install Claude Code (link: https://claude.com/claude-code)
- [ ] Verify Claude Code opens successfully
- [ ] Test connection: Can you chat with Claude in the terminal?
- [ ] Clone Nexus template repository (provide link)
- [ ] Test file access: Can Claude read files in your Nexus folder?

**Facilitator Pre-Work** (complete 24 hours before):
- [ ] Test all slides render correctly
- [ ] Dry run full workshop (time yourself)
- [ ] Prepare troubleshooting laptop (backup machine ready)
- [ ] Book backup facilitator for technical support
- [ ] Set up Zoom/Teams with screen share enabled
- [ ] Prepare "stuck" checklist (see Section 4)

**Materials Needed**:
- This facilitator guide (printed or second monitor)
- Workshop slides (final-presentation.md)
- Participant troubleshooting checklist (handout)
- Timer (visible to you, not participants)

---

## Section 2: Phase-by-Phase Timing Breakdown

**Total Duration**: 90 minutes

### Phase 1 - Foundation (30 minutes)
**Timing**: 0:00 - 0:30

**Activities**:
- Welcome & agenda overview (3 min)
- Present Slides 1-11 (20 min)
  - Slides 1-2: Problems (both audiences)
  - Slides 3-5: Architecture (memory + structure)
  - Slide 6: Skills & 7-phase lifecycle (Solutions team focus)
  - Slides 7-9: How it works + examples
  - Slides 10-11: Transition to hands-on
- Q&A checkpoint (5 min)
- Setup verification (2 min)

**Key Milestone**: Everyone has Claude Code open and Nexus folder loaded

**Check-in Question**: "Who can see their Nexus folder in Claude Code?" (show of hands)

---

### Phase 2 - Live Onboarding (55 minutes)
**Timing**: 0:30 - 1:25

**Activity**: Guided walk-through of Project 00: Define Goals

**Sub-phases**:
- **0:30-0:40** (10 min): Section 1 - Set up goals.md
  - Participants write their role, 3-month goal, long-term vision
  - Example prompts: "Help me define my role at [Company]"

- **0:40-0:50** (10 min): Section 2 - Create roadmap.md
  - Break 3-month goal into milestones
  - Example: "Turn my goal into 3 milestones with timelines"

- **0:50-1:00** (10 min): Section 3 - Understand workspace organization
  - Tour 5-folder system (00-system, 01-memory, etc.)
  - Explain boundaries (what AI manages vs what you control)

- **1:00-1:15** (15 min): Section 4 - Projects vs Skills decision framework
  - Walk through 4 real scenarios
  - Participants categorize: Project or Skill?
  - Discussion: Why did you choose that?

- **1:15-1:25** (10 min): Section 5 - Memory persistence demo
  - Everyone runs close-session skill
  - Restart Claude Code
  - Watch AI reload goals.md automatically
  - "Your AI now remembers you!" celebration moment

**Key Milestone**: Everyone completes Project 00 with goals + roadmap in place

**Check-in Question**: "Who saw their goals.md load automatically?" (hands up)

---

### Phase 3 - Wrap-Up (5 minutes)
**Timing**: 1:25 - 1:30

**Activities**:
- Recap what was built (2 min)
- Next steps & resources (2 min)
- Final Q&A (1 min)

**Next Steps to Share**:
1. Create your first real project (use create-project skill)
2. Extract a repeatable workflow into a skill (use create-skill skill)
3. Join #nexus-users Slack channel for support
4. Book 1:1 office hours if you get stuck

**Resources to Share**:
- Nexus documentation: [Link to internal docs]
- Troubleshooting guide: [Link to FAQ]
- Office hours signup: [Link to calendar]

---

## Section 3: Facilitator Talking Points

### Slides 1-2: Problem Framing (Both Audiences)

**Slide 1: The 3 Universal Problems**

**Talking Points**:
> "Before we dive into solutions, let's talk about the problems we all face with AI tools today. These affect both sales and solutions teams."

**Problem #1: Lost Work**
- Sales example: "You create a great proposal in ChatGPT, close the tab, it's gone forever."
- Solutions example: "You spend 4 hours mapping a client's process in Claude, next day you can't find it."
- Key insight: "AI has no memory. Every session starts from zero."

**Problem #2: No Reuse**
- Sales example: "You craft a perfect discovery questions template. Next prospect? Start over."
- Solutions example: "You build Client A's onboarding flow. Client B needs similar? Rebuild from scratch."
- Key insight: "No way to turn one-time work into reusable templates."

**Problem #3: Can't Share Knowledge**
- Sales example: "Top performer has amazing email templates. Rest of team? No access."
- Solutions example: "Lead consultant creates brilliant scoping workflow. Leaves company? Knowledge gone."
- Key insight: "Individual expertise doesn't become institutional knowledge."

**Audience Engagement**:
> "By show of hands: How many of you have lost work in ChatGPT/Claude because you closed the tab?" (wait for response)

**Transition to Slide 2**:
> "So why do these problems exist? Let's look at the root cause..."

---

**Slide 2: Why These Problems Exist**

**Talking Points**:
> "The problem isn't that AI is bad. The problem is structural."

**Web AI = Stateless (No Memory)**
- "Tools like ChatGPT and Claude.ai are designed to be stateless."
- "Every session is independent. No context carries over."
- Visual: Show diagram of Session 1 → Close → Session 2 (blank slate)

**Claude Code Alone = No Structure**
- "Claude Code solves memory (can read/write files), but doesn't give you organization."
- "You end up with files scattered everywhere, no naming conventions, no system."
- Sales analogy: "Like having Google Drive with no folders."
- Solutions analogy: "Like having GitHub with no repo structure."

**The Gap**:
> "You need TWO things to solve this: Memory (Claude Code) + Structure (Nexus). That's what we're building today."

**Transition to Slide 3**:
> "Let's look at how Nexus provides that structure..."

---

### Slides 3-5: Solution Architecture (Memory + Structure)

**Slide 3: The Nexus Solution - Architecture**

**Talking Points**:
> "Nexus is a 5-folder system that gives your AI work permanent structure."

**The 5 Folders** (walk through diagram):
1. **00-system**: Framework (AI's brain, pre-built skills)
   - You never touch this, it's like an operating system

2. **01-memory**: Your context (goals, roadmap, learnings)
   - This is what makes AI remember you

3. **02-projects**: Temporal work (beginning, middle, end)
   - Sales example: "Build proposal for Acme Corp"
   - Solutions example: "Client A implementation (setup → go-live)"

4. **03-skills**: Reusable workflows (run again and again)
   - Sales example: "Generate discovery questions skill"
   - Solutions example: "Run scoping interview skill"

5. **04-workspace**: Your files (totally custom, you control)
   - Whatever folder structure you want
   - AI doesn't manage this, you do

**Key Insight**:
> "Clear boundaries: AI manages 00-01-02-03, you manage 04. No chaos."

**Transition to Slide 4**:
> "Let's zoom in on the memory system, because that's what makes this work..."

---

**Slide 4: Solution #1 - Memory System**

**Talking Points**:
> "This is the magic that makes your AI remember you across sessions."

**Show code snippet** (goals.md example):
```markdown
## Current Role
Solutions Engineer at Beam.ai

## Short-Term Goal (3 months)
Build 10 client agentic workflows

## Long-Term Vision (1-3 years)
Become lead AI solutions architect
```

**Explain**:
> "You write this once. Every time you start Claude Code, it automatically loads this file. Your AI knows your context instantly."

**Demo Preview**:
> "In 30 minutes, you'll create YOUR version of this. Then we'll test it—close Claude, reopen, and watch it load automatically."

**Pause for questions**: "Any questions about how memory works?"

---

**Slide 5: Solution #2 - Project Structure**

**Talking Points**:
> "Projects are for temporal work—things with a beginning, middle, and end."

**The 4-Folder Pattern**:
```
05-my-project/
  ├── 01-planning/    (What are we building? Steps?)
  ├── 02-resources/   (Research, references, inputs)
  ├── 03-working/     (Drafts, work-in-progress)
  └── 04-outputs/     (Final deliverables)
```

**Sales Example**:
- Project: "Create proposal for Acme Corp"
- 01-planning: Discovery notes, proposal outline
- 02-resources: Acme's website, competitor analysis
- 03-working: Proposal draft v1, v2, v3
- 04-outputs: Final proposal PDF

**Solutions Example**:
- Project: "Client A Implementation"
- 01-planning: Timeline, tasks, milestones
- 02-resources: Client docs, process maps
- 03-working: Configuration files, test results
- 04-outputs: Deployment guide, handoff docs

**Key Insight**:
> "Same structure every time. No guessing where things go. AI knows how to navigate it."

**Transition to Slide 6**:
> "Now let's talk about Skills—this is especially powerful for Solutions team..."

---

### Slide 6: Skills with 7-Phase Lifecycle (Solutions Team Focus)

**Talking Points**:
> "Skills are reusable workflows. Build once, use many times. For Solutions team, this is game-changing."

**The Problem** (Solutions team):
- Current state: 12-21 weeks per client
- Manual work every time: scoping, setup, testing, deployment
- Rebuilding same workflows for every client

**The Solution** (7-Phase Skills Library):
> "Imagine having a library of pre-built workflows for every phase of your client lifecycle."

**Walk Through 7 Phases** (use diagram):
1. **Pre-Contract Assessment** (Skill: Lead qualification)
2. **Project Setup** (Skill: Client onboarding)
3. **Discovery & Scoping** (Skills: Process mapping, requirements gathering)
4. **Build & Implement** (Skill: Configuration automation)
5. **Testing & Optimization** (Skill: Test case generator)
6. **Go Live** (Skill: Deployment checklist)
7. **Maintenance** (Skills: Status reporting, issue tracking)

**The Impact**:
- Before: 12-21 weeks, fully manual
- After: 6-10 weeks, Skills library
- Result: **2x client capacity** (handle twice as many clients with same team)

**Real Quote** (from JTBD research):
> "Include solutions team early in discovery" → We built a Skill for that
> "Share timeline with action points" → We built a Skill for that
> "Gather detailed process information" → We built a Skill for that

**For Sales Team**:
> "Same concept applies to you. Build 'Generate Proposal' skill once, reuse for every prospect."

**Pause for questions**: "Questions about Skills?"

---

### Slides 7-9: How It Works + Examples

**Slide 7: How It Works - 3-Step Process**

**Talking Points**:
> "Let's walk through a typical Nexus session in 3 steps."

**Step 1: Load Context**
- You: "Continue project 05-client-A"
- AI loads: Project files, memory, relevant skills
- Takes 2 seconds

**Step 2: Work Together**
- You collaborate with AI on actual work
- AI suggests next steps based on tasks.md
- You guide, AI executes

**Step 3: Save Everything**
- You: "Done for today"
- AI runs close-session skill
- Saves progress, updates memory, creates session report
- Next session picks up exactly where you left off

**Key Insight**:
> "No manual 'where was I?' investigation. System tracks everything."

---

**Slide 8: Real Example - Projects as Templates**

**Talking Points**:
> "Let's see how this works in practice with real examples."

**Sales Example: Proposal Template Reuse**
- Create once: "Perfect proposal for SaaS companies"
- Reuse forever:
  - Prospect A: Clone template → Customize → Send
  - Prospect B: Clone template → Customize → Send
  - New hire joins: They get the template, instant best practices

**Solutions Example: Client Implementation Reuse**
- Client A: Build full implementation (12 weeks)
- Client B: Clone Client A project → 6 weeks (50% faster)
- Client C: Clone refined template → 4 weeks (67% faster)
- Pattern recognition: AI learns from each iteration

**Team Collaboration**:
- One person builds the Skill
- Entire team can use it
- Knowledge compounds (doesn't disappear when people leave)

**Transition to Slide 9**:
> "Let's see the before/after comparison..."

---

**Slide 9: Before vs After**

**Talking Points**:
> "Here's what changes when you use Nexus."

**Show Table**:

| Aspect | Before | After |
|--------|--------|-------|
| **Lost Work** | Every session starts from zero | Memory persists across sessions |
| **Reuse** | Rebuild same things repeatedly | Build once, reuse forever |
| **Knowledge Sharing** | Siloed in individuals' heads | Captured in Skills library |
| **Onboarding** | New hires start from scratch | New hires get proven templates |
| **Efficiency** | Linear (more work = more time) | Exponential (work gets faster) |

**Sales Team Before/After**:
- Before: 3 hours per proposal, inconsistent quality
- After: 45 min per proposal, consistent best practices

**Solutions Team Before/After**:
- Before: 12-21 weeks per client
- After: 6-10 weeks per client

**Key Insight**:
> "The second time is faster than the first. The third is faster than the second. Work compounds."

---

### Slides 10-11: Transition to Hands-On

**Slide 10: Workshop Preview - What We'll Build Together**

**Talking Points**:
> "Okay, enough slides. Let's build this together. In the next 55 minutes, you'll create your own Nexus workspace."

**What You'll Build**:
1. **goals.md** - Your role, 3-month goal, long-term vision
2. **roadmap.md** - Break goal into milestones with timeline
3. **Workspace understanding** - Tour the 5-folder system
4. **Decision framework** - When to use Projects vs Skills
5. **Memory test** - Watch your AI remember you automatically

**Sales Team Example Use Case**:
- After this workshop: Create "Client Proposal Workflow" skill
- Build once, use for every prospect
- Share with team

**Solutions Team Example Use Case**:
- After this workshop: Create "Client Implementation Tracking" project
- Use 7-phase structure for every client
- Build Skills library over time

**Timing Reminder**:
> "We have 55 minutes. Stay focused, follow along, ask questions if stuck."

---

**Slide 11: Ready to Start?**

**Talking Points**:
> "Any questions before we dive into hands-on work?"

**Call-to-Action**:
> "Open Claude Code. Make sure you can see your Nexus folder. Type in: 'Load orchestrator.md and start onboarding.' Let's go!"

**Setup Verification**:
- Walk around (if in-person) or check Zoom screens
- Ensure everyone has Claude Code open
- Ensure everyone can see their Nexus folder structure
- Address any technical issues NOW (before starting hands-on)

**Transition**:
> "Great! Everyone's ready. Let's build your memory system..."

---

## Section 4: Troubleshooting Scenarios

### Scenario 1: Claude Code Setup Issues

**Symptoms**:
- Participant can't install Claude Code
- Claude Code won't open
- Authentication errors

**Solutions**:
1. **Pre-workshop prevention** (best approach):
   - Send setup instructions 48 hours early
   - Test installation before workshop
   - Have troubleshooting session day before

2. **During workshop**:
   - Move participant to backup facilitator (1:1 troubleshooting)
   - Let rest of group continue
   - Participant rejoins when fixed

3. **Cannot fix during workshop**:
   - Participant observes this session
   - Schedule 1:1 makeup session later
   - Provide recording for review

**Prevention Tips**:
- Test on participant's actual machines (not just yours)
- Account for corporate firewalls/VPNs
- Have IT contact on standby

---

### Scenario 2: Network/Firewall Problems During Hands-On

**Symptoms**:
- Claude Code loses connection mid-session
- MCP servers fail to connect
- File read/write errors

**Solutions**:
1. **Quick fixes** (try these first, 2 min max):
   - Restart Claude Code
   - Check internet connection
   - Disable VPN temporarily

2. **If quick fixes fail**:
   - Move participant to backup machine (if available)
   - OR pair participant with neighbor (watch their screen)
   - Continue workshop, schedule makeup session

3. **If multiple participants affected**:
   - Pause workshop (5 min max)
   - Switch to demo mode (facilitator screen shares)
   - Participants follow along visually
   - Schedule makeup hands-on session

**Prevention Tips**:
- Test corporate network ahead of time
- Have backup hotspot ready
- Pre-download all materials (offline-capable)

---

### Scenario 3: Sales Team Confusion on Technical Concepts

**Symptoms**:
- Blank stares during architecture slide
- Questions like "What's a YAML file?"
- Falling behind during hands-on

**Solutions**:
1. **Use analogies** (avoid jargon):
   - Don't say: "YAML metadata in frontmatter"
   - Say: "Settings at the top of the file, like email headers"

2. **Show, don't tell**:
   - Don't explain file structure abstractly
   - Open actual files, show what's inside

3. **Pair with Solutions team member**:
   - "Alex, can you help Sarah with this part?"
   - Builds cross-team collaboration

4. **Simplify task**:
   - Sales doesn't need to understand system internals
   - Focus on: "Type this, you'll get this result"

**Prevention Tips**:
- Pre-workshop: Ask sales team about technical comfort level
- Adjust depth accordingly (skip technical deep dives)
- Focus on outcomes, not mechanisms

---

### Scenario 4: Solutions Team Dismisses as "Too Basic"

**Symptoms**:
- "I already have my own system"
- Disengaged during presentation
- Not participating in hands-on

**Solutions**:
1. **Acknowledge their expertise**:
   > "You're right, you probably have something working. This is about standardization so the whole team has one system."

2. **Appeal to team benefits**:
   - Individual expertise → Institutional knowledge
   - Onboarding new hires 3x faster
   - Collaborating across team members

3. **Show advanced features**:
   - Jump to Slide 6 (7-phase lifecycle)
   - Show MCP integrations (Airtable, Linear, Notion)
   - Discuss Skills library compound effects

4. **Make it optional but appealing**:
   > "Try it for 2 weeks. If your current system is better, keep using it. But I bet you'll see value in team standardization."

**Prevention Tips**:
- Pre-workshop survey: "Do you have an existing system?"
- If yes, emphasize team/company benefits over individual
- Position as "company standard" (not "better than yours")

---

### Scenario 5: Workshop Running Behind Schedule

**Symptoms**:
- 30-min mark: Still on Slide 4 (should be done with all slides)
- 60-min mark: Still in Section 1 of Project 00 (should be in Section 4)
- 80-min mark: Not done with Project 00

**Solutions - Skip Strategies**:

**If behind by 5-10 min**:
- Skip detailed Q&A on each slide
- Save questions for end
- Move faster through Slides 7-9 (less critical)

**If behind by 10-20 min**:
- Skip Slide 8 entirely (examples, less critical)
- Shorten Project 00 Section 4 (Projects vs Skills)
  - Show 2 scenarios instead of 4
  - Skip discussion, just present answers
- Shorten Section 5 (memory test)
  - Demonstrate once on facilitator screen
  - Skip individual testing

**If behind by 20+ min**:
- **HARD STOP** at 1:20 (10 min before end)
- Rapid wrap-up:
  > "We're running behind. Let's finish Project 00 async. I'll send instructions. Quick recap of what we learned..."
- Focus on ensuring everyone has:
  - ✅ Claude Code working
  - ✅ Nexus folder loaded
  - ✅ goals.md started (even if incomplete)
- Schedule makeup session for those who want full hands-on

**Prevention Tips**:
- Practice workshop with timer
- Build in 5-min buffer (plan for 85 min, schedule 90)
- Have "skip plan" ready before workshop starts

---

## Section 5: FAQ Handling Strategies

### FAQ 1: "How is this different from Cursor / GitHub Copilot / etc.?"

**Answer Framework**:
> "Great question. Tools like Cursor and Copilot are amazing for writing code. Nexus is different—it's for organizing your work with AI, not just coding."

**Key Distinctions**:
- **Cursor/Copilot**: Code completion, autocomplete, in-editor AI
- **Nexus**: Work organization system (memory, projects, skills, knowledge capture)

**Analogy**:
> "Cursor is like having a really smart keyboard. Nexus is like having a filing cabinet that remembers everything you've ever worked on."

**When to use what**:
- Use Cursor/Copilot: When writing code files
- Use Nexus: When organizing projects, capturing workflows, building knowledge library
- Use both: They complement each other

**Bottom line**:
> "Not competitors. Different problems. You can use Nexus WITH Cursor if you want."

---

### FAQ 2: "What if I already have my own system?"

**Answer Framework**:
> "That's great! The question is: Does your system solve these 3 problems?" (point to Slide 1)

**Diagnostic Questions**:
1. "If you close your AI chat, can you pick up exactly where you left off next session?"
   - If no → Memory problem

2. "Can you take work you did for Client A and reuse it for Client B in 10 minutes?"
   - If no → Reusability problem

3. "If you left the company tomorrow, would your team have access to all your workflows?"
   - If no → Knowledge sharing problem

**If they answer "yes" to all 3**:
> "Then you have a great system! Nexus might not add value for you personally. But think about team standardization—if everyone used the same system, would that help?"

**If they answer "no" to any**:
> "That's what Nexus fixes. Try it for 2 weeks. If your old system is still better, you can always switch back."

---

### FAQ 3: "How long does onboarding really take?"

**Answer Framework**:
> "Great question. Let me break it down by what you actually need to get started."

**Onboarding Tiers**:

**Tier 1: Minimum viable (30 min)**
- Complete Project 00 (define goals)
- You now have working memory system
- Can start using Nexus today

**Tier 2: Comfortable (90 min)**
- Project 00 + Project 01 (create first project)
- You understand projects structure
- Can organize work effectively

**Tier 3: Power user (3 hours)**
- All 4 onboarding projects (00, 01, 02, 03)
- You understand skills, mental models, full system
- Can build custom workflows

**Bottom line**:
> "Today's workshop gets you to Tier 1. You'll be functional immediately. Deeper mastery comes over time."

**For busy people**:
> "Do Project 00 today (30 min). Do Projects 01-03 over the next week when you have time. No rush."

---

### FAQ 4: "Can I use this for [non-AI-Agent-Company use case]?"

**Examples**:
- Personal use (organizing personal projects)
- Side business (freelance work)
- Academic research (dissertation, papers)
- Content creation (blog posts, newsletters)

**Answer Framework**:
> "Absolutely! Nexus is a general-purpose work organization system. It works for any knowledge work."

**Validation**:
- Memory system: Works for any work (remembers your context)
- Projects: Any temporal work (beginning, middle, end)
- Skills: Any repeatable workflow
- Workspace: Totally custom (you control it)

**Examples**:
- **Personal use**: Track home renovation project, remember preferences
- **Freelance**: Manage client projects, reuse proposal templates
- **Academic**: Track dissertation chapters, organize research notes
- **Content**: Build content calendar, reuse writing workflows

**Caveat**:
> "Company-provided Nexus instance might have usage policies. Check with IT. But system itself is designed to be flexible."

**Encouragement**:
> "Actually, using it for personal work is great practice. You'll get better at it, then apply skills to work projects."

---

### FAQ 5: "What if Claude Code changes and breaks Nexus?"

**Answer Framework**:
> "That's a valid concern. Here's how we handle it."

**Nexus Design Principles**:
1. **Plain text files**: Goals are .md files, not proprietary format
   - If Nexus breaks, your files are still readable
   - Can migrate to another system easily

2. **Minimal dependencies**: Nexus uses basic file operations (read, write, edit)
   - Not dependent on experimental APIs
   - Works with any AI that can read/write files

3. **Version control ready**: Everything is text files in Git
   - If something breaks, roll back
   - Full history preserved

**What we monitor**:
- Claude Code updates (monthly check)
- Breaking changes (update Nexus if needed)
- Community feedback (fix issues quickly)

**Worst case scenario**:
> "If Claude Code disappeared tomorrow, your files are just Markdown. You can open them in any editor, use with ChatGPT, or switch to different AI tool. You haven't lost anything."

**Bottom line**:
> "Low risk. Your data is yours, in portable format. Nexus is a structure, not a lock-in."

---

## Section 6: Audience Engagement Techniques

### Check-Ins for Sales Team (Ensure Not Lost)

**Technique 1: Visual Comprehension Checks**
> "By show of hands: Who can see the 5-folder structure on their screen?" (wait for hands)

**Why this works**:
- Non-verbal feedback (less pressure than asking "Any questions?")
- Shows you WHO is stuck (can follow up individually)
- Builds confidence (everyone else raises hand → social proof)

**When to use**:
- After architecture slide (Slide 3)
- Before starting hands-on (setup verification)
- Midway through Project 00 (progress check)

---

**Technique 2: Paired Explanations**
> "Turn to the person next to you and explain what we just covered. 60 seconds."

**Why this works**:
- Forces active processing (can't just nod along)
- Reveals misunderstandings immediately
- Low stakes (explaining to peer, not whole group)

**When to use**:
- After Slide 5 (project structure)
- After Project 00 Section 2 (roadmap creation)

---

**Technique 3: Real-World Scenarios**
> "Sales team: Think of your last proposal. Where would that go in the 4-folder structure?" (wait for answers)

**Why this works**:
- Grounds abstract concepts in their actual work
- Validates understanding through application
- Shows relevance immediately

**When to use**:
- During Slide 5 (project structure)
- During Project 00 Section 4 (Projects vs Skills)

---

### Depth Questions for Solutions Team (Maintain Engagement)

**Technique 1: Technical Extensions**
> "Solutions team: What MCP integrations would you add to this Skills library?" (open discussion)

**Why this works**:
- Engages technical expertise
- Shows advanced capabilities
- Prevents "this is too basic" dismissal

**When to use**:
- During Slide 6 (Skills & 7-phase lifecycle)
- During wrap-up (next steps discussion)

---

**Technique 2: Architecture Challenges**
> "How would you structure a Skill for monitoring client production systems?" (whiteboard discussion)

**Why this works**:
- Invites problem-solving (not just passive learning)
- Demonstrates system flexibility
- Respects their expertise

**When to use**:
- If time allows during Phase 2
- During breaks (informal discussion)

---

**Technique 3: Real JTBD Connections**
> "Remember the JTBD research quote: 'Include solutions team early in discovery'? How would you build that into a Skill?" (group discussion)

**Why this works**:
- Connects to actual team pain points
- Shows Nexus solving real problems they identified
- Invites co-creation (not just consumption)

**When to use**:
- During Slide 6 (Skills)
- During Phase 2 (if discussion emerges)

---

### Celebration Moments ("Great! Your memory is working!")

**Why celebrate small wins?**
- Builds momentum and confidence
- Reinforces learning
- Creates positive association with system

**Celebration Moments**:

**Moment 1: First File Load**
> "Who just saw their goals.md load automatically? Raise your hand! 🎉 That's your memory system working!"

**When**: After Project 00 Section 5 (memory test)

---

**Moment 2: Roadmap Creation**
> "You just turned a vague goal into concrete milestones. That's strategic thinking! 🎯"

**When**: After Project 00 Section 2 (roadmap complete)

---

**Moment 3: Project vs Skill Decision**
> "You nailed it! That scenario is definitely a Skill, not a Project. You're getting this! 💡"

**When**: During Project 00 Section 4 (decision framework)

---

**Moment 4: Workshop Completion**
> "You now have a working Nexus instance with memory, goals, and roadmap. You built this in 90 minutes! 🚀"

**When**: End of Phase 3 (wrap-up)

---

### Pause Points for Questions

**Strategic Pause Points** (build into agenda):

**Pause 1: After Slide 6** (5 min)
> "Pause for questions. Slide 6 is dense. What's unclear?"

**Why here**: Slide 6 (Skills) is conceptually heaviest, especially for Solutions team

---

**Pause 2: After Project 00 Section 3** (3 min)
> "Quick check-in. Everyone understand the 5-folder system?"

**Why here**: Before decision framework (Section 4), ensure foundation is solid

---

**Pause 3: Before Close-Session** (2 min)
> "Last chance for questions before we test memory persistence."

**Why here**: Memory test is the "aha moment"—ensure no blockers

---

**Pause 4: Wrap-Up Q&A** (5 min)
> "Open floor. Any questions about what we built today or next steps?"

**Why here**: Catch remaining confusion before they leave

---

## Section 7: Real-Time Pacing Tips

### 30-Min Mark Checkpoint

**Where you should be**: Starting Project 00 (slides complete)

**If you're behind**:
- ❌ Still presenting slides → Skip Slide 8 (examples), move faster
- ❌ Still on Slide 6 → Skip detailed Q&A, defer to post-workshop

**If you're ahead**:
- ✅ Extra 5 min → Deeper Q&A on Slides 6-7
- ✅ Extra 10 min → Show advanced demo (MCP integration preview)

**Check-in action**:
> Look at timer. Announce: "We're right on track. Let's dive into hands-on work."

---

### 60-Min Mark Checkpoint

**Where you should be**: Halfway through Project 00 (completed Sections 1-2, starting Section 3)

**If you're behind** (still on Section 1):
- Shorten Section 2 (roadmap): Show example, skip detailed breakdown
- Shorten Section 4 (Projects vs Skills): 2 scenarios instead of 4
- Must reach Section 5 (memory test) by 1:15

**If you're ahead**:
- ✅ Extra time → Let participants explore 04-workspace customization
- ✅ Extra time → Demonstrate create-project skill (preview)

**Check-in action**:
> "Great progress! We're halfway through Project 00. Stay focused."

---

### 80-Min Mark Checkpoint

**Where you should be**: Wrapping up Project 00, starting Phase 3 (wrap-up)

**If you're behind** (not done with Project 00):
- **HARD DECISION TIME**: Stop at 1:20 (10 min before end)
- Rapid wrap-up:
  > "We're out of time. You've completed most of Project 00. I'll send instructions to finish the rest async. Let's recap what we built..."
- Ensure everyone has:
  - ✅ goals.md created
  - ✅ Claude Code working
  - ✅ Next steps clear

**If you're ahead**:
- ✅ Extra time → Preview Project 01 (first real project)
- ✅ Extra time → Show create-skill demo
- ✅ Extra time → Extended Q&A

**Check-in action**:
> "Final 10 minutes. Let's recap what we accomplished today..."

---

### "Running Behind" Contingency Strategies

**Strategy 1: Dynamic Skip Plan**

**If behind by 5-10 min**:
- Cut: Detailed explanations, extra examples
- Keep: Core concepts, hands-on work

**If behind by 10-20 min**:
- Cut: Slide 8 (examples), Project 00 Section 4 (shorten to 2 scenarios)
- Keep: Memory test (Section 5)—this is the "aha moment"

**If behind by 20+ min**:
- Cut: Everything except Project 00 Sections 1-2 (goals + roadmap)
- Deliver: Async instructions for rest
- Schedule: Makeup session

---

**Strategy 2: Facilitator Speed Adjustments**

**Talk faster** (but stay clear):
- Skip filler words ("um", "so", "basically")
- Use bullet points instead of full sentences
- Let slides speak for themselves (less narration)

**Skip optional content**:
- Analogies (if concept is clear without them)
- War stories (save for office hours)
- Edge case discussions (defer to FAQ doc)

---

**Strategy 3: Participant Time Optimization**

**Reduce "wait time"**:
- Don't wait for every participant to finish before moving on
- Use "buddy system" (fast finishers help slow participants)
- Show finished example on screen (participants can catch up later)

**Batch questions**:
- "Hold questions until the checkpoint" (don't interrupt flow)
- Answer common questions once (not individually)

---

**Strategy 4: Async Completion Path**

**If you can't finish in 90 min**:

**Provide takeaway materials**:
- [ ] Recorded walkthrough of Project 00 (participants finish on own time)
- [ ] Written instructions for Sections 3-5
- [ ] Office hours signup (1:1 support)

**Set expectations**:
> "We covered the hardest parts today. The rest you can finish in 30 min on your own. I've sent instructions. Book office hours if you get stuck."

---

### Pacing Best Practices

**1. Visible Timer** (for facilitator only)
- Use phone/laptop timer
- Check every 10 minutes
- Adjust speed if drifting

**2. Pre-Planned Cuts**
- Know BEFORE workshop what you'll cut if behind
- Don't decide in real-time (too stressful)
- Have 3 versions: Full (90 min), Short (75 min), Minimal (60 min)

**3. Ruthless Prioritization**
- Must-have: Project 00 Sections 1-2 (goals + roadmap)
- Nice-to-have: Section 5 (memory test)
- Optional: Section 4 (decision framework depth)

**4. Energy Management**
- Start fast (capitalize on high energy)
- Slow down for memory test (most important moment)
- End strong (celebration, not rushed panic)

---

## Workshop Success Metrics

**Measure success by**:

### Immediate (End of Workshop)
- [ ] 90%+ participants completed Project 00 Sections 1-2 (goals + roadmap)
- [ ] 80%+ participants saw memory persistence work (Section 5)
- [ ] 100% participants have Claude Code functional
- [ ] <5% participants completely lost/frustrated

### 1-Week Post-Workshop
- [ ] 60%+ participants created their first real project
- [ ] 40%+ participants created their first skill
- [ ] <10% requests for 1:1 makeup sessions (low support burden)

### 1-Month Post-Workshop
- [ ] 50%+ active users (using Nexus weekly)
- [ ] 3+ user-created Skills shared in #nexus-users
- [ ] Positive feedback in team survey

---

## Facilitator Self-Reflection

**After the workshop, ask yourself**:

1. **Timing**: Did I finish on time? If not, what took longer than expected?
2. **Engagement**: Did both audiences stay engaged? Any drop-off moments?
3. **Technical Issues**: What broke? How can I prevent it next time?
4. **Clarity**: What concepts were confusing? How can I explain better?
5. **Celebration**: Did I celebrate small wins? Did participants feel accomplished?

**Update this guide based on your learnings!**

---

**End of Workshop Facilitator Guide**

**Version**: 1.0
**Last Updated**: 2025-11-25
**Next Review**: After first workshop delivery

Good luck! You've got this. 🚀
