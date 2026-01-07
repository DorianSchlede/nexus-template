# Key Learnings - Integrated Subagent Testing System

**Project 41** | Last Updated: 2026-01-07

---

## 1. Custom subagent_type is BROKEN

**Problem**: Custom `subagent_type` values (like `test-orchestrator`, `test-case-analyzer`) don't work reliably.

**Solution**: Use `general-purpose` with a two-step prompt pattern.

**Pattern**:
```python
Task(
    subagent_type="general-purpose",  # NOT custom types!
    model="sonnet",
    prompt="""
FIRST: Read the instructions from:
{path_to_prompt_file}

THEN: Execute this request:
{actual_task}
"""
)
```

---

## 2. Skill Structure for Subagent Skills

**Pattern**: Separate orchestration logic from subagent instructions.

```
validate-feature/
├── SKILL.md                           # Orchestration logic
├── scripts/
│   ├── run-tests.py                   # Main runner
│   ├── fetch-traces.py                # Trace collection
│   └── worktree-manager.py            # Isolation
└── prompts/
    ├── test-orchestrator-prompt.md    # Subagent instructions
    └── test-case-analyzer-prompt.md   # Subagent instructions
```

**Why**:
- Prompts can be updated without changing code
- Subagents read full instructions at runtime
- Cleaner separation of concerns

---

## 3. Two-Step Prompt Loading

**Pattern**: Tell subagent to read prompt file first, then execute task.

```python
prompt = f"""
FIRST: Read the orchestrator instructions from:
{prompt_file_path}

WORKDIR: {worktree_path}

THEN: Execute this user request:
{scenario_prompt}
"""
```

**Benefits**:
- Subagent gets full context
- Prompt file can be large without bloating Task call
- Easy to update instructions without changing code

---

## 4. Task Config Output Format

**Old pattern** (just prompt string):
```json
{
  "prompts": ["spawn test-orchestrator\n\nDo X"]
}
```

**New pattern** (full Task parameters):
```json
{
  "task_configs": [
    {
      "subagent_type": "general-purpose",
      "model": "sonnet",
      "prompt": "FIRST: Read...\nTHEN: Do X",
      "description": "Test run 0 for scenario"
    }
  ],
  "invocation_pattern": "general-purpose with two-step prompt"
}
```

---

## 5. Score Comments are Unlimited

**Discovery**: Langfuse score comments can be 10,000+ characters.

**Implication**: Can store full analysis, evidence, and recommendations in score comments.

---

## 6. From Project 34 (Inherited)

These patterns from Project 34 remain valid:

1. **Worktree isolation** - Always use git worktrees for test isolation
2. **Retry with exponential backoff** - 5s, 10s, 15s for Langfuse ingestion
3. **GET /traces/{id} for observations** - List API doesn't include them
4. **Absolute paths** - Use `Path.resolve()` for worktree paths
5. **Subagents don't know they're tested** - Authentic behavior

---

## File Locations

| File | Purpose |
|------|---------|
| `prompts/test-orchestrator-prompt.md` | Instructions for test execution |
| `prompts/test-case-analyzer-prompt.md` | Instructions for trace analysis |
| `scripts/run-tests.py` | Generates Task configs with two-step pattern |

---

*These learnings apply to all subagent-based skills, not just validate-feature.*
