# Airtable Filter Syntax Reference

**Complete guide to Airtable formula filters for querying records.**

---

## Basic Syntax

Filters use Airtable formula syntax with `filterByFormula` parameter:

```bash
uv run python query_records.py --base appXXX --table "Tasks" --filter "{Status}='Active'"
```

**Key Rules:**
- Field names in curly braces: `{Field Name}`
- Strings in single quotes: `'value'`
- Numbers without quotes: `42`
- Field names are case-sensitive
- Spaces in field names are OK: `{Due Date}`

---

## Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equal to | `{Status}='Done'` |
| `!=` | Not equal to | `{Status}!='Archived'` |
| `>` | Greater than | `{Priority}>3` |
| `<` | Less than | `{Count}<10` |
| `>=` | Greater or equal | `{Rating}>=4` |
| `<=` | Less or equal | `{Progress}<=0.5` |

---

## Logical Operators

### AND()
All conditions must be true:
```
AND({Status}='Active', {Priority}='High')
```

### OR()
At least one condition true:
```
OR({Status}='Todo', {Status}='In Progress')
```

### NOT()
Negates condition:
```
NOT({Completed})
```

### Combined
```
AND(
  OR({Status}='Active', {Status}='Pending'),
  {Priority}='High'
)
```

---

## Text Functions

### FIND()
Find substring (case-sensitive), returns position or 0:
```
FIND('urgent', LOWER({Name}))>0
```

### SEARCH()
Find substring (case-insensitive), returns position or error:
```
SEARCH('urgent', {Name})>0
```

### LOWER() / UPPER()
```
LOWER({Category})='support'
```

### LEN()
```
LEN({Description})>100
```

### TRIM() / LEFT() / RIGHT() / MID()
```
LEFT({Code}, 3)='PRJ'
```

### REGEX_MATCH()
```
REGEX_MATCH({Email}, '@company\\.com$')
```

---

## Text Comparison Patterns

### Contains (case-insensitive)
```
SEARCH('keyword', {Name})>0
```

### Starts with
```
LEFT({Name}, 3)='PRJ'
```

### Ends with
```
RIGHT({Email}, 12)='@example.com'
```

### Exact match (case-insensitive)
```
LOWER({Status})='active'
```

---

## Numeric Functions

### Basic Math
```
{Price}*{Quantity}>1000
{Total}-{Discount}>=500
```

### ABS() / CEILING() / FLOOR() / ROUND()
```
ABS({Variance})>10
ROUND({Score}, 1)=4.5
```

### MOD() / POWER() / SQRT()
```
MOD({ID}, 2)=0
```

### MIN() / MAX() / SUM() / AVERAGE()
```
MAX({Price}, {MinPrice})>100
```

---

## Date Functions

### IS_AFTER() / IS_BEFORE() / IS_SAME()
```
IS_AFTER({Due Date}, TODAY())
IS_BEFORE({Start Date}, '2025-01-01')
IS_SAME({Created}, TODAY(), 'day')
```

### TODAY() / NOW()
```
{Due Date}=TODAY()
{Created}>DATEADD(TODAY(), -7, 'days')
```

### DATEADD()
```
# Records due within next 7 days
AND(
  {Due Date}>=TODAY(),
  {Due Date}<=DATEADD(TODAY(), 7, 'days')
)
```

### DATETIME_DIFF()
```
DATETIME_DIFF({Due Date}, TODAY(), 'days')<7
```

### DATE Extraction
```
YEAR({Created})=2025
MONTH({Created})=1
DAY({Due Date})=15
WEEKNUM({Date})=3
```

---

## Boolean / Checkbox

### True values
```
{Completed}=TRUE()
{Completed}
{Is Active}=1
```

### False values
```
{Completed}=FALSE()
NOT({Completed})
{Is Active}=0
```

---

## Empty / Blank Values

