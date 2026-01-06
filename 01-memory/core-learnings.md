# Core Learnings

> **Purpose**: Capture insights, patterns, and best practices (accumulates over time)
>
> **Updated**: Automatically by close-session skill after each session

---

## What Works Well

### 7-Level Synthesis Pipeline (2025-12-29)
- **Deterministic Scripts for Routing/Allocation**: Using Python scripts (L1-L3, L5-L6) instead of LLM for deterministic tasks reduces hallucination and ensures reproducibility
- **Parallel Subagent Spawning**: 38 subagents spawned in 3 waves (15+15+8) completed extraction efficiently
- **File Path Passing**: Passing `prompt=f"Read and follow instructions in: {file_path}"` instead of reading content into orchestrator saves massive context tokens
- **YAML Multi-Document Handling**: Using `yaml.safe_load_all()` handles frontmatter + body pattern gracefully
- **Greedy Bin-Packing**: 70k token budget per batch keeps subagents within context limits

---

## What to Avoid

### Subagent Orchestration Anti-Patterns (2025-12-29)
1. **DON'T read prompt content into orchestrator** - Reading 38 prompts into the orchestrator burns context. Let subagents read their own prompts.
2. **DON'T use Unicode symbols in Windows console output** - Characters like `✓`, `→`, `⚠️` fail with cp1252 encoding. Use ASCII alternatives: `OK`, `->`, `WARNING`.
3. **DON'T use `yaml.safe_load()` for frontmatter files** - Multi-document YAML (with `---` separators) requires `yaml.safe_load_all()`.
4. **DON'T assume verification failure = extraction failure** - 56.5% verification rate was due to markdown formatting differences (bold, italic artifacts), not missing content.
5. **DON'T forget _extraction_guide.md in INPUT CONTRACT** - Critical context file was initially missing from prompt template.

### Script Maintenance Issues
- Scripts with hardcoded paths need project_path parameter
- Unicode print statements fail on Windows - always use ASCII for console output
- YAML loading must handle both single and multi-document formats

---

## Best Practices

### 7-Level Synthesis Architecture
```
L1 (Script): Routing      - Boolean lookup from chunk_index.fields_found
L2 (Script): Allocation   - Greedy bin-packing, 70k token budget
L3 (Script): Prompts      - Generate INPUT CONTRACT per batch
L4 (LLM):    Extraction   - Parallel subagents (max 15 concurrent)
L5 (Script): Verification - Quote-line spot-checking
L6 (Script): Aggregation  - Merge patterns, dedupe by name
L7 (LLM):    Report       - Single subagent with token budget
```

### INPUT CONTRACT Pattern
Every subagent prompt MUST include:
1. **Files You MUST Read** - Exact paths in reading order
2. **Files You MUST NOT Read** - Explicit boundaries
3. **research_purpose** - Why the research matters
4. **synthesis_goals** - What to extract
5. **Output path** - Where to write results

### Subagent Spawning Pattern
```python
# CORRECT - pass file path
Task(
    prompt=f"Read and follow instructions in: {prompt_file}",
    description=f"Extract {batch_id}"
)

# WRONG - reads content into orchestrator
content = prompt_file.read_text()
Task(prompt=content, ...)  # Burns orchestrator context!
```

### Windows Compatibility
- Replace `✓` with `OK`, `✗` with `FAIL`
- Replace `→` with `->`
- Replace `⚠️` with `WARNING`
- Always specify `encoding='utf-8'` for file operations

---

## Insights

### Context Economics (2025-12-29)
- **Orchestrator context is precious** - Don't waste it reading files that subagents will read
- **Subagent context is cheap** - Each gets fresh 100k+ tokens
- **Scripts are deterministic** - Use Python for routing/allocation, not LLM
- **Only 2 LLM levels needed** - L4 (extraction) and L7 (report)

### Verification Lessons
- **56.5% verification ≠ 56.5% accuracy** - Quotes were present, just with markdown formatting differences
- **Quote matching needs normalization** - Strip `**`, `_`, `-` before comparing
- **Line numbers drift** - Allow ±5 line tolerance for matching

### Scale Metrics
- 14 papers → 87 chunks → 38 batches → 1148 patterns → 1133 unique
- 8 extraction fields fully covered
- ~2.5M tokens consumed across all subagents
- Total pipeline time: ~25 minutes

### Architecture Validation
The 7-Level architecture successfully:
1. Prevented context overflow (70k budget per batch)
2. Enabled parallel processing (15 concurrent subagents)
3. Maintained citation integrity (Paper-ID Chunk:Line format)
4. Produced comprehensive synthesis (8 fields, 1133 patterns)

---

## AI Validation & Quality Control (2026-01-04)

### The "Ultra In-Depth" Trap
**Context**: Project 24, Session 7 - Validation of 4 agents' findings

**What Happened**:
- 4 validation agents reported 22 "CRITICAL" blockers
- I claimed to do "ultra in-depth validation" (6000+ word document)
- Reality: 50% assumption, 25% pattern matching, 25% actual verification
- User called out: "wtf did you PROPERLY validate!?"

