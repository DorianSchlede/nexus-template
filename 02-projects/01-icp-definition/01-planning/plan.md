# ICP Definition - Plan

**Last Updated**: 2025-12-24

---

## Approach

**Methodik**: Hypothesen-basierte ICP-Entwicklung mit iterativer Validierung

```
Phase 1: Framework & Hypothese     → ICP v0.1 (Best Practices)
Phase 2: Interview-Validierung     → ICP v0.5 (10-15 Interviews)
Phase 3: Refinement & Scoring      → ICP v1.0 (25-30 Interviews)
Phase 4: Operationalisierung       → Target List + Outreach
```

**Kern-Prinzip**: "Quality over quantity" - 10 gut ausgewählte Interviews > 50 random Interviews.

---

## Key Decisions

| Entscheidung | Gewählt | Begründung |
|--------------|---------|------------|
| **ICP-Ansatz** | Hypothesen-first | Pre-revenue, wenig Kunden-Daten verfügbar |
| **Validierung** | JTBD-Interviews | Jobs-to-be-Done zeigt 34% höhere Conversion |
| **Sample Size** | 25-30 Interviews | Statistische Signifikanz bei Interview 25-30 |
| **Scoring** | Traffic-Light + Punkte | Einfach (Grün/Gelb/Rot) + präzise (0-100) |
| **Anti-ICP** | Parallel entwickeln | Spart 15-20h/Rep/Monat durch frühe Disqualifikation |

---

## Execution Framework

### Phase 1: ICP Framework Design

**Ziel**: Hypothesen-basiertes ICP v0.1 erstellen

**Deliverables**:
1. ICP-Dokument mit allen Dimensionen
2. Scoring-Rubrik (0-100 Punkte)
3. Anti-ICP Kriterien
4. Buyer Persona Templates

**Ressourcen** (in `02-resources/`):
- [01-icp-framework-dimensions.md](../02-resources/01-icp-framework-dimensions.md)
- [02-scoring-rubrik-template.md](../02-resources/02-scoring-rubrik-template.md)
- [03-anti-icp-framework.md](../02-resources/03-anti-icp-framework.md)

---

### Phase 2: Interview-Validierung

**Ziel**: ICP-Hypothesen mit echten Gesprächen validieren

**Deliverables**:
1. Interview-Leitfaden (JTBD-basiert)
2. 10-15 durchgeführte Interviews
3. Pattern-Analyse (Affinity Mapping)
4. ICP v0.5 Update

**Ressourcen** (in `02-resources/`):
- [04-jtbd-interview-questions.md](../02-resources/04-jtbd-interview-questions.md)
- [05-affinity-mapping-methode.md](../02-resources/05-affinity-mapping-methode.md)
- [08-sample-size-guidance.md](../02-resources/08-sample-size-guidance.md)

---

### Phase 3: Persona Mapping

**Ziel**: Buying Committee für ICP dokumentieren

**Deliverables**:
1. Champion Persona
2. Economic Buyer Persona
3. User/Admin Persona
4. Technical Validator Persona
5. Multi-Threading Strategie

**Ressourcen** (in `02-resources/`):
- [06-persona-template.md](../02-resources/06-persona-template.md)
- [07-buying-committee-mapping.md](../02-resources/07-buying-committee-mapping.md)

---

### Phase 4: Operationalisierung

**Ziel**: ICP in Praxis umsetzen

**Deliverables**:
1. Target Company Liste (10-20)
2. Lead Scoring in CRM/Airtable
3. Outreach-Priorisierung

**Ressourcen** (in `02-resources/`):
- [09-crm-scoring-fields.md](../02-resources/09-crm-scoring-fields.md)
- [10-target-list-criteria.md](../02-resources/10-target-list-criteria.md)

---

## Resources Needed

**Tools/Access**:
- LinkedIn Sales Navigator (Company Research)
- Interview-Recording Tool (Grain, Otter, etc.)
- Airtable/Notion (ICP-Dokumentation)
- HubSpot (Lead Scoring)

**People/Expertise**:
- Gründer-Team für Interview-Durchführung
- Potentielle Kunden für Validierung

**Information/Data**:
- Existierende Hypothesen (D1, D2, D9, V1)
- Bisherige Gespräche/Erkenntnisse
- Competitor-Analyse (wer sind deren Kunden?)

---

## Dependencies & Links

**Workspace Files**:
- `04-workspace/08-strategy/` - Strategie-Dokumente
- `04-workspace/01-hypotheses/` - Hypothesen-Tracking

**External Systems**:
- HubSpot CRM - Lead Scoring
- LinkedIn - Company Research
- Calendly - Interview Scheduling

**Related Goals**:
- 100+ Interviews in 3 Monaten
- 5 Pilot-Kunden finden

