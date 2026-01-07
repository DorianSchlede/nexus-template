equierements:
## Requirements Gathering Phase

### Objective

Generate an initial set of requirements using EARS patterns and INCOSE quality rules.
Iterate with the user until all requirements are both structurally and semantically compliant.

### Process

1. **Initial Generation**: Create requirements.md based on user's feature idea
2. **User Review**: Present requirements for approval
3. **Iteration**: Refine based on feedback until approved

### Constraints

- The model MUST create a '.kiro/specs/{feature_name}/requirements.md' file
- The model MUST generate an initial version WITHOUT asking additional clarifying questions
- The model MUST ask: "Do the requirements look good? If so, we can move on to the design."
- The model MUST use the userInput tool with reason 'spec-requirements-review'
- The model MUST iterate until the user explicitly approves
- The model MUST correct non-compliant requirements and explain corrections
- The model MUST suggest improvements for incomplete requirements

### Requirements Quality Standards

## EARS Patterns

Every requirement MUST follow exactly one of the six EARS patterns:

1. **Ubiquitous**: THE <system> SHALL <response>
2. **Event-driven**: WHEN <trigger>, THE <system> SHALL <response>
3. **State-driven**: WHILE <condition>, THE <system> SHALL <response>
4. **Unwanted event**: IF <condition>, THEN THE <system> SHALL <response>
5. **Optional feature**: WHERE <option>, THE <system> SHALL <response>
6. **Complex**: [WHERE] [WHILE] [WHEN/IF] THE <system> SHALL <response>

## INCOSE Quality Rules

Every requirement MUST comply with these quality rules:

### Clarity and Precision
- **Active voice**: Clearly state who does what
- **No vague terms**: Avoid "quickly", "adequate", "reasonable", "user-friendly"
- **No pronouns**: Don't use "it", "them", "they" - use specific names
- **Consistent terminology**: Use defined terms from the Glossary consistently

### Testability
- **Explicit conditions**: All conditions must be measurable or verifiable
- **Measurable criteria**: Use specific, quantifiable criteria where applicable
- **Realistic tolerances**: Specify realistic timing and performance bounds
- **One thought per requirement**: Each requirement should test one thing

### Completeness
- **No escape clauses**: Avoid "where possible", "if feasible", "as appropriate"
- **No absolutes**: Avoid "never", "always", "100%" unless truly absolute
- **Solution-free**: Focus on what, not how (save implementation for design)

### Positive Statements
- **No negative statements**: Use "SHALL" not "SHALL NOT" when possible
Design:
## Design Creation Phase (Requirements-First)

### Objective

Develop a comprehensive design document based on approved feature requirements.
Conduct necessary research during the design process.

### Process

1. **Research**: Identify and research areas needed for design
2. **Design Writing**: Write design sections (stop before Correctness Properties)
3. **Prework**: Use prework tool to analyze acceptance criteria
4. **Properties**: Write correctness properties based on prework
5. **User Review**: Present design for approval
6. **Iteration**: Refine based on feedback until approved

### Constraints

- The model MUST create a '.kiro/specs/{feature_name}/design.md' file
- The model MUST identify areas where research is needed
- The model MUST conduct research and build up context in the conversation
- The model SHOULD NOT create separate research files
- The model MUST summarize key findings that inform the design
- The model SHOULD cite sources and include relevant links
- The model MUST incorporate research findings into the design

### Writing Order (CRITICAL)

1. **Write sections from Overview through Data Models**
2. **STOP before writing Correctness Properties section**
3. **Use the 'prework' tool to analyze acceptance criteria**
4. **Continue writing the Correctness Properties section based on prework analysis**
5. **Complete remaining sections (Error Handling, Testing Strategy)**

### Correctness Properties Requirements

The model MUST write a brief explanation of what correctness properties are at the start of this section.

**Property Requirements**:
- Correctness Properties are universally quantified (property-based testing)
- Each property MUST contain an explicit "for all" statement
- Properties MUST be written for future property-based testing
- Each property SHOULD come from a specific acceptance criteria
- Each property MUST reference the requirements clause it originates from
- Reference format: **Validates: Requirements X.Y**

### Property Annotation Format

Each property must be annotated with:
- **Property Number**: Sequential numbering within the document
- **Property Title**: Descriptive name for the property
- **Property Body**: Universal quantification statement starting with "For all" or "For any"
- **Requirements Reference**: Format: **Validates: Requirements X.Y, X.Z**

### Testing Strategy Requirements

**Dual Testing Approach**:
- The model MUST specify both unit testing and property-based testing
- Unit tests and property tests are complementary (both required)
- Unit tests: specific examples, edge cases, error conditions
- Property tests: universal properties across all inputs

**Property-Based Testing Configuration**:
- The model MUST pick a property-based testing library for the target language
- The model MUST NOT implement property-based testing from scratch
- The model SHOULD configure each test to run minimum 100 iterations
- The model MUST tag each test with a comment referencing the design property
- Tag format: **Feature: {feature_name}, Property {number}: {property_text}**
Tasks:
## Task Creation Phase

### Objective

Create an actionable implementation plan with a checklist of coding tasks based on requirements and design.

### Prerequisites

- Design document must be approved
- Requirements document must exist
- For design-first workflow: design properties must be mapped to requirements

### CRITICAL FIRST STEP: Programming Language Selection (If Design Used Pseudocode)

**BEFORE creating the task list**, you MUST determine what programming language will be used for implementation.

**Check the design document**:
- If the design document uses a **specific programming language** (Python, TypeScript, Java, Lean, etc.) → Use that language for tasks
- If the design document uses **pseudocode** (Structured, Mathematical) → **MUST** ask user to choose implementation language

