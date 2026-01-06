# MetaTuner (AutoTuner) Algorithm Documentation

> **Generated**: 2025-12-28
> **Source**: `C:\Users\dsber\infinite\auto-company\mutagent-monorepo\mutagent\src\framework\metatuner\`
> **Purpose**: Comprehensive documentation to inform test dataset construction for Airtable integration

---

## Table of Contents

1. [Core Architecture](#core-architecture)
2. [Pipeline Stages](#pipeline-stages)
3. [Services Layer](#services-layer)
4. [Data Models](#data-models)
5. [API Endpoints](#api-endpoints)
6. [Existing Test Patterns](#existing-test-patterns)
7. [Test Dataset Requirements](#test-dataset-requirements)
8. [Airtable Mapping Guide](#airtable-mapping-guide)

---

## Core Architecture

### Overview

The AutoTuner (internally called `MetaTuner`) is an iterative prompt optimization framework implemented in TypeScript. It automatically improves prompts by analyzing execution feedback, identifying failure patterns, and generating optimized prompt variants through LLM-based mutation. The system uses a hybrid Class-Based + Event-Driven architecture with immutable state management patterns.

**Key Algorithm Flow:**
1. Execute prompts against test datasets
2. Analyze execution feedback to identify patterns
3. Optimize/mutate prompts based on failure analysis
4. Evaluate optimized prompts for improvement
5. Consolidate results and iterate until goal is reached

### Main Entry Points

**File:** `src/framework/metatuner/index.ts`

**Primary Class:** `MetaTuner`

| Method | Description |
|--------|-------------|
| `run(input: MetaTunerInput)` | Single iteration execution - runs one optimization cycle |
| `tune(input: MetaTunerInput)` | Multi-iteration tuning - loops until goal/limit reached |
| `stream(input: MetaTunerInput)` | AsyncGenerator yielding events for real-time monitoring |
| `loadCheckpoint(checkpointId)` | Resume from saved state |
| `saveCheckpoint(state, id)` | Persist current state |

### Execution Flow

```
                                     +------------------+
                                     |    MetaTuner     |
                                     |   .run() / .tune()|
                                     +--------+---------+
                                              |
                                              v
                                     +------------------+
                                     |  TunerExecutor   |
                                     |   .execute()     |
                                     +--------+---------+
                                              |
           +----------------------------------+----------------------------------+
           |                                  |                                  |
           v                                  v                                  v
    +-------------+                   +---------------+                  +-------------+
    |   init()    |                   |  useContext() |                  |  validate() |
    | (Pipeline   |                   | (Create       |                  | (Check      |
    |  selection) |                   |  PromptTuner  |                  |  state)     |
    +-------------+                   |  Context)     |                  +-------------+
                                      +---------------+
                                              |
                                              v
                              +-------------------------------+
                              |     PromptTunerPipeline       |
                              |       (7 Stages)              |
                              +-------------------------------+
