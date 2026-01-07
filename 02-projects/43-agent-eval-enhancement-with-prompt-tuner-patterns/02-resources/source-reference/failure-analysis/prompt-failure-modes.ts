export interface PromptFailureModes {
  // All Categories of Failures
  categories: string[];
  // Failures by Category
  failures: Record<string, PromptFailureMode[]>;
}

export interface PromptFailureMode {
  // Failure Mode ID
  id: string;
  // Linked Execution ID
  executionId: string;
  // Mode Label
  label: string | 'global';
  // Description of The Failure Mode in Human-Readable Format
  description: string;

  // Error Category (TBD: Should be a enum)
  errorCategory?: string;

  // Failure Details -> (What)
  failureDetails: string;

  // Root Cause ( Why / How)
  rootCause: RootCause;

  // Origin (Where) & Suggested Fix
  origin: FailureOrigin;

  // Impact (How this failure mode impacts the output quality)
  impact: string;

  // Severity
  severity: 'low' | 'medium' | 'high' | 'critical';

  // Addressed/Fixed in the Mutation
  isFixed?: boolean;
}

export interface RootCause {
  // Description of the Root Cause being unveiled
  description: string;
  // Root Cause Analysis via Recursive Why
  investigation: string;
  // Issue Origin
  issueOrigin: 'prompt' | 'output-schema' | 'input-schema';
  // Evidence
  evidence: string[];
  // Category
  category:
    | 'INSTRUCTION_AMBIGUITY'
    | 'MISSING_CONTEXT'
    | 'OUTPUT_FORMAT_MISMATCH'
    | 'CONSTRAINT_VIOLATION'
    | 'REASONING_GAP'
    | 'EDGE_CASE_UNHANDLED'
    | 'VARIABLE_MISUSE'
    | 'SCHEMA_DESCRIPTION_WEAK'
    | 'MISSING_SECTION';
}

export interface PromptSection {
  // Area of the Section
  type: 'system' | 'human';
  // Section Name or Tag
  section: string;
  // Current Text of the Section
  currentText: string;
  // Rationale for Selecting the Section and Text as the Problem Area
  rationale: string;
  // Evidence for the Proposed Section
  evidence: string[];
  // Suggested Text of the Section
  // suggestedText: string;
  // Justification for the Suggested Text
  // justification: string;
  // Expected Impact of the Suggested Text
  // expectedImpact: string;
  // Supporting References for the Suggestion
  // supportingReferences: string[];
}

export interface MissingPromptSection {
  // Type of the Missing Section
  type: 'missing-section';
  // Target Prompt Type where the Section is Missing
  targetPromptType: 'system' | 'human';
  // Rationale for Selecting the Section and Text as the Problem Area
  rationale: string;
  // Evidence for the Proposed Section
  evidence: string[];
}

export interface PromptVariable {
  // Type of the Variable (Input or Output)
  type: 'input' | 'output';
  // Key Name of the Variable
  name: string;
  // Current Description of the Variable
  currentDescription: string;
  // Rationale for Selecting the Variable and Description as the Problem Area
  rationale: string;
  // Evidence for the Proposed Description
  evidence: string[];
  // Suggested Description of the Variable
  // suggestedDescription: string;
  // Justification for the Suggested Description
  // justification: string;
  // Expected Impact of the Suggested Description
  // expectedImpact: string;
  // Supporting References for the Suggestion
  // supportingReferences: string[];
}

export type FailureOrigin = PromptSection | PromptVariable | MissingPromptSection;
