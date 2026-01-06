# Lifecycle Finite State Machine Templates

**Synthesized from**: 11 ontology research papers
**Generated**: 2026-01-01
**Version**: 1.0

---

## Executive Summary

This document provides reusable finite state machine (FSM) templates for entity lifecycles in the UDWO metamodel. Patterns are extracted from foundational ontologies (UFO, DOLCE, BFO), process mining standards (XES, OCEL), and agentic workflow research.

---

## 1. XES Standard Lifecycle (IEEE 1849)

The most widely adopted lifecycle model for process mining.

### 1.1 State Diagram

```
                          ┌─────────────────────────────┐
                          │                             │
                          ▼                             │
┌──────────┐    ┌──────────────┐    ┌──────────────┐   │
│ schedule │───►│    assign    │───►│    start     │───┤
└──────────┘    └──────────────┘    └──────────────┘   │
                                           │           │
                          ┌────────────────┼───────────┘
                          │                │
                          ▼                ▼
                    ┌──────────┐    ┌──────────────┐
                    │  suspend │◄───│   running    │
                    └──────────┘    └──────────────┘
                          │                │
                          ▼                ▼
                    ┌──────────┐    ┌──────────────┐
                    │  resume  │───►│   complete   │
                    └──────────┘    └──────────────┘
                                           │
                          ┌────────────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │    abort     │
                    └──────────────┘
```

### 1.2 State Definitions

| State | Description | Entry Condition |
|-------|-------------|-----------------|
| `schedule` | Activity is planned but not yet assigned | Activity created |
| `assign` | Activity assigned to resource | Resource allocation |
| `start` | Activity execution has begun | Resource begins work |
| `running` | Activity is actively executing | After start |
| `suspend` | Activity temporarily paused | Interruption event |
| `resume` | Activity restarted from suspension | Continuation signal |
| `complete` | Activity successfully finished | Normal termination |
| `abort` | Activity terminated abnormally | Error/cancellation |

### 1.3 Transition Table

| From | To | Trigger | Guard |
|------|-----|---------|-------|
| schedule | assign | `assignment_event` | resource_available |
| assign | start | `start_event` | prerequisites_met |
| start | running | automatic | - |
| running | suspend | `suspend_event` | - |
| running | complete | `completion_event` | success_criteria_met |
| running | abort | `abort_event` | error_condition |
| suspend | resume | `resume_event` | - |
| resume | running | automatic | - |

### 1.4 YAML Specification

```yaml
lifecycle: xes_standard
version: "1849-2016"
source: "IEEE XES Standard"

states:
  - id: schedule
    type: initial
    description: "Activity planned"
  - id: assign
    type: intermediate
    description: "Resource assigned"
  - id: start
    type: intermediate
    description: "Execution begun"
  - id: running
    type: intermediate
    description: "Actively executing"
  - id: suspend
    type: intermediate
    description: "Temporarily paused"
  - id: resume
    type: intermediate
    description: "Restarted from pause"
  - id: complete
    type: final_success
    description: "Successfully finished"
  - id: abort
    type: final_failure
    description: "Abnormally terminated"

transitions:
  - from: schedule
    to: assign
    trigger: assignment_event
  - from: assign
    to: start
    trigger: start_event
  - from: start
    to: running
    trigger: auto
  - from: running
    to: suspend
    trigger: suspend_event
  - from: running
    to: complete
    trigger: completion_event
  - from: running
    to: abort
    trigger: abort_event
  - from: suspend
    to: resume
    trigger: resume_event
  - from: resume
    to: running
    trigger: auto
```

---

## 2. Object Lifecycle (OCEL 2.0)

General object lifecycle for process mining with dynamic attributes.

### 2.1 State Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   created   │────►│   active    │────►│  completed  │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │ ▲
      │                   │ │
      ▼                   ▼ │
┌─────────────┐     ┌─────────────┐
│   blocked   │     │  modified   │
└─────────────┘     └─────────────┘
```

### 2.2 YAML Specification

```yaml
lifecycle: ocel_object
version: "2.0"
source: "OCEL 2.0 Specification"

