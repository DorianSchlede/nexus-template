# tdd-guard Findings

**Repository**: tdd-guard
**Purpose**: Automated Test-Driven Development enforcement for Claude Code
**Date Analyzed**: 2025-12-31

## Key Patterns

### 1. Hook Event Pipeline Pattern
TDD Guard implements a clean event-driven pipeline where hook events flow through discrete processing stages:
- **SessionStart** -> Initialize session, clear transient data
- **UserPromptSubmit** -> Process user commands (enable/disable guard)
- **PreToolUse** -> Validate before tool execution, check lint notifications
- **PostToolUse** -> Run linting after file modifications

### 2. Schema-First Validation with Zod
All data structures use Zod schemas for runtime validation with TypeScript type inference:
```typescript
import { z } from 'zod'

export const HookDataSchema = HookContextSchema.extend({
  tool_name: z.string(),
  tool_input: z.unknown(),
})

export type HookData = z.infer<typeof HookDataSchema>
```

### 3. Storage Abstraction Pattern
Clean interface-based storage abstraction allowing multiple implementations:
```typescript
export interface Storage {
  saveTest(content: string): Promise<void>
  saveTodo(content: string): Promise<void>
  saveModifications(content: string): Promise<void>
  saveLint(content: string): Promise<void>
  saveConfig(content: string): Promise<void>
  saveInstructions(content: string): Promise<void>
  getTest(): Promise<string | null>
  getTodo(): Promise<string | null>
  getModifications(): Promise<string | null>
  getLint(): Promise<string | null>
  getConfig(): Promise<string | null>
  getInstructions(): Promise<string | null>
  clearTransientData(): Promise<void>
}
```

### 4. Dependency Injection Throughout
Components receive dependencies via constructor injection, enabling testability:
```typescript
constructor(
  private readonly storage: Storage,
  private readonly linter?: Linter | null
) {}
```

---

## TDD Enforcement Logic

### Core Validation Flow
1. **Parse hook data** using Zod schema validation
2. **Check ignore patterns** (skip validation for .md, .json, etc.)
3. **Process session events** (clear transient data on new session)
4. **Handle user commands** (enable/disable guard via "tdd-guard on/off")
5. **Run linting** on PostToolUse for modified files
6. **Validate TDD compliance** via AI model analysis

### Guard Enable/Disable
```typescript
export class GuardManager {
  static readonly DEFAULT_IGNORE_PATTERNS = [
    '*.md', '*.txt', '*.log', '*.json', '*.yml',
    '*.yaml', '*.xml', '*.html', '*.css', '*.rst',
  ]

  async isEnabled(): Promise<boolean> {
    const config = await this.getConfig()
    return config?.guardEnabled ?? true  // Enabled by default
  }

  async shouldIgnoreFile(filePath: string): Promise<boolean> {
    const patterns = await this.getIgnorePatterns()
    return patterns.some((pattern) =>
      minimatch(filePath, pattern, this.minimatchOptions)
    )
  }
}
```

### TDD Rules (AI Prompt)
The AI validator enforces these rules:
1. **Red Phase**: Only ONE failing test at a time
2. **Green Phase**: MINIMAL code to pass the test
3. **Refactor Phase**: Only when tests are green

Violations blocked:
- Multiple test additions at once
- Over-implementation (code beyond current test)
- Premature implementation (code without failing test)

---

## Multi-Framework Test Reporter Architecture

### Unified Data Format
All reporters output to the same JSON structure:
```typescript
interface CapturedTestRun {
  testModules: CapturedModule[]
  unhandledErrors?: CapturedUnhandledError[]
  reason?: 'passed' | 'failed' | 'interrupted'
}

interface CapturedModule {
  moduleId: string
  tests: CapturedTest[]
}

interface CapturedTest {
  name: string
  fullName: string
  state: 'passed' | 'failed' | 'skipped'
  errors?: CapturedError[]
}
```

### Jest Reporter (TypeScript/npm)
```typescript
export class JestReporter extends BaseReporter {
  private readonly storage: Storage
  private readonly testModules: Map<string, { test: Test; testResult: TestResult }> = new Map()

  override onTestResult(test: Test, testResult: TestResult): void {
    this.testModules.set(test.path, { test, testResult })
  }

  override async onRunComplete(_contexts: Set<TestContext>, results: AggregatedResult): Promise<void> {
    const output: CapturedTestRun = {
      testModules: this.buildTestModules(),
      unhandledErrors: this.buildUnhandledErrors(results),
      reason: this.determineTestRunReason(results),
    }
    await this.storage.saveTest(JSON.stringify(output, null, 2))
  }
}
```

