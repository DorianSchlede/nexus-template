---
id: 12-precompact-hook
name: PreCompact Hook für Resume-State
status: IN_PROGRESS
description: Load when user mentions 'precompact hook', 'auto resume', 'context preservation', 'save state before compact'
created: 2025-12-31
---

# PreCompact Hook für automatische Resume-State Persistierung

## Problem
Wenn Context voll wird und kompaktiert wird, verliert Claude den aktiven Skill/Phase. Die `_resume.md` muss manuell aktualisiert werden - das passiert oft nicht.

## Lösung
Ein Claude Code Hook der **automatisch vor jeder Kompaktierung** die `_resume.md` aktualisiert.

## Technische Details

### Hook Event: PreCompact
- Triggers: `manual` (/compact) und `auto` (context voll)
- Input: JSON mit `transcript_path`, `session_id`, `trigger`
- Timeout: 10 Sekunden

### Was der Hook tut
1. Liest `00-system/.cache/context_startup.json` für aktives Projekt
2. Parsed Transcript für letzten `--skill` Aufruf
3. Schreibt `_resume.md` im Projekt-Ordner

### Dateien
```
.claude/
├── settings.json          # Hook-Konfiguration
└── hooks/
    └── save-resume-state.py  # Hook-Script
```

## Warum das wichtig ist
- **Automatisch**: Kein manuelles Update nötig
- **Zuverlässig**: Wird IMMER vor Compact ausgeführt
- **Nahtlos**: User merkt nichts, Resume funktioniert einfach
