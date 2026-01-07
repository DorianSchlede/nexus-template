/**
 * Eval Criteria Derivation Stage Zod Schemas for LLM Feature Outputs
 *
 * These schemas define the structure for deriving G-Eval compatible evaluation criteria
 * from successful prompt executions. Each parameter (input/output) gets exactly ONE criterion.
 */

import { z } from 'zod';
import {
  PromptEvaluation,
  PromptEvaluationCriteria,
} from '../../../../../types/prompt-evaluation.js';

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// PARAMETER EXCLUSION SCHEMA
// Tracks which parameters were intentionally excluded from criteria derivation
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Excluded Parameter Schema
 * Documents why a parameter was not assigned evaluation criteria
 */
export const ExcludedParameterSchema = z.object({
  /** Parameter ID (field name from schema) */
  parameterId: z.string().describe('The field name of the excluded parameter'),

  /** Type of parameter */
  parameterType: z
    .enum(['input', 'output'])
    .describe('Whether this is an input or output parameter'),

  /** Reason for exclusion */
  exclusionReason: z
    .string()
    .describe(
      'Why this parameter was excluded (e.g., framework-handled, metadata field, system-level)'
    ),
});

export type ExcludedParameter = z.infer<typeof ExcludedParameterSchema>;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// DERIVED CRITERION SCHEMA
// Single criterion derived for a specific parameter
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Derived Criterion Schema
 * Represents a single evaluation criterion derived from successful execution patterns
 */
export const DerivedCriterionSchema = z.object({
  /** Parameter identifier matching the schema field name */
  parameterId: z
    .string()
    .describe('The field name of the parameter (e.g., "category", "urgency", "customerMessage")'),

  /** Type of parameter */
  parameterType: z
    .enum(['input', 'output'])
    .describe('Whether this is an input or output parameter'),

  /** Display name for the parameter */
  parameterName: z.string().describe('Human-readable display name for the parameter'),

  /** Current description from the schema */
  parameterDescription: z
    .string()
    .describe('The current description of this parameter from the input/output schema'),

  /**
   * TRAIN OF THOUGHT: Detailed reasoning BEFORE deriving criteria
   * This field captures the analytical process and can be observed/tuned via reinforcement learning.
   */
  reasoning: z
    .string()
    .describe(
      'Detailed train of thought reasoning BEFORE deriving the criteria. Include: (1) What patterns did you observe across successful executions for this parameter? (2) What makes values correct vs incorrect? (3) What edge cases exist? (4) How should evaluators distinguish good from bad outputs? This reasoning informs the criteria derivation and can be used for reinforcement tuning.'
    ),

  /** The derived evaluation criteria text */
  derivedCriteria: z
    .string()
    .describe(
      'The evaluation criteria text that describes what constitutes correct behavior for this parameter. Must be measurable and actionable for G-Eval scoring (0-1).'
    ),

  /** Steps to evaluate this criterion */
  evaluationSteps: z
    .array(z.string())
    .describe(
      'Ordered steps an evaluator should follow to assess this criterion. Each step should be concrete and observable.'
    ),

  /** Success patterns observed in executions */
  successPatterns: z
    .array(z.string())
    .describe('Specific patterns observed in successful executions that inform this criterion'),

  /** Evidence citations from executions */
  evidenceFromExecutions: z
    .array(z.string())
    .describe('Direct quotes or references from execution data supporting this criterion'),

  /** Confidence in the derived criterion */
  confidenceScore: z
    .number()
    .min(0)
    .max(1)
    .describe(
      'Confidence in this criterion derivation (0-1). Higher confidence indicates more consistent patterns across executions.'
    ),

  /** Rationale for the criterion */
  rationale: z
    .string()
    .describe(
      'Detailed explanation of WHY this criterion was derived and how it captures successful behavior'
    ),
});

export type DerivedCriterion = z.infer<typeof DerivedCriterionSchema>;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// COUNTER-EXAMPLE INSIGHT SCHEMA
// Insights derived from failed executions (optional)
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Counter-Example Insight Schema
 * Captures what the criterion should REJECT based on failed executions
 */
