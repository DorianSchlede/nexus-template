# Query Guide: AI Development Platform

> **Purpose**: How to query Airtable for MetaTuner dataset construction
> **Base ID**: `appFPoOfBpUv73M5A`
> **Last Updated**: 2025-12-28

---

## Table IDs Quick Reference

| Table | ID | Primary Use |
|-------|-----|-------------|
| Agents | `tblVEJD2inVhae855` | Filter by agent |
| Nodes | `tblPJ9VKG74mKv7JK` | Filter by node |
| NodeVersions | `tblh0GsN5Et3ApzLS` | Get prompt templates |
| Variables | `tblf2ohTHmsucjVUj` | Variable definitions |
| AgentTasks | `tblsEzGhn4XJjNrkt` | Task executions |
| NodeTasks | `tblNdPnVWDragZtcK` | Node executions (filled prompts) |
| VariableTasks | `tblKhpqLs06kI01yv` | Extraction results (AIValue) |
| Datasets | `tbltUrvSBnfOb4S8v` | Test dataset containers |
| DatasetTasks | `tbl9lACSI4fDUzAv4` | Expected task outcomes |
| DatasetNodes | `tblflNTX3tR0onX13` | Expected node outcomes |
| DatasetVariables | `tblsHYj8CrdHbY8Bt` | **Ground truth** (Expected Value) |
| BID Feedback | `tblH9H6wAD90a9Q88` | Human corrections |

---

## Core Data Flow

```
                    GROUND TRUTH                          ACTUAL EXECUTION
                    ════════════                          ════════════════

DatasetVariables ◄──────────────────────────────────────► VariableTasks
     │                                                          │
     │  Expected Value                              AIValue     │
     │  Variable (link)                             Variable    │
     │  DatasetTask (link)                          AgentTask   │
     │  OriginalAgentTask (link) ◄─── MUST MATCH ──► AgentTask  │
     │                                                          │
     ▼                                                          ▼
DatasetNodes ◄─────────────────────────────────────────► NodeTasks
     │                                                          │
     │  NodeVersion (link)                          Filled Prompt
     │  NodeInput                                   Node Output │
     │                                                          │
     ▼                                                          ▼
NodeVersions                                              AgentTasks
     │                                                          │
     │  Prompt (template)                           Task Input  │
     │  Model                                       Task Output │
     │  Structured Outputs                          Status      │
```

---

## Link Integrity: How Records Connect

### The Join Key

To match `VariableTasks` (actual) with `DatasetVariables` (expected), use these formulas:

**VariableTasks.`Map Dataset Variable ID`**:
```
{DatasetTasks (from AgentTask)} | {Array ID} | {Variable Name}
```

**DatasetVariables.`Map To Variable Task ID`**:
```
{DatasetTask} | {Array Index} | {Variable Name}
```

These should match for the same extraction!

### Direct Links to Verify

| From Table | Link Field | To Table | Verification |
|------------|------------|----------|--------------|
| VariableTasks | `DatasetVariable` | DatasetVariables | Direct link exists |
| VariableTasks | `AgentTask` | AgentTasks | Same as DatasetVariables.OriginalAgentTask |
| DatasetVariables | `OriginalVariableTask` | VariableTasks | Inverse of above |
| DatasetVariables | `DatasetNodes` | DatasetNodes | Node context for variable |
| DatasetNodes | `NodeVersion` | NodeVersions | Expected prompt version |
| DatasetNodes | `NodeTask` | NodeTasks | Actual node execution |

---

## Query Patterns for Dataset Construction

### 1. Get All Expected Values with Context

**Table**: `DatasetVariables`

**Fields to fetch**:
```
Variable Name
Expected Value
Expected Value Status
Variable Type (from Variable)
Agent (from OriginalAgentTask)
DatasetTask
DatasetNodes
OriginalVariableTask
AIValue (from OriginalVariableTask)
VariableTaskAccuracy (from OriginalVariableTask)
```

**Filter**: `{Expected Value}!=BLANK()`

**Purpose**: All ground truth values that are filled in.

---

### 2. Get Actual Extractions with Accuracy

**Table**: `VariableTasks`

**Fields to fetch**:
```
VariableTask Name
AIValue
Expected Value
Accuracy
VariableTaskAccuracy
Variable Name
Agent (from Node) (from Variable)
NodeTaskPrompt
DatasetVariable
```

**Filter**: `{DatasetVariable}!=BLANK()`

**Purpose**: All extractions that have ground truth to compare against.

---

### 3. Get Prompts for a Specific Node

**Table**: `NodeVersions`

**Fields to fetch**:
```
Node Version Name
Prompt
Model
Structured Outputs Full
Input Parameters
Version Number
```

**Filter**: `FIND('NodeName', {Node})`

**Purpose**: Get all prompt versions for a specific node.

---

### 4. Find Low Accuracy Cases (Edge Cases)

**Table**: `VariableTasks`

**Filter**:
```
AND(
  {VariableTaskAccuracy}=0,
  {DatasetVariable}!=BLANK()
)
```

**Purpose**: Cases where AI got it wrong - best for improvement datasets.

---