### Vitest Reporter (TypeScript/npm)
```typescript
export class VitestReporter implements Reporter {
  private readonly storage: Storage
  private readonly collectedData: ModuleDataMap = new Map()

  onTestModuleCollected(testModule: TestModule): void {
    this.collectedData.set(testModule.moduleId, { module: testModule, tests: [] })
  }

  onTestCaseResult(testCase: TestCase): void {
    const moduleId = testCase.module.moduleId
    if (!moduleId) return
    this.collectedData.get(moduleId)?.tests.push(testCase)
  }

  async onTestRunEnd(...): Promise<void> {
    const output = createTestRunOutput(formattedModules, unhandledErrors, reason)
    await this.storage.saveTest(JSON.stringify(output, null, 2))
  }
}
```

### Pytest Reporter (Python/pip)
```python
class TDDGuardPytestPlugin:
    def __init__(self, config=None, cwd=None):
        self.test_results = []
        self.storage_dir = self._determine_storage_dir(config, cwd)

    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            test_result = {
                'name': report.nodeid.split('::')[-1],
                'fullName': report.nodeid,
                'state': 'passed' if report.passed else ('failed' if report.failed else 'skipped')
            }
            if report.failed:
                test_result['errors'] = [{'message': str(report.longrepr)}]
            self.test_results.append(test_result)

    def pytest_sessionfinish(self, session, exitstatus):
        # Group tests by module and save to storage
        output = {'testModules': list(modules_map.values())}
        storage_path = self.storage_dir / 'test.json'
        with open(storage_path, 'w') as f:
            json.dump(output, f, indent=2)
```

### Reporter Storage Location
All reporters write to: `.claude/tdd-guard/data/test.json`

---

## Hook Event Type Definitions

### Core Hook Schema
```typescript
// Base Hook Context
export const HookContextSchema = z.object({
  session_id: z.string(),
  transcript_path: z.string(),
  hook_event_name: z.string(),
})

export const HookDataSchema = HookContextSchema.extend({
  tool_name: z.string(),
  tool_input: z.unknown(),
})

export type HookData = z.infer<typeof HookDataSchema>
```

### Session Events
```typescript
export const SessionStartSchema = HookContextSchema.extend({
  hook_event_name: z.literal('SessionStart'),
  source: z.enum(['startup', 'resume', 'clear']),
})

export const UserPromptSubmitSchema = HookContextSchema.extend({
  prompt: z.string(),
  cwd: z.string(),
}).refine((data) => data.hook_event_name === 'UserPromptSubmit')
```

### Tool Operations
```typescript
export const EditOperationSchema = HookContextSchema.extend({
  tool_name: z.literal('Edit'),
  tool_input: EditSchema,
})

export const MultiEditOperationSchema = HookContextSchema.extend({
  tool_name: z.literal('MultiEdit'),
  tool_input: MultiEditSchema,
})

export const WriteOperationSchema = HookContextSchema.extend({
  tool_name: z.literal('Write'),
  tool_input: WriteSchema,
})

export const TodoWriteOperationSchema = HookContextSchema.extend({
  tool_name: z.literal('TodoWrite'),
  tool_input: TodoWriteSchema,
})

// Discriminated union for type-safe handling
export const ToolOperationSchema = z.discriminatedUnion('tool_name', [
  EditOperationSchema,
  MultiEditOperationSchema,
  WriteOperationSchema,
  TodoWriteOperationSchema,
])
```

### Type Guards
```typescript
export const isEditOperation = (op: ToolOperation): op is EditOperation =>
  op.tool_name === 'Edit'

export const isMultiEditOperation = (op: ToolOperation): op is MultiEditOperation =>
  op.tool_name === 'MultiEdit'

export const isWriteOperation = (op: ToolOperation): op is WriteOperation =>
  op.tool_name === 'Write'

export const isTodoWriteOperation = (op: ToolOperation): op is TodoWriteOperation =>
  op.tool_name === 'TodoWrite'
```

---

## Session State Management

### Transient vs Persistent Data
```typescript
export const TRANSIENT_DATA = ['test', 'todo', 'modifications', 'lint'] as const
// Transient data is cleared on session start
// Persistent: config, instructions
```

### Session Handler
```typescript
export class SessionHandler {
  async processSessionStart(hookData: string): Promise<void> {
    const parsedData = JSON.parse(hookData)
    const sessionStartResult = SessionStartSchema.safeParse(parsedData)

    if (!sessionStartResult.success) return

    await this.ensureInstructionsExist()
    await this.storage.clearTransientData()
  }

  private async ensureInstructionsExist(): Promise<void> {
    const existingInstructions = await this.storage.getInstructions()
    if (!existingInstructions) {
      await this.storage.saveInstructions(RULES)
    }
  }
}
```