### Check for empty
```
{Name}=BLANK()
{Notes}=''
LEN({Description})=0
```

### Check for not empty
```
{Name}!=BLANK()
{Notes}!=''
LEN({Description})>0
```

### Handling empty in comparisons
```
AND({Status}!='', {Status}!='Archived')
```

---

## Select Fields

### Single Select
```
{Status}='Active'
OR({Priority}='High', {Priority}='Critical')
```

### Multiple Selects (check if contains)
```
FIND('Backend', ARRAYJOIN({Tags}))>0
```

---

## Linked Records

### Check if has linked records
```
{Projects}!=BLANK()
LEN(ARRAYJOIN({Projects}))>0
```

### Count linked records
```
# Use with count field or rollup
{Project Count}>0
```

---

## Common Filter Patterns

### Active items
```
AND({Status}!='Done', {Status}!='Archived')
```

### Overdue tasks
```
AND(
  {Due Date}<TODAY(),
  NOT({Completed})
)
```

### This week's items
```
AND(
  {Due Date}>=DATEADD(TODAY(), -WEEKDAY(TODAY()), 'days'),
  {Due Date}<DATEADD(TODAY(), 7-WEEKDAY(TODAY()), 'days')
)
```

### Assigned to me (with collaborator field)
```
# Requires knowing user ID or using view filter instead
{Assignee}='usrXXXXXX'
```

### High priority unfinished
```
AND(
  {Priority}='High',
  NOT({Completed}),
  {Due Date}<=DATEADD(TODAY(), 7, 'days')
)
```

### Recent updates
```
{Last Modified}>=DATEADD(TODAY(), -7, 'days')
```

### Search multiple fields
```
OR(
  SEARCH('keyword', {Name})>0,
  SEARCH('keyword', {Description})>0,
  SEARCH('keyword', {Notes})>0
)
```

---

## Script Usage Examples

### Basic filter
```bash
uv run python query_records.py --base "CRM" --table "Contacts" \
  --filter "{Status}='Active'"
```

### Combined conditions
```bash
uv run python query_records.py --base appXXX --table "Tasks" \
  --filter "AND({Status}!='Done', {Priority}='High')"
```

### Date filter
```bash
uv run python query_records.py --base appXXX --table "Tasks" \
  --filter "{Due Date}<=TODAY()"
```

### Text search
```bash
uv run python query_records.py --base appXXX --table "Projects" \
  --filter "SEARCH('mobile', LOWER({Name}))>0"
```

### With sorting and limit
```bash
uv run python query_records.py --base appXXX --table "Tasks" \
  --filter "{Status}='Active'" \
  --sort "-Due Date" \
  --limit 10
```

---

## Escaping Special Characters

### Single quotes in values
```
{Name}='John\\'s Project'
```

### In bash command
```bash
--filter "{Name}='John'\''s Project'"
# or
--filter '{Name}="John'"'"'s Project"'
```

### Curly braces in field names
```
# Not supported - rename field to avoid braces
```

---

## Performance Tips

1. **Use indexed fields**: Primary field, linked record fields
2. **Keep formulas simple**: Complex formulas slow down queries
3. **Limit OR clauses**: Many ORs are slower than indexed lookups
4. **Use views**: Pre-filtered views are faster than formula filters
5. **Batch requests**: Use pagination instead of huge single requests

---

## Limitations

- Max formula length: ~16,000 characters
- Can't filter by attachment content
- Can't filter by button field
- Rollup/Lookup filters may be slow
- No full-text search across all fields (use OR with SEARCH)

---

## Differences from Notion

| Notion | Airtable |
|--------|----------|
| `equals`, `contains` | `=`, `SEARCH()` |
| `is_not_empty` | `!=BLANK()` |
| `past_week` | `DATEADD(TODAY(), -7, 'days')` |
| JSON filter object | Formula string |
| Property names | `{Field Name}` syntax |

---

**Last Updated:** 2025-12-31
