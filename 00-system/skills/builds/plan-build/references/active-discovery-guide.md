# Active Discovery Guide

> **Purpose**: Document active research patterns for Phase 2 discovery
> **Related**: [REQ-1, REQ-2, REQ-3a] from Enhanced Active Discovery build

---

## Overview

Active discovery transforms Phase 2 from passive (questions only) to active (AI researches based on user answers). The flow is:

```
ASK → RESEARCH → ASK (+ optional follow-up research)

Phase 2a: Discovery Questions (understand what user wants)
    ↓
Phase 2b: Active Research (targeted by answers)
    ↓
Phase 2c: Informed Follow-ups + Optional Follow-up Research
    ↓ (if gaps found)
    Loop back to 2b (max 2 loops)
```

**Why This Matters**:
- AI needs to understand WHAT user wants before knowing WHERE to look
- Research is targeted by discovery answers, not blind exploration
- Follow-ups can trigger additional research if new areas emerge

---

## Phase 2a: Discovery Questions

**Purpose**: Understand what the user wants to build BEFORE researching.

### Standard Questions

Ask these FIRST to understand the build:

```markdown
Let me understand what you're building:

1. **What are you building?**
   - Describe the feature/system in 1-2 sentences

2. **What problem does this solve?**
   - Why is this needed? What pain point does it address?

3. **Who/what will use this?**
   - Users? Other systems? Internal tools?

4. **Any constraints or requirements?**
   - Must integrate with existing systems?
   - Performance requirements?
   - Technology preferences or restrictions?

5. **What does success look like?**
   - How will you know this build is complete?
```

### Extract Search Targets from Answers

AI analyzes answers to determine what to search:

```yaml
# From user's answers:
build_description: "Add OAuth2 authentication to API endpoints"
problem: "Users can't log in with Google/GitHub, only username/password"
users: "End users of the web app"
constraints:
  - "Must work with existing session system"
  - "Support Google and GitHub providers"
success: "Users can click 'Login with Google' and access the app"

# AI extracts search targets:
search_targets:
  keywords: ["auth", "oauth", "login", "session", "google", "github"]
  likely_areas: ["src/auth/", "src/api/", "src/middleware/"]
  related_systems: ["session management", "user model", "API routes"]
```

---

## Phase 2b: Active Research

**Research is now TARGETED by discovery answers from Phase 2a.**

### Step 1: Extract Search Targets from Discovery Answers

Before searching, analyze the user's answers:
- Build description → primary keywords
- Problem statement → related patterns
- Constraints → systems to check for conflicts
- Success criteria → areas that must work together

### Step 2: Assess Complexity

**Determine exploration strategy based on build scope:**

| Complexity | Indicators | Strategy |
|------------|------------|----------|
| **Simple** | Single file/function, clear location, small change | Direct Grep/Glob only (0 agents) |
| **Medium** | Single component/feature, affects 5-15 files | 1-2 targeted subagents |
| **Complex** | Multi-component, system-wide, 15+ files | 3-5 specialized subagents |

**Complexity Heuristics:**

```python
def assess_complexity(scope_answers):
    """
    Determine exploration complexity from user's scoping answers.
    Returns: "simple", "medium", or "complex"
    """
    indicators = {
        "simple": 0,
        "medium": 0,
        "complex": 0
    }

    # Check search areas count
    search_areas = scope_answers.get("search_areas", [])
    if len(search_areas) <= 1:
        indicators["simple"] += 2
    elif len(search_areas) <= 3:
        indicators["medium"] += 2
    else:
        indicators["complex"] += 2

    # Check intent keywords
    intent = scope_answers.get("intent", "").lower()
    simple_keywords = ["fix", "update", "add field", "rename", "typo"]
    complex_keywords = ["system", "architecture", "refactor", "multi", "entire", "all"]

    if any(kw in intent for kw in simple_keywords):
        indicators["simple"] += 1
    if any(kw in intent for kw in complex_keywords):
        indicators["complex"] += 2

    # Check constraints complexity
    constraints = scope_answers.get("constraints", [])
    if len(constraints) >= 3:
        indicators["complex"] += 1

    # Return highest scoring complexity
    return max(indicators, key=indicators.get)
```

### Step 2: Dynamic Subagent Exploration

**CRITICAL**: Both the NUMBER and PURPOSE of agents are dynamic.

#### 2.1 Determine Agent Count

```python
def get_agent_count(complexity):
    """Map complexity to agent count."""
    return {
        "simple": 0,    # Direct Grep/Glob only
        "medium": 2,    # 1-2 targeted agents
        "complex": 4    # 3-5 specialized agents
    }.get(complexity, 2)
```

#### 2.2 Determine Agent Purposes

**Purpose comes from THREE sources:**

1. **Build Topic** - What the build is about
2. **User's Scope Answers** - Areas they mentioned
3. **Codebase Structure** - What exists to explore

