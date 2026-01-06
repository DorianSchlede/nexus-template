# AI Development Platform - Filter Guide

> **Purpose**: Quick reference for intelligent filtering on this Airtable base
> **Base ID**: `appFPoOfBpUv73M5A`
> **Last Updated**: 2025-12-28

---

## Quick Filter Patterns

### By Use Case

| I want to find... | Table | Filter Formula | Key Fields |
|-------------------|-------|----------------|------------|
| Failed tasks | `AgentTasks` | `{Status}='FAILED'` | Status, Agent, Task ID |
| Low accuracy extractions | `VariableTasks` | `{Accuracy}=0` | Accuracy, AIValue, Expected Value |
| Human corrections | `BID Feedback` | `{ComparisonResult}='Mismatch'` | AI_Value, User_Value, Variable_text |
| Missing AI values | `BID Feedback` | `{ComparisonResult}='AI NULL'` | Variable_text, Category |
| Active evaluations | `DatasetRun` | `{Status}='In progress'` | Status, DatasetRun Name |
| Completed evaluations | `DatasetRun` | `{Status}='Done'` | Avg Variable Accuracy |
| Tasks needing input | `AgentTasks` | `{Status}='USER_INPUT_REQUIRED'` | Task ID, Actual Task Input |
| Production agents | `Agents` | `{Agent Type}='Production'` | Agent Name, Agent BID |

---

## Primary Filter Columns by Table

### AgentTasks (Execution Records)
```yaml
Status Filters:
  - {Status}='COMPLETED'
  - {Status}='FAILED'
  - {Status}='IN_PROGRESS'
  - {Status}='USER_INPUT_REQUIRED'
  - {Status}='QUEUED'
  - {Status}='CONSENT_REQUIRED'

Performance Filters:
  - {Avg Variable Accuracy} < 0.8    # Low accuracy tasks
  - {Duration Mins} > 5              # Long running tasks
  - {Last Node Match} = 0            # Wrong path taken

Date Filters:
  - IS_AFTER({Created}, '2025-01-01')
  - IS_SAME({Created}, TODAY(), 'day')

Combination Example:
  AND({Status}='COMPLETED', {Avg Variable Accuracy} < 0.8)
```

### VariableTasks (Extraction Results)
```yaml
Accuracy Filters:
  - {Accuracy} = 0                   # Wrong extractions
  - {Accuracy} = 1                   # Correct extractions
  - {VariableTaskAccuracy} < 1       # Partial matches

Value Comparison:
  - {AIValue} = BLANK()              # No AI value
  - {Expected Value} != BLANK()      # Has ground truth
  - {AIValue} != {Expected Value}    # Mismatch

Variable Type (via lookup):
  - FIND('Key Variable', {Variable Type (from Variable)})
```

### BID Feedback (Human Corrections)
```yaml
Comparison Result:
  - {ComparisonResult}='Match'       # AI was correct
  - {ComparisonResult}='Mismatch'    # AI was wrong
  - {ComparisonResult}='AI NULL'     # AI returned nothing

Category Filters:
  - {Category}='contact_data'
  - {Category}='classification'
  - {Category}='classification_data'
  - {Category}='edge_case_variables'
  - {Category}='feedback'

Classification:
  - {Classification}='Insolvenz'
  - {Group}='Inso 1'

Time Filters:
  - {User_Response_Time_Days} > 7    # Slow response
```

### Agents (Agent Definitions)
```yaml
Type Filters:
  - {Agent Type}='Production'
  - {Agent Type}='Custom Instance'
  - {Agent Type}='E2E'
  - {Agent Type}='Staging'

Status:
  - {Monitor Task}=TRUE()            # Monitored agents

Workspace:
  - {Workspace}='[Workspace Name]'
```

### DatasetRun (Evaluations)
```yaml
Status:
  - {Status}='Todo'
  - {Status}='In progress'
  - {Status}='Done'

Performance:
  - {Avg Variable Accuracy} < 0.9    # Below threshold
  - {Count Of Tasks} > 10            # Large evaluations

Type:
  - {Task Type}='Agent Evaluation'
  - {Task Type}='Node Evaluation'
```

### DatasetVariables (Ground Truth)
```yaml
Status:
  - {Expected Value Status}='To Do'
  - {Expected Value Status}='In progress'
  - {Expected Value Status}='Done'

Review:
  - {Review}=TRUE()                  # AI matched expected
  - {Review}=FALSE()                 # AI didn't match

Has Expected:
  - {Expected Value}!=BLANK()
```

---

## Complex Filter Examples

### 1. Find All Accuracy Issues for a Specific Agent
```
Table: VariableTasks
Filter: AND(
  {Accuracy}=0,
  FIND('MyAgentName', {Agent (from AgentTask)})
)
```

### 2. Recent Mismatches in Contact Data
```
Table: BID Feedback
Filter: AND(
  {ComparisonResult}='Mismatch',
  {Category}='contact_data',
  IS_AFTER({AI_CreationTime}, DATEADD(TODAY(), -7, 'days'))
)
```