```

### State Management

**State Hierarchy:**

```
MetaTunerState
├── id: string                          // Unique session ID
├── checkpointId?: string               // For resumption
├── identifiers?: MetaTunerIdentifiers  // Context (user, workspace, etc.)
├── input?: MetaTunerInput              // Original input configuration
├── config: MetaTunerConfig             // Optimization parameters
├── status: MetaTunerStatus             // READY|RUNNING|PAUSED|COMPLETED|FAILED|INTERRUPTED
├── globalContext?: MetaTunerGlobalContext
│   ├── iteration: number               // Current iteration number
│   ├── bestIteration?: number          // Best performing iteration
│   ├── highestScore?: number           // Best score achieved
│   ├── currentScore?: number           // Current iteration score
│   ├── previousScore?: number          // Previous iteration score
│   ├── improvementRatio?: number       // Score improvement ratio
│   ├── scoreHistory?: number[]         // All historical scores
│   ├── stagnationCount?: number        // Iterations without improvement
│   ├── lossCount?: number              // Iterations with declining score
│   ├── isTerminated?: boolean          // Early termination flag
│   └── context?: PromptTunerContext    // Mode-specific context
├── current?: MetaTunerIteration        // Current iteration snapshot
└── iterations?: MetaTunerIteration[]   // All iteration history
```

### Configuration Options

```typescript
interface MetaTunerConfig {
  tuningMode: MetaTunerMode;      // PROMPT | TOOL | WORKFLOW | AGENT
  maxIterations: number;          // Default: 10
  threshold: number;              // Goal score (0.00-1.00), Default: 0.9
  patience: number;               // Iterations without improvement before early stop, Default: 3
  minImprovement: number;         // Minimum improvement to count as success, Default: 0.01
  improvementRatio: number;       // Required improvement ratio, Default: 0.1
  mutationConfig?: MutationConfig;
  retryConfig?: RetryConfig;
}
```

---

## Pipeline Stages

The pipeline consists of 7 stages executed in sequence.

### Stage 1: Dataset Analysis

**Purpose:** Validates and prepares the tuning dataset by analyzing existing executions or routing to execution if none exist.

**Inputs:**
```typescript
interface DatasetAnalysisInput {
  prompt: string | ChatPromptTemplate;
  inputSchema: z.ZodSchema<any>;
  outputSchema: z.ZodSchema<any>;
  dataset: PromptDataset;
  evals: PromptEvaluation[];
  executions?: PromptExecutions;  // Optional - if missing, routes to Dataset Execution
}
```

**Outputs:**
- `state.globalContext.context.executions` (PromptDatasetExecution)
- `state.globalContext.context.evals` (PromptEvaluation[])

### Stage 2: Dataset Execution

**Purpose:** Executes the prompt against all dataset items and collects evaluation results.

**Inputs:**
```typescript
interface DatasetExecutionContext {
  dataset: PromptDataset;
  prompt: MutationPrompt;
  evals: PromptEvaluation[];
}
```

**Outputs:**
```typescript
interface PromptDatasetExecution {
  id: string;
  dataset?: PromptDataset;
  results: PromptExecution[];
}
```

### Stage 3: Feedback Analysis

**Purpose:** Analyzes execution results to identify patterns, root causes, and generate actionable recommendations.

**Outputs:**
```typescript
interface FeedbackAnalysis {
  successPatterns: string[];
  failurePatterns: string[];
  rootCauses: RootCause[];
  promptModifications: PromptModification[];
  preservationElements: string[];
  potentialTradeoffs: string[];
  implementationPriority: string[];
  summary: string;
}
```

### Stage 4: Prompt Mutation

**Purpose:** Generates an improved version of the prompt based on feedback analysis.

**Outputs:**
```typescript
interface MutationOutput {
  critique: string;
  keyIssues: string[];
  modifications: PromptMutation[];
  outputVariables: OutputVariable[];
  revisedPrompt: string;
  preservedElements: string[];
  potentialRegressions: string[];
  diffChanges: string;
}
```

### Stage 5: Prompt Input Mutation

**Purpose:** Mutates the input parameter descriptions and schema. (TODO - placeholder)

### Stage 6: Prompt Output Mutation

**Purpose:** Mutates the output parameter descriptions and schema. (TODO - placeholder)

### Stage 7: Result Analysis

**Purpose:** Analyzes mutation results, updates metrics, determines if tuning should continue or terminate.

**Termination Conditions:**
- `lossCount >= 3`: Too many performance decreases
- `stagnationCount >= patience`: No improvement for configured patience period
- `bestScore >= threshold`: Goal score reached (default: 0.9)
- `improvementRatio >= config.improvementRatio`: Improvement ratio achieved
- `iterations.length >= maxIterations`: Max iterations reached (default: 10)

---

## Data Models

### Core Input Types

```typescript
interface MetaTunerPromptInput {
  prompt: string | ChatPromptTemplate;
  inputSchema: z.ZodSchema<any>;
  dataset: PromptDataset;
  evals: MetaTunerEval[];
  outputSchema?: z.ZodSchema<any>;
  executions?: PromptExecutions;
}
```

### Dataset Structure

```typescript
interface PromptDataset {
  name: string;
  description: string;
  items: PromptDatasetItem[];
  metadata?: Record<string, any>;
  tags?: string[];
}

