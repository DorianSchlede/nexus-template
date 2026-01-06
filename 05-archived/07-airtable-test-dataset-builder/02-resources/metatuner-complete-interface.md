# MetaTuner Complete Interface Reference

> **Generated**: 2026-01-04
> **Purpose**: Define the complete JSON structure for MetaTuner-compatible test datasets

---

## Complete Export Structure

The export should contain everything needed to run MetaTuner optimization:

```json
{
  "metadata": {
    "datasetName": "string",
    "agent": "string",
    "node": "string",
    "promptType": "extraction|classification|generation|routing",
    "tier": "gold|silver|bronze",
    "itemCount": number,
    "outputVariableCount": number,
    "averageScore": number,
    "succeededCount": number,
    "failedCount": number,
    "generated_at": "ISO timestamp",
    "source": "airtable-export"
  },
  "metatunerPromptInput": MetaTunerPromptInput,
  "promptDataset": PromptDataset,
  "PromptExecutions": PromptExecutions
}
```

---

## Interface Definitions

### 1. PromptDataset (Core Dataset)

```typescript
interface PromptDataset {
  name: string;           // Dataset name
  description: string;    // Dataset description
  items: PromptDatasetItem[];  // Test cases
  metadata?: Record<string, any>;  // Custom metadata
  tags?: string[];        // Tags for filtering
}

interface PromptDatasetItem {
  id: string;                                    // Unique item ID
  input: Record<string, any>;                    // Input variables for prompt
  actualOutput?: string | Record<string, any>;   // LLM-generated output
  expectedOutput?: string | Record<string, any>; // Ground truth
  userFeedback?: string;                         // Human feedback
  metadata?: Record<string, any>;                // Per-item metadata
}
```

### 2. MetaTunerPromptInput (Tuning Configuration)

```typescript
interface MetaTunerPromptInput {
  prompt: string;                    // Prompt template (or ChatPromptTemplate)
  inputSchema: Record<string, any>;  // JSON Schema for input variables
  dataset: PromptDataset;            // The test dataset
  evals: PromptEvaluation[];         // Evaluation criteria
  outputSchema?: Record<string, any>; // JSON Schema for expected output
  executions?: PromptExecutions;     // Pre-existing execution results
}
```

### 3. MutationPrompt (Versioned Prompt)

```typescript
interface MutationPrompt {
  version: number;                           // Prompt version number
  prompt: string;                            // Prompt template
  inputSchema?: Record<string, any>;         // JSON Schema for inputs
  inputParameters?: Record<string, any>;     // Input parameter descriptions
  outputSchema?: Record<string, any>;        // JSON Schema for outputs
  outputParameters?: Record<string, any>;    // Output parameter descriptions
  model?: string;                            // LLM model to use
}
```

### 4. PromptEvaluation (Evaluation Criteria)

```typescript
interface PromptEvaluation {
  id: string;                    // Evaluation ID
  name: string;                  // Evaluation name
  criteria: string;              // Evaluation criteria description
  threshold: number;             // Score threshold for success (0.0-1.0)
  evaluationChecklist?: string[]; // Checklist items
  evaluationParams: string[];    // Parameters to evaluate
  model?: string;                // LLM model for evaluation
}
```

### 5. PromptExecution (Single Execution Result)

```typescript
interface PromptExecution {
  id: string;                                    // Execution ID
  prompt?: string;                               // Prompt used
  input?: Record<string, any>;                   // Input values
  output: string | Record<string, any>;          // Actual LLM output
  expectedOutput?: string | Record<string, any>; // Expected output
  systemFeedback?: string;                       // System-generated feedback
  userFeedback?: string;                         // Human feedback
  evaluation?: PromptEvaluationResult;           // Evaluation results
  metadata?: Record<string, any>;                // Additional metadata
}
```

### 6. PromptExecutions (Execution Bundle)

```typescript
interface PromptExecutions {
  id: string;                      // Bundle ID
  executions: PromptExecution[];   // Array of executions
}
```

### 7. PromptEvaluationResult (Evaluation Outcome)

```typescript
interface PromptEvaluationResult {
  id: string;                                    // Result ID
  success: boolean;                              // Overall success
  score: number;                                 // Overall score (0.0-1.0)
  llmScore?: number;                             // LLM-judged score
  successRate?: number;                          // Success rate
  evaluations: PromptEvaluationMetricResult[];   // Per-metric results
}

interface PromptEvaluationMetricResult {
  id: string;                    // Metric ID
  name: string;                  // Metric/variable name
  reasoning: string;             // Evaluation reasoning
  evaluatedChecklist: string[];  // Evaluated checklist items
  score: number;                 // Score (0.0-1.0)
  llmScore: number;              // LLM-judged score
  success: boolean;              // Pass/fail
  failureMode: string;           // Failure reason
  systemFeedback: string;        // Feedback for improvement
  error?: string;                // Error message if any
}
```

---

## Complete JSON Export Example