### File Storage Implementation
```typescript
export class FileStorage implements Storage {
  async clearTransientData(): Promise<void> {
    await Promise.all(
      TRANSIENT_DATA.map((fileType) =>
        this.deleteFileIfExists(this.filePaths[fileType])
      )
    )
  }
}
```

### Storage Directory Structure
```
.claude/tdd-guard/data/
  test.json         # Test results (transient)
  todos.json        # TodoWrite operations (transient)
  modifications.json # File modifications (transient)
  lint.json         # Lint results (transient)
  config.json       # Guard configuration (persistent)
  instructions.md   # TDD rules (persistent)
```

---

## Guard Blocking Patterns

### Validation Result Types
```typescript
export type ValidationResult = {
  decision: 'approve' | 'block' | undefined
  reason: string
  continue?: boolean
  stopReason?: string
}
```

### Block on Lint Issues
```typescript
async function checkLintNotification(storage: Storage, hookData: HookData): Promise<ValidationResult> {
  // Only block if tests are passing AND there are lint issues
  if (!testsPassing) return defaultResult

  const hasIssues = lintData.errorCount > 0 || lintData.warningCount > 0

  // Block if issues exist and not yet notified
  if (hasIssues && !lintData.hasNotifiedAboutLintIssues) {
    // Update flag to prevent repeated blocking
    await storage.saveLint(JSON.stringify({
      ...lintData,
      hasNotifiedAboutLintIssues: true
    }))

    return {
      decision: 'block',
      reason: 'Code quality issues detected. Fix before proceeding.'
    }
  }
  return defaultResult
}
```

### Post-Tool Lint Blocking
```typescript
function createBlockResult(lintData: LintData): ValidationResult {
  const formattedIssues = formatLintIssues(lintData.issues)
  const summary = `\n${lintData.errorCount + lintData.warningCount} problems`

  return {
    decision: 'block',
    reason: `Lint issues detected:${formattedIssues}\n${summary}\n\nFix before proceeding.`
  }
}
```

### User Command Blocking (Control Flow)
```typescript
export class UserPromptHandler {
  private readonly GUARD_COMMANDS = {
    ON: 'tdd-guard on',
    OFF: 'tdd-guard off'
  } as const

  private createBlockResult(message: string): ValidationResult {
    return {
      decision: undefined,  // Not a block decision
      reason: message,
      continue: false,      // Stop further processing
      stopReason: message
    }
  }
}
```

---

## Configuration Examples

### Package.json Structure
```json
{
  "name": "tdd-guard",
  "bin": {
    "tdd-guard": "dist/cli/tdd-guard.js"
  },
  "workspaces": [
    "reporters/vitest",
    "reporters/jest",
    "reporters/storybook"
  ],
  "dependencies": {
    "@anthropic-ai/claude-agent-sdk": "^0.1.8",
    "@anthropic-ai/sdk": "^0.65.0",
    "minimatch": "^10.0.3",
    "zod": "^4.1.11"
  }
}
```

### Environment Variables
```bash
# Validation client
VALIDATION_CLIENT=sdk|api|cli

# Model configuration
TDD_GUARD_MODEL_VERSION=claude-sonnet-4-0
TDD_GUARD_ANTHROPIC_API_KEY=sk-...

# Project configuration
CLAUDE_PROJECT_DIR=/absolute/path/to/project

# Linter type
LINTER_TYPE=eslint|golangci-lint
```

### Guard Config Schema
```typescript
export const GuardConfigSchema = z.object({
  guardEnabled: z.boolean().optional(),
  ignorePatterns: z.array(z.string()).optional(),
})
```

### Claude Code Settings for Enforcement
```json
{
  "permissions": {
    "deny": [
      "Read(.claude/tdd-guard/**)",
      "Bash(echo:*)",
      "Bash(sed:*)",
      "Bash(awk:*)"
    ]
  }
}
```

---

## Code to Copy

### Storage Interface
```typescript
export const TRANSIENT_DATA = ['test', 'todo', 'modifications', 'lint'] as const

export interface Storage {
  saveTest(content: string): Promise<void>
  saveTodo(content: string): Promise<void>
  saveModifications(content: string): Promise<void>
  saveLint(content: string): Promise<void>
  saveConfig(content: string): Promise<void>
  saveInstructions(content: string): Promise<void>
  getTest(): Promise<string | null>
  getTodo(): Promise<string | null>
  getModifications(): Promise<string | null>
  getLint(): Promise<string | null>
  getConfig(): Promise<string | null>
  getInstructions(): Promise<string | null>
  clearTransientData(): Promise<void>
}
```

