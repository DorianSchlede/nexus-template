# Linked Skills Table Schema

**Design for storing complete skill bundles with unlimited file storage.**

## Problem

Airtable's `multilineText` field has a ~100KB limit. Large skills (master skills with many scripts) cannot store complete bundles.

Current workaround: Store only `SKILL.md` for large skills (partial bundles).

## Solution: Linked Tables

Split storage across two linked tables:

### Table 1: Skills (main table)

| Field | Type | Description |
|-------|------|-------------|
| Name | singleLineText | Skill name (primary field) |
| Description | multilineText | From YAML frontmatter |
| Version | singleLineText | Semantic version |
| Team | singleSelect | Category (hubspot, langfuse, etc.) |
| Purpose | multilineText | Extracted from ## Purpose |
| SkillMD | multilineText | SKILL.md content (plain text) |
| Files | Link to SkillFiles | Linked records for all files |
| FileCount | Rollup | COUNT(Files) |
| IsComplete | Formula | `FileCount > 0` or check if all files present |

### Table 2: SkillFiles (linked table)

| Field | Type | Description |
|-------|------|-------------|
| Skill | Link to Skills | Parent skill (1:many) |
| FilePath | singleLineText | Relative path (e.g., `scripts/helper.py`) |
| Content | multilineText | Base64-encoded file content |
| FileSize | number | Original file size in bytes |
| FileType | singleSelect | Extension category (py, md, json, yaml, etc.) |

## Benefits

1. **No size limits** - Each file is a separate record
2. **Queryable** - Can search files by path, type, or content
3. **Granular updates** - Update single files without re-uploading entire skill
4. **Versioning ready** - Can add version field to track file changes
5. **Metadata rich** - Can add file-level metadata (author, modified date, etc.)

## Implementation

### Upload Flow

```python
def upload_skill_linked(base_id, skills_table, files_table, skill_path):
    # 1. Create/update main skill record
    skill_record = create_skill_record(skills_table, skill_path)

    # 2. For each file in skill directory
    for file_path in skill_path.rglob('*'):
        if file_path.is_file():
            # 3. Create file record linked to skill
            create_file_record(files_table, skill_record['id'], file_path)
```

### Download Flow

```python
def download_skill_linked(base_id, skills_table, files_table, skill_name, output_dir):
    # 1. Find skill record
    skill = get_skill_by_name(skills_table, skill_name)

    # 2. Get all linked file records
    files = get_linked_files(files_table, skill['id'])

    # 3. Extract each file
    for file_record in files:
        path = file_record['FilePath']
        content = base64.b64decode(file_record['Content'])
        write_file(output_dir / skill_name / path, content)
```

## Migration Path

1. Create `SkillFiles` table in Airtable
2. Update `upload_local_skills.py` to use linked tables
3. Update `download_skill.py` to read from linked tables
4. Re-upload all 50 partial skills with complete bundles
5. Keep backward compatibility with existing `Content` field

## Table Creation Commands

```bash
# Create SkillFiles table
python manage_tables.py create --base app1gngDx52VAgjVQ --name "SkillFiles" \
  --fields '[
    {"name": "FilePath", "type": "singleLineText"},
    {"name": "Content", "type": "multilineText"},
    {"name": "FileSize", "type": "number", "options": {"precision": 0}},
    {"name": "FileType", "type": "singleSelect", "options": {"choices": [
      {"name": "py"}, {"name": "md"}, {"name": "json"}, {"name": "yaml"}, {"name": "txt"}, {"name": "other"}
    ]}}
  ]' --token MUTAGENT

# Add link field to Skills table
python manage_fields.py create --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --name "Files" --type multipleRecordLinks \
  --link-table <SkillFiles_table_id> --token MUTAGENT
```

## Query Examples

```bash
# Get all Python files for a skill
python query_records.py --base app1gngDx52VAgjVQ --table SkillFiles \
  --filter "{FileType}='py'" --token MUTAGENT

# Get files for a specific skill (using linked record)
# Note: Airtable API requires lookup through the Skills table
```

---

**Status**: Design complete, ready for implementation
**Created**: 2025-12-31