### 3. High-Priority Failed Evaluations
```
Table: DatasetRun
Filter: AND(
  {Status}='Done',
  {Avg Variable Accuracy} < 0.7
)
Sort: -Avg Variable Accuracy
```

### 4. Pending Ground Truth to Fill
```
Table: DatasetVariables
Filter: AND(
  {Expected Value Status}='To Do',
  {Expected Value}=BLANK()
)
```

### 5. Tasks with Wrong Classification
```
Table: BID Feedback Task
Filter: {Right Classification}=0
Fields: Task ID, AI_Classification, User_Classification, Basic Reasoning
```

---

## Filter Functions Reference

### Comparison
| Function | Example |
|----------|---------|
| Equals | `{Field}='value'` |
| Not equals | `{Field}!='value'` |
| Greater than | `{Field}>10` |
| Less than | `{Field}<0.5` |
| Is blank | `{Field}=BLANK()` |
| Is not blank | `{Field}!=BLANK()` |

### Logical
| Function | Example |
|----------|---------|
| AND | `AND({A}='x', {B}='y')` |
| OR | `OR({A}='x', {A}='y')` |
| NOT | `NOT({A}='x')` |

### Text Search
| Function | Example | Note |
|----------|---------|------|
| FIND | `FIND('text', {Field})` | Returns position, 0 if not found |
| SEARCH | `SEARCH('text', {Field})` | Case-insensitive FIND |
| REGEX_MATCH | `REGEX_MATCH({Field}, 'pattern')` | Full regex support |
| LOWER | `LOWER({Field})='text'` | Case-insensitive compare |

### Date Functions
| Function | Example |
|----------|---------|
| TODAY | `{Date}=TODAY()` |
| IS_AFTER | `IS_AFTER({Date}, '2025-01-01')` |
| IS_BEFORE | `IS_BEFORE({Date}, TODAY())` |
| IS_SAME | `IS_SAME({Date}, TODAY(), 'day')` |
| DATEADD | `DATEADD(TODAY(), -7, 'days')` |

### Array/Multiple Select
| Function | Example |
|----------|---------|
| Check contains | `FIND('value', ARRAYJOIN({Field}))` |
| Exact match | `{Field}='value'` (single value only) |

---

## Usage with Existing Scripts

### query_records.py
```bash
# From Nexus root
python 00-system/skills/airtable/airtable-master/scripts/query_records.py \
  --base "AI Development Platform" \
  --table "VariableTasks" \
  --filter "{Accuracy}=0" \
  --fields "VariableTask Name,AIValue,Expected Value" \
  --limit 20 \
  --json
```

### Python API
```python
from query_records import query_records, load_env, resolve_base_id

load_env()
base_id = resolve_base_id("AI Development Platform")

records = query_records(
    base_id=base_id,
    table_ref="BID Feedback",
    filter_formula="AND({ComparisonResult}='Mismatch', {Category}='contact_data')",
    fields=["Variable_text", "AI_Value", "User_Value"],
    limit=50
)
```

---

## Intelligent Query Patterns

### Pattern 1: Error Analysis Pipeline
```
1. Query BID Feedback where ComparisonResult='Mismatch'
2. Group by Category → identify most common error types
3. For each error type, query VariableTasks to find prompts
4. Cross-reference with NodeVersions to find prompt text
```

### Pattern 2: Performance Trending
```
1. Query DatasetRun where Status='Done', sorted by Created
2. Extract Avg Variable Accuracy over time
3. Identify version changes via AgentVersion links
4. Correlate accuracy changes with version changes
```

### Pattern 3: Ground Truth Gaps
```
1. Query DatasetVariables where Expected Value=BLANK()
2. Filter by Variable Type='Key Variable' (highest priority)
3. Link back to OriginalAgentTask for source documents
4. Generate list for manual annotation
```

---

## Field ID Reference (for API)

> Note: filterByFormula requires field NAMES, not IDs. But IDs are useful for other API calls.

| Table | Key Field | Field ID |
|-------|-----------|----------|
| AgentTasks | Status | fldi0YHCgYJrjRbr8 |
| AgentTasks | Task ID | fldAnP5SBpLxiWtSA |
| VariableTasks | Accuracy | fld53vRcKPcO2JYul |
| VariableTasks | AIValue | flduB9HRcICOjSFqf |
| BID Feedback | ComparisonResult | fldQbcJbPEJdX3qH5 |
| BID Feedback | Category | fldssaNtPunOkB7rC |
| DatasetRun | Status | fldO7Wnx4IqAmrTxY |
| DatasetVariables | Expected Value | fldNJlDMArS5Zdf2I |

---

## Next Steps

To build on this filter guide:
1. Create preset filter library for common queries
2. Build natural language → filter translator
3. Add cross-table query orchestration
4. Implement result aggregation utilities