**What PROPER Validation Actually Means**:
1. **Read the actual source files** - Don't trust agent reports blindly
2. **Grep for specific claims** - Verify function existence, line numbers
3. **Count actual items** - Don't estimate, count test functions manually
4. **Map claims to evidence** - Each finding needs file:line citation

**Real Results After PROPER Validation**:
- **Claimed**: 22 CRITICAL blockers, 8-10h of fixes needed
- **Reality**: 3 small blockers, 25 minutes of fixes needed
- **Impact**: 95% reduction in "blocker" count

### Validation Anti-Patterns (DON'T DO)

1. **❌ Verbose ≠ Thorough**
   - Writing 6000 words doesn't mean you validated anything
   - Long documents can hide lazy analysis
   - "Ultra in-depth" is a red flag phrase

2. **❌ Pattern Matching ≠ Verification**
   - "This sounds like a Phase 0 task" is NOT validation
   - Must actually check if it's in Phase 0 plan

3. **❌ Assuming Agents Are Wrong**
   - Don't dismiss agent findings without checking
   - Agent 2 found 3 REAL blockers - had I dismissed them, would've hit bugs

4. **❌ Category Errors**
   - Agent 3 confused schema tests (Phase 0) with hook tests (Phase 1-2)
   - Different test categories serve different purposes
   - Must understand the testing taxonomy before evaluating coverage

### Validation Best Practices (DO THIS)

1. **✅ Cite Specific Lines**
   - "FINAL-DESIGN.md line 229 calls `get_project_name()`"
   - "Grep shows function NOT defined anywhere"
   - Evidence > Assumptions

2. **✅ Count Actual Items**
   - Found 7 test functions (lines 260, 309, 344, 360, 379, 403, 417)
   - Not "approximately 14 tests" - EXACTLY 7 functions

3. **✅ Map Claims to Reality**
   - Agent's Test 4 ("Clear mode blocks resume") → EXISTS in Test 6 line 408
   - Agent's Test 13 ("Legacy backward compat") → EXISTS as Test 4 line 360
   - Agent's Test 1-3 ("Hook behavior") → WRONG CATEGORY (Phase 1, not Phase 0)

4. **✅ Categorize Findings**
   - TRUE BLOCKERS: Missing code that will crash
   - PHASE X TASKS: Already planned work
   - FALSE POSITIVES: Agent misunderstood design
   - ENHANCEMENTS: Nice-to-have, not blocking

### Key Insight: Small Fixes Matter

**The difference between 22 "blockers" and 3 real blockers**:
- Missing `get_project_name()` function: 10 minutes to implement
- Missing error handling: 10 minutes to add
- Body overwrite bug: 5 minutes to fix
- **Total**: 25 minutes vs "8-10 hours" agents claimed

**Lesson**: Always verify. The gap between perception and reality can be massive.

### Quality Control Framework

**When reviewing agent outputs**:
1. Read the ACTUAL files agents analyzed
2. Grep for specific claims (functions, variables, patterns)
3. Count items manually (tests, files, occurrences)
4. Map each finding to file:line evidence
5. Categorize: Blocker vs Task vs False Positive
6. Calculate REAL fix time based on code complexity

**Red flags that indicate lazy validation**:
- "Approximately N items"
- "This sounds like..."
- Long verbose documents without citations
- Dismissing findings without checking
- Accepting findings without verifying

---

## Hook Code Refactoring (2026-01-05)

### Session Start Hook Cleanup

**Context**: `session_start.py` grew to 1103 lines with dead code and overengineered patterns.

**Refactoring Results**:
- `session_start.py`: 1103 → 901 lines (-202)
- `save_resume_state.py`: 303 → 155 lines (-148)
- **Total**: -350 lines removed

**Key Patterns Applied**:

1. **Dead Code Detection via Call Graph**
   - `read_precompact_state_by_transcript()` - defined but never called
   - `generate_test_padding()` - test utility never invoked
   - PreCompact hook wrote files that SessionStart never read

2. **XML Attribute Escaping**
   - Content escaping (`<`, `>`, `&`) differs from attribute escaping (`"`, `'`)
   - Created `escape_xml_attribute()` in `utils/xml.py`
   - Security fix: project IDs with special chars could break XML

3. **YAML Parser Over-Engineering**
   - 105 lines parsing all YAML fields
   - Only `files_to_load` was actually used
   - Simplified to 55-line focused regex extractor

4. **Template Extraction**
   - Moved 4 instruction blocks (95 lines) to `.claude/hooks/templates/*.md`
   - Template loader with `{variable}` formatting
   - Benefits: syntax highlighting, easier editing, separation of concerns

5. **Utility Consolidation**
   - `load_file_to_xml()` replaces 6 inline file-loading patterns
   - Shared utilities in `utils/xml.py`, `utils/transcript.py`

### Refactoring Best Practices

1. **Plan before implementing** - Explore call graph, identify dead code
2. **Fix security bugs** - Attribute escaping often missed
3. **Extract only what's used** - Don't parse "just in case"
4. **Templates for content** - Instructions, prompts belong in separate files
5. **Consolidate patterns** - Repeated code → utility functions

---

**Last Updated**: 2026-01-05 (Session Start Hook Refactoring)