interface PromptDatasetItem {
  id: string;
  input: Record<string, any>;           // Input values matching inputSchema
  actualOutput?: string | Record<string, any>;
  expectedOutput?: string | Record<string, any>;
  userFeedback?: string;
  metadata?: Record<string, any>;
}
```

### Execution Results

```typescript
interface PromptExecution {
  id: string;
  prompt?: string;
  input?: Record<string, any>;
  output: string | Record<string, any>;
  expectedOutput?: string | Record<string, any>;
  systemFeedback?: string;
  userFeedback?: string;
  evaluation?: PromptEvaluationResult;
  metadata?: Record<string, any>;
}
```

### Evaluation Results

```typescript
interface PromptEvaluationResult {
  id: string;
  success: boolean;
  score: number;           // 0.0 - 1.0
  llmScore?: number;
  successRate?: number;
  evaluations: PromptEvaluationMetricResult[];
}

interface PromptEvaluationMetricResult {
  id: string;
  name: string;
  reasoning: string;
  evaluatedChecklist: string[];
  score: number;
  llmScore: number;
  success: boolean;
  failureMode: string;
  systemFeedback: string;
  error?: string;
}
```

### MutationPrompt (Versioned Prompt)

```typescript
interface MutationPrompt {
  version: number;
  prompt: string | ChatPromptTemplate;
  inputSchema?: z.ZodSchema<any>;
  inputParameters?: Record<string, any>;
  outputSchema?: z.ZodSchema<any>;
  outputParameters?: Record<string, any>;
  model?: string;
}
```

---

## API Endpoints

### Prompts Module

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/prompt` | List prompts with pagination |
| POST | `/api/prompt` | Create new prompt |
| GET | `/api/prompt/:id` | Get prompt by ID |
| PATCH | `/api/prompt/:id` | Update prompt |
| DELETE | `/api/prompt/:id` | Delete prompt |
| POST | `/api/prompt/:id/versions` | Create new version |

### Prompt Datasets Module

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/prompts/datasets` | List datasets |
| GET | `/api/prompts/datasets/:id` | Get dataset by ID |
| PATCH | `/api/prompts/datasets/:id` | Update dataset |
| DELETE | `/api/prompts/datasets/:id` | Delete dataset |
| POST | `/api/prompts/datasets/:id/clone` | Clone dataset |
| GET | `/api/prompts/datasets/:id/export` | Export dataset |
| GET | `/api/prompts/datasets/:id/items` | List dataset items |
| POST | `/api/prompts/datasets/:id/items` | Add dataset item |
| POST | `/api/prompts/datasets/:id/items/bulk` | Bulk add items |

### Prompt Evaluations Module

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/prompts/evaluations` | List evaluations |
| POST | `/api/prompts/evaluations` | Create evaluation |
| GET | `/api/prompts/evaluations/:id` | Get evaluation by ID |
| POST | `/api/prompts/evaluations/:id/run` | Run evaluation (NOT IMPLEMENTED) |
| GET | `/api/prompts/evaluations/:id/result` | Get evaluation results |

---

## Existing Test Patterns

### Mock Data Structures

```typescript
const config: MetaTunerConfig = {
  tuningMode: MetaTunerMode.PROMPT,
  maxIterations: 10,
  threshold: 0.9,
  patience: 3,
  minImprovement: 0.01,
  improvementRatio: 0.1,
  mutationConfig: {
    promptMutation: {
      model: 'gpt-4o',
      evolutionContext: 'You are a helpful assistant.',
    },
  },
  retryConfig: {
    enabled: true,
    maxRetries: 3,
    retryDelay: 1000,
  },
};
```

### Gaps in Test Coverage

1. **LLM Integration Tests Missing** - No actual LLM call mocking
2. **Dataset Input Validation** - No tests for malformed datasets
3. **Evaluation Execution** - No tests for metric calculations
4. **Mutation Pipeline Tests** - Stages not tested in isolation
5. **Error Recovery** - No retry logic tests
6. **Iteration Loop Tests** - Incomplete implementation
7. **Streaming Tests** - Generator not tested
8. **Checkpoint/Restore Tests** - Not tested

