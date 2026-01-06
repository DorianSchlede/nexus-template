# AI Development Platform - Database Guide

> **Base ID**: `appFPoOfBpUv73M5A`
> **Last Updated**: 2025-12-28
> **Total Tables**: 25

---

## Quick Reference: When to Use Each Table

| Use Case | Primary Table | Related Tables |
|----------|--------------|----------------|
| Create a new agent | `Agents` | `Workspace`, `Users` |
| Run an agent task | `AgentTasks` | `Agents`, `NodeTasks`, `VariableTasks` |
| Evaluate agent performance | `DatasetRun` | `Datasets`, `DatasetTasks`, `AgentTasks` |
| Track extraction accuracy | `VariableTasks` | `Variables`, `DatasetVariables` |
| Manage prompts/versions | `NodeVersions` | `Nodes`, `AgentVersions` |
| Store expected outputs | `DatasetTasks` | `DatasetVariables`, `DatasetNodes` |
| Get user feedback | `BID Feedback` | `BID Feedback Task`, `Variables` |

---

## Architecture Overview

```
                            ┌─────────────┐
                            │   Users     │
                            └──────┬──────┘
                                   │ owns
                            ┌──────▼──────┐
                            │  Workspace  │
                            └──────┬──────┘
                                   │ contains
                            ┌──────▼──────┐
                            │   Agents    │◄────────────────┐
                            └──────┬──────┘                 │
              ┌────────────────────┼────────────────────┐   │
              │                    │                    │   │
       ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
       │    Nodes    │      │AgentVersions│      │  Datasets   │
       └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
              │                    │                    │
       ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
       │  Variables  │      │NodeVersions │      │ DatasetRun  │
       └─────────────┘      └─────────────┘      └──────┬──────┘
                                                        │
                                                 ┌──────▼──────┐
                                                 │ AgentTasks  │
                                                 └──────┬──────┘
                                          ┌─────────────┼─────────────┐
                                   ┌──────▼──────┐           ┌──────▼──────┐
                                   │  NodeTasks  │           │VariableTasks│
                                   └─────────────┘           └─────────────┘
```

---

## Domain Model: 4 Core Domains

### 1. ENTITY DOMAIN (Structure)
Defines WHAT exists - the blueprints.

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **Users** | Platform users (owners) | `Name`, `Email`, `Role` (admin/ae/pe), `API Key` |
| **Workspace** | Logical container for agents | `Workspace Name`, `Workspace BID` |
| **Agents** | AI agent definitions | `Agent Name`, `Agent BID`, `Agent Type` (Custom/Production/E2E/Staging) |
| **Nodes** | Steps within an agent workflow | `Name`, `Tool BID`, `Index`, `NodeLevel` |
| **Variables** | Data fields extracted by nodes | `Variable Name`, `Variable Type` (Key/Additional/Other), `paramName`, `paramDescription` |

### 2. VERSION DOMAIN (Evolution)
Tracks HOW things change over time.

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **AgentVersions** | Snapshots of agent configuration | `Version Number`, `BeamGraphID`, links to `NodeVersions` |
| **NodeVersions** | Prompt + model configuration | `Prompt`, `Model`, `Tool Type`, `Structured Outputs Full`, `Input Parameters` |

### 3. EXECUTION DOMAIN (Runtime)
Captures WHAT HAPPENED when agent ran.

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **AgentTasks** | Complete agent execution | `Task ID`, `Status`, `Actual Task Input/Output`, `Duration Mins` |
| **NodeTasks** | Individual node execution | `Filled Prompt`, `Node Output`, `UserConsent` |
| **VariableTasks** | Variable extraction result | `AIValue`, `Expected Value`, `Accuracy` |
| **AgentTaskList** | Queue/batch management | Links to `Agents` |

### 4. EVALUATION DOMAIN (Quality)
Measures HOW GOOD the results are.

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **Datasets** | Collection of test cases | `Dataset Name`, `Type` (Small/Edge Case/Full Agent) |
| **DatasetRun** | Evaluation execution | `Status` (Todo/In Progress/Done), `Avg Variable Accuracy` |
| **DatasetTasks** | Expected task-level outcomes | `Task Input`, `Expected Output Status`, `Expected Last Node` |
| **DatasetNodes** | Expected node-level outcomes | Links expected paths |
| **DatasetVariables** | Expected values per variable | `Expected Value`, `Match Type` |
| **Match Types** | How to compare values | `Match Type Name`, `Description` |
| **DatasetRunVariableImprovements** | Tracks optimization iterations | Links to runs/variables |

