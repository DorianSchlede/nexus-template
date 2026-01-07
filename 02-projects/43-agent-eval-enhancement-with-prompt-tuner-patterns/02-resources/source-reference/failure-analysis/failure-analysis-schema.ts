/**
 * Failure Analysis Stage Zod Schemas for LLM Feature Outputs
 */

import { z } from 'zod';
import {
  PromptSectionSchema,
  PromptVariableSchema,
  MissingPromptSectionSchema,
  PromptSection as SchemaPromptSection,
  PromptVariable as SchemaPromptVariable,
  MissingPromptSection as SchemaMissingPromptSection,
} from '../shared/shared-analysis-schemas.js';
import {
  PromptFailureMode,
  PromptSection,
  PromptVariable,
  MissingPromptSection,
  FailureOrigin,
} from '../../../../types/prompt-failure-modes.js';

/**
 * Identified root cause of prompt or response schema issues.
 */
export const RootCauseSchema = z.object({
  issueDescription: z
    .string()
    .describe('Detailed description of the Execution Problem which is being investigated.'),
  investigation: z
    .string()
    .describe(
      'Detailed investigation, train of thought and Recursive Why Analysis of the issue for Root Cause analysis.'
    ),
  category: z
    .enum([
      'INSTRUCTION_AMBIGUITY', // Unclear or conflicting instructions
      'MISSING_CONTEXT', // Required context not provided
      'MISSING_SECTION', // Entire prompt section is missing and needs to be added
      'OUTPUT_FORMAT_MISMATCH', // Output doesn't match schema expectations
      'CONSTRAINT_VIOLATION', // Guardrails/constraints not followed
      'REASONING_GAP', // Missing reasoning steps or failed reasoning chains
      'EDGE_CASE_UNHANDLED', // Scenario not covered by prompt instructions
      'VARIABLE_MISUSE', // Input variable used incorrectly
      'SCHEMA_DESCRIPTION_WEAK', // Input/Output schema description insufficient
    ])
    .describe('Classification category of the root cause'),
  issueOrigin: z
    .enum(['prompt', 'output-schema', 'input-schema'])
    .describe('Specifies whether the issue impacts the Prompt, Output Schema, or Input Schema.'),
  evidence: z
    .array(z.string())
    .describe(
      'Specific execution references and citations from Input/Output/Prompt illustrating this issue.'
    ),
  description: z.string().describe('Precise explanation of the root cause.'),
});

export type RootCause = z.infer<typeof RootCauseSchema>;

/**
 * Identified failure mode of prompt or response schema issues.
 */
export const FailureModeSchema = z.object({
  /** Label of the failure mode. */
  label: z.string().describe('Name of the failure mode.'),
  // Category of the failure mode. -> TBD
  // category: z.string().nullish().describe('Category of the failure mode.'),
  /** Description of the failure mode. */
  description: z.string().describe('Description of the failure mode.'),
  /** Root cause of the failure mode. */
  rootCause: RootCauseSchema.describe('Root cause of the failure mode.'),
  // Failure Origin: Prompt Section (modify), Missing Section (add), or Variable (modify description)
  origin: z
    .discriminatedUnion('type', [
      PromptSectionSchema,
      PromptVariableSchema,
      MissingPromptSectionSchema,
    ])
    .describe(
      'Specific part of the prompt or response schema targeted. Use PromptSection for modifying existing sections, MissingPromptSection for adding entirely new sections, or PromptVariable for modifying schema descriptions.'
    ),
  /** Impact of the failure mode on output quality. */
  impact: z
    .string()
    .describe('Exact description of the impact of the failure mode on output quality.'),

  /** Severity of the failure mode's impact on output quality. */
  severity: z.enum(['low', 'medium', 'high', 'critical']).describe('Severity of the failure mode.'),
});

export type FailureMode = z.infer<typeof FailureModeSchema>;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/** Feedback Analysis v2 */
export const FailureAnalysisSchema = z.object({
  /** Detailed pre-reasoning for comprehensive Failure Mode and Root Cause analysis. */
  analysisReasoning: z
    .string()
    .describe('Detailed pre-reasoning for comprehensive Failure Mode and Root Cause analysis.'),
  /** Detailed failure modes of issues, including evidence and impact assessment. */
  failureModes: z
    .array(FailureModeSchema)
    .describe('Detailed failure modes of issues, including evidence and impact assessment.'),
  /** Summary of the failure analysis. */
  summary: z
    .string()
    .describe('Concise overview highlighting key issues and priority recommendations.'),
});

export type FailureAnalysis = z.infer<typeof FailureAnalysisSchema>;

///////////////////////////////////////////////////////////////////////////////////////////////////
// CONVERTERS: LLM Schema Types -> Native PromptTuner Types
///////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Convert a FailureAnalysis (LLM output) to an array of PromptFailureModes (native type)
 * @param executionId - The execution ID this analysis belongs to
 * @param failureAnalysis - The LLM FailureAnalysis output
 * @returns Array of native PromptFailureMode objects
 */
export function toPromptFailureModes(
  executionId: string,
  failureAnalysis: FailureAnalysis
): PromptFailureMode[] {
  return failureAnalysis.failureModes.map((mode) => toPromptFailureMode(executionId, mode));
}

/**
 * Convert a single FailureMode (LLM schema) to PromptFailureMode (native type)
 * @param executionId - The execution ID this failure mode belongs to
 * @param failureMode - The LLM FailureMode
 * @returns Native PromptFailureMode object
 */
export function toPromptFailureMode(
  executionId: string,
  failureMode: FailureMode
): PromptFailureMode {
  return {
    id: crypto.randomUUID(),
    executionId,
    label: failureMode.label,
    description: failureMode.description,
    failureDetails: failureMode.rootCause.issueDescription,
    impact: failureMode.impact,
    severity: failureMode.severity,
    rootCause: {
      description: failureMode.rootCause.description,
      investigation: failureMode.rootCause.investigation,
      issueOrigin: failureMode.rootCause.issueOrigin,
      evidence: failureMode.rootCause.evidence,
      category: failureMode.rootCause.category,
    },
    origin: toFailureOrigin(failureMode.origin),
  };
}

/**
 * Convert LLM origin (discriminated union) to native FailureOrigin
 * Handles PromptSection, PromptVariable, and MissingPromptSection types
 */
function toFailureOrigin(
  origin: SchemaPromptSection | SchemaPromptVariable | SchemaMissingPromptSection
): FailureOrigin {
  // Check for MissingPromptSection (type: 'missing-section')
  if (origin.type === 'missing-section') {
    const schema = origin as SchemaMissingPromptSection;
    return {
      type: 'missing-section',
      targetPromptType: schema.targetPromptType,
      rationale: schema.rationale,
      evidence: schema.supportingEvidence,
    } satisfies MissingPromptSection;
  }

  // Check for PromptVariable (has 'variable' field)
  if ('variable' in origin) {
    const schema = origin as SchemaPromptVariable;
    return {
      type: schema.type,
      name: schema.variable, // Note: schema uses 'variable', native uses 'name'
      currentDescription: schema.currentDescription,
      rationale: schema.rationale,
      evidence: schema.supportingEvidence,
    } satisfies PromptVariable;
  }

  // Otherwise it's PromptSection (has 'section' field)
  const schema = origin as SchemaPromptSection;
  return {
    type: schema.type,
    section: schema.section,
    currentText: schema.currentText,
    rationale: schema.rationale,
    evidence: schema.supportingEvidence,
  } satisfies PromptSection;
}