states:
  - id: created
    type: initial
    description: "Object initialized with epoch attributes"
    temporal_marker: "epoch (1970-01-01 00:00 UTC)"
  - id: active
    type: intermediate
    description: "Object participating in events"
  - id: modified
    type: intermediate
    description: "Attribute value changed"
  - id: blocked
    type: intermediate
    description: "Object temporarily unavailable"
  - id: completed
    type: final
    description: "No further events expected"

transitions:
  - from: created
    to: active
    trigger: first_e2o_event
    action: "oaval timestamp updated"
  - from: active
    to: modified
    trigger: attribute_change_event
    action: "oaval(o, oa, t) updated"
  - from: modified
    to: active
    trigger: auto
  - from: active
    to: blocked
    trigger: blocking_event
  - from: blocked
    to: active
    trigger: unblocking_event
  - from: active
    to: completed
    trigger: final_event

dynamic_attributes:
  tracking: "oaval: (O × OA × U_time) → U_val"
  lookup: "oaval^[t]_oa(o) returns latest value at time t"
  changed_field: "Tracks which attribute changed"
```

---

## 3. UFO Walk Lifecycle (Phase Transitions)

Example of intrinsic lifecycle phases from UFO.

### 3.1 State Diagram

```
┌─────────────────┐          ┌─────────────────┐
│  OngoingWalk    │─────────►│ FinalizedWalk   │
└─────────────────┘          └─────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
          ┌─────────────────┐              ┌─────────────────┐
          │ SuccessfulWalk  │              │ RedirectedWalk  │
          └─────────────────┘              └─────────────────┘
```

### 3.2 YAML Specification

```yaml
lifecycle: ufo_walk_phase
version: "1.0"
source: "UFO Guizzardi et al. 2021"

states:
  - id: ongoing_walk
    type: initial_phase
    description: "Walk mode is being manifested"
    phase_type: "anti-rigid sortal"
  - id: finalized_walk
    type: intermediate_phase
    description: "Walk manifestation completed"
  - id: successful_walk
    type: final_phase
    description: "Arrived at originally intended destination"
    condition: "arrivedAt(walk, originallyIntendedDestination)"
  - id: redirected_walk
    type: final_phase
    description: "Arrived at different destination"
    condition: "arrivedAt(walk, differentDestination)"

transitions:
  - from: ongoing_walk
    to: finalized_walk
    trigger: walk_completion_event
    description: "Walk perdurant manifestation completes"
  - from: finalized_walk
    to: successful_walk
    trigger: destination_reached
    guard: "destination == originallyIntendedDestination"
  - from: finalized_walk
    to: redirected_walk
    trigger: destination_reached
    guard: "destination != originallyIntendedDestination"

ontological_notes:
  - "Phases are anti-rigid sortals with intrinsic contingent conditions"
  - "Phase change represents qualitative change while maintaining identity"
  - "Each new JoggingEvent creates new JoggingProcess (monotonic accumulation)"
```

---

## 4. Activity Lifecycle (PROV-O / PROV-AGENT)

Provenance-centric activity lifecycle.

### 4.1 State Diagram

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ pending  │────►│  executing   │────►│  completed   │
└──────────┘     └──────────────┘     └──────────────┘
                        │
                        ▼
                ┌──────────────┐
                │   informed   │ (dependency state)
                └──────────────┘
```

### 4.2 YAML Specification

