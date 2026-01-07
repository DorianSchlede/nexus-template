export interface PromptSuccessModes {
  // All Categories of Successes
  categories: string[];
  // Successes by Category
  successes: Record<string, PromptSuccessMode[]>;
}

export interface PromptSuccessMode {
  // Success Mode ID
  id: string;
  // Linked Execution ID
  executionId: string;
  // Mode Label
  label: string | 'global';
  // Description of The Success Mode in Human-Readable Format
  description: string;

  // Success Details -> (What)
  successDetails: string;

  // Root Cause ( Why / How)
  rootCause: SuccessRootCause;

  // Origin (Where) & Suggested Fix
  origin: SuccessOrigin;

  // Impact (How this success mode impacts the output quality)
  impact: string;

  // Severity
  severity: 'low' | 'medium' | 'high' | 'critical';

  // Addressed/Fixed in the Mutation
  isPreserved?: boolean;
}

export interface SuccessRootCause {
  // Description of the Root Cause being unveiled
  description: string;
  // Root Cause Analysis via Recursive Why
  investigation: string;
  // Issue Origin
  successPattern: string;
  // Evidence
  evidence: string[];
}

export interface SuccessPromptSection {
  // Area of the Section
  type: 'system' | 'human';
  // Section Name or Tag
  section: string;
  // Current Text of the Section
  currentText: string;
  // Rationale explaining why this section contributes to success
  rationale: string;
  // Critical elements within this section that must be preserved
  criticalElements: string[];
  // Risk assessment if this section is modified or removed
  modificationRisk: string;
  // Evidence from executions demonstrating success
  evidence: string[];
}

export interface SuccessPromptVariable {
  // Type of the Variable (Input or Output)
  type: 'input' | 'output';
  // Key Name of the Variable
  name: string;
  // Current Description of the Variable
  currentDescription: string;
  // Rationale explaining why this variable description contributes to success
  rationale: string;
  // Critical aspects of the description that must be preserved
  criticalAspects: string[];
  // Risk assessment if this description is modified
  modificationRisk: string;
  // Evidence from executions demonstrating success
  evidence: string[];
}

export type SuccessOrigin = SuccessPromptSection | SuccessPromptVariable;