---

## Open Questions

- [ ] Welche Hypothesen (D1, D2, D9, V1) sind am kritischsten für ICP?
- [ ] Gibt es schon Interview-Daten die wir nutzen können?
- [ ] Welche Branchen/Segmente priorisieren wir zuerst?
- [ ] Wie definieren wir "AI Agent" für unsere Zielgruppe?

---

## Mental Models Applied

**First Principles** (für ICP-Definition):
- Was sind die fundamentalen Eigenschaften eines idealen Kunden?
- Welche Annahmen über den Markt müssen wir hinterfragen?

**Pre-Mortem** (für Risiken):
- Was wenn unser ICP zu eng definiert ist?
- Was wenn Interviews andere Patterns zeigen als erwartet?

**Jobs-to-be-Done** (für Interviews):
- Welchen "Job" versucht der Kunde zu erledigen?
- Was ist der "struggling moment" der zum Kauf führt?

---

## Ressourcen-Index

Alle Best-Practice Ressourcen sind in `02-resources/` gespeichert:

| # | Datei | Inhalt |
|---|-------|--------|
| 01 | [icp-framework-dimensions.md](../02-resources/01-icp-framework-dimensions.md) | 5 ICP-Dimensionen (Firmographics, Technographics, etc.) |
| 02 | [scoring-rubrik-template.md](../02-resources/02-scoring-rubrik-template.md) | 0-100 Scoring System, Traffic Light, BANT+ |
| 03 | [anti-icp-framework.md](../02-resources/03-anti-icp-framework.md) | Disqualifikation, Red Flags, Anti-Personas |
| 04 | [jtbd-interview-questions.md](../02-resources/04-jtbd-interview-questions.md) | Jobs-to-be-Done Interview-Leitfaden |
| 05 | [affinity-mapping-methode.md](../02-resources/05-affinity-mapping-methode.md) | Pattern-Analyse, Clustering, Saturation |
| 06 | [persona-template.md](../02-resources/06-persona-template.md) | YAML Persona-Dokumentation |
| 07 | [buying-committee-mapping.md](../02-resources/07-buying-committee-mapping.md) | 5 B2B Buyer Rollen, Multi-Threading |
| 08 | [sample-size-guidance.md](../02-resources/08-sample-size-guidance.md) | Wann genug Interviews? Saturation |
| 09 | [crm-scoring-fields.md](../02-resources/09-crm-scoring-fields.md) | HubSpot/Airtable Felder & Automation |
| 10 | [target-list-criteria.md](../02-resources/10-target-list-criteria.md) | Company-Filterung, Research Sources |

---

## Sources & References

### ICP Frameworks
- [The Ultimate Framework to build your ICP for SaaS startups](https://www.mrrunlocked.com/p/framework-ideal-customer-profile)
- [A Framework for Defining and Refining Your ICP | a16z](https://a16z.com/framework-define-refine-icp/)
- [Creating an ICP transformed our company | PostHog](https://posthog.com/newsletter/ideal-customer-profile-framework)
- [ICP for SaaS: A Practical Framework | Cornel Lazar](https://cornellazar.com/icp-for-saas-a-practical-framework-to-define-your-ideal-customer-profile)

### Scoring & Qualification
- [How to Create a Matrix Scoring Model | Marketo](https://nation.marketo.com/)
- [Lead Scoring Explained | HubSpot](https://blog.hubspot.com/marketing/lead-scoring-instructions)
- [MEDDIC vs BANT vs CHAMP](https://meddicc.com/resources/)

### Interview Methods
- [Jobs to be Done Framework | Hotjar](https://www.hotjar.com/product-management-glossary/jobs-to-be-done/)
- [How to Validate ICP with 25 Interviews | M1 Project](https://www.m1-project.com/blog/how-to-validate-your-icp-with-just-25-interviews-instead-of-50)
- [Customer Interviews Guide | Product Talk](https://www.producttalk.org/)

### Persona Mapping
- [B2B Buyer Persona and ICP Complete Guide 2025](https://gotoclient.com/blog/buyer-persona-icp-guide/)
- [How to Engage the Modern B2B Buying Committee](https://revnew.com/blog/engage-b2b-buying-committee)
- [5 Key B2B SaaS Buying Personas for 2025](https://imm.com/blog/)

### Anti-ICP
- [The Ultimate Guide to Identifying Bad Fit Customers](https://gtmonday.substack.com/)
- [How to Qualify Leads Fast | Close](https://www.close.com/blog/how-to-qualify-leads-fast)
- [Why Disqualifying Customers is a Growth Strategy | Lighter Capital](https://www.lightercapital.com/blog/)

---

*Next: Complete steps.md to break down execution*
