# {{project_name}} - Discovery

**Project Type**: Research
**Discovery Method**: create-research-project skill

---

## Discovery Status

**Skill Used**: create-research-project
**Load Command**: `python 00-system/core/nexus-loader.py --skill create-research-project`

*This file is populated by the create-research-project skill during discovery.*

---

## Research Question

{{research_question}}

---

## Research Purpose

{{research_purpose}}

---

## Extraction Schema

*Fields to extract from each paper:*

| Field | Description | Priority |
|-------|-------------|----------|
| {{field_name}} | {{description}} | High/Medium/Low |

---

## Paper Search Results

| Metric | Value |
|--------|-------|
| Papers Found | {{papers_found}} |
| Papers Selected | {{papers_selected}} |
| Papers Downloaded | {{papers_downloaded}} |
| Papers Failed | {{papers_failed}} |

---

## Selected Papers

| Paper | Authors | Year | Relevance |
|-------|---------|------|-----------|
| {{title}} | {{authors}} | {{year}} | {{relevance_score}} |

---

## Generated Resources

| File | Purpose |
|------|---------|
| `02-resources/_briefing.md` | Research question and extraction schema |
| `02-resources/_analysis_kit.md` | Subagent context for analysis |
| `02-resources/_search_results.md` | Raw search results |
| `02-resources/_selection_log.md` | Paper selection decisions |

---

## Dependencies

### External Systems

- paper-search skill (9 academic APIs)
- pdf-preprocess skill (PDF to markdown)

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| PDF download failures | Medium | Low | Multiple sources |
| Low relevance papers | Low | Medium | Abstract review |

---

*Populated by create-research-project skill*
