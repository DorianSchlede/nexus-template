/**
 * Success Analysis Stage Zod Schemas for LLM Feature Outputs
 * These schemas are designed for identifying and preserving successful patterns,
 * distinct from failure-oriented schemas that focus on problems and fixes.
 */

import { z } from 'zod';
import {
  PromptSuccessMode,
  SuccessOrigin,
  SuccessPromptSection,
  SuccessPromptVariable,
  SuccessRootCause,
} from '../../../../types/prompt-success-modes.js';

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SUCCESS-ORIENTED ORIGIN SCHEMAS
// These schemas focus on PRESERVATION rather than modification
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Success Prompt Section Schema
 * Identifies a prompt section that contributes to successful outcomes and should be preserved.
 */
export const SuccessPromptSectionSchema = z.object({
  /** Type of the prompt section (System or Human). */
  type: z.enum(['system', 'human']).describe('System or Human prompt Type. Always lowercased.'),

  /** Prompt Section that contributes to success */
  section: z
    .string()
    .describe(
      'XML tag name or Markdown heading identifying the successful section (e.g., "## Task Context" or "<instructions>")'
    ),

  /** Current Text of the prompt section that is working well. */
  currentText: z
    .string()
    .describe('The exact text of the prompt section that contributes to successful execution.'),

  /** Rationale explaining why this section contributes to success. */
  successRationale: z
    .string()
    .describe(
      'Detailed explanation of WHY this section contributes to successful outcomes. What specific aspects make it effective?'
    ),

  /** Key elements within this section that must be preserved. */
  criticalElements: z
    .array(z.string())
    .describe(
      'Specific phrases, instructions, or structural elements within this section that are essential for success and must not be modified.'
    ),

  /** Risk assessment if this section is modified or removed. */
  modificationRisk: z
    .string()
    .describe(
      'Description of what could go wrong if this section is modified or removed during optimization. What failures might occur?'
    ),

  /** Evidence from executions demonstrating this section contributes to success. */
  successEvidence: z
    .array(z.string())
    .describe(
      'Specific references and citations from successful executions showing how this section led to correct outputs.'
    ),
});

export type SuccessAnalysisPromptSection = z.infer<typeof SuccessPromptSectionSchema>;

/**
 * Success Prompt Variable Schema
 * Identifies a prompt variable (input/output schema description) that contributes to successful outcomes.
 */
export const SuccessPromptVariableSchema = z.object({
  /** Type of the prompt variable. */
  type: z.enum(['input', 'output']).describe('Input or Output variable. Always lowercased.'),

  /** Key Name of the prompt variable. */
  variable: z.string().describe('Key (Name) of the prompt variable.'),

  /** Current Description of the prompt variable that is working well. */
  currentDescription: z
    .string()
    .describe('The exact description of the prompt variable that effectively guides LLM output.'),

  /** Rationale explaining why this variable description contributes to success. */
  successRationale: z
    .string()
    .describe(
      'Detailed explanation of WHY this variable description leads to correct outputs. What makes it effective?'
    ),

  /** Key aspects of the description that must be preserved. */
  criticalAspects: z
    .array(z.string())
    .describe(
      'Specific words, constraints, or formatting guidance within this description that are essential for correct output structure.'
    ),

  /** Risk assessment if this description is modified. */
  modificationRisk: z
    .string()
    .describe(
      'Description of what output quality issues might occur if this variable description is changed. What errors might appear?'
    ),

  /** Evidence from executions demonstrating this description guides correct outputs. */
  successEvidence: z
    .array(z.string())
    .describe(
      'Specific references showing how this variable description led to correctly structured outputs in successful executions.'
    ),
});

export type SuccessAnalysisPromptVariable = z.infer<typeof SuccessPromptVariableSchema>;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SUCCESS ROOT CAUSE SCHEMA
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/** Success Root Cause Schema */
export const SuccessRootCauseSchema = z.object({
  /** Detailed description of the successful execution scenario being investigated. */
  scenarioDescription: z
    .string()
    .describe(
      'Detailed description of the successful execution scenario being investigated. What inputs were provided and what correct outputs were produced?'
    ),

  /** Investigation and recursive Why analysis for understanding success. */
  investigation: z
    .string()
    .describe(
      'Detailed investigation using Recursive Why Analysis to understand the root cause of success. Ask "Why did this work?" repeatedly until reaching the fundamental reason.'
    ),

  /** The successful pattern that has been identified. */
  successPattern: z
    .string()
    .describe(
      'Clear description of the successful pattern identified. What consistent behavior or output quality was observed across multiple executions?'
    ),

  /** Evidence from multiple executions supporting this success pattern. */
  evidence: z
    .array(z.string())
    .describe(
      'Specific execution references and citations from Input/Output/Prompt illustrating this successful pattern across multiple runs.'
    ),
});

