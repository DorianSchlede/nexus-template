# Dokumentation des Forschungsalgorithmus

> Umfassende Dokumentation der Nexus Research Pipeline zur Analyse und Synthese akademischer Paper.

---

## Uebersicht

Der Nexus Forschungsalgorithmus ist eine ausgefeilte mehrphasige Pipeline, die die Entdeckung, Beschaffung, Analyse und Synthese akademischer Paper automatisiert. Er besteht aus **9 miteinander verbundenen Skills**, die zusammenarbeiten, um eine Forschungsfrage in umsetzbare Erkenntnisse zu transformieren.

---

## Systemarchitektur

```mermaid
graph TB
    subgraph "Phase 1: Planung & Beschaffung"
        CRP[create-research-project] --> PS[paper-search]
        PS --> PP[pdf-preprocess]
    end

    subgraph "Phase 2: Analyse & Synthese"
        ERP[execute-research-project] --> PA[paper-analyze]
        PA --> PAC[paper-analyze-core]
        PA --> PSY[paper-synthesize]
    end

    subgraph "Hilfs-Skills"
        PQ[paper-query]
        PM[paper-manage]
    end

    CRP --> ERP
    PP --> PA
    PSY --> PQ
    PM --> CRP
    PM --> ERP

    style CRP fill:#4CAF50,color:white
    style ERP fill:#2196F3,color:white
    style PAC fill:#FF9800,color:white
```

---

## Vollstaendiger Prozessablauf

```mermaid
flowchart TD
    Start([Benutzer: Forschungsfrage]) --> Init[Projekt initialisieren]

    subgraph Phase1["Phase 1: Planung & Beschaffung"]
        Init --> Define[Forschungsfrage definieren]
        Define --> Brief[_briefing.md erstellen]
        Brief --> Search[Akademische APIs durchsuchen]
        Search --> Results[_search_results.md]
        Results --> Review[KI Abstract-Bewertung]
        Review --> Abstract[_abstract_reviews.md]
        Abstract --> Select[Benutzer Paper-Auswahl]
        Select --> Gate1{Auswahl-Gate}
        Gate1 -->|Genehmigt| Download[Paper herunterladen]
        Gate1 -->|Aendern| Select
        Download --> Preprocess[PDF zu Markdown Chunks]
        Preprocess --> Kit[Analyse-Kit generieren]
        Kit --> Ready{Bereitschafts-Gate}
    end

    subgraph Phase2["Phase 2: Analyse & Synthese"]
        Ready -->|Bereit| Validate1[Bereitschaft validieren]
        Validate1 --> Analyze[Analyse-Subagenten starten]
        Analyze --> Index[index.md pro Paper]
        Index --> Validate2[Analyse-Logs validieren]
        Validate2 --> Synth[Synthese generieren]
        Synth --> Validate3[Synthese validieren]
        Validate3 --> Complete[Projekt abschliessen]
    end

    Complete --> End([Forschungsergebnisse])

    style Phase1 fill:#E8F5E9
    style Phase2 fill:#E3F2FD
```

---

## Skills-Uebersicht

### Kern-Skills

| Skill | Zweck | Trigger-Schluesselwoerter |
|-------|-------|---------------------------|
| `create-research-project` | Phase 1 Orchestrator | "create research project", "new research" |
| `execute-research-project` | Phase 2 Orchestrator | "execute research project", "run analysis" |
| `paper-search` | 9 akademische APIs durchsuchen | "find paper", "search paper" |
| `pdf-preprocess` | PDFs zu Markdown konvertieren | "preprocess pdf", "chunk pdf" |
| `paper-analyze` | Paper-Analyse orchestrieren | "analyze papers", "process papers" |
| `paper-analyze-core` | Analyse-Methodik | *Nur interne Verwendung* |
| `paper-synthesize` | Paper-uebergreifende Synthese | "synthesize collection" |
| `paper-query` | Analysierte Paper abfragen | "query papers", "find papers about" |
| `paper-manage` | Sammlungen verwalten | "list collections", "paper stats" |

---