---

## Test Dataset Requirements

Based on the algorithm analysis, test datasets for Airtable should include:

### Required Fields per Test Case

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier |
| `input` | JSON | Yes | Input matching inputSchema |
| `expectedOutput` | JSON | Yes | Ground truth output |
| `actualOutput` | JSON | No | LLM-generated output |
| `userFeedback` | string | No | Human feedback |
| `systemFeedback` | string | No | LLM-generated feedback |
| `score` | number | No | Evaluation score (0.0-1.0) |
| `success` | boolean | No | Pass/fail flag |
| `metadata` | JSON | No | Additional context |

### Dataset Categories to Build

1. **Happy Path Dataset** - Cases that should succeed
2. **Edge Case Dataset** - Boundary conditions
3. **Failure Dataset** - Known failure patterns
4. **Regression Dataset** - Previously failed, now fixed
5. **Performance Dataset** - Large/complex inputs

### Per-Stage Test Data Requirements

| Stage | Required Data |
|-------|--------------|
| Dataset Analysis | Valid PromptDataset with items matching schemas |
| Dataset Execution | MutationPrompt + PromptEvaluation definitions |
| Feedback Analysis | PromptDatasetExecution with mixed success/failure |
| Prompt Mutation | FeedbackAnalysis with identified issues |
| Result Analysis | Previous + current PromptDatasetExecution |

---

## Airtable Mapping Guide

### Mapping from AI Development Platform to MetaTuner

| Airtable Table | MetaTuner Type | Field Mapping |
|----------------|----------------|---------------|
| `NodeVersions.Prompt` | `MutationPrompt.prompt` | Direct mapping |
| `NodeTasks.Filled Prompt` | `PromptExecution.prompt` | Prompt with values |
| `NodeTasks.Node Output` | `PromptExecution.output` | Actual LLM response |
| `DatasetVariables.Expected Value` | `PromptDatasetItem.expectedOutput` | Ground truth |
| `VariableTasks.AIValue` | `PromptExecution.output` | Extracted value |
| `VariableTasks.Accuracy` | `PromptEvaluationResult.score` | 0 or 1 |
| `BID Feedback.User_Value` | `PromptDatasetItem.userFeedback` | Human correction |
| `BID Feedback.ComparisonResult` | `PromptEvaluationResult.success` | Match/Mismatch |

### Recommended Airtable Structure for Test Datasets

**Table: TestDatasets**
- Dataset Name (text)
- Description (long text)
- Type (single select: Small, Edge Case, Full Agent)
- Tags (multiple select)

**Table: TestDatasetItems**
- Dataset (link to TestDatasets)
- Input JSON (long text)
- Expected Output JSON (long text)
- Actual Output JSON (long text)
- User Feedback (long text)
- Score (number 0-1)
- Success (checkbox)
- Metadata JSON (long text)

**Table: TestEvaluations**
- Dataset (link to TestDatasets)
- Prompt Version (link to prompts)
- Avg Score (rollup)
- Success Rate (rollup)
- Run Date (date)
- Status (single select: Pending, Running, Complete)

---

## Key Files Reference

| File Path | Purpose |
|-----------|---------|
| `metatuner/index.ts` | Public exports |
| `metatuner/metatuner.ts` | Main MetaTuner class |
| `metatuner/executor/tuner-executor.ts` | Execution orchestration |
| `metatuner/config/metatuner-config.ts` | Configuration & defaults |
| `metatuner/types/tuner-state.ts` | MetaTunerState class |
| `metatuner/types/tuner-input.ts` | Input type definitions |
| `metatuner/pipelines/prompt-tuner/prompt-tuner-pipeline.ts` | Pipeline definition |
| `metatuner/pipelines/prompt-tuner/types/*.ts` | Prompt-specific types |
| `metatuner/pipelines/prompt-tuner/stages/*/` | Stage implementations |

---

*Documentation compiled from parallel research agents analyzing the mutagent-monorepo codebase.*