```yaml
lifecycle: prov_activity
version: "1.0"
source: "PROV-AGENT 2024"

states:
  - id: pending
    type: initial
    description: "Activity planned but not started"
  - id: executing
    type: intermediate
    description: "Activity using entities and generating outputs"
    prov_relations: ["used", "wasGeneratedBy"]
  - id: informed
    type: intermediate
    description: "Activity received output from prior activity"
    prov_relation: "wasInformedBy"
  - id: completed
    type: final
    description: "Activity finished, outputs generated"

transitions:
  - from: pending
    to: executing
    trigger: activity_initiation
    prov_event: "wasStartedBy"
  - from: executing
    to: informed
    trigger: dependency_event
    prov_event: "wasInformedBy(this, other)"
  - from: informed
    to: executing
    trigger: auto
  - from: executing
    to: completed
    trigger: completion_event
    prov_event: "wasEndedBy"
    action: "wasGeneratedBy entities created"

agent_participation:
  wasAssociatedWith: "Links Activity to responsible Agent"
  wasAttributedTo: "Links generated Entity to Agent"
```

---

## 5. Entity Visibility Lifecycle (Event Knowledge Graphs)

Based on df-path observation in event logs.

### 5.1 State Diagram

```
┌─────────────┐     ┌─────────────────────┐     ┌─────────────┐
│ not_visible │────►│ first_event_observed│────►│   active    │
└─────────────┘     └─────────────────────┘     └─────────────┘
                                                      │ ▲
                                                      │ │
                                                      ▼ │
┌─────────────┐                                 ┌──────────────────────┐
│  invisible  │◄────────────────────────────────│ last_event_observed  │
└─────────────┘                                 └──────────────────────┘
```

### 5.2 YAML Specification

```yaml
lifecycle: event_kg_visibility
version: "1.0"
source: "Event Knowledge Graphs (Fahland 2022)"

states:
  - id: not_visible
    type: initial
    description: "Entity may exist but no events observed"
    note: "Entity may have existed before observation window"
  - id: first_event_observed
    type: intermediate
    description: "Starting event - no incoming df for this entity"
    df_property: "no incoming df-relationship"
  - id: active
    type: intermediate
    description: "Intermediate events occurring"
    df_property: "has both incoming and outgoing df"
  - id: last_event_observed
    type: intermediate
    description: "Ending event - no outgoing df for this entity"
    df_property: "no outgoing df-relationship"
  - id: invisible
    type: final
    description: "No more events expected in observation window"
    note: "Entity may continue to exist after window"

transitions:
  - from: not_visible
    to: first_event_observed
    trigger: starting_event
    description: "First event correlated to entity"
  - from: first_event_observed
    to: active
    trigger: intermediate_event
    description: "Subsequent events with incoming/outgoing df"
  - from: active
    to: active
    trigger: intermediate_event
  - from: active
    to: last_event_observed
    trigger: ending_event
    description: "Event with no outgoing df"
  - from: last_event_observed
    to: invisible
    trigger: observation_window_close

synchronization_patterns:
  entity_creation: "Intermediate event for n, starting event for n1...nk"
  entity_completion: "Intermediate event for n, ending event for n1...nk"
  batching: "Multiple entities of same type synchronize in one event"
```

---

## 6. Agentic Workflow Lifecycle

From Agentic RAG and Multi-Agent Taxonomy.

### 6.1 State Diagram

```
                              ┌─────────────────────┐
                              │                     │
                              ▼                     │
┌────────────┐    ┌─────────────┐    ┌───────────┐ │    ┌───────────┐
│query_recv'd│───►│ evaluating  │───►│retrieving │─┼───►│synthesizng│
└────────────┘    └─────────────┘    └───────────┘ │    └───────────┘
                                                   │          │
                                     ┌─────────────┘          │
                                     │                        ▼
                               ┌──────────┐            ┌───────────┐
                               │ refining │◄───────────│ completed │
                               └──────────┘            └───────────┘
                                     │                        ▲
                                     └────────────────────────┘
```

### 6.2 YAML Specification