### 5. FEEDBACK DOMAIN (Human Loop)
Captures CORRECTIONS and learning.

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **BID Feedback** | Human vs AI value comparison | `AI_Value`, `User_Value`, `Final_Value`, `ComparisonResult`, `FinalComparisonResult` |
| **BID Feedback Task** | Task-level feedback aggregation | Links to feedback rows |
| **BID Feedback Contact** | Contact extraction feedback | Contact role/type corrections |

### 6. TEST DOMAIN (Regression)
Manages TEST CASES for quality assurance.

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **TestCase** | Individual test scenario | Links to `Agents`, `AgentTasks` |
| **TestCaseGroup** | Grouped test scenarios | Collection of test cases |
| **ExpectedJson** | Expected JSON outputs | Structured expected results |
| **Prompt** | Prompt templates | `Case Study` prompts |

---

## Table Details & Relationships

### Users (17 fields)
**Primary Key**: `User ID` (formula from Name)
**Role**: Platform user management

```yaml
Links OUT:
  - Agents (1:N) → owns agents
  - Datasets (1:N) → creates datasets
  - AgentVersions (1:N) → created versions
  - NodeVersions (1:N) → created prompt versions

Key Fields:
  - Role: admin | ae | pe
  - API Key: authentication
  - Profile Photo: attachment
```

### Workspace (8 fields)
**Primary Key**: `Workspace AID` (RECORD_ID)
**Role**: Organizational container

```yaml
Links OUT:
  - Agents (1:N) → contains agents

Lookups:
  - Datasets (via Agents)
  - Nodes (via Agents)
  - Variables (via Nodes via Agents)
  - AgentTasks (via Agents)
```

### Agents (37 fields)
**Primary Key**: `Agent AID` (RECORD_ID)
**Role**: Core entity representing an AI agent

```yaml
Links OUT:
  - User (N:1) → owner
  - Workspace (N:1) → belongs to
  - Nodes (1:N) → workflow steps
  - Active Agent Version (1:1) → current version
  - Agent Versions (1:N) → all versions
  - Agent Tasks (1:N) → execution history
  - Datasets (1:N) → evaluation datasets
  - AgentTaskList (1:N) → task queue
  - Dataset Tasks (1:N)
  - TestCase, TestCaseGroup, ExpectedJson

Key Fields:
  - Agent Name, Agent BID
  - Agent Type: Custom Instance | Production | E2E | Staging
  - Monitor Task: TRUE | FALSE
  - API Key, BaseURL
  - Webhook ID
```

### Nodes (24 fields)
**Primary Key**: `Node AID` (RECORD_ID)
**Role**: Individual step in agent workflow

```yaml
Links OUT:
  - Agent (N:1) → belongs to agent
  - Variables (1:N) → data fields to extract
  - Active Node Version (1:1) → current prompt/config
  - NodeVersions (1:N) → version history
  - TaskNodes (1:N) → execution records
  - DatasetNodes (1:N)
  - DatasetRun (1:N)
  - DatasetVariables (1:N)
  - DatasetRunImprovements (1:N)

Key Fields:
  - Name, Tool BID
  - Index (order in workflow)
  - NodeLevel (hierarchy)
  - Node UID
```

### Variables (30 fields)
**Primary Key**: `Variable AID` (RECORD_ID)
**Role**: Data field extracted by a node

```yaml
Links OUT:
  - Node (N:1) → belongs to node
  - NodeVersion (N:M) → version associations
  - VariableTask (1:N) → extraction results
  - DatasetVariable (1:1) → expected value mapping
  - Match Type (N:1) → comparison method
  - DatasetRunImprovements (1:N)
  - BID Feedback (1:N) → human corrections

Key Fields:
  - Variable Name
  - Variable Type: Key Variable | Additional Variable | Other Variable
  - paramName, paramDescription
  - fillType, required, staticValue
```