### 5. Find High Accuracy Cases (Happy Path)

**Table**: `VariableTasks`

**Filter**:
```
AND(
  {VariableTaskAccuracy}=1,
  {DatasetVariable}!=BLANK()
)
```

**Purpose**: Cases where AI got it right - for regression testing.

---

### 6. Find Human Corrections

**Table**: `BID Feedback`

**Filter**: `{ComparisonResult}='Mismatch'`

**Fields**:
```
Variable_text
AI_Value
User_Value
Category
TaskID
```

**Purpose**: Human-corrected values for training data.

---

### 7. Validate Link Integrity

**Check 1**: DatasetVariables without VariableTask link
```
Table: DatasetVariables
Filter: AND({Expected Value}!=BLANK(), {OriginalVariableTask}=BLANK())
```

**Check 2**: VariableTasks without DatasetVariable link
```
Table: VariableTasks
Filter: AND({AIValue}!=BLANK(), {DatasetVariable}=BLANK())
```

**Check 3**: DatasetNodes without NodeVersion
```
Table: DatasetNodes
Filter: {NodeVersion}=BLANK()
```

---

## Building a Complete Test Case

To build one MetaTuner test item, you need:

```python
{
    "id": DatasetVariables.record_id,
    "input": {
        # From AgentTasks via DatasetVariables.OriginalAgentTask
        "taskInput": AgentTasks["Actual Task Input"]
    },
    "expectedOutput": DatasetVariables["Expected Value"],
    "actualOutput": VariableTasks["AIValue"],  # via OriginalVariableTask link
    "prompt": NodeTasks["Filled Prompt"],      # via DatasetNodes.NodeTask
    "score": VariableTasks["VariableTaskAccuracy"],
    "metadata": {
        "agent": DatasetVariables["Agent (from OriginalAgentTask)"],
        "variable": DatasetVariables["Variable Name"],
        "variableType": DatasetVariables["Variable Type (from Variable)"],
        "nodeVersion": DatasetNodes["NodeVersion"],
        "source": f"DatasetVariables.{record_id}"
    }
}
```

---

## Query Execution

### Using Existing Scripts

```bash
# From Nexus root
python 00-system/skills/airtable/airtable-master/scripts/query_records.py \
  --base "appFPoOfBpUv73M5A" \
  --table "DatasetVariables" \
  --filter "{Expected Value}!=BLANK()" \
  --fields "Variable Name,Expected Value,Agent (from OriginalAgentTask)" \
  --limit 100 \
  --json
```

### Using Python Directly

```python
import os
import requests

BASE_ID = "appFPoOfBpUv73M5A"
TABLE_NAME = "DatasetVariables"
API_KEY = os.environ.get("AIRTABLE_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

params = {
    "filterByFormula": "{Expected Value}!=BLANK()",
    "fields[]": ["Variable Name", "Expected Value", "OriginalVariableTask"],
    "pageSize": 100
}

url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
response = requests.get(url, headers=headers, params=params)
records = response.json().get("records", [])
```

---

## Aggregation Queries

### Count Expected Values by Agent

```python
# Pseudo-query logic
1. Fetch all DatasetVariables with Expected Value
2. Follow link: DatasetVariables → OriginalAgentTask → Agent
3. Group by Agent name
4. Count per group
```

### Count by Variable Type

```python
# Filter by Variable Type lookup
{Variable Type (from Variable)} = "Key Variable"
{Variable Type (from Variable)} = "Additional Variable"
```

### Count by Accuracy

```python
# From VariableTasks
accuracy_0 = filter("{VariableTaskAccuracy}=0")  # Wrong
accuracy_1 = filter("{VariableTaskAccuracy}=1")  # Correct
```

---

## Rate Limits & Best Practices

| Limit | Value |
|-------|-------|
| Requests per second (per base) | 5 |
| Requests per second (per token) | 50 |
| Max records per request | 100 |
| Max batch size (create/update) | 10 |

**Best Practices**:
1. Always paginate - use `offset` from response
2. Cache results locally when possible
3. Use `fields[]` to fetch only needed columns
4. Batch requests with 200ms delay between
5. Handle 429 (rate limit) with exponential backoff

---

## Common Pitfalls

### 1. Linked Record Values
Linked record fields return arrays of record IDs, not values.
Use lookup fields to get actual values:
- `{Agent}` → returns `["recXXX"]`
- `{Agent Name (from Agent)}` → returns `["Agent Name"]`

### 2. Formula Fields
Formula fields are read-only and computed server-side.
Can't filter by formula fields that reference other formula fields.

### 3. Multiple Select / Multiple Links
These return arrays. Use `FIND()` or `ARRAYJOIN()` for filtering:
```
FIND("value", ARRAYJOIN({MultiSelectField}))
```

### 4. Blank vs Empty
- `BLANK()` = field has no value
- `""` = field has empty string
Use `{Field}!=BLANK()` for most cases.

---

## Next Steps

1. **Run inventory.py** - Get counts of all expected values
2. **Run validate_links.py** - Find broken/missing links
3. **Run export_dataset.py** - Export MetaTuner-compatible JSON