```yaml
lifecycle: agentic_workflow
version: "1.0"
source: "Agentic RAG Survey 2024"

states:
  - id: query_received
    type: initial
    description: "User query submitted to system"
  - id: evaluating
    type: intermediate
    description: "Coordinating agent analyzing query"
  - id: retrieving
    type: intermediate
    description: "Specialized agents fetching data"
  - id: synthesizing
    type: intermediate
    description: "LLM integrating retrieved information"
  - id: refining
    type: intermediate
    description: "Quality check failed, iterative improvement"
  - id: completed
    type: final
    description: "Response delivered to user"

transitions:
  - from: query_received
    to: evaluating
    trigger: query_analysis_start
  - from: evaluating
    to: retrieving
    trigger: source_selection_complete
  - from: retrieving
    to: synthesizing
    trigger: retrieval_complete
  - from: synthesizing
    to: refining
    trigger: quality_check_failed
  - from: synthesizing
    to: completed
    trigger: quality_check_passed
  - from: refining
    to: retrieving
    trigger: re_retrieval_needed
  - from: refining
    to: synthesizing
    trigger: refinement_complete

workflow_patterns:
  - pattern: prompt_chaining
    ordering: sequential_dependent
  - pattern: routing
    ordering: conditional_branching
  - pattern: parallelization
    ordering: concurrent
  - pattern: orchestrator_workers
    ordering: dynamic_delegation
  - pattern: evaluator_optimizer
    ordering: iterative_loop
```

---

## 7. Task-Management Activity Lifecycle

From Multi-Agent Taxonomy (Haendler 2023).

### 7.1 State Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Task-Management Activity                      │
│                                                                 │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐ │
│  │Decomposition │───►│  Orchestration   │───►│   Synthesis   │ │
│  └──────────────┘    └──────────────────┘    └───────────────┘ │
│        │                     │                      │           │
│        ▼                     ▼                      ▼           │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐ │
│  │DecomposeTask │    │  DelegateTask    │    │ EvaluateResult│ │
│  │ CreateTask   │    │  ExecuteTask     │    │ MergeResult   │ │
│  └──────────────┘    └──────────────────┘    └───────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 YAML Specification

```yaml
lifecycle: task_management_activity
version: "1.0"
source: "Multi-Agent Architecture Taxonomy (Haendler 2023)"

phases:
  - id: decomposition
    type: phase
    description: "Breaking down goal into sub-tasks"
    actions:
      - DecomposeTask
      - CreateTask
  - id: orchestration
    type: phase
    description: "Assigning and executing tasks"
    actions:
      - DelegateTask
      - ExecuteTask
  - id: synthesis
    type: phase
    description: "Combining results"
    actions:
      - EvaluateResult
      - MergeResult

action_definitions:
  - id: DecomposeTask
    description: "Breaking down task into sub-tasks, optionally ordering and prioritizing"
  - id: CreateTask
    description: "Defining and generating new tasks"
  - id: DelegateTask
    description: "Delegating task to another agent (Receiver)"
  - id: ExecuteTask
    description: "Actually executing a given task"
  - id: EvaluateResult
    description: "Assessing outcomes of a task"
  - id: MergeResult
    description: "Integrating or combining task results"

transitions:
  - from: goal_received
    to: decomposition
    trigger: start_event
  - from: decomposition
    to: orchestration
    trigger: tasks_created
  - from: orchestration
    to: synthesis
    trigger: tasks_executed
  - from: synthesis
    to: completed
    trigger: total_result_delivered

activity_log: "Tracks all actions performed"
activity_memory: "Stores context and learnings"
```

---

## 8. Graph of Thoughts Lifecycle

Thought transformation lifecycle from GoT.

### 8.1 State Diagram

```
┌──────────────┐
│  generated   │
└──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│   scored     │───►│  selected    │
└──────────────┘    └──────────────┘
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  aggregated  │   │   refined    │   │    split     │
└──────────────┘   └──────────────┘   └──────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │    final     │
                   └──────────────┘
```

### 8.2 YAML Specification