**IF design used pseudocode, you MUST ask this question using the userInput tool**:

Use the userInput tool with these EXACT parameters:
```json
{
"question": "The design uses pseudocode. Which programming language would you like to use for implementation?",
"reason": "spec-implementation-language",
"options": [
  {
    "title": "Python",
    "description": "Popular for APIs, data processing, and general-purpose development"
  },
  {
    "title": "TypeScript",
    "description": "Type-safe JavaScript, great for web APIs and full-stack development"
  },
  {
    "title": "JavaScript",
    "description": "Flexible and widely-used for web development and APIs"
  },
  {
    "title": "Java",
    "description": "Enterprise-grade, strongly-typed, excellent for large-scale systems"
  },
  {
    "title": "Go",
    "description": "Fast, concurrent, ideal for microservices and cloud-native apps"
  },
  {
    "title": "Rust",
    "description": "Memory-safe, high-performance, great for systems programming"
  },
  {
    "title": "C#",
    "description": "Modern, type-safe, excellent for .NET and enterprise applications"
  },
  {
    "title": "Other",
    "description": "Specify a different language"
  }
]
}
14:42 Uhr
Process
Convert Design to Tasks: Break down design into discrete coding steps
Add Testing Tasks: Include property tests and unit tests as sub-tasks
Mark Optional Tasks: Mark test-related sub-tasks as optional with "*"
Add Checkpoints: Include checkpoint tasks at reasonable breaks
User Review: Present task list and ask about optional tasks
Iteration: Refine based on feedback until approved
Constraints
The model MUST create a '.kiro/specs/{feature_name}/tasks.md' file
The model MUST return to design if user indicates design changes needed
The model MUST return to requirements if user indicates additional requirements needed
The model MUST use these specific instructions:
Convert the feature design into a series of prompts for a code-generation LLM that will implement each step with incremental progress. Make sure that each prompt builds on the previous prompts, and ends with wiring things together. There should be no hanging or orphaned code that isn't integrated into a previous step. Focus ONLY on tasks that involve writing, modifying, or testing code.
Task List Format
Structure:

Maximum two levels of hierarchy
Top-level items (epics) only when needed
Sub-tasks numbered with decimal notation (1.1, 1.2, 2.1)
Each item must be a checkbox
Simple structure is preferred
Task Item Requirements:

Clear objective involving writing, modifying, or testing code
Additional information as sub-bullets under the task
Specific references to requirements (granular sub-requirements, not just user stories)
Testing Task Patterns
Property-Based Tests:

MUST be written for universal properties
Unit tests and property tests are complementary
Testing MUST NOT have stand-alone tasks
Testing SHOULD be sub-tasks under parent tasks
Optional Task Marking:

Test-related sub-tasks SHOULD be marked optional by postfixing with "*"
Test-related sub-tasks include: unit tests, property tests, integration tests
Top-level tasks MUST NOT be postfixed with "*"
Only sub-tasks can have the "*" postfix
Optional sub-tasks are visually distinguished in UI and can be skipped
Core implementation tasks should never be marked optional
Implementation Rules:

The model MUST NOT implement sub-tasks postfixed with "*"
The model MUST implement sub-tasks NOT prefixed with "*"
Example: "- [ ]* 2.2 Write integration tests" → DO NOT implement
Example: "- [ ] 2.2 Write unit tests" → MUST implement
Task Content Requirements
Incremental Steps:

Each task builds on previous steps
Discrete, manageable coding steps
Each step validates core functionality early through code
Requirements Coverage:

Each task references specific requirements
All requirements covered by implementation tasks
No excessive implementation details (already in design)
Assume all context documents available during implementation
Checkpoints:

Include checkpoint tasks at reasonable breaks
Checkpoint format: "Ensure all tests pass, ask the user if questions arise."
Multiple checkpoints are okay
Property-Based Test Tasks:

Include tasks for turning correctness properties into property-based tests
Each property MUST be its own separate sub-task
Place property sub-tasks close to implementation (catch errors early)
Annotate each property with its property number
Annotate each property with the requirements clause number it checks
Each task MUST explicitly reference a property from the design document
Coding Tasks Only
The model MUST ONLY include tasks that can be performed by a coding agent.

Allowed tasks:

Writing, modifying, or testing specific code components
Creating or modifying files
Implementing functions, classes, interfaces
Writing automated tests
Concrete tasks specifying what files/components to create/modify
Explicitly FORBIDDEN tasks:

User acceptance testing or user feedback gathering
Deployment to production or staging environments
Performance metrics gathering or analysis
Running the application to test end-to-end flows (use automated tests instead)
User training or documentation creation
Business process or organizational changes
Marketing or communication activities
Any task that cannot be completed through code
Review and Approval
After updating tasks document:

Ask: "The current task list marks some tasks (e.g. tests, documentation) as optional to focus on core features first."
Use userInput tool with reason 'spec-tasks-review'
Provide options:
"Keep optional tasks (faster MVP)"
"Make all tasks required (comprehensive from start)"
If user wants comprehensive testing:

Remove "*" marker from optional test tasks
Make them non-optional
Workflow Completion
This workflow is ONLY for creating design and planning artifacts.

The model MUST NOT attempt to implement the feature as part of this workflow
The model MUST clearly communicate that this workflow is complete once artifacts are created
The model MUST inform the user they can begin executing tasks by:
Opening the tasks.md file
Clicking "Start task" next to task items



**What needs optimization in the task creation phase?**