### AgentVersions (21 fields)
**Primary Key**: `AgentVersion AID` (RECORD_ID)
**Role**: Snapshot of agent configuration

```yaml
Links OUT:
  - Agent (N:1) → parent agent (as Active)
  - Agents (N:M) → all associated agents
  - Created By (N:1) → user
  - Node Versions (1:N) → prompt configs
  - Tasks (1:N) → executions using this version
  - Datasets (1:N) → evaluations
  - DatasetTasks (1:N)
  - DatasetRun (1:N)

Key Fields:
  - AgentVersionName
  - BeamGraphID
  - Version Number
  - Created At, Updated At

Rollups:
  - Avg Production Accuracy
  - Avg Evaluation Accuracy
```

### NodeVersions (37 fields)
**Primary Key**: `NodeVersion AID` (RECORD_ID)
**Role**: Prompt and configuration for a node

```yaml
Links OUT:
  - Node (N:1) → parent node
  - Agent Versions (N:M) → associated agent versions
  - Created By (N:1) → user
  - TaskNodes (1:N)
  - TaskVariables (1:N)
  - Variables (1:N)
  - DatasetNodes (1:N)
  - DatasetRun (1:N)
  - DatasetRunImprovements (1:N)

Key Fields:
  - Node Version Name
  - Prompt (the actual prompt text!)
  - Model (e.g., gpt-4, claude-3)
  - Structured Outputs Full (JSON schema)
  - Input Parameters
  - Condition, Branch Name
  - Require Consent
  - Tool Type
  - Version Number
  - Is Variant
  - BeamToolID

Formulas:
  - Prompt Word Count
```

### AgentTasks (64 fields)
**Primary Key**: `AirtableTaskID` (RECORD_ID)
**Role**: Complete execution of an agent

```yaml
Links OUT:
  - Agent (N:1) → which agent ran
  - AgentVersion (N:1) → which version
  - NodeTasks (1:N) → node-level results
  - VariableTasks (1:N) → variable-level results
  - Dataset (N:M) → evaluation context
  - DatasetRun (N:M) → run context
  - DatasetTasks (N:M) → expected outcomes
  - NodeVersions (N:M)
  - DatasetNodes, DatasetVariables
  - Synced Task (self-reference)
  - Test Case (N:M)

Key Fields:
  - Task ID (Beam platform ID)
  - Custom ID
  - Actual Task Input/Output (JSON)
  - Task Type: Task | Agent Evaluation
  - Status: COMPLETED | FAILED | USER_INPUT_REQUIRED | IN_PROGRESS | QUEUED | CONSENT_REQUIRED
  - Duration Mins
  - Actual Last Node
  - BID Case ID
  - Actual Attachments, Actual URLs

Rollups:
  - Avg Node Accuracy
  - Avg Variable Accuracy
  - Total Variables

Formulas:
  - Last Node Match (path accuracy)
  - Path Selection (Right/Wrong)
  - LangfuseURL, BeamURL (debug links)
```

### NodeTasks (61 fields)
**Primary Key**: `NodeTask AID` (RECORD_ID)
**Role**: Execution of a single node

```yaml
Links OUT:
  - AgentTask (N:1) → parent task
  - Node Version (N:1) → which version ran
  - Node (N:1) → which node
  - VariableTasks (1:N) → variable extractions
  - DatasetNode (N:1) → expected outcome
  - DatasetTasks (N:M)
  - DatasetNodes (N:M)
  - DatasetRun (N:M)
  - DatasetRunLink (N:M)

Key Fields:
  - NodeTask Name
  - Task Type: Task | Agent Evaluation | Node Evaluation
  - NodeTask Status
  - Filled Prompt (actual prompt with values!)
  - Node Output (LLM response)
  - Actual Node Input/Feedback
  - UserConsent
  - AgentGraphNodeID

Rollups:
  - TaskNodeAccuracy
  - Variable Accuracy Avg
  - Total VariableTasks
```

### VariableTasks (62 fields)
**Primary Key**: `VariableTask AID` (RECORD_ID)
**Role**: Individual variable extraction result