```yaml
lifecycle: graph_of_thoughts
version: "1.0"
source: "Graph of Thoughts (Besta et al. 2023)"

states:
  - id: generated
    type: initial
    description: "Thought created as graph vertex"
    properties: ["content", "connections"]
  - id: scored
    type: intermediate
    description: "Thought evaluated for correctness"
    properties: ["score", "validity"]
  - id: selected
    type: intermediate
    description: "Thought selected via KeepBestN"
  - id: aggregated
    type: intermediate
    description: "Combined with other thoughts"
    transformation: "Aggregation"
  - id: refined
    type: intermediate
    description: "Content modified via self-loop"
    transformation: "Refining"
  - id: split
    type: intermediate
    description: "Decomposed into sub-thoughts"
    transformation: "Split"
  - id: final
    type: final
    description: "Final solution thought"

transformations:
  - id: Generation
    input: "existing thought"
    output: "one or more new thoughts"
    graph_change: "V+, E+"
  - id: Aggregation
    input: "multiple thoughts"
    output: "synergistic outcome"
    graph_change: "V+ with multiple incoming edges"
  - id: Refining
    input: "thought"
    output: "modified thought (same vertex)"
    graph_change: "self-loop (v, v)"
  - id: Split
    input: "complex thought"
    output: "parallelizable sub-thoughts"
    graph_change: "V+ with branching edges"

transitions:
  - from: generated
    to: scored
    trigger: Score_operation
  - from: scored
    to: selected
    trigger: KeepBestN_operation
  - from: selected
    to: aggregated
    trigger: Aggregation_transformation
  - from: selected
    to: refined
    trigger: Refining_transformation
  - from: selected
    to: split
    trigger: Split_transformation
  - from: refined
    to: final
    trigger: convergence_criterion
  - from: aggregated
    to: final
    trigger: convergence_criterion
```

---

## 9. Generic Entity Lifecycle Template

A composable template for custom entity lifecycles.

```yaml
lifecycle: generic_entity
version: "1.0"

# Define your states
states:
  - id: initial
    type: initial
    description: "Entity created"
  - id: active
    type: intermediate
    description: "Entity participating in events"
  - id: modified
    type: intermediate
    description: "Entity state changed"
  - id: suspended
    type: intermediate
    description: "Entity temporarily inactive"
  - id: completed
    type: final_success
    description: "Entity lifecycle ended normally"
  - id: terminated
    type: final_failure
    description: "Entity lifecycle ended abnormally"

# Define transitions
transitions:
  - from: initial
    to: active
    trigger: activation_event
  - from: active
    to: modified
    trigger: state_change_event
  - from: modified
    to: active
    trigger: auto
  - from: active
    to: suspended
    trigger: suspension_event
  - from: suspended
    to: active
    trigger: resumption_event
  - from: active
    to: completed
    trigger: completion_event
  - from: active
    to: terminated
    trigger: termination_event

# Extension points
hooks:
  on_enter_state: "callback when entering state"
  on_exit_state: "callback when leaving state"
  on_transition: "callback during transition"

guards:
  check_preconditions: "validate before transition"
  check_invariants: "validate after transition"
```

---

## 10. Usage Guidelines

### 10.1 Selecting a Lifecycle Template

| Use Case | Recommended Template |
|----------|---------------------|
| Process mining with XES logs | XES Standard Lifecycle |
| Object-centric process mining | Object Lifecycle (OCEL) |
| Provenance tracking | Activity Lifecycle (PROV) |
| Agent workflow orchestration | Agentic Workflow or Task-Management |
| Event log analysis | Entity Visibility Lifecycle |
| LLM reasoning flows | Graph of Thoughts |
| Custom entity tracking | Generic Entity Template |

### 10.2 Composition Patterns

Templates can be composed:

1. **Hierarchical**: Parent activity lifecycle contains child task lifecycles
2. **Parallel**: Multiple entity lifecycles synchronized at shared events
3. **Sequential**: One lifecycle ends, triggers another to begin

### 10.3 Validation Rules

All lifecycles should satisfy:

- Every state is reachable from initial
- At least one final state exists
- No orphan transitions (all from/to states exist)
- Deterministic: max one auto-transition from any state

---

*Generated by Claude Opus 4.5 from temporal pattern extraction of 11 ontology research papers*