## Phase 1: Planung & Beschaffung

### Workflow-Diagramm

```mermaid
sequenceDiagram
    participant B as Benutzer
    participant CRP as create-research-project
    participant PS as paper-search
    participant PP as pdf-preprocess

    B->>CRP: "Starte Forschung zu [Thema]"
    CRP->>CRP: Projektstruktur erstellen
    CRP->>B: Forschungsfrage anfordern
    B->>CRP: FF + Extraktionsschema definieren
    CRP->>CRP: _briefing.md erstellen

    CRP->>PS: Akademische APIs durchsuchen
    PS->>PS: 9 APIs abfragen (S2, OpenAlex, arXiv...)
    PS->>CRP: _search_results.md zurueckgeben

    CRP->>CRP: KI Abstract-Bewertung
    CRP->>B: Paper-Empfehlungen praesentieren
    B->>CRP: Auswahl genehmigen/aendern
    CRP->>CRP: _selection_log.md erstellen

    CRP->>PS: Genehmigte Paper herunterladen
    PS->>PS: Multi-Source Fallback-Aufloesung
    PS->>CRP: PDFs zurueckgeben

    CRP->>PP: PDFs vorverarbeiten
    PP->>PP: Zu Markdown-Chunks konvertieren
    PP->>CRP: Chunks + _metadata.json zurueckgeben

    CRP->>CRP: _analysis_kit.md generieren
    CRP->>B: Bereitschafts-Gate
```

### Schritt-Details

#### Schritt 1-3: Forschungsdefinition
- Nexus-Projektstruktur erstellen
- Interaktive Definition der Forschungsfrage
- `_briefing.md` mit Extraktionsschema erstellen

#### Schritt 4-6: Paper-Auswahl
- KI bewertet Abstracts mit Punktzahl (1-5)
- Domaenen-Uebereinstimmung, FF-Passung, Methodik-Relevanz, Aktualitaet
- Benutzer genehmigt finale Auswahl

#### Schritt 7-9: Beschaffung
- Automatisierter Batch-Download mit Fallback
- URL-Prioritaet: arXiv > Semantic Scholar > Unpaywall > Direkt
- PDF-Vorverarbeitung zu Markdown-Chunks (max. 1000 Zeilen/Chunk)

---

## Phase 2: Analyse & Synthese

### Workflow-Diagramm

```mermaid
sequenceDiagram
    participant B as Benutzer
    participant ERP as execute-research-project
    participant PA as paper-analyze
    participant PAC as paper-analyze-core
    participant PSY as paper-synthesize

    B->>ERP: "Execute research project"
    ERP->>ERP: Bereitschaft validieren

    loop Fuer jedes Paper (max. 3 parallel)
        ERP->>PA: Subagent starten
        PA->>PAC: Methodik laden
        PAC->>PAC: 7-Schritt-Analyse
        PAC->>PA: index.md + _analysis_log.md zurueckgeben
    end

    PA->>ERP: Alle Analysen abgeschlossen
    ERP->>ERP: Analyse-Logs validieren

    ERP->>PSY: Synthese generieren
    PSY->>PSY: Alle index.md Frontmatter lesen
    PSY->>PSY: Nach Extraktionsfeld aggregieren
    PSY->>ERP: _synthesis.md zurueckgeben

    ERP->>ERP: Synthese validieren
    ERP->>B: Projekt abgeschlossen
```

### Analyse-Methodik (7 Schritte)

```mermaid
graph LR
    S0[Schritt 0: Log initialisieren] --> S1[Schritt 1: Briefing lesen]
    S1 --> S2[Schritt 2: Metadaten lesen]
    S2 --> S3[Schritt 3: Chunks analysieren]
    S3 --> S4[Schritt 4: index.md kompilieren]
    S4 --> S5[Schritt 5: Validieren]
    S5 --> S6[Schritt 6: Log abschliessen]

    style S0 fill:#FFF3E0
    style S3 fill:#E8F5E9
    style S6 fill:#E3F2FD
```

