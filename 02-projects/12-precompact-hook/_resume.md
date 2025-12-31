---
updated: "2025-12-31T01:45:00"
phase: "planning"
last_skill: "execute-project"
project_id: "12-precompact-hook"
---

# Resume Context

## Knowledge Dump - Session 2025-12-31

### Was heute gemacht wurde (Nexus Loader Improvements)

1. **Cache System implementiert** (`nexus-loader.py`, `config.py`)
   - Output > 30k chars → schreibt nach `00-system/.cache/context_startup.json`
   - Gibt kurzen JSON zurück mit `next_step: "READ THIS FILE NOW: ..."`

2. **Resume Loading Sequence** (`state.py`)
   - `--resume` gibt jetzt `EXECUTE_MANDATORY_LOADING_SEQUENCE` zurück
   - 3-Schritt Sequenz: Cache lesen → Skill laden → Projekt laden
   - `STOP: "🛑 DO NOT CONTINUE WORKING WITHOUT LOADING CONTEXT FIRST"`
   - `FAILURE_CONSEQUENCES` Array erklärt was passiert ohne Loading

3. **Skill Detection aus `_resume.md`**
   - Liest `phase` und `last_skill` aus YAML frontmatter
   - Mappt Phase zu Skill: analysis→analyze-research-project, synthesis→synthesize-research-project
   - Keine Keywords mehr - alles explizit

4. **CLAUDE.md vereinfacht**
   - Nur noch: "Run loader, follow its instructions"
   - Instruktion für AI: Update `_resume.md` vor Context-Ende

### Commits heute
```
e7c566e Use _resume.md for skill/phase detection instead of keywords
b0f56b2 Read _resume.md to determine correct skill for resume
a2f8a83 Add research project detection for resume loading
1e2772e Enforce mandatory context loading on resume
0bf2c27 Add cache system for large loader outputs + resume loading sequence
```

### Nächstes Projekt: PreCompact Hook

**Ziel**: Automatisch `_resume.md` aktualisieren bevor Context kompaktiert wird

**Dateien zu erstellen**:
1. `.claude/settings.json` - Hook-Konfiguration
2. `.claude/hooks/save-resume-state.py` - Script das:
   - Transcript parst für letzten Skill
   - Aktives Projekt aus Cache liest
   - `_resume.md` schreibt

**Hook Config**:
```json
{
  "hooks": {
    "PreCompact": [{
      "hooks": [{
        "type": "command",
        "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/save-resume-state.py\"",
        "timeout": 10
      }]
    }]
  }
}
```

**Script Input** (stdin JSON):
```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../xxx.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "auto" | "manual"
}
```

**Script Logic**:
1. JSON von stdin lesen
2. `context_startup.json` laden für aktives Projekt
3. Transcript JSONL parsen für `--skill X` Pattern
4. Phase aus Skill ableiten
5. `_resume.md` schreiben

### Wichtige Dateipfade
- Cache: `00-system/.cache/context_startup.json`
- Resume: `02-projects/{id}/_resume.md`
- State Logic: `00-system/core/nexus/state.py` (build_instructions, Zeile 137-262)
- Config: `00-system/core/nexus/config.py` (CACHE_DIR, CACHE_STARTUP_FILE)
- Loader: `00-system/core/nexus-loader.py` (main(), Zeile 165-202)