**Purpose Determination Logic:**

```python
def determine_agent_purposes(build_topic, scope_answers, complexity):
    """
    Dynamically determine what each agent should explore.
    Returns list of {focus_area, search_patterns, prompt_context}
    """
    purposes = []

    # Source 1: Extract focus areas from build topic
    topic_areas = extract_topic_areas(build_topic)
    # e.g., "OAuth2 authentication" → ["auth", "oauth", "security", "tokens"]

    # Source 2: Add areas from user's scope answers
    user_areas = scope_answers.get("search_areas", [])

    # Source 3: Discover codebase structure (quick glob)
    codebase_areas = discover_codebase_structure()
    # e.g., ["src/api/", "src/auth/", "src/models/", "src/utils/"]

    # Combine and deduplicate
    all_areas = list(set(topic_areas + user_areas))

    # Map areas to codebase locations
    for area in all_areas:
        matching_paths = find_matching_paths(area, codebase_areas)
        if matching_paths:
            purposes.append({
                "focus_area": area,
                "search_patterns": build_search_patterns(area),
                "codebase_paths": matching_paths,
                "prompt_context": f"Explore {area} implementation"
            })

    # Limit based on complexity
    max_agents = get_agent_count(complexity)
    return purposes[:max_agents]
```

**Example: "Add OAuth2 Authentication" Build**

```yaml
build_topic: "Add OAuth2 authentication to API"
scope_answers:
  search_areas: ["src/auth/", "middleware"]
  constraints: ["Support Google, GitHub providers"]

# AI determines purposes:
agent_purposes:
  - focus_area: "Authentication patterns"
    search_patterns: ["auth", "login", "session", "token"]
    codebase_paths: ["src/auth/", "src/middleware/"]
    prompt_context: "Find existing auth patterns and session management"

  - focus_area: "API middleware"
    search_patterns: ["middleware", "interceptor", "guard"]
    codebase_paths: ["src/api/middleware/", "src/middleware/"]
    prompt_context: "Find request interceptors and auth guards"

  - focus_area: "User management"
    search_patterns: ["user", "account", "profile"]
    codebase_paths: ["src/models/user", "src/services/user"]
    prompt_context: "Find user model and related services"

  - focus_area: "Security patterns"
    search_patterns: ["security", "encrypt", "hash", "secret"]
    codebase_paths: ["src/utils/", "src/config/"]
    prompt_context: "Find security utilities and config patterns"
```

#### 2.3 Generate Agent Prompts

**Dynamic Prompt Template:**

```markdown
# Codebase Exploration Agent - {focus_area}

You are exploring the codebase to inform a BUILD for: "{build_topic}"

## Your Focus Area
**{focus_area}**: {prompt_context}

## Search Targets
Look for files matching these patterns:
{search_patterns_as_list}

Starting from these paths:
{codebase_paths_as_list}

## User Context
The user mentioned these constraints:
{user_constraints}

## Your Task

1. Search for files matching the patterns above
2. Read relevant files (max 10 most important)
3. Document:
   - What exists currently
   - How it's structured
   - Key functions/classes
   - Potential impact of changes
   - Integration points
4. Return a structured summary (don't dump file contents)

## Output Format

Return:
```
### {focus_area} Findings

**Files Found**: {count}
**Key Files**:
- `path/to/file.py` - {what it does}
- `path/to/other.py` - {what it does}

**Current Implementation**:
{2-3 sentence summary of what exists}

**Key Patterns**:
- {pattern 1}
- {pattern 2}

**Impact Assessment**:
{how the build might affect this area}

**Integration Points**:
- {where new code would connect}
```
```

#### 2.4 Parallel Execution Pattern

**CRITICAL: Spawn ALL agents in a single message.**

```python
# Correct: Single message with multiple Task calls
for i, purpose in enumerate(agent_purposes):
    Task(
        subagent_type="Explore",
        prompt=generate_agent_prompt(purpose, build_topic, scope_answers),
        description=f"Exploring {purpose['focus_area']}"
    )

# All agents spawn simultaneously and run in parallel
```

**Announce to user:**
```
I'm launching {N} exploration agents to research your codebase:

1. {focus_area_1} - {what it will explore}
2. {focus_area_2} - {what it will explore}
...

This will take ~30 seconds. You'll see consolidated findings when complete.
```

### Step 3: Simple Search Fallback

**For simple builds (0 agents), use direct Grep/Glob:**

```python
def simple_search(scope_answers):
    """Direct search for simple builds - no subagents."""

    search_areas = scope_answers.get("search_areas", [])
    patterns = build_search_patterns(scope_answers.get("intent", ""))

    findings = []

    for pattern in patterns:
        # Use Grep tool
        results = Grep(
            pattern=pattern,
            path=search_areas[0] if search_areas else ".",
            output_mode="files_with_matches",
            head_limit=10
        )
        findings.extend(results)

    return findings
```