```json
{
  "datasetName": "1-schreiben-bank-gold",

  "metadata": {
    "agent": "TZV Agent 03.09",
    "node": "1. Schreiben Bank",
    "promptType": "extraction",
    "tier": "gold",
    "itemCount": 60,
    "averageScore": 0.875,
    "succeededCount": 51,
    "failedCount": 9,
    "generated_at": "2026-01-04T12:00:00Z",
    "source": "airtable-export"
  },

  "promptDataset": {
    "name": "1. Schreiben Bank-gold",
    "description": "Extraction dataset for bank letter processing",
    "items": [
      {
        "id": "task-uuid-1",
        "input": {
          "pdf_content": "...",
          "task": "...",
          "beamTaskId": "TZV-1234"
        },
        "expectedOutput": {
          "bIsBankersOrderStatus": "true",
          "cCaseClassification": "Schreiben Bank"
        },
        "actualOutput": {
          "bIsBankersOrderStatus": "true",
          "cCaseClassification": "Schreiben Bank"
        },
        "metadata": {
          "score": 1.0,
          "evaluation": {
            "id": "eval_task-uuid-1",
            "success": true,
            "score": 1.0,
            "successRate": 1.0,
            "evaluations": [...]
          }
        }
      }
    ],
    "tags": ["gold", "extraction", "schreiben-bank"]
  },

  "metatunerPromptInput": {
    "prompt": "# Role\nYou are a detail-oriented data extraction specialist...",

    "inputSchema": {
      "type": "object",
      "properties": {
        "pdf_content": {
          "type": "string",
          "description": "The PDF document content (markdown converted)"
        },
        "task": {
          "type": "string",
          "description": "Task metadata including clientId, case_id, subfolder"
        },
        "beamTaskId": {
          "type": "string",
          "description": "Beam task identifier"
        }
      },
      "required": ["pdf_content"]
    },

    "inputParameters": {
      "pdf_content": "Bank letter document content in markdown format",
      "task": "Task metadata JSON with case routing information",
      "beamTaskId": "Unique task identifier from Beam system"
    },

    "outputSchema": {
      "type": "object",
      "properties": {
        "bIsBankersOrderStatus": {
          "type": "string",
          "enum": ["true", "false", "null"],
          "description": "Whether standing order was confirmed"
        },
        "cCaseClassification": {
          "type": "string",
          "enum": ["Schreiben Bank", "Sonstiges"],
          "description": "Document classification"
        }
      },
      "required": ["bIsBankersOrderStatus", "cCaseClassification"]
    },

    "outputParameters": {
      "bIsBankersOrderStatus": "Boolean string indicating if bank confirmed standing order setup",
      "cCaseClassification": "Classification based on document type and subfolder"
    },

    "evals": [
      {
        "id": "eval-exact-match",
        "name": "Exact Match Evaluation",
        "criteria": "Output values must exactly match expected values",
        "threshold": 1.0,
        "evaluationParams": ["bIsBankersOrderStatus", "cCaseClassification"],
        "evaluationChecklist": [
          "bIsBankersOrderStatus matches expected",
          "cCaseClassification matches expected"
        ]
      }
    ],

    "dataset": "<<reference to promptDataset above>>"
  },

  "PromptExecutions": {
    "id": "exec-1-schreiben-bank-gold",
    "executions": [
      {
        "id": "task-uuid-1",
        "prompt": "# Role\nYou are a detail-oriented...",
        "input": {
          "pdf_content": "...",
          "task": "...",
          "beamTaskId": "TZV-1234"
        },
        "output": {
          "bIsBankersOrderStatus": "true",
          "cCaseClassification": "Schreiben Bank"
        },
        "expectedOutput": {
          "bIsBankersOrderStatus": "true",
          "cCaseClassification": "Schreiben Bank"
        },
        "evaluation": {
          "id": "eval_task-uuid-1",
          "success": true,
          "score": 1.0,
          "successRate": 1.0,
          "evaluations": [
            {
              "id": "task-uuid-1_bIsBankersOrderStatus",
              "name": "bIsBankersOrderStatus",
              "reasoning": "Compared expected 'true' with actual 'true'",
              "evaluatedChecklist": [],
              "score": 1.0,
              "llmScore": 1.0,
              "success": true,
              "failureMode": "",
              "systemFeedback": ""
            }
          ]
        }
      }
    ]
  }
}
```

---

## Key Differences from Current Export

| Field | Current Export | Full MetaTuner Format |
|-------|----------------|----------------------|
| `inputSchema` | Not included | JSON Schema for input validation |
| `outputSchema` | Not included | JSON Schema for output validation |
| `inputParameters` | Not included | Human-readable parameter descriptions |
| `outputParameters` | Not included | Human-readable output descriptions |
| `evals` | Not included | Evaluation criteria definitions |
| `executions` | Embedded in items | Separate top-level PromptExecutions |
| `metatunerPromptInput` | Not included | Complete tuning configuration |

---

## Schema Generation from Airtable

**Input Schema** can be derived from:
- Node's input structure (pdf_content, task, beamTaskId, etc.)
- Classification context fields

**Output Schema** can be derived from:
- DatasetVariables linked to the node
- Variable names and expected value patterns

**Evaluation Criteria**:
- Default: exact match for all output variables
- Can add LLM-as-judge for complex outputs

---

*This document defines the target JSON structure for full MetaTuner compatibility.*