```yaml
Links OUT:
  - Variable (N:1) → which variable
  - AgentTask (N:1) → parent agent task
  - NodeTask (N:1) → parent node task
  - Node Versions (N:M)
  - DatasetVariable (N:1) → expected value
  - DatasetRun (N:M)
  - DatasetRunImprovements (N:M)
  - DatasetTasks (N:M)
  - DatasetNodes (N:M)

Key Fields:
  - VariableTask Name
  - AIValue (what the AI extracted)
  - Expected Value (what was expected)
  - Accuracy (1 if match, 0 if not)
  - AI Issue Analysis, AI Optimization Suggestion
  - Variable Task UID
  - Array ID (for array elements)

Formulas:
  - VariableTaskAccuracy
  - LLM Score (AI-generated accuracy)
```

### Datasets (23 fields)
**Primary Key**: `AirtableDatasetID` (RECORD_ID)
**Role**: Collection of test cases for evaluation

```yaml
Links OUT:
  - Agents (N:M) → agents to evaluate
  - Active AgentVersion (N:M)
  - Created By (N:1) → user
  - Agent Tasks (1:N) → execution results
  - DatasetTasks (1:N) → expected outcomes
  - DatasetRuns (1:N) → evaluation runs
  - DatasetVariables (1:N)

Key Fields:
  - Dataset Name
  - Description
  - Type: Small | Edge Case | Full Agent
  - Created At

Counts:
  - Count (Agent Tasks)
  - Count (DatasetRuns)
```

### DatasetRun (48 fields)
**Primary Key**: `DatasetRun AID` (RECORD_ID)
**Role**: Single evaluation run

```yaml
Links OUT:
  - Datasets (N:M) → which datasets
  - AgentTasks (1:N) → execution results
  - AgentVersion (N:M)
  - NodeVersions (N:M)
  - NodeTasks (1:N)
  - VariableTasks (1:N)
  - DatasetTasks (1:N)
  - DatasetVariable (1:N)
  - Node to Run (N:M)
  - DatasetRunImprovements (1:N)
  - Case Study (Prompt) (N:M)

Key Fields:
  - DatasetRun Name
  - Task Type: Agent Evaluation | Node Evaluation
  - Status: Todo | In progress | Done
  - Webhook ID

Rollups:
  - Count Of Tasks
  - Total Variables
  - Total Analyzed Variables
  - Avg Variable Accuracy
  - Avg KeyV/AddV/OtherV Accuracy
```

### DatasetTasks (41 fields)
**Primary Key**: `DatasetTask AID` (RECORD_ID)
**Role**: Expected task-level outcomes - the "ground truth" for what a task SHOULD produce

```yaml
Links OUT:
  - Dataset (N:1) → parent dataset
  - Agent Task (1:N) → actual execution results
  - DatasetRun (N:M) → evaluation runs
  - Expected Last Node (N:1) → which node should be final
  - DatasetNodes (1:N) → expected node-level outcomes
  - DatasetVariables (1:N) → expected variable values
  - Agents (N:M) → which agents to test
  - AgentVersions (N:M) → which versions
  - Node Tasks (1:N) → actual node executions
  - Variables Tasks (1:N) → actual variable extractions

Key Fields:
  - DatasetTask Name
  - TaskInput (the input JSON to send)
  - Attachments (test attachments)
  - Expected Output Status: Done | In Progress | To Do
  - Expected Last Node Status: To Do | In Progress | Completed
  - DatasetTask Status: To Do | In progress | Open Question | Completed
  - Beam Task ID (external reference)
  - Dataset Task UID
  - Notes

Lookups (from Agent Task):
  - Actual Last Node
  - BID Case ID
  - Actual Task Input
  - Actual Attachments
  - URLs

Rollups:
  - Accuracy Rollup (from Variables Tasks) → avg accuracy score
  - Evaluation Tasks (count)
```

### DatasetNodes (36 fields)
**Primary Key**: `RecordID` (RECORD_ID)
**Role**: Expected node-level outcomes - which node should run and what it should produce