**When to use simple search:**
- Single file/function changes
- Clear, specific location known
- User said "just update X" or "fix this one thing"

### Step 4: Related Builds Check

**Scan 02-builds/ for similar work:**

```python
def check_related_builds(build_name, build_intent):
    """Find builds with similar names or purposes."""

    builds_dir = Path("02-builds/active")
    related = []

    # Extract keywords from build name and intent
    keywords = extract_keywords(build_name + " " + build_intent)

    for build_folder in builds_dir.iterdir():
        if not build_folder.is_dir():
            continue

        # Read overview.md for description
        overview = build_folder / "01-planning" / "01-overview.md"
        if overview.exists():
            content = overview.read_text()

            # Check for keyword matches
            matches = sum(1 for kw in keywords if kw.lower() in content.lower())

            if matches >= 2:  # At least 2 keyword matches
                related.append({
                    "build_id": build_folder.name,
                    "relevance": matches,
                    "path": str(build_folder)
                })

    return sorted(related, key=lambda x: x["relevance"], reverse=True)[:3]
```

**Display related builds:**
```markdown
### Related Builds Found

| Build | Relevance | Why |
|-------|-----------|-----|
| `02-auth-refactor` | High | Modifies same auth files |
| `05-api-updates` | Medium | Touches API middleware |

**Action**: Consider if this build should merge with or depend on existing work.
```

### Step 5: Related Skills Check

**Scan 03-skills/ and 00-system/skills/ for reusable skills:**

```python
def check_related_skills(keywords):
    """Find skills that could be reused or affected."""

    skill_locations = [
        Path("03-skills"),
        Path("00-system/skills")
    ]

    related = []

    for location in skill_locations:
        for skill_folder in location.rglob("SKILL.md"):
            content = skill_folder.read_text()

            # Check description in YAML frontmatter
            matches = sum(1 for kw in keywords if kw.lower() in content.lower()[:500])

            if matches >= 1:
                skill_name = skill_folder.parent.name
                related.append({
                    "skill": skill_name,
                    "location": str(skill_folder.parent),
                    "relevance": matches
                })

    return sorted(related, key=lambda x: x["relevance"], reverse=True)[:5]
```

### Step 6: Web Search (Optional)

**Query Templates by Build Type:**

| Build Type | Query Template |
|------------|----------------|
| **build** | `"{topic}" best practices 2026`, `"{topic}" architecture patterns` |
| **skill** | `"{topic}" automation patterns`, `"{topic}" workflow design` |
| **strategy** | `"{topic}" market analysis`, `"{topic}" competitive landscape` |
| **content** | `"{topic}" content strategy`, `"{topic}" best examples` |
| **process** | `"{topic}" workflow optimization`, `"{topic}" process design` |

**Query Construction:**

```python
def build_web_queries(build_type, build_topic, constraints):
    """Generate targeted web search queries."""

    base_queries = {
        "build": [
            f"{build_topic} implementation best practices",
            f"{build_topic} architecture patterns 2026",
            f"{build_topic} common pitfalls to avoid"
        ],
        "skill": [
            f"{build_topic} automation workflow",
            f"how to automate {build_topic}"
        ],
        "strategy": [
            f"{build_topic} market analysis 2026",
            f"{build_topic} industry trends"
        ],
        "content": [
            f"{build_topic} content strategy examples",
            f"best {build_topic} content 2026"
        ],
        "process": [
            f"{build_topic} process optimization",
            f"{build_topic} workflow efficiency"
        ]
    }

    queries = base_queries.get(build_type, base_queries["build"])

    # Add constraint-specific queries
    for constraint in constraints[:2]:  # Max 2 constraint queries
        queries.append(f"{build_topic} {constraint}")

    return queries[:3]  # REQ-NF-2: Max 3 queries
```

**Skip Option:**
```
Would you like me to search the web for best practices?
- Yes (recommended) - I'll search for "{topic}" patterns
- Skip - proceed with codebase findings only
```

### Step 7: Aggregate Findings

**Consolidate all research into structured format:**

```markdown
## AI Research Findings

### Codebase Research

**Files Analyzed**: {count}
**Key Files**:
- `path/file.py` - {purpose}

**Existing Patterns**:
{summary of what exists}

**Impact Assessment**:
{how build affects existing code}

### Related Builds & Skills

**Related Builds**:
| Build | Status | Relevance |
|-------|--------|-----------|
| {build} | {status} | {why related} |

**Related Skills**:
- `{skill}` - {could reuse/affects}

### Web Research (if performed)

**Best Practices Found**:
1. {practice 1} - Source: {url}
2. {practice 2} - Source: {url}

**Patterns to Consider**:
- {pattern from web research}
```

