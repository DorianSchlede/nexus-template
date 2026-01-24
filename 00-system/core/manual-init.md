# NEXUS MANUAL INITIALIZATION

⚠️ **Use this only when the SessionStart hook fails to load automatically.**

This happens when:
- Using Claude outside of Claude Code extension (web, API, other tools)
- Hook system is disabled or malfunctioning
- VSCode extension is not installed

---

## Manual Loading Sequence

### Execute the Nexus Loader (Same as SessionStart Hook)

The SessionStart hook calls Python functions from the nexus loader. Do the same:

**Step 1: Run the loader script**
```bash
python3 -c "
import sys
sys.path.insert(0, '00-system/core')
from nexus.loaders import load_full_startup_context
context = load_full_startup_context('.')
print(context)
"
```

**Step 2: Read the output and follow the instructions**

The loader will output the complete startup context including:
- Orchestrator instructions
- User goals
- Active builds
- Available skills
- Next action (display_menu or continue_working)

---

## Quick Copy-Paste Template

```markdown
I'm initializing Nexus manually. Please run:

python3 -c "
import sys
sys.path.insert(0, '00-system/core')
from nexus.loaders import load_full_startup_context
print(load_full_startup_context('.'))
"

Then follow the instructions from the output.
```

---

## Why Hook System is Preferred

The SessionStart hook provides:
- ✅ **Automatic** workspace detection (multi-window safe)
- ✅ **Automatic** build detection and resume
- ✅ **Automatic** skill routing
- ✅ **Safety checks** (rm, git, .env protections)
- ✅ **Workspace isolation** (prevents cross-contamination)

Manual initialization:
- ❌ Requires manual steps each session
- ❌ No automatic build resume
- ❌ No safety protections
- ❌ No workspace validation
- ❌ Error-prone

---

## For Developers

To replicate hook behavior programmatically:

### Python API Example
```python
from pathlib import Path
import anthropic

class NexusSession:
    def __init__(self, workspace_path: str):
        self.workspace = Path(workspace_path)
        self.client = anthropic.Anthropic()

    def initialize(self):
        # Load orchestrator
        orchestrator = (self.workspace / "00-system/core/orchestrator.md").read_text()

        # Load goals
        goals = (self.workspace / "01-memory/goals.md").read_text()

        # Detect active builds
        builds_dir = self.workspace / "02-builds"
        active_build = None
        for build in builds_dir.iterdir():
            if build.is_dir() and not build.name.startswith(("_", ".")):
                resume_file = build / "01-planning/resume-context.md"
                if resume_file.exists():
                    active_build = build.name
                    break

        # Build system prompt
        system_prompt = f"{orchestrator}\n\n# User Goals\n{goals}"

        if active_build:
            overview = (builds_dir / active_build / "01-planning/01-overview.md").read_text()
            system_prompt += f"\n\n# Active Build: {active_build}\n{overview}"

        return system_prompt
```

### Claude Projects (claude.ai)
```yaml
# Add to Project Custom Instructions:
You are operating in a Nexus environment.

On every session start:
1. Read 00-system/core/orchestrator.md
2. Read 01-memory/goals.md
3. Scan 02-builds/ for active builds
4. Load build context if found, otherwise display menu
```

---

## Troubleshooting

**Hook not loading?**
- Check `.claude/hooks/session_start.py` exists
- Check Python 3.8+ is installed
- Check hook file permissions (should be executable)
- Check logs at `00-system/.cache/session_start_output.log`

**Wrong workspace loaded?**
- This only happens with hooks enabled
- See multi-window fixes in SessionStart hook
- Manual mode doesn't have this issue (but has no workspace detection at all)

**Build not resuming?**
- Check `02-builds/{build-id}/01-planning/resume-context.md` exists
- Verify `session_id` field matches current session (hook only)
- Manual mode requires you to manually select the build

---

## Version History

- **v1.0** (2026-01-23): Initial manual initialization guide
  - Added after removing observability server
  - Added after implementing multi-window workspace fixes
