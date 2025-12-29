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

**Last Updated**: 2025-12-29 (Project 10 Synthesis Complete)
