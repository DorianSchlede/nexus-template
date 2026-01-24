# Improved Onboarding Design - Discovery

**Build Type**: Strategy
**Purpose**: Design optimal learning sequence for new Nexus users

---

## Current State

*Where are we now?*

### Situation Analysis

**Current Onboarding (v4)**:
- Everything is optional ("suggested" but skippable)
- Menu shows: setup memory → create folders → learn builds/skills/integrations
- User can jump directly into work without setup
- Build 03 implementing auto-trigger learning via PostToolUse hook (contextual micro-lessons)
- No structured progression or mandatory steps

**What Users See (First Session)**:
```
MEMORY: Not configured → 'setup memory' (8 min)
FOLDERS: Not organized → 'create folders' (5 min)
CURRENT WORK: None
```

User can say anything and system will respond - no forced path.

### Pain Points

**Creator's Observations:**
1. **Users don't understand HOW to use the system** - they see capabilities but not workflow
2. **Users don't know how to break down work into builds** - confusion between build vs execute modes
3. **Critical setup gets skipped** - memory and workspace setup are optional, but system works poorly without them
4. **No clear learning path** - 6 learning skills with no obvious sequence

**Fundamental Confusion**:
- Users think this is chat, not a system builder
- Don't understand scope boundary (1 Nexus instance = 1 user goal)
- Don't understand BUILD vs EXECUTE distinction early enough

### Constraints

- **First 5 minutes are critical** - must establish mental model or user gets lost
- **Onboarding fatigue** - can't force 30+ minutes of tutorials before value
- **Backward compatibility** - existing users shouldn't break
- **Hook limitations** - PostToolUse triggers are reactive, not proactive for onboarding sequence

---

## Desired State (Creator's Vision)

**Ideal First 5 Minutes** - User understands:
- "NEXUS = System builder for business people"
- "2 core modes: BUILD (has end) vs EXECUTE (via skills, repeats)"
- "First session = Memory setup = defines THIS instance's scope"
- "1 Nexus instance = 1 user goal"

**Ideal Sequence (MANDATORY)**:
1. **Memory Setup** → Define role, goals, scope of this instance (5-7 min)
2. **Workspace Setup** → Organize folders for this goal (5 min)
3. **Roadmap** → Plan what builds user will do (NEW concept, ~10 min)
4. **First Build** → Guided build creation with explanations (20-30 min)

**After Onboarding Complete**:
- User has working system scoped to their goal
- User understands BUILD vs EXECUTE
- User has roadmap of planned work
- Learning skills (learn-builds, learn-skills, etc.) available but optional

---

## Options Analysis

### Option 1: Mandatory Linear Onboarding (Creator's Preference)

**Description**: First session forces 4-step sequence (memory → workspace → roadmap → first build). User cannot skip. System doesn't work until onboarding complete.

**Pros**:
- Guarantees proper setup (no broken states)
- Establishes mental model before user gets confused
- Creates complete working system in one session
- Clear progression with visible milestones
- Roadmap gives user ownership of plan

**Cons**:
- 40-50 minutes before user can "just try it"
- High commitment for curious users
- Feels restrictive ("let me skip!")
- Hard to interrupt/resume mid-onboarding

**Effort**: Medium (implement onboarding state machine in SessionStart hook)
**Risk**: Medium (some users may bounce if forced commitment too high)

### Option 2: Hybrid - Mandatory Core + Optional Deep Learning

**Description**: Force memory + workspace setup (10-12 min mandatory). Roadmap optional. First build is guided with inline tips. Deep learning skills (learn-builds, learn-skills) remain optional via auto-trigger.

**Pros**:
- Balances setup guarantees with user freedom
- Lower time commitment (12 min vs 50 min)
- User can "learn by doing" after core setup
- Leverages existing auto-trigger system from build 03
- Less intimidating for new users

**Cons**:
- Users might skip roadmap planning (miss big picture)
- First build quality depends on inline tips (no deep understanding)
- Partial onboarding might still leave confusion
- Roadmap concept gets lost if optional

**Effort**: Low (extend SessionStart hook, reuse build 03 auto-triggers)
**Risk**: Low (incremental improvement over current state)

### Option 3: Adaptive - Smart Suggestions Based on User Type

**Description**: SessionStart asks "What brings you here?" → Routes to different onboarding paths based on user goal complexity. Simple goals get minimal onboarding. Complex goals get full sequence.

**Pros**:
- Optimized for each user's needs
- No forced steps for simple use cases
- Full guidance for complex use cases
- Feels personalized and intelligent

**Cons**:
- Complex routing logic (multiple paths to maintain)
- Risk of wrong classification (user says "simple" but needs complex)
- More development effort
- Harder to test all paths

**Effort**: High (build classification logic, multiple onboarding paths)
**Risk**: High (complexity, edge cases, maintenance burden)

---

## Stakeholders

| Stakeholder | Interest | Influence |
|-------------|----------|-----------|
| **New Users** | Need to understand system quickly without frustration | High - they decide to adopt or bounce |
| **System Creator** | Wants proper setup (memory + workspace) before users start | High - defines requirements |
| **Existing Users** | Don't want breaking changes to their workflow | Medium - backward compat constraint |
| **Power Users** | Want to skip tutorials and dive deep | Low - edge case, can handle advanced paths |

