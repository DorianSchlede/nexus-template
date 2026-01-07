/**
 * Feedback Analysis Stage Zod Schemas for LLM Feature Outputs
 */

import { z } from 'zod';

/**
 * Execution status for distinguishing successful vs failed execution analysis
 */

export enum ExecutionStatus {
  SUCCESSFUL = 'successful',
  FAILED = 'failed',
}

/**
 * Prompt Section Schema
 */
export const PromptSectionSchema = z.object({
  /** Type of the prompt section (System or Human). */
  type: z.enum(['system', 'human']).describe('System or Human prompt Type.'),
  /** Prompt Section where the Problem Appears */
  section: z
    .string()
    .describe(
      'XML tag name or Markdown heading identifying the section (e.g., "## Task Context" or "<query>"'
    ),
  /** Current Text of the prompt section. */
  currentText: z.string().describe('Current text of the prompt section.'),
  rationale: z
    .string()
    .describe(
      'Rationale for selecting the particular section and text as the problem area based on the Root Cause analysis.'
    ),
  /** Evidence for the proposed text. */
  supportingEvidence: z
    .array(z.string())
    .describe(
      'References and citations from the Execution and evaluation data supporting the rationale for selecting the particular section and text as the problem area based on the Root Cause analysis.'
    ),
  /** Proposed Text of the prompt section. */
  // proposedText: z
  //   .string()
  //   .describe(
  //     'Recommended improved text of the prompt section. Must enforce the user feedback or the expected output.'
  //   ),
  /** Justification for the proposed text. */
  // justification: z
  //   .string()
  //   .describe(
  //     'Detailed rationale explaining how this modification addresses the identified issue/s.'
  //   ),
  /** Expected Impact of the proposed text. */
  // expectedImpact: z.string().describe('Expected improvements from implementing this modification.'),
  /** Supporting References of the proposed text. */
  // supportingReferences: z
  //   .array(z.string())
  //   .describe(
  //     'References and citations from the Execution and evaluation data supporting this recommendation.'
  //   ),
});

export type PromptSection = z.infer<typeof PromptSectionSchema>;

/**
 * Missing Prompt Section Schema
 * Used when the failure mode requires adding an ENTIRELY NEW section to the prompt,
 * rather than modifying an existing section. This is for additive changes.
 */
export const MissingPromptSectionSchema = z.object({
  /** Discriminator type for missing section. */
  type: z
    .literal('missing-section')
    .describe('Indicates this is a missing section that needs to be added to the prompt.'),

  /** Target prompt type where the section should be added. */
  targetPromptType: z
    .enum(['system', 'human'])
    .describe('Which prompt (System or Human) should contain the new section.'),

  /** Proposed section name/heading for the new section. */
  proposedSectionName: z
    .string()
    .describe(
      'The XML tag name or Markdown heading for the new section (e.g., "## Edge Cases" or "<constraints>")'
    ),

  /** Where to insert the new section relative to existing sections. */
  insertionPoint: z
    .object({
      position: z
        .enum(['before', 'after', 'start', 'end'])
        .describe(
          'Where to insert: "before"/"after" a reference section, or "start"/"end" of the prompt.'
        ),
      referenceSection: z
        .string()
        .optional()
        .describe(
          'The existing section name to insert before/after. Required if position is "before" or "after".'
        ),
    })
    .describe('Specifies where in the prompt the new section should be inserted.'),

  /** Rationale for why this section is missing and needs to be added. */
  rationale: z
    .string()
    .describe(
      'Detailed explanation of WHY this section is missing and how its absence causes the failure mode. What gap does it fill?'
    ),

  /** Evidence for the proposed section. */
  supportingEvidence: z
    .array(z.string())
    .describe(
      'References and citations from the Execution and evaluation data supporting the rationale for selecting the particular section and text as the problem area based on the Root Cause analysis.'
    ),

  /** The complete proposed text for the new section. */
  // proposedText: z
  //   .string()
  //   .describe(
  //     'The complete text content for the new section. Must be self-contained and address the identified gap.'
  //   ),

  // /** Justification for the proposed section content. */
  // justification: z
  //   .string()
  //   .describe(
  //     'Detailed rationale explaining how adding this section addresses the identified failure mode.'
  //   ),

  // /** Expected impact of adding this section. */
  // expectedImpact: z
  //   .string()
  //   .describe(
  //     'Expected improvements from adding this new section. How will it prevent the failure mode?'
  //   ),

  // /** Supporting references from execution data. */
  // supportingReferences: z
  //   .array(z.string())
  //   .describe(
  //     'References and citations from execution data showing where this missing guidance caused failures.'
  //   ),
});

export type MissingPromptSection = z.infer<typeof MissingPromptSectionSchema>;

/**
 * Prompt Input/Output Variable Schema
 */
export const PromptVariableSchema = z.object({
  /** Type of the prompt variable. */
  type: z.enum(['input', 'output']).describe('Input or Output variable.'),
  /** Key Name of the prompt variable. */
  variable: z.string().describe('Key (Name) of the prompt variable.'),
  /** Current Description of the prompt variable. */
  currentDescription: z.string().describe('Current description of the prompt variable.'),
  /** Rationale for selecting the particular variable and description as the problem area based on the Root Cause analysis. */
  rationale: z
    .string()
    .describe(
      'Rationale for selecting the particular variable and description as the problem area based on the Root Cause analysis.'
    ),
  /** Evidence for the proposed variable. */
  supportingEvidence: z
    .array(z.string())
    .describe(
      'References and citations from the Execution and evaluation data supporting the rationale for selecting the particular variable and description as the problem area based on the Root Cause analysis.'
    ),
  /** Proposed Description of the prompt variable. */
  // proposedDescription: z
  //   .string()
  //   .describe(
  //     'Recommended improved description of the prompt variable. Must enforce the user feedback or the expected output.'
  //   ),
  /** Justification for the proposed description. */
  // justification: z
  //   .string()
  //   .describe(
  //     'Detailed rationale explaining how this modification addresses the identified issue/s.'
  //   ),
  /** Expected Impact of the proposed description. */
  // expectedImpact: z.string().describe('Expected improvements from implementing this modification.'),
  /** Supporting References of the proposed description. */
  // supportingReferences: z
  //   .array(z.string())
  //   .describe(
  //     'References and citations from the Execution and evaluation data supporting this recommendation.'
  //   ),
});

export type PromptVariable = z.infer<typeof PromptVariableSchema>;
