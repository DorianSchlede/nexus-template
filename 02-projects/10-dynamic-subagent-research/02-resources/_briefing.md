---
research_question: "Wie können strukturierte Handover-Protokolle die Datenqualität bei LLM-Subagent-Interaktionen verbessern?"
research_purpose: "Wissenschaftliche Analyse der entwickelten Dynamic Subagent Patterns für High-Quality Data Transfer. Ziel: Pattern-Catalog, Best-Practice Guidelines, und akademische Publikation."
domain: "multi_agent"
schema_version: "2.3"
focus_areas:
  - LLM multi-agent coordination
  - Subagent communication protocols
  - Data quality verification
  - Prompt engineering for extraction
  - Information loss prevention
skip_sections: ["Acknowledgments", "Author Contributions", "Funding", "References"]
extraction_fields:
  # Pattern-Identifikation
  - name: pattern_definition
    description: "Definition eines Handover-Patterns mit Namen, Zweck, und Mechanismus"
    type: object
    examples:
      - "3-Point Evidence: start (100 chars) + mid (100 chars) + end (100 chars)"
      - "Hash Chain: SHA256 verification at each transfer"
      - "Ticket-based Handover: Input Manifest + Output Contract + Completion Receipt"

  - name: mechanism_type
    description: "Art des Mechanismus"
    type: enum
    vocabulary:
      - verification  # Prüft ob etwas korrekt ist
      - enforcement   # Erzwingt ein bestimmtes Verhalten
      - detection     # Erkennt Probleme/Fehler
      - prevention    # Verhindert Probleme im Voraus

  - name: failure_mode
    description: "Was passiert wenn das Pattern verletzt wird"
    type: string
    examples:
      - "Output REJECTED"
      - "Warning issued, continue"
      - "Retry with stricter constraints"

  # Implementierung
  - name: implementation_detail
    description: "Konkrete Code-Implementierung (Funktion, Klasse, Datenstruktur)"
    type: object
    examples:
      - "def extract_reading_proof(file_path: Path) -> ReadingProof"
      - "class HandoverManager"
      - "@dataclass ReadingProof"

  - name: integration_point
    description: "Wo im Pipeline wird das Pattern angewendet"
    type: enum
    vocabulary:
      - prompt_generation   # Beim Erstellen des Subagent-Prompts
      - execution          # Während der Subagent-Ausführung
      - verification       # Nach der Ausführung zur Prüfung
      - handover           # Beim Transfer zwischen Komponenten

  # Evaluation
  - name: quality_metric
    description: "Messbare Qualitätsmetriken die das Pattern beeinflusst"
    type: object
    examples:
      - "Verification rate > 90%"
      - "Hash mismatch < 5%"
      - "Citation accuracy > 95%"

  - name: limitation
    description: "Bekannte Einschränkungen oder Nachteile des Patterns"
    type: string
    examples:
      - "Erhöht Token-Verbrauch um ~500 tokens"
      - "Funktioniert nicht bei sehr kurzen Chunks"
      - "Erfordert deterministische Hash-Berechnung"

  # Kontext
  - name: related_pattern
    description: "Andere Patterns die mit diesem zusammenhängen"
    type: array
    examples:
      - "Ticket-based → Hash-Chain (Dependency)"
      - "3-Point Evidence → Spot-Check (Alternative)"

sub_questions:
  - id: RQ1
    question: "Forced Reading - Verhindert 3-Point Evidence tatsächlich Skimming?"
    focus_fields: [pattern_definition, mechanism_type, quality_metric]
  - id: RQ2
    question: "Hash Verification - Wie hoch ist die Detection-Rate bei inkompletten Reads?"
    focus_fields: [implementation_detail, quality_metric, failure_mode]
  - id: RQ3
    question: "Domain Personas - Verbessern spezialisierte Personas die Extraktionsqualität?"
    focus_fields: [pattern_definition, integration_point, limitation]
  - id: RQ4
    question: "ULTRASEARCH Protocol - Reduziert Ticket-based Handover den Information Loss?"
    focus_fields: [pattern_definition, mechanism_type, related_pattern]
---

# Research Briefing: Dynamic Subagent Handover Patterns

## Forschungskontext

Diese Forschung analysiert intern entwickelte Patterns für High-Quality Data Transfer in LLM-Subagent-Systemen. Die Dokumentation umfasst:

- **2 Dokumentationsdateien**: System README und ULTRASEARCH Patterns
- **5 Code-Module**: Factory, Forced Reading, Generator, Verifier, Handover Manager

## Extraktion Guidelines

### Pattern-Identifikation

Für jedes identifizierte Pattern dokumentiere:
1. **Name**: Eindeutiger Bezeichner (z.B. "3-Point Evidence")
2. **Zweck**: Was das Pattern erreichen soll
3. **Mechanismus-Typ**: verification/enforcement/detection/prevention
4. **Implementation**: Code-Referenz mit Chunk:Line

### Zitierformat

Verwende: `Resource-Name (Chunk N:Line-Line)`

Beispiele:
- `README (Chunk 1:42-48)` für Dokumentation
- `factory_py (Chunk 1:137-168)` für Code

### Quality Criteria

- Jede Extraktion muss Quellenangabe haben
- Quotes müssen 50-150 Zeichen sein
- Alle 7 Ressourcen müssen analysiert werden
- Mindestens 5 Patterns pro Hauptdokument

## Ressourcen-Übersicht

| ID | Ressource | Typ | Tokens (est.) | Priorität |
|----|-----------|-----|---------------|-----------|
| readme_md | README.md | Docs | ~3,300 | HIGH |
| ultrasearch_md | ULTRASEARCH_HANDOVER_PATTERNS.md | Docs | ~5,700 | HIGH |
| factory_py | dynamic_subagent_factory.py | Code | ~6,500 | HIGH |
| forced_reading_py | forced_reading_contract.py | Code | ~4,000 | HIGH |
| generator_py | generate_dynamic_research_subagent.py | Code | ~3,600 | MEDIUM |
| verifier_py | verify_subagent_reading.py | Code | ~4,700 | MEDIUM |
| handover_py | handover_manager.py | Code | ~6,000 | MEDIUM |

**Total**: ~33,800 tokens
