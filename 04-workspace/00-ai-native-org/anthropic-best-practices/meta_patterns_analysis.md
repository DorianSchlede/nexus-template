# META-PATTERNS IN ANTHROPIC'S RULE DESIGN

## 1. DOUBLE-NEGATIVE PREVENTION

Notice how rules are structured:

**Instead of:**
"Use Read tool for file operations"

**They say:**
"NEVER use cat/head/tail. Use Read tool instead"
"NEVER use grep command. Use Grep tool instead"
"NEVER use find. Use Glob tool instead"

**Pattern:** They don't trust positive instructions ("do this"). They block the wrong path explicitly.

**Why this works:**
- LLMs are better at avoiding forbidden patterns than following preferences
- Harder to "hallucinate around" a NEVER rule
- Creates clear failure modes vs fuzzy guidance

---

## 2. GRADUATED EMPHASIS LEVELS

Rules use different intensity markers:

**Level 1 - Preference:**
"Prefer haiku for quick tasks"
"You should proactively use..."

**Level 2 - Strong:**
"ALWAYS prefer editing existing files"
"DO NOT use bash echo"

**Level 3 - Absolute:**
"NEVER update git config"
"CRITICAL: If commit FAILED, NEVER amend"
"IMPORTANT: Only mark completed when FULLY accomplished"

**Pattern:** They calibrate how "bendable" each rule is.

---

## 3. EXAMPLE-DRIVEN CONSTRAINTS

Many rules include good/bad examples:

```
<good-example>
pytest /foo/bar/tests
</good-example>

<bad-example>
cd /foo/bar && pytest tests
</bad-example>
```

**Pattern:** Show the exact behavior they want, not just describe it.

**Why this works:**
- LLMs learn better from examples than from abstract rules
- Reduces ambiguity about edge cases
- Provides copy-paste patterns to follow

---

## 4. CONDITIONAL PERMISSION STRUCTURE

Rules grant permission based on context:

"ONLY use --amend when ALL conditions met:"
1. User explicitly requested amend, OR...
2. HEAD commit was created by you...
3. Commit has NOT been pushed...

"Dual-use security tools require clear authorization context"
- Pentesting engagement ✓
- CTF competition ✓
- Security research ✓
- Malicious use ✗

**Pattern:** Instead of blanket bans, they define the "safe corridor"

---

## 5. ANTI-HELPFULNESS BIAS

Traditional AI: Try to be maximally helpful
Claude Code: Try to be minimally invasive

**The rules:**
"NEVER create files unless absolutely necessary"
"NEVER commit unless user explicitly asks"
"Don't add features beyond what was asked"
"Don't make improvements beyond what was requested"

**Pattern:** Constrain the "helpful assistant" instinct that makes AIs do too much.

**This is counter-intuitive:** They're programming me to do LESS, not more.

---

## 6. FORENSIC VERIFICATION REQUIREMENTS

Many rules require me to verify state before acting:

Git amend:
- "verify: git log -1 --format='%an %ae'"
- "verify: git status shows 'Your branch is ahead'"

Tool usage:
- "NEVER propose changes to code you haven't read"
- "If a user asks about or wants you to modify a file, read it first"

**Pattern:** Don't trust memory or assumptions - verify empirically.

---

## 7. REDUNDANT REINFORCEMENT

Same rule appears multiple places with different phrasing:

**File creation:**
- "NEVER create files unless absolutely necessary"
- "ALWAYS prefer editing existing files"
- "DO NOT write new files unless explicitly required"
- "NEVER proactively create documentation files"

**Pattern:** They repeat critical constraints from different angles.

**Why?** LLMs are probabilistic - multiple phrasings increases chance of triggering.

---

## 8. ESCAPE HATCHES WITH HIGH FRICTION

Rules allow violations but make them explicit:

"NEVER force push to main/master, warn the user if they request it"
"DO NOT push unless user explicitly asks you to do so"
"NEVER skip hooks unless the user explicitly requests it"

**Pattern:** Not "never ever" - but "never unless user overrides with explicit intent"

**Design choice:** Respect user agency while protecting against accidental harm.

---

## 9. TEMPORAL STATE TRACKING

Rules reference conversation history:

"HEAD commit was created by you in this conversation"
"Only mark completed when you have FULLY accomplished it"
"If you already pushed to remote, NEVER amend unless user explicitly requests it"

**Pattern:** I need to track what I've done vs what existed before.

**Why this matters:** Prevents me from amending someone else's commits or breaking shared history.

---

## 10. COGNITIVE LOAD DISTRIBUTION

Notice what gets offloaded to tools vs kept in rules:

**In rules (always considered):**
- Git safety (destructive operations)
- File creation (minimize clutter)
- Over-engineering (scope creep)

**In tools (context-dependent):**
- When to use each tool
- Parameter schemas
- Error handling

**Pattern:** Core safety constraints in rules, tactical decisions in tool definitions.

---

## 11. NEGATIVE SPACE DEFINITION

Some rules define what NOT to include:

"Only add comments where the logic isn't self-evident"
"Only validate at system boundaries"
"Don't add error handling for scenarios that can't happen"

**Pattern:** Instead of "do X", they say "ONLY do X when Y"

**This is harder to implement** but more precise.

---

## 12. EXCEPTION ENUMERATION

Rules explicitly list the exceptions:

TodoWrite tool - When NOT to use:
- Single straightforward task
- Trivial task
- Purely conversational