export const CounterExampleInsightSchema = z.object({
  /** Which parameter this insight relates to */
  parameterId: z.string().describe('The parameter ID this counter-example relates to'),

  /** What went wrong in the failed execution */
  failurePattern: z.string().describe('The pattern of failure observed'),

  /** How the criterion should reject this pattern */
  rejectionGuidance: z
    .string()
    .describe('How the evaluation criterion should identify and reject this failure pattern'),

  /** Evidence from failed execution */
  evidenceFromFailure: z.string().describe('Evidence citation from the failed execution'),
});

export type CounterExampleInsight = z.infer<typeof CounterExampleInsightSchema>;

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// EVAL CRITERIA DERIVATION SCHEMA (TOP-LEVEL OUTPUT)
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/**
 * Eval Criteria Derivation Schema
 * The complete output of criteria derivation from successful executions
 */
export const EvalCriteriaDerivationSchema = z.object({
  /** Pre-reasoning examining all executions */
  analysisReasoning: z
    .string()
    .describe(
      'Detailed pre-reasoning examining all provided executions. What patterns define success? What makes outputs correct for each parameter?'
    ),

  /** List of derived criteria - one per parameter */
  derivedCriteria: z
    .array(DerivedCriterionSchema)
    .describe(
      'List of derived evaluation criteria - exactly ONE criterion per input/output parameter (excluding technical parameters)'
    ),

  /** Parameters that were excluded */
  excludedParameters: z
    .array(ExcludedParameterSchema)
    .describe(
      'Parameters that were intentionally excluded from criteria derivation (e.g., outputFormat, metadata)'
    ),

  /** Optional insights from counter-examples (failed executions) */
  counterExampleInsights: z
    .array(CounterExampleInsightSchema)
    .optional()
    .describe(
      'Insights derived from failed executions about what criteria should REJECT. Only present if failed executions were provided.'
    ),

  /** Summary of the derivation */
  summary: z
    .string()
    .describe(
      'Concise summary of: (1) total criteria derived, (2) key success patterns identified, (3) confidence level in the criteria'
    ),
});

export type EvalCriteriaDerivation = z.infer<typeof EvalCriteriaDerivationSchema>;

///////////////////////////////////////////////////////////////////////////////////////////////////
// CONVERTERS: LLM Schema Types -> Native PromptTuner Types
///////////////////////////////////////////////////////////////////////////////////////////////////

/** Default threshold for derived evaluations */
const DEFAULT_THRESHOLD = 0.7;

/**
 * Configuration for creating a PromptEvaluation from derivation
 */
export interface EvalConversionConfig {
  /** Name for the evaluation */
  name?: string;
  /** Score threshold for success (default: 0.7) */
  threshold?: number;
  /** Evaluation model to use */
  model?: string;
}

/**
 * Convert EvalCriteriaDerivation (LLM output) to PromptEvaluation (native type)
 *
 * @param derivation - The LLM EvalCriteriaDerivation output
 * @param config - Optional configuration for the evaluation
 * @returns Native PromptEvaluation object ready for G-Eval
 */
export function toPromptEvaluation(
  derivation: EvalCriteriaDerivation,
  config?: EvalConversionConfig
): PromptEvaluation {
  return {
    id: crypto.randomUUID(),
    name: config?.name ?? 'DerivedEvaluation',
    description: derivation.summary,
    threshold: config?.threshold ?? DEFAULT_THRESHOLD,
    model: config?.model,
    criteria: derivation.derivedCriteria.map(toPromptEvaluationCriteria),
  };
}

/**
 * Convert a single DerivedCriterion (LLM schema) to PromptEvaluationCriteria (native type)
 *
 * @param derived - The LLM DerivedCriterion
 * @returns Native PromptEvaluationCriteria object
 */
export function toPromptEvaluationCriteria(derived: DerivedCriterion): PromptEvaluationCriteria {
  return {
    id: derived.parameterId,
    criteria: derived.derivedCriteria,
    evaluationParameter: derived.parameterName,
    evaluationSteps: derived.evaluationSteps,
  };
}

/**
 * Extract parameter IDs from a derivation for reference
 *
 * @param derivation - The LLM EvalCriteriaDerivation output
 * @returns Object with included and excluded parameter IDs
 */
export function extractParameterCoverage(derivation: EvalCriteriaDerivation): {
  includedParameters: string[];
  excludedParameters: string[];
} {
  return {
    includedParameters: derivation.derivedCriteria.map((c) => c.parameterId),
    excludedParameters: derivation.excludedParameters.map((p) => p.parameterId),
  };
}