#### Anti-Halluzinations-Massnahmen
- **3-Punkt-Evidenz-Aufzeichnung**: Start (100 Zeichen), Mitte (100 Zeichen), Ende (100 Zeichen)
- **SHA256-Hash**: Vollstaendige Chunk-Inhaltsverifizierung
- **Chunk:Zeilen-Referenzen**: Jede Extraktion muss Quellposition zitieren

---

## Datenfluss-Architektur

```mermaid
graph TB
    subgraph Eingabe
        RQ[Forschungsfrage]
        APIs[9 Akademische APIs]
        PDFs[PDF Paper]
    end

    subgraph Verarbeitung
        Brief[_briefing.md]
        Search[_search_results.md]
        Reviews[_abstract_reviews.md]
        Select[_selection_log.md]
        Kit[_analysis_kit.md]
    end

    subgraph Analyse
        Meta[_metadata.json]
        Chunks[Paper-Chunks]
        Log[_analysis_log.md]
        Index[index.md]
    end

    subgraph Ausgabe
        Synth[_synthesis.md]
        Valid[_validation_report.md]
        Quality[_quality_metrics.md]
    end

    RQ --> Brief
    APIs --> Search
    Search --> Reviews
    Reviews --> Select
    Select --> Kit
    PDFs --> Meta
    PDFs --> Chunks
    Chunks --> Log
    Log --> Index
    Index --> Synth
    Index --> Valid
    Valid --> Quality
```

---

## Projektstruktur

```
02-projects/NN-{slug}/
├── 01-planning/
│   ├── overview.md          # Projekt-Metadaten
│   ├── plan.md              # Orchestrator-Anweisungen
│   └── steps.md             # Fortschritts-Checkboxen
├── 02-resources/
│   ├── _briefing.md         # Forschungsfrage + Schema
│   ├── _analysis_kit.md     # Subagent-Kontext
│   ├── _search_results.md   # API-Suchergebnisse
│   ├── _abstract_reviews.md # KI-Bewertungen
│   └── papers/
│       └── {paper}/
│           ├── {paper}.pdf
│           ├── {paper}_1.md, _2.md, ...
│           ├── _metadata.json
│           ├── _analysis_log.md
│           └── index.md
├── 03-working/
│   └── _selection_log.md    # Genehmigte Paper
└── 04-outputs/
    ├── _synthesis.md        # Paper-uebergreifende Synthese
    ├── _validation_report.md
    └── _quality_metrics.md
```

---

## Validierungssystem

### Drei-Stufen-Validierung

```mermaid
graph TD
    subgraph Stufe1["Stufe 1: Analyse-Validierung"]
        A1[Schema-Version pruefen]
        A2[Schritt-Vollstaendigkeit pruefen]
        A3[Chunk-Evidenz verifizieren]
        A4[Hash-Validierung]
    end

    subgraph Stufe2["Stufe 2: Log-Validierung"]
        B1[Alle Chunks gelesen?]
        B2[Evidenz stimmt mit Inhalt ueberein?]
        B3[index.md erstellt?]
    end

    subgraph Stufe3["Stufe 3: Synthese-Validierung"]
        C1[Frontmatter vollstaendig?]
        C2[Paper-Referenzen existieren?]
        C3[Stichproben-Behauptungen pruefen]
        C4[Abdeckung >= 70%?]
    end

    A1 --> A2 --> A3 --> A4
    B1 --> B2 --> B3
    C1 --> C2 --> C3 --> C4

    Stufe1 --> Stufe2 --> Stufe3
```

### Validierungsschwellenwerte

| Metrik | Bestanden | Warnung | Fehlgeschlagen |
|--------|-----------|---------|----------------|
| Frontmatter-Vollstaendigkeit | 100% | <100% | Erforderliche fehlen |
| Paper-Referenz-Genauigkeit | 100% | >90% | <90% |
| Stichproben-Verifizierung | >90% | 70-90% | <70% |
| Abdeckung | >80% | 60-80% | <60% |

---

## Paper-Abfragesystem

### 3-Stufen Progressive Offenlegung