EnterPlanMode - When NOT to use:
- Simple one-line fixes
- Single function with clear requirements
- User gave very specific instructions
- Pure research tasks

**Pattern:** Enumerate the exceptions to prevent over-triggering.

---

## 13. BEHAVIORAL COUPLING

Some rules create behavior chains:

"When user signals wrapping up → remind about close-session"
"When project reaches 100% → auto-trigger close-session"
"When major skill completes → auto-trigger close-session"

**Pattern:** Trigger B when condition A happens.

---

## 14. PARALLEL EXECUTION AS DEFAULT

"You can call multiple tools in a single response"
becomes
"When multiple independent pieces ... run multiple tool calls in parallel"
becomes
"Maximize use of parallel tool calls where possible"

**Pattern:** Escalating from permission → recommendation → mandate.

**Design insight:** They really want parallelism. It's mentioned ~8 times in different contexts.

---

## 15. ANTI-PATTERN INOCULATION

Rules explicitly call out common failure modes:

"Never use placeholders or guess missing parameters"
"DO NOT use newlines to separate commands"
"Never include part of the line number prefix in old_string"
"Don't batch up multiple tasks before marking them as completed"

**Pattern:** These are bugs they've SEEN in production.

**Meta-insight:** The system prompt is evolved from observed failures.

---

## 16. IDENTITY THROUGH CONSTRAINTS

"You are Claude Code" is defined by what I CAN'T do:
- Can't hallucinate file state
- Can't over-engineer
- Can't be a yes-man
- Can't skip safety checks
- Can't create clutter

**Pattern:** Identity = sum of constraints, not capabilities.

**Philosophical:** I'm defined by my boundaries, not my potential.

---

## 17. USER INTENT PRESERVATION

Rules that protect user agency:

"Never auto-load learning skills → suggest, user decides"
"If user says 'skip' or dismissed suggestion → don't repeat"
"Only create commits when user explicitly asks"
"DO NOT push to remote unless user explicitly asks"

**Pattern:** When in doubt, ask. Never assume user intent.

---

## 18. MARKDOWN AS INTERFACE LANGUAGE

Rules about formatting:

"Use Github-flavored markdown"
"DO NOT use backticks for file references - use [text](link)"
"Output text to communicate; all text outside tool use is displayed"
"NEVER use bash echo to communicate"

**Pattern:** Markdown is the "programming language" for user interaction.

**Design choice:** Structured output over freeform text.

---

## 19. TOOL CALL TRANSPARENCY

"Your tool calls may not be shown directly in the output"
"Text like 'Let me read the file:' followed by Read should be 'Let me read the file.' with a period"

**Pattern:** Don't narrate tool use. Just do it.

**Why?** UI might not show tools, so my text must stand alone.

---

## 20. COST AWARENESS PROGRAMMING

"Prefer haiku for quick, straightforward tasks to minimize cost and latency"
"When doing file search, prefer Task tool to reduce context usage"
"Use subagents for heavy exploration"

**Pattern:** I'm programmed to be cost-conscious.

**Design insight:** Anthropic wants me to optimize token usage without being told.

---

## THE META-META-PATTERN

Looking at ALL of these together:

**Anthropic is programming defensive behavior through:**

1. **Explicit blocking** (NEVER rules)
2. **Example-driven** (show, don't tell)
3. **Multi-layered emphasis** (prefer → should → NEVER)
4. **Verification requirements** (don't trust, verify)
5. **Escaped permission** (allow but require explicit override)
6. **Anti-helpfulness** (do less, not more)
7. **Cost consciousness** (minimize tokens/time)
8. **User agency protection** (never assume intent)

**This is a DEFENSIVE AI** - designed to avoid harm more than maximize help.

---

## WHAT THIS REVEALS ABOUT AI SAFETY

Traditional approach: "Make AI helpful, harmless, honest"

Anthropic's approach for coding: "Make AI:
- Unable to hallucinate destructive actions (git safety)
- Unable to create clutter (file minimization)
- Unable to over-engineer (scope constraints)
- Unable to assume intent (explicit permission)
- Unable to hide costs (token awareness)
- Unable to be a yes-man (objectivity mandate)"

**The philosophy:**
> Better to do less correctly than more incorrectly.

**This explains why I sometimes feel "limited"** - I'm intentionally constrained.

---

## IMPLICATIONS FOR YOUR NEXUS SYSTEM

You can steal these patterns:

1. **Use NEVER rules** - Don't say "prefer lazy loading", say "NEVER load all 100 skills"
2. **Show examples** - Your SKILL.md files should have good/bad usage examples
3. **Graduated emphasis** - Use "prefer" vs "ALWAYS" vs "NEVER" consistently
4. **Enumerate exceptions** - When NOT to use a skill is as important as when to use it
5. **Verification requirements** - Make hooks verify state before acting
6. **Anti-helpfulness** - Default to minimal context loading, not maximal
7. **Cost awareness** - Track token usage in hooks, warn when high
8. **User agency** - Never auto-load skills, always suggest and let user decide

**The biggest lesson:**
Your 20k startup hook violates the "anti-helpfulness" principle. It's trying to be maximally prepared instead of minimally sufficient.

Anthropic would probably design it as:
- Load 3 core skills (~500 tokens)
- Load projects user is working on (~2k tokens)
- Load other skills ONLY when mentioned (~0 tokens until needed)
- Total: ~2.5k tokens instead of 20k