### Step 8: Present Findings

**Display consolidated findings BEFORE follow-up questions:**

```
RESEARCH COMPLETE
----------------------------------------------------

Codebase Analysis:
  - Found {N} related files in {areas}
  - Key patterns: {patterns}
  - Impact: {summary}

Related Work:
  - {N} related builds found
  - {N} reusable skills identified

Web Research:
  - {N} best practices found
  - Key recommendation: {summary}

Based on these findings, I have follow-up questions...
```

---

## Phase 2c: Informed Follow-ups + Optional Follow-up Research

**Questions are now INFORMED by research findings. Follow-ups can trigger additional research.**

### Question Pattern

```
Given I found {finding}, how should we handle {aspect}?
```

**Examples:**

| Finding | Follow-up Question |
|---------|-------------------|
| "Found existing session management in src/auth/session.py" | "Should we extend the existing session system or create a new OAuth-specific one?" |
| "Build 02-auth-refactor is also modifying auth files" | "Should this build wait for 02-auth-refactor to complete, or proceed independently?" |
| "Web search suggests JWT over sessions for OAuth" | "The existing system uses sessions. Should we migrate to JWT or keep sessions for backward compatibility?" |

### Type-Specific Follow-ups

Continue with the type's discovery.md template questions, but prefix with relevant findings:

```markdown
Given my research:
- {finding 1}
- {finding 2}

{Original template question}
```

### Follow-up Research Loop

**If user's answers reveal new areas to explore:**

```markdown
Your answer mentions {new_area} that I didn't search earlier.
Should I research {new_area} before we continue?

Options:
1. Yes, research {new_area} (recommended)
2. No, I have enough context
```

**If yes:** Loop back to Phase 2b with targeted search for the new area
**If no:** Continue to mental models

**Constraints:**
- Max 2 follow-up research loops to prevent infinite discovery
- Each follow-up loop should be more targeted than the initial search
- After 2 loops, proceed with "known unknowns" documented

**Example flow with follow-up research:**

```
Phase 2a: User describes OAuth feature
    ↓
Phase 2b: AI searches auth/, security/, users/
    ↓
Phase 2c: AI asks "Should we extend sessions or use JWT?"
         User: "Actually, we also need to support SAML for enterprise"
    ↓
AI: "You mentioned SAML. Should I research SAML patterns in the codebase?"
    User: "Yes"
    ↓
Phase 2b (loop 1): AI searches for SAML, enterprise auth
    ↓
Phase 2c: AI asks informed questions about SAML integration
    ↓
Continue to mental models
```

---

## Build Type Examples

### Example 1: Simple Build (0 agents)

**User**: "Fix the typo in the login error message"

```yaml
complexity: simple
agent_count: 0
strategy: Direct Grep

# Direct search
Grep(pattern="login.*error", path="src/", output_mode="content")

# Found: src/auth/messages.py:42
# Change: "Login faild" → "Login failed"
```

### Example 2: Medium Build (2 agents)

**User**: "Add email verification to signup flow"

```yaml
complexity: medium
agent_count: 2
purposes:
  - focus_area: "Signup flow"
    search: ["signup", "register", "create account"]
  - focus_area: "Email system"
    search: ["email", "mail", "notification"]
```

### Example 3: Complex Build (4 agents)

**User**: "Refactor the entire authentication system to support SSO"

```yaml
complexity: complex
agent_count: 4
purposes:
  - focus_area: "Current auth implementation"
    search: ["auth", "login", "session"]
  - focus_area: "User management"
    search: ["user", "account", "profile"]
  - focus_area: "Security infrastructure"
    search: ["security", "token", "encrypt"]
  - focus_area: "API integration points"
    search: ["middleware", "guard", "interceptor"]
```

---

## Integration with Templates

Each discovery.md template gets these new sections:

```markdown
## Initial Scoping
{Answers from Phase 2a questions}

## AI Codebase Research
{Findings from Phase 2b subagents}

## AI Web Research (Optional)
{Best practices from web search}

## Related Builds & Skills
{Related work found}

## Follow-up Questions
{Type-specific questions, informed by research}
```

---

## Performance Guidelines

- **30-second timeout** for codebase research (REQ-NF-1)
- **Max 3 web queries** to avoid context bloat (REQ-NF-2)
- **Top 10 files** per focus area to keep results manageable
- **Summarize, don't dump** - findings are summaries, not file contents
- **Parallel execution** - spawn all agents in single message

---

## Skip Conditions

**Skip active research for:**

| Build Type | Skip Research | Reason |
|------------|---------------|--------|
| integration | Yes | add-integration skill handles discovery |
| research | Yes | create-research-build skill handles discovery |
| skill | Partial | Uses create-skill for scaffold, but run codebase search |

---

*Reference for plan-build Phase 2 Active Research*