---

## Dependencies

### Related Decisions

- **Build 03 completion** - Auto-trigger learning system should inform this design
- **Mental model clarity** - "BUILD vs EXECUTE" framing must be solid before onboarding teaches it
- **Roadmap concept** - Need to define what "roadmap" means (new build type? planning skill? custom flow?)
- **SessionStart hook capabilities** - Can we enforce mandatory steps via hook?

### External Factors

- **User attention span** - 5 min tolerance for "intro" content, 50 min tolerance if seeing value
- **Business user context** - Non-technical users need plain language, not system jargon
- **Instance scoping clarity** - Users must understand "1 instance = 1 goal" boundary early

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Forced onboarding drives users away** | Medium | High | Option 2 hybrid approach (12 min mandatory vs 50 min) |
| **Users skip memory setup and system breaks** | High (current) | High | Make memory mandatory (all options enforce this) |
| **Roadmap concept unclear/confusing** | High | Medium | Define roadmap clearly before implementation |
| **Auto-trigger lessons conflict with onboarding** | Medium | Medium | Disable auto-triggers during onboarding sequence |
| **Users don't understand "1 instance = 1 goal"** | High | Medium | Explicit callout during memory setup |
| **Backward compat breaks existing users** | Low | High | Check onboarding status flag before enforcing |

### Open Questions - RESOLVED

- [x] **What IS the roadmap step?** → **SYSTEM VISION with checkboxes** - Shows user the FULL system they could build (Skills, Builds, Knowledge) with checkboxes to visualize journey
- [x] **How do we explain "1 instance = 1 goal"?** → **Goals.md IS the scope** - It's always loaded, defines the boundaries. Explicit in Phase 2 setup
- [x] **Should workspace setup be templated per goal type?** → **YES** - Inferred from system vision (sales system, content system, etc.)
- [x] **Do we keep auto-trigger learning from build 03?** → **YES** - After onboarding, for advanced features (not replacing core onboarding)
- [ ] **What happens if user force-quits mid-onboarding?** → Resume from phase, or offer quick setup

---

## Creator's True Vision (From Strategy Docs)

**The ACTUAL 5-Phase Onboarding** (from strategy-nexus/onboarding.md):

| Phase | Purpose | Time | Key Innovation |
|-------|---------|------|----------------|
| **1. Prime Mindset** | Think BIG | 1 min | "What kind of SYSTEM do you want to build?" |
| **2. Setup Context** | Capture world | 2 min | 3 questions: role, pain, magic wand → saves to goals.md |
| **3. Design System Vision** | Show potential | 3 min | **ROADMAP = Full system vision with checkboxes** |
| **4. Build First Piece** | Create first component | 3 min | Guided build, framed as "adding to YOUR system" |
| **5. Celebrate & Expand** | Momentum | 1 min | "Your system is 25% built - what's next?" |

**Total: <10 minutes** (vs old model: 60 min across 6 skills)

### The Roadmap Concept (Phase 3)

**NOT a build, NOT a skill - it's a VISION DOCUMENT:**

```
+-------------------------------------------------------------+
|               YOUR [SALES/CONTENT/etc] SYSTEM               |
+-------------------------------------------------------------+
|  SKILLS (what you'll run):                                  |
|  [ ] "follow-up for [client]"                               |
|  [ ] "proposal for [client]"                                |
|  [ ] "pipeline report"                                      |
|                                                             |
|  BUILDER (to create the above):                             |
|  [ ] follow-up-email skill                                  |
|  [ ] proposal-generator skill                               |
|  [ ] sales-playbook                                         |
|                                                             |
|  KNOWLEDGE (Your system remembers):                         |
|  [ ] Your role and context                                  |
|  [ ] Your writing style                                     |
|  [ ] Client information                                     |
+-------------------------------------------------------------+
```

**Purpose**: User sees WHOLE system (not just first task) → Creates excitement → User chooses where to start

### Language That MUST Be Used (Era 3)

| Context | Say (Era 3) | NOT (Era 2) |
|---------|-------------|-------------|
| Opening | "Your personal system builder" | "How can I help?" |
| First question | "What kind of SYSTEM do you want to build?" | "What do you need?" |
| Context setup | "Let's set up your system's brain" | "Tell me about yourself" |
| During build | "Adding to your system" | "I'll do that for you" |
| After output | "Your system is X% built" | "Task complete" |
| Next steps | "What should we build next?" | "What else?" |

### The Mental Model Shift

**From**: "I use AI to help with tasks" (ChatGPT, Claude)
**To**: "I BUILD MY system that does work for me" (Nexus)

| Old Model | New Model |
|-----------|-----------|
| AI helps with tasks | I BUILD systems that do tasks |
| Sessions are ephemeral | My system grows over time |
| Chat = work | Build = create / Work = use |
| AI is the tool | MY system is what I've built |

### Key Design Principles (From Product Overview)

1. **Progressive Disclosure** - Don't load everything, load metadata + expand on-demand
2. **BUILD vs EXECUTE** - Two modes, everything flows through one
3. **Compounding** - Every session makes system smarter
4. **Ownership Language** - "YOU built" not "AI created"

---

*This discovery document captures decision context. Next: Apply mental models to validate approach.*
