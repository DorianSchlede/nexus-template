# Lead Scoring Rubrik Template

> **Source**: Best Practices Research (December 2024)
> **Usage**: Lade diese Ressource wenn du das Scoring-System aufsetzt

---

## Traffic Light System

| Score | Status | Aktion |
|-------|--------|--------|
| **80-100** | 🟢 GRÜN | Sofort kontaktieren, Top-Priorität |
| **60-79** | 🟡 GELB | Nurturing, weitere Qualifikation |
| **0-59** | 🔴 ROT | Deprioritize oder Disqualify |

**Benchmark**: Companies with robust ICPs have **68% higher account win rates** (TOPO/Gartner).

---

## Scoring Matrix

### FIRMOGRAPHICS (Max 40 Punkte)

```
□ Industry Match:           ___/15 Punkte
  - Exakt passend: 15
  - Teilweise passend: 10
  - Nicht passend: 0

□ Company Size:             ___/15 Punkte
  - 100-500 MA: 15
  - 50-99 oder 501-1000: 10
  - <50 oder >1000: 5
  - Komplett außerhalb: 0

□ Revenue/Funding:          ___/10 Punkte
  - Series A-C: 10
  - Seed: 5
  - Pre-Seed oder Public: 0
```

### TECHNOGRAPHICS (Max 25 Punkte)

```
□ AI/Automation Usage:      ___/15 Punkte
  - Nutzt bereits AI Agents: 15
  - Nutzt Automation (Zapier etc): 10
  - Plant AI-Einsatz: 5
  - Kein AI-Interesse: 0

□ Tech Stack Fit:           ___/10 Punkte
  - Moderne Cloud-Stack: 10
  - Mixed: 5
  - Legacy only: 0
```

### BEHAVIORAL (Max 35 Punkte)

```
□ Buying Intent:            ___/15 Punkte
  - Aktiv suchend: 15
  - Interessiert: 10
  - Passiv: 5
  - Kein Interesse: 0

□ Pain Urgency:             ___/10 Punkte
  - Kritisch/Dringend: 10
  - Wichtig: 7
  - Nice-to-have: 3
  - Kein Pain: 0

□ Decision Authority:       ___/10 Punkte
  - Entscheider: 10
  - Influencer: 7
  - User only: 3
```

**TOTAL SCORE: ___/100**

---

## Qualifikations-Framework (BANT+)

| Kriterium | Fragen | Score-Impact |
|-----------|--------|--------------|
| **Budget** | Gibt es allociertes Budget für AI? | +15 wenn ja |
| **Authority** | Sprichst du mit Entscheider? | +10 wenn ja |
| **Need** | Klarer Pain der zu Mutagent passt? | +15 wenn ja |
| **Timeline** | Wann wollen sie kaufen? | +10 wenn <3 Monate |
| **Champion** | Gibt es internen Fürsprecher? | +10 wenn ja |

---

## Alternative Frameworks

### CHAMP (Challenge-First)
| Kriterium | Fokus |
|-----------|-------|
| **Challenges** | Was sind ihre Probleme? (Pain first!) |
| **Authority** | Wer entscheidet? |
| **Money** | Budget-Situation? |
| **Prioritization** | Wie dringend? |

### MEDDIC (Enterprise)
| Kriterium | Fokus |
|-----------|-------|
| **Metrics** | Quantifizierbarer Impact? |
| **Economic Buyer** | Wer kontrolliert Budget? |
| **Decision Criteria** | Auswahl-Kriterien? |
| **Decision Process** | Formaler Kaufprozess? |
| **Identify Pain** | Kern-Business-Pain? |
| **Champion** | Interner Fürsprecher? |

---

## Weighted Scoring Formula

```
Total Score = (Firmographic × 0.40) + (Behavioral × 0.35) + (Technographic × 0.25)
```

### Time Decay (Optional)

| Aktion Alter | Punkte-Wert |
|--------------|-------------|
| Letzte 7 Tage | 100% |
| 8-30 Tage | 75% |
| 31-90 Tage | 50% |
| 90+ Tage | 25% |

---

## Sources

- [Lead Scoring Explained | HubSpot](https://blog.hubspot.com/marketing/lead-scoring-instructions)
- [How to Create a Matrix Scoring Model | Marketo](https://nation.marketo.com/t5/champion-program-blogs/how-to-create-a-matrix-scoring-model-in-marketo-engage/ba-p/331263)
- [What is Lead Scoring | ZoomInfo](https://pipeline.zoominfo.com/marketing/lead-scoring)
- [MEDDIC vs BANT vs CHAMP | LeadsAtScale](https://leadsatscale.com/insights/b2b-lead-qualification-framework-bant-vs-champ-vs-meddic/)
- [Sales Qualification Frameworks 2024 | Demodesk](https://demodesk.com/resources-guides/sales-qualification-frameworks-in-2024-how-to-choose-the-right-one-for-your-business)
- [Lead Scoring: The Definitive Guide | Creatio](https://www.creatio.com/glossary/lead-scoring)
- [Clearbit's ICP and Lead Scoring Model](https://clearbit.com/blog/icp-and-lead-scoring-model)