export type SuccessAnalysisRootCause = z.infer<typeof SuccessRootCauseSchema>;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SUCCESS MODE SCHEMA
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/** Success Mode Schema */
export const SuccessModeSchema = z.object({
  /** Label of the success mode. */
  label: z
    .string()
    .describe(
      'Label format: [Pattern Type] [target_element] Section. Pattern Types based on section purpose: "Effective" (role/context/task), "Clear" (criteria/definitions), "Well-Structured" (procedural/enumerated), "Explicit" (constraints/triggers). Examples: "Effective [role] Section", "Clear [categories] Section", "Well-Structured [instructions] Section", "Explicit [escalation_triggers] Section". Focus on prompt sections only.'
    ),

  /** Description of the success mode. */
  description: z
    .string()
    .describe(
      'Detailed description of what this success mode represents and how it contributes to successful prompt execution.'
    ),

  /** Root cause analysis explaining why this element leads to success. */
  rootCause: SuccessRootCauseSchema.describe(
    'Root cause analysis explaining WHY this prompt element or pattern leads to successful outcomes.'
  ),

  /** Origin of the success mode - the specific prompt element responsible. */
  origin: z
    .union([SuccessPromptSectionSchema, SuccessPromptVariableSchema])
    .describe(
      'The specific prompt section or variable that is responsible for this success pattern and should be preserved.'
    ),

  /** Impact of this success mode on output quality. */
  impact: z
    .string()
    .describe(
      'Detailed description of the positive impact this success mode has on output quality, correctness, and consistency.'
    ),

  /** Preservation priority - how critical is it to keep this element unchanged. */
  severity: z
    .enum(['low', 'medium', 'high', 'critical'])
    .describe(
      'Severity decision tree (use FIRST match): CRITICAL = constraints/boundaries preventing WRONG outputs (escalation_triggers, output_requirements, category disambiguation). HIGH = criteria/rules guiding CORRECT outputs (urgency_criteria, categorization rules, procedural instructions). MEDIUM = context improving QUALITY (role, task overview). LOW = supplementary info (examples, background).'
    ),
});

export type SuccessMode = z.infer<typeof SuccessModeSchema>;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SUCCESS ANALYSIS SCHEMA (TOP-LEVEL OUTPUT)
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Success Analysis Schema
 * The complete output of Success Analysis, identifying patterns to preserve during optimization.
 */
export const SuccessAnalysisSchema = z.object({
  /** Detailed pre-reasoning examining all successful executions. */
  analysisReasoning: z
    .string()
    .describe(
      'Detailed pre-reasoning examining all provided successful executions. What common patterns appear? What prompt elements consistently contribute to success?'
    ),

  /** List of identified success modes that should be preserved. */
  successModes: z
    .array(SuccessModeSchema)
    .describe(
      'List of identified Success Modes - the patterns and elements that contribute to successful outcomes and should be preserved during optimization.'
    ),

  /** Summary of preservation recommendations. */
  summary: z
    .string()
    .describe(
      'Concise overview summarizing: (1) the key successful patterns identified, (2) the critical elements that must be preserved, and (3) risks of modifying these elements.'
    ),
});

export type SuccessAnalysis = z.infer<typeof SuccessAnalysisSchema>;

///////////////////////////////////////////////////////////////////////////////////////////////////
// CONVERTERS: LLM Schema Types -> Native PromptTuner Types
///////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Convert a SuccessAnalysis (LLM output) to an array of PromptSuccessModes (native type)
 * @param executionId - The execution ID this analysis belongs to
 * @param successAnalysis - The LLM SuccessAnalysis output
 * @returns Array of native PromptSuccessMode objects
 */
export function toPromptSuccessModes(
  executionId: string,
  successAnalysis: SuccessAnalysis
): PromptSuccessMode[] {
  return successAnalysis.successModes.map((mode) => toPromptSuccessMode(executionId, mode));
}

/**
 * Convert a single SuccessMode (LLM schema) to PromptSuccessMode (native type)
 * @param executionId - The execution ID this success mode belongs to
 * @param successMode - The LLM SuccessMode
 * @returns Native PromptSuccessMode object
 */
export function toPromptSuccessMode(
  executionId: string,
  successMode: SuccessMode
): PromptSuccessMode {
  return {
    id: crypto.randomUUID(),
    executionId,
    label: successMode.label,
    description: successMode.description,
    successDetails: successMode.rootCause.scenarioDescription,
    impact: successMode.impact,
    severity: successMode.severity,
    rootCause: toSuccessRootCause(successMode.rootCause),
    origin: toSuccessOrigin(successMode.origin),
  };
}

/**
 * Convert LLM SuccessRootCause to framework SuccessRootCause
 */
function toSuccessRootCause(rootCause: SuccessAnalysisRootCause): SuccessRootCause {
  return {
    description: rootCause.scenarioDescription,
    investigation: rootCause.investigation,
    successPattern: rootCause.successPattern,
    evidence: rootCause.evidence,
  };
}

/**
 * Convert LLM origin (union) to framework SuccessOrigin
 * Handles SuccessAnalysisPromptSection and SuccessAnalysisPromptVariable types
 */
function toSuccessOrigin(
  origin: SuccessAnalysisPromptSection | SuccessAnalysisPromptVariable
): SuccessOrigin {
  // Check for SuccessAnalysisPromptVariable (has 'variable' field)
  if ('variable' in origin) {
    const schema = origin as SuccessAnalysisPromptVariable;
    return {
      type: schema.type,
      name: schema.variable, // Note: schema uses 'variable', framework uses 'name'
      currentDescription: schema.currentDescription,
      rationale: schema.successRationale,
      criticalAspects: schema.criticalAspects,
      modificationRisk: schema.modificationRisk,
      evidence: schema.successEvidence,
    } satisfies SuccessPromptVariable;
  }

  // Otherwise it's SuccessAnalysisPromptSection (has 'section' field)
  const schema = origin as SuccessAnalysisPromptSection;
  return {
    type: schema.type,
    section: schema.section,
    currentText: schema.currentText,
    rationale: schema.successRationale,
    criticalElements: schema.criticalElements,
    modificationRisk: schema.modificationRisk,
    evidence: schema.successEvidence,
  } satisfies SuccessPromptSection;
}
