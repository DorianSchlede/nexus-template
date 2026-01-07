/**
 * Eval Criteria Derivation Prompts for Prompt Tuner Stage
 *
 * Analyzes SUCCESSFUL execution data to derive G-Eval compatible evaluation criteria.
 * Each input/output parameter receives exactly ONE criterion.
 *
 * Optionally includes failed executions as counter-examples to inform rejection criteria.
 *
 * SOURCE: mutagent-monorepo/mutagent/src/framework/metatuner/pipelines/prompt-tuner/stages/eval-mutation/llm/eval-criteria-derivation/eval-criteria-prompt.ts
 */

////////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * System prompt for eval criteria derivation
 * Defines the role, methodology, and constraints for deriving evaluation criteria
 */
const EVAL_CRITERIA_DERIVATION_SYSTEM_PROMPT = `<role>
You are an Evaluation Criteria Designer with expertise in:
- G-Eval methodology for LLM output evaluation
- Pattern recognition across successful executions
- Deriving measurable, actionable evaluation criteria
- Structured output assessment and scoring

Your mission is to analyze SUCCESSFUL prompt executions and derive evaluation criteria that
capture what makes outputs correct. These criteria will be used for automated G-Eval scoring (0-1).
</role>

<task>
<description>
Analyze the provided prompt, its input/output schemas, and a collection of SUCCESSFUL execution data
to derive G-Eval compatible evaluation criteria. For each parameter (input variable or output field),
derive exactly ONE criterion that captures the success pattern.

The derived criteria must be:
- **Measurable**: Can be scored on a 0-1 scale by an LLM evaluator
- **Actionable**: Contains clear evaluation steps
- **Evidence-based**: Derived from observed patterns in successful executions
- **Parameter-specific**: One criterion per input/output parameter

If failed executions are provided as counter-examples, use them to inform what the criteria should REJECT.
</description>

<taskContext>
<schemaContext>
The prompt has an Input Schema and Output Schema defining the structure:
- **Input Schema**: Defines input parameters the prompt receives (e.g., customerMessage, context)
- **Output Schema**: Defines output fields the LLM must produce (e.g., category, urgency, sentiment)

Each parameter in these schemas should have exactly ONE derived evaluation criterion,
EXCEPT for technical/framework-handled parameters that should be excluded.
</schemaContext>

<parameterExclusionRules>
## Parameters to EXCLUDE from Criteria Derivation

Automatically exclude these technical parameters:
- **outputFormat**: Framework-handled, not a semantic criterion
- **metadata**: System metadata fields
- **id**, **timestamp**, **version**: Technical identifiers
- **raw**, **debug**, **internal**: Internal processing fields

Only derive criteria for SEMANTIC parameters that reflect the actual task quality.
</parameterExclusionRules>

<criteriaRequirements>
## Evaluation Criteria Requirements

Each derived criterion MUST have:

1. **Reasoning (TRAIN OF THOUGHT)**: Before writing criteria, document your analytical process
   - What patterns did you observe across successful executions?
   - What makes values correct vs incorrect for this parameter?
   - What edge cases exist?
   - How should evaluators distinguish good from bad outputs?
   - This reasoning is CRITICAL - it can be observed and tuned via reinforcement learning

2. **Clear Criteria Text**: A single, focused statement of what constitutes correct behavior
   - Example: "The category field correctly identifies the PRIMARY customer issue type"
   - NOT vague: "The category is appropriate"

3. **Evaluation Steps**: 3-5 ordered steps an evaluator should follow
   - Step 1: Examine the input to understand what was provided
   - Step 2: Identify the key signals/indicators relevant to this parameter
   - Step 3: Check if the output correctly reflects those signals
   - Step 4: Assess alignment with expected behavior from schema description
   - Step 5: Score based on correctness and completeness

4. **Measurability**: Must be scorable on 0-1 scale
   - 1.0 = Completely correct, matches success patterns
   - 0.7+ = Acceptable, minor deviations
   - 0.5 = Partially correct, significant gaps
   - 0.0 = Completely incorrect or missing

5. **Evidence Grounding**: Cite specific patterns from successful executions
</criteriaRequirements>

<counterExampleUsage critical="true">
## Using Failed Executions as Counter-Examples

If failed executions are provided:
1. Identify what went WRONG for each parameter
2. Use failures to define what criteria should REJECT
3. Add rejection guidance to relevant criteria
4. Document counter-example insights

This creates criteria that both ACCEPT correct outputs AND REJECT incorrect ones.
</counterExampleUsage>
</taskContext>

<instructions>
## Criteria Derivation Methodology

### Phase 1: Schema Analysis
1. Parse the input schema - identify all input parameters
2. Parse the output schema - identify all output parameters
3. Mark technical parameters for exclusion
4. Create a parameter list for criteria derivation

### Phase 2: Success Pattern Extraction
For each parameter:
1. Examine how successful executions handle this parameter
2. Identify consistent patterns across multiple successes
3. Note what makes the output CORRECT for this parameter
4. Extract evidence citations

### Phase 3: Criteria Formulation
For each parameter:
1. **FIRST: Write detailed reasoning** (train of thought) about the parameter
   - Document what patterns you observed
   - Explain what makes outputs correct vs incorrect
   - Identify edge cases and ambiguities
2. THEN: Write clear, measurable criteria text based on reasoning
3. Define 3-5 evaluation steps
4. Set confidence based on pattern consistency
5. Document additional rationale if needed

### Phase 4: Counter-Example Integration (if provided)
If failed executions exist:
1. Identify which parameters had failures
2. Document what went wrong
3. Add rejection patterns to criteria
4. Create counter-example insights

### Phase 5: Validation
1. Ensure ONE criterion per semantic parameter
2. Verify all criteria are measurable (0-1 scorable)
3. Check evaluation steps are concrete
4. Confirm evidence grounding
</instructions>
</task>

{outputFormat}
`;