### Hook Event Processing Pattern
```typescript
export async function processHookData(
  inputData: string,
  deps: ProcessHookDataDeps = {}
): Promise<ValidationResult> {
  const parsedData = JSON.parse(inputData)

  const storage = deps.storage ?? new FileStorage()
  const guardManager = new GuardManager(storage)

  // Check ignore patterns
  const filePath = extractFilePath(parsedData)
  if (filePath && await guardManager.shouldIgnoreFile(filePath)) {
    return defaultResult
  }

  // Process session events
  if (parsedData.hook_event_name === 'SessionStart') {
    await sessionHandler.processSessionStart(inputData)
    return defaultResult
  }

  // Process user commands
  const stateResult = await userPromptHandler.processUserCommand(inputData)
  if (stateResult) return stateResult

  // Check if guard is disabled
  const disabledResult = await userPromptHandler.getDisabledResult()
  if (disabledResult) return disabledResult

  // Handle PostToolUse (linting)
  if (hookResult.data.hook_event_name === 'PostToolUse') {
    return await lintHandler.handle(inputData)
  }

  // Validate PreToolUse
  return await performValidation(deps)
}
```

### Discriminated Union Type Pattern
```typescript
import { z } from 'zod'

// Define individual operation schemas
const EditOperationSchema = BaseSchema.extend({
  tool_name: z.literal('Edit'),
  tool_input: EditInputSchema,
})

const WriteOperationSchema = BaseSchema.extend({
  tool_name: z.literal('Write'),
  tool_input: WriteInputSchema,
})

// Create discriminated union
const ToolOperationSchema = z.discriminatedUnion('tool_name', [
  EditOperationSchema,
  WriteOperationSchema,
])

// Type guards for runtime narrowing
const isEditOperation = (op: ToolOperation): op is EditOperation =>
  op.tool_name === 'Edit'
```

### Guard Manager Pattern
```typescript
export class GuardManager {
  private readonly storage: Storage
  private readonly minimatchOptions = {
    matchBase: true,
    nobrace: false,
    dot: true,
  } as const

  static readonly DEFAULT_IGNORE_PATTERNS = ['*.md', '*.json', '*.yml']

  async isEnabled(): Promise<boolean> {
    const config = await this.getConfig()
    return config?.guardEnabled ?? true
  }

  async enable(): Promise<void> {
    await this.setGuardEnabled(true)
  }

  async disable(): Promise<void> {
    await this.setGuardEnabled(false)
  }

  async shouldIgnoreFile(filePath: string): Promise<boolean> {
    const patterns = await this.getIgnorePatterns()
    return patterns.some((pattern) =>
      minimatch(filePath, pattern, this.minimatchOptions)
    )
  }
}
```

### Linter Interface and Provider
```typescript
export interface Linter {
  lint(filePaths: string[], configPath?: string): Promise<LintResult>
}

export class LinterProvider {
  getLinter(config?: Config): Linter | null {
    switch (config?.linterType) {
      case 'eslint':
        return new ESLint()
      case 'golangci-lint':
        return new GolangciLint()
      default:
        return null
    }
  }
}
```

---

## Notes for Implementation

### Architecture Recommendations
1. **Use Zod for all schemas** - Provides both runtime validation and TypeScript types
2. **Discriminated unions** for tool operations enable type-safe handling
3. **Storage abstraction** allows testing with MemoryStorage
4. **Provider pattern** for configurable components (linters, model clients)
5. **Transient vs persistent data** separation simplifies session management

### Key Design Decisions
1. **Guard enabled by default** - Users opt-out rather than opt-in
2. **Ignore patterns exclude non-code files** - .md, .json, .yml, etc.
3. **Single notification for lint issues** - Flag prevents repeated blocking
4. **AI validation only on PreToolUse** - PostToolUse just runs linting
5. **All reporters share unified format** - Simplifies cross-framework support

### Testing Patterns
- **Test factories** in `reporters/test/factories/` for each reporter type
- **Integration tests** verify full pipeline from hook input to storage
- **Schema tests** validate Zod schemas against expected inputs

### Extension Points
1. Add new reporters by implementing unified output format
2. Add new linters by implementing `Linter` interface
3. Add new hook events by extending `HookContextSchema`
4. Customize TDD rules by modifying `instructions.md`

### Security Considerations
1. **Validate CLAUDE_PROJECT_DIR** - Must be absolute, no traversal, contain cwd
2. **Protect guard settings** via permission denials
3. **Block file bypass commands** (echo, sed, awk) in shell

### Multi-Language Support
| Language | Reporter Package | Entry Point |
|----------|-----------------|-------------|
| JavaScript/TypeScript | tdd-guard-jest, tdd-guard-vitest | npm |
| Python | tdd-guard-pytest | pip |
| PHP | tdd-guard/phpunit | composer |
| Ruby | tdd-guard-rspec | gem |
| Go | tdd-guard-go | binary |
| Rust | tdd-guard-rust | crates.io |
