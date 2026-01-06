# Notion Filter Syntax Reference

> Quick reference for filtering database queries in notion-connect skill.

---

## Filter Modes

### Skills Database Mode (AND Filters Supported)

When using `--skills` mode for the Beam Nexus Skills database, **multiple filters with AND logic** are supported:

```bash
# Single filter
python search_skill_database.py --skills --team Solutions

# Multiple filters (AND logic)
python search_skill_database.py --skills --team Solutions --integration "Beam AI"
python search_skill_database.py --skills --team General --integration Linear --name notion

# Available Skills Mode Filters:
--team <team>           # General, Solutions, Engineering, Sales
--integration <tool>    # Beam AI, Linear, Notion, etc.
--name <partial>        # Partial match on skill name (case-insensitive)
--owner <user-id>       # Filter by creator user ID
```

### General Database Mode (Single Filter)

When using `--db` mode for any database, **one filter per query** is currently supported:

```bash
# Works:
python search_skill_database.py --db "Projects" --filter "Status = In Progress"

# Does NOT work (yet):
--filter "Status = In Progress AND Priority = High"
```

---

## Basic Syntax

```
--filter "Property Operator Value"
```

**Examples**:
```bash
--filter "Status = Active"
--filter "Priority = High"
--filter "Name contains project"
```

---

## Operators by Property Type

### Text Properties (title, rich_text, url, email, phone)

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `"Name = Project Alpha"` | Exact match |
| `!=` | `"Name != Draft"` | Not equal |
| `contains` | `"Name contains design"` | Contains substring |
| `does_not_contain` | `"Name does_not_contain test"` | Excludes substring |
| `starts_with` | `"Name starts_with 2025"` | Starts with |
| `ends_with` | `"Name ends_with v2"` | Ends with |
| `is_empty` | `"Description is_empty"` | Is blank |
| `is_not_empty` | `"Description is_not_empty"` | Has value |

### Select & Status Properties

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `"Status = In Progress"` | Equals option |
| `!=` | `"Priority != Low"` | Not equals |
| `is_empty` | `"Status is_empty"` | No selection |
| `is_not_empty` | `"Status is_not_empty"` | Has selection |

### Multi-Select Properties

| Operator | Example | Description |
|----------|---------|-------------|
| `contains` | `"Tags contains Design"` | Has option |
| `does_not_contain` | `"Tags does_not_contain Archive"` | Missing option |
| `is_empty` | `"Tags is_empty"` | No selections |
| `is_not_empty` | `"Tags is_not_empty"` | Has selections |

### Number Properties

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `"Points = 5"` | Equals |
| `!=` | `"Points != 0"` | Not equals |
| `>` | `"Points > 10"` | Greater than |
| `<` | `"Points < 100"` | Less than |
| `>=` | `"Points >= 5"` | Greater or equal |
| `<=` | `"Points <= 20"` | Less or equal |
| `is_empty` | `"Points is_empty"` | No value |
| `is_not_empty` | `"Points is_not_empty"` | Has value |

### Date Properties (date, created_time, last_edited_time)

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `"Due Date = 2025-01-15"` | Equals date |
| `>` | `"Due Date > 2025-01-01"` | After date |
| `<` | `"Due Date < 2025-12-31"` | Before date |
| `>=` | `"Created >= 2025-01-01"` | On or after |
| `<=` | `"Created <= 2025-06-30"` | On or before |
| `is_empty` | `"Due Date is_empty"` | No date set |
| `is_not_empty` | `"Due Date is_not_empty"` | Has date |

**Date formats**: `YYYY-MM-DD` (e.g., `2025-01-15`)

### Checkbox Properties

| Operator | Example | Description |
|----------|---------|-------------|
| `=` | `"Completed = true"` | Is checked |
| `=` | `"Completed = false"` | Is unchecked |

**Values**: `true`, `false`, `yes`, `no`, `1`, `0`, `checked`

### People Properties

| Operator | Example | Description |
|----------|---------|-------------|
| `contains` | `"Assignee contains user-id"` | Assigned to user |
| `does_not_contain` | `"Assignee does_not_contain user-id"` | Not assigned |
| `is_empty` | `"Assignee is_empty"` | Unassigned |
| `is_not_empty` | `"Assignee is_not_empty"` | Has assignee |

### Files Properties

| Operator | Example | Description |
|----------|---------|-------------|
| `is_empty` | `"Attachments is_empty"` | No files |
| `is_not_empty` | `"Attachments is_not_empty"` | Has files |

---

## Common Examples

### Status-based queries
```bash
# Active items
--filter "Status = In Progress"

# Not started
--filter "Status = Not Started"

# Completed
--filter "Status = Done"
```

### Priority queries
```bash
# High priority only
--filter "Priority = High"

# Exclude low priority
--filter "Priority != Low"
```

### Date-based queries
```bash
# Due this week (before end of week)
--filter "Due Date < 2025-01-17"

# Overdue (before today)
--filter "Due Date < 2025-01-10"

# Created recently
--filter "Created >= 2025-01-01"
```

### Content searches
```bash
# Find by name
--filter "Name contains quarterly"

# Tasks with descriptions
--filter "Description is_not_empty"
```

### Tag filtering
```bash
# Design-related
--filter "Tags contains Design"

# Not archived
--filter "Tags does_not_contain Archive"
```

---

## Combining with Sort

```bash
# High priority, sorted by due date
--filter "Priority = High" --sort "Due Date" --sort-dir asc

# Recent items, newest first
--filter "Status = In Progress" --sort "Created" --sort-dir desc
```

---

## Limitations

1. **General mode single filter**: `--db` mode supports ONE filter per query
   - **Skills mode supports AND**: Use `--skills` with multiple flags for combined filters
2. **Case-sensitive options**: Select/Multi-select values must match exactly
3. **People by ID**: People filters require user ID, not name
4. **No relation filtering**: Relation properties have limited filter support

---

## Troubleshooting

**"Property not found"**
- Check property name matches exactly (case-sensitive)
- Run `discover_databases.py --refresh` to update schemas

**"Invalid value"**
- For select properties, value must match an existing option
- For dates, use YYYY-MM-DD format

**"Unsupported filter"**
- Some property types (formula, rollup, relation) have limited filter support
- Check Notion API docs for full filter capabilities

---

*For advanced filters, see: [Notion API Filter Documentation](https://developers.notion.com/reference/post-database-query-filter)*