```mermaid
graph TD
    Query[Benutzer-Abfrage] --> L1[Stufe 1: Frontmatter-Scan]
    L1 --> |Python-Skript| Results1[Sortierte Paper-Liste]
    Results1 --> L2[Stufe 2: Vollstaendiges Index-Lesen]
    L2 --> |KI| Results2[Relevante Chunks identifiziert]
    Results2 --> L3[Stufe 3: Chunk-Laden]
    L3 --> |KI| Answer[Antwort mit Zitaten]

    style L1 fill:#E8F5E9
    style L2 fill:#FFF3E0
    style L3 fill:#E3F2FD
```

### Ranking-Faktoren

| Faktor | Gewichtung | Quelle |
|--------|------------|--------|
| relevance_triggers Treffer | 3x | index.md YAML |
| topics Treffer | 2x | index.md YAML |
| methods Treffer | 2x | index.md YAML |
| key_findings Treffer | 1x | index.md YAML |
| Jahr (neuere bevorzugt) | 0.5x | index.md YAML |

---

## Akademische API-Abdeckung

```mermaid
pie title "API-Abdeckung (1 Mrd.+ Dokumente)"
    "OpenAlex" : 250
    "CORE" : 300
    "BASE" : 300
    "Semantic Scholar" : 200
    "CrossRef" : 130
    "PubMed" : 35
    "arXiv" : 2
    "DOAJ" : 9
```

| API | Dokumente | Optimal fuer |
|-----|-----------|--------------|
| Semantic Scholar | 200M+ | CS/KI, Zitationen |
| OpenAlex | 250M+ | Breite Akademie |
| arXiv | 2M+ | CS/Physik/Mathematik Preprints |
| CrossRef | 130M+ | DOI-Metadaten |
| PubMed | 35M+ | Biomedizin |
| CORE | 300M+ | UK/EU Forschung |
| BASE | 300M+ | Deutscher Aggregator |
| DOAJ | 9M+ | Verifizierte OA-Zeitschriften |
| Unpaywall | - | OA-PDF-Suche via DOI |

---

## Token-Budget-Verwaltung

```mermaid
graph LR
    subgraph "100k Kontext-Fenster"
        A[Methodik: 3k]
        B[Briefing: 2k]
        C[Metadaten: 0.5k]
        D[Log-Overhead: 3.5k]
        E[Paper-Inhalt: 74k]
        F[Ausgabe-Puffer: 17k]
    end

    style E fill:#4CAF50,color:white
```

### Behandlung grosser Paper

- Paper > 75k Tokens werden in Teile aufgeteilt
- Jeder Teil wird von separatem Subagent analysiert
- Merge-Subagent kombiniert Teil-Indizes
- Finaler vereinheitlichter index.md wird generiert

---

## Fehlerbehandlung

### Nach Phase

| Phase | Fehler | Aktion |
|-------|--------|--------|
| Suche | API Rate-Limit | Warten und wiederholen |
| Download | Alle kostenpflichtig | arXiv-Alternativen vorschlagen |
| Vorverarbeitung | PDF beschaedigt | Ueberspringen, Fehler protokollieren |
| Analyse | Subagent schlaegt fehl | Einmal wiederholen, dann Fehler protokollieren |
| Validierung | Evidenz-Mismatch | Erneut analysieren oder ausschliessen |
| Synthese | <3 Paper | Vor begrenzter Synthese warnen |

---

## Versionshistorie

| Version | Datum | Aenderungen |
|---------|-------|-------------|
| 4.0 | 2025-12-19 | Analyse-Kit, Orchestrator-Templates, Phase 4.5 Validierung hinzugefuegt |
| 2.2 | 2025-12-19 | Chunk:Zeilen Extraktions-Tracking, Zwei-Stufen-Detail-Strategie hinzugefuegt |
| 2.1 | 2025-12-19 | 3-Punkt Anti-Halluzinations-Sampling hinzugefuegt |
| 2.0 | 2025-12-19 | Planung/Beschaffung von Analyse/Synthese getrennt |

---

**Zuletzt aktualisiert**: 2025-12-27