```yaml
Links OUT:
  - Dataset Task (N:M) → parent test case
  - NodeTask (1:N) → actual node executions
  - NodeVersion (N:1) → expected version to run
  - Original Task (N:1) → reference AgentTask
  - Original TaskNode (N:1) → reference NodeTask
  - DatasetVariables (1:N) → expected variable values
  - DatasetTasks (N:M) → additional task links
  - VariableTasks (1:N) → actual variable results

Key Fields:
  - DatasetNode Name (combines test case + node)
  - NodeInput (expected input JSON)
  - DatasetVariableRaw (raw expected values)
  - Dataset Node UID

Lookups (from NodeTask):
  - Expected Output Status
  - Filled Prompt
  - Node Output
  - Actual Node Input
  - Original Prompt Lookup
  - Original Output Schema
  - Model
  - Input Parameters
  - Condition
  - Branch Name
  - Require Consent
  - Agent, Workspace
```

### DatasetVariables (50 fields)
**Primary Key**: `DatasetVariable AID` (RECORD_ID)
**Role**: Expected values for each variable - the "ground truth" for extraction accuracy

```yaml
Links OUT:
  - Variable (N:M) → schema variable definition
  - DatasetTask (N:1) → parent test case
  - DatasetNodes (N:1) → parent node expectation
  - Datasets (N:M) → parent dataset
  - DatasetRun (N:M) → evaluation runs
  - OriginalAgentTask (N:1) → source task
  - OriginalVariableTask (1:N) → source extraction
  - Node (N:1) → which node extracts this
  - Expected JSON (N:M) → structured expected output

Key Fields:
  - Variable Name (combined test case + variable)
  - Expected Value (THE GROUND TRUTH!)
  - Expected Value Status: To Do | In progress | Done
  - Latest AI Value (most recent extraction)
  - Array Index (for array elements)
  - DatasetVariable UID
  - VariableMapping UID (composite key)
  - Feedback (notes/corrections)

Lookups:
  - BID Case ID (from OriginalAgentTask)
  - AIValue (from OriginalVariableTask)
  - VariableTaskAccuracy (from OriginalVariableTask)
  - Variable Type (from Variable)
  - Status (from OriginalAgentTask)
  - Custom ID, Actual Task Input, Agent

BID Integration:
  - BIDFeedbackID, BIDFeedbackID Link
  - GroupID, User_Value, AI_Value
  - ComparisonResult, FinalComparisonResult

Formulas:
  - Map To Variable Task ID (for matching)
  - Review (AI matches expected?)
```

### BID Feedback (54 fields)
**Primary Key**: Record ID
**Role**: Human-in-the-loop corrections - captures when AI was wrong and human fixed it

```yaml
Links OUT:
  - Variable (N:M) → which variable was corrected
  - BID Task (N:1) → parent feedback task
  - GroupID (N:M) → BID Feedback Contact (for contact extractions)

Key Fields:
  - RefNo (reference number)
  - CaseID (case identifier)
  - Variable_text, Variable_DE (variable names in EN/DE)
  - TaskID (Beam task reference)
  - RunID (run reference)

Values:
  - AI_Value (what AI extracted)
  - User_Value (what human corrected to)
  - Final_Value (resolved/accepted value)

Comparison:
  - ComparisonResult: Match | AI NULL | Mismatch
  - FinalComparisonResult: - | Match | Mismatch | AI NULL
  - Accuracy (formula: 1 if Match, 0 otherwise)

Timestamps:
  - AI_CreationTime
  - User_CreationTime
  - TaskCreationTime
  - TaskCompletionTime
  - User_Response_Time_Days

Classification:
  - Category: contact_data | classification | classification_data | edge_case_variables | feedback
  - Mainfolder: Insolvenz
  - Subfolder: Schreiben Rechtsanwalt | Schreiben Schuldnerb. | etc.
  - Classification, Required
  - Group: Inso 1-5
  - Agent Version: v1.1
  - State (numeric)

Lookups (from BID Task):
  - AI_Classification, User_Classification
  - Basic Reasoning, Classification Reasoning
  - Variable_Contact_Null, Variable_Contact_Mismatch
  - Variable_ClassificationData_Mismatch

Lookups (from GroupID):
  - Contact Role, Contact Type
  - Missing Contact Variables
  - Wrong Contact Variables

Links:
  - Task Link (formula → BID platform URL)
```

### BID Feedback Task (26 fields)
**Primary Key**: Record ID
**Role**: Aggregates feedback at task level - summarizes all variable corrections for a single task

