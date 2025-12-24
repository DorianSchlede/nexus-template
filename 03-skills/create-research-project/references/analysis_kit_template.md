---
project_id: "{project_id}"
project_path: "02-projects/{project_id}"
generated: "{date}"
---

# Analysis Kit for {project_name}

**This file contains everything a subagent needs to analyze a paper in this project.**

---

## Research Question

{research_question}

---

## Extraction Schema

Extract these fields from each paper:

| Field | Description | Priority |
|-------|-------------|----------|
{extraction_schema_rows}

---

## Focus Areas

Look specifically for:
{focus_areas}

---

## Skip Sections

Don't extract from:
- Acknowledgments
- Author Contributions
- Funding
- References (unless citing specific patterns)

---

## Output Requirements

### 1. Analysis Log (`_analysis_log.md`)

For methodology reference, read: `03-skills/paper-analyze-core/references/analysis_log_template.md`

Key requirements:
- Record evidence spans (start_string, end_string) for each finding
- Include chunk reference for every extraction
- Log which chunks were read

### 2. Index File (`index.md`)

For output format, read: `03-skills/paper-analyze-core/references/index_template.md`

**REQUIRED YAML frontmatter fields:**

```yaml
---
paper_id: "{paper_id}"
chunks_expected: {N}      # From _metadata.json
chunks_read: {N}          # Must equal chunks_expected
analysis_complete: true   # Set to true when done
high_priority_fields_found: {N}  # Count of HIGH priority fields with extractions
---
```

Key requirements:
- YAML frontmatter with paper metadata AND validation fields above
- Extracted fields matching schema above
- Chunk navigation with summaries

---

## File Locations (use {paper_id} variable)

| Purpose | Path |
|---------|------|
| Paper chunks | `02-resources/papers/{paper_id}/{paper_id}_N.md` |
| Chunk metadata | `02-resources/papers/{paper_id}/_metadata.json` |
| Analysis log output | `02-resources/papers/{paper_id}/_analysis_log.md` |
| Index output | `02-resources/papers/{paper_id}/index.md` |

**Note:** `{paper_id}` is provided by orchestrator. All paths are relative to project root.

---

## Subagent Instructions

```
1. Read this analysis kit (you're reading it now)
2. Read the methodology: 03-skills/paper-analyze-core/SKILL.md
3. Read the paper's _metadata.json to get chunk list
4. Read ALL chunks listed in _metadata.json
5. Extract findings per the schema above
6. Write _analysis_log.md and index.md with REQUIRED frontmatter
```

**CRITICAL RULES:**
- Do NOT read the PDF file
- Do NOT skip any chunks
- Include chunk reference for every finding (e.g., "Chunk 3")
- Set `chunks_read` = `chunks_expected` (validates you read everything)
- Set `analysis_complete: true` only when fully done

---

## Validation Contract

Your output will be validated. The following MUST be true:

| Check | Requirement |
|-------|-------------|
| `index.md` exists | File must be created |
| `chunks_read == chunks_expected` | All chunks were read |
| `analysis_complete == true` | Analysis finished |
| `high_priority_fields_found >= 1` | At least 1 HIGH priority extraction |
| Evidence has chunk refs | Every finding cites a chunk |

**If validation fails, the paper will be retried.**