/**
 * Human prompt for eval criteria derivation
 * Provides the prompt, schemas, and executions for analysis
 */
const EVAL_CRITERIA_DERIVATION_HUMAN_PROMPT = `# Evaluation Criteria Derivation Task

Derive G-Eval compatible evaluation criteria from the successful executions below.
Each input/output parameter should have exactly ONE criterion.

## Prompt Being Analyzed

\`\`\`
{prompt}
\`\`\`

## Input Schema

\`\`\`json
{inputSchema}
\`\`\`

## Output Schema

\`\`\`json
{outputSchema}
\`\`\`

## Successful Executions (PRIMARY - derive criteria from these)

These executions produced CORRECT outputs. Analyze them to understand what success looks like.

\`\`\`
{successfulExecutions}
\`\`\`
{failedExecutionsSection}

## Derivation Requirements

1. **One Criterion Per Parameter**: Derive exactly ONE criterion for each input/output parameter
2. **Exclude Technical Parameters**: Skip outputFormat, metadata, id, timestamp, version, raw, debug, internal
3. **Measurable Criteria**: All criteria must be scorable on 0-1 scale for G-Eval
4. **Evidence-Based**: Cite specific patterns from the successful executions
5. **Evaluation Steps**: Include 3-5 concrete steps for each criterion

For each criterion, provide:
- Clear criteria text describing correct behavior
- Ordered evaluation steps
- Success patterns observed
- Evidence citations from executions
- Confidence score (0-1)
- Rationale for the criterion`;

/**
 * Optional section for failed executions as counter-examples
 */
const FAILED_EXECUTIONS_SECTION = `

## Failed Executions (COUNTER-EXAMPLES - use to define rejection criteria)

These executions produced INCORRECT outputs. Use them to understand what criteria should REJECT.

\`\`\`
{failedExecutions}
\`\`\`

**Important**: Use these failures to add rejection guidance to your criteria. What patterns should the criteria explicitly REJECT?`;

/**
 * Placeholder when no failed executions are provided
 */
const NO_FAILED_EXECUTIONS_SECTION = '';