```yaml
Links OUT:
  - BID Feedback (1:N) → individual variable corrections

Key Fields:
  - Task ID (Beam task reference)
  - Task Link (formula → BID platform URL)

Error Analysis:
  - Variable_Contact_Null (missing contact data)
  - Variable_Contact_Mismatch (wrong contact data)
  - Variable_ClassificationData_Mismatch
  - AI_Classification, User_Classification
  - Right Classification (formula: AI matches User?)

Rollups (from BID Feedback):
  - Group
  - ContactRole_MismatchOrNull
  - AI_ContactRole_MismatchOrNull
  - User_ContactRole_MismatchOrNull
  - UserType_ContactRole_MismatchOrNull

GroupID Lookups:
  - GroupID_Contact_Null
  - GroupID_Contact_Mismatch

AI Analysis Fields:
  - Root Analysis (AI-generated analysis of errors)
  - Classification Reasoning
  - Basic Reasoning (formula: identifies error type)
  - Basic Reasoning v2 (formula: multi-error detection)

Error Types (from Basic Reasoning):
  - "Wrong Classification" - AI classified wrong category
  - "Wrong Data Extraction" - classification right, data wrong
  - "Missing Contact Data" - contact fields empty
  - "Wrong Contact Data" - contact fields incorrect
```

### BID Feedback Contact (9 fields)
**Primary Key**: `Group ID`
**Role**: Groups contact-related feedback by contact entity

```yaml
Links OUT:
  - BID Feedback (1:N) → feedback rows for this contact

Key Fields:
  - Group ID (unique contact identifier)

Lookups (from BID Feedback):
  - Contact Role (what role the contact has)
  - Contact Type (type of contact)
  - Missing Contact Variables (which fields were null)
  - Wrong Contact Variables (which fields were wrong)
  - Category
  - Variable_text
  - User_Value
```

---

## Common Query Patterns

### 1. Get Agent Performance
```
AgentTasks
  → filter by Agent, DatasetRun
  → rollup Avg Variable Accuracy
```

### 2. Find Accuracy Issues
```
VariableTasks
  → filter where Accuracy = 0
  → lookup Variable.Variable Name
  → lookup NodeTask.Filled Prompt
```

### 3. Compare Versions
```
AgentVersions
  → compare Version A vs Version B
  → rollup Avg Production Accuracy
```

### 4. Track Feedback Loop
```
BID Feedback
  → filter by CaseID
  → check ComparisonResult
  → update prompts based on Mismatch
```

### 5. Run Evaluation
```
1. Create DatasetRun linked to Dataset
2. Trigger AgentTasks via webhook
3. Match VariableTasks to DatasetVariables
4. Calculate Accuracy rollups
```

---

## Field Naming Conventions

| Prefix/Suffix | Meaning |
|---------------|---------|
| `*_AID` | Airtable Record ID (RECORD_ID()) |
| `*_BID` | Beam Platform ID |
| `*_UID` | Unique Identifier (external) |
| `* (from X)` | Lookup field from linked table |
| `* (from X) (from Y)` | Nested lookup |
| `Avg *` | Rollup average |
| `Count *` | Rollup count |
| `Total *` | Rollup sum |

---

## Status Values

### AgentTasks.Status
- `COMPLETED` - Task finished successfully
- `FAILED` - Task failed
- `USER_INPUT_REQUIRED` - Waiting for user input
- `IN_PROGRESS` - Currently running
- `QUEUED` - Waiting to start
- `CONSENT_REQUIRED` - Waiting for user consent

### DatasetRun.Status
- `Todo` - Not started
- `In progress` - Running
- `Done` - Completed

### BID Feedback.ComparisonResult
- `Match` - AI matched human
- `AI NULL` - AI returned nothing
- `Mismatch` - AI was wrong

---

## Integration Points

### Webhook Triggers
- `Agents.Webhook ID` - Trigger agent runs
- `DatasetRun.Webhook ID` - Trigger evaluations

### External Links
- `AgentTasks.LangfuseURL` - Tracing/debugging
- `AgentTasks.BeamURL` - Platform task view
- `BID Feedback.Task Link` - BID platform

### API Keys
- `Users.API Key` - User authentication
- `Agents.API Key` - Agent-level auth
