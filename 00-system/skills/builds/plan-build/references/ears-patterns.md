# EARS Patterns

**Purpose**: Requirement templates for Build and Skill build types

---

## The Six EARS Patterns

Every requirement MUST follow exactly ONE pattern.

### 1. Ubiquitous (Always True)

**Template**: THE `<system>` SHALL `<response>`

**When to use**: Requirements that always apply, unconditionally

**Examples**:
- THE API SHALL return JSON responses
- THE system SHALL log all errors
- THE skill SHALL use active voice in outputs

---

### 2. Event-Driven (Trigger → Response)

**Template**: WHEN `<trigger>`, THE `<system>` SHALL `<response>`

**When to use**: Something happens, system responds

**Examples**:
- WHEN user clicks submit, THE form SHALL validate inputs
- WHEN API returns error, THE client SHALL retry up to 3 times
- WHEN skill completes, THE system SHALL update resume-context.md

---

### 3. State-Driven (While Condition Holds)

**Template**: WHILE `<condition>`, THE `<system>` SHALL `<response>`

**When to use**: Continuous behavior during a state

**Examples**:
- WHILE connection is active, THE client SHALL send heartbeats every 30s
- WHILE processing, THE system SHALL display progress indicator
- WHILE in discovery phase, THE router SHALL accept user corrections

---

### 4. Unwanted Behavior (Exception Handling)

**Template**: IF `<condition>`, THEN THE `<system>` SHALL `<response>`

**When to use**: Error handling, edge cases

**Examples**:
- IF rate limit exceeded, THEN THE API SHALL return 429
- IF file not found, THEN THE reader SHALL return descriptive error
- IF validation fails, THEN THE form SHALL highlight invalid fields

---

### 5. Optional Feature

**Template**: WHERE `<option>`, THE `<system>` SHALL `<response>`

**When to use**: Configurable or optional behavior

**Examples**:
- WHERE caching enabled, THE service SHALL store responses for 5 minutes
- WHERE debug mode active, THE logger SHALL include stack traces
- WHERE user prefers verbose output, THE skill SHALL show intermediate steps

---

### 6. Complex (Multiple Conditions)

**Template**: [WHERE] [WHILE] [WHEN/IF] THE `<system>` SHALL `<response>`

**When to use**: Combine multiple conditions

**Examples**:
- WHERE admin, WHEN delete requested, THE system SHALL require confirmation
- WHILE authenticated, WHEN session expires, THE app SHALL redirect to login
- WHERE API v2, IF deprecated endpoint called, THE server SHALL return warning

---

## Quality Checklist

After writing requirements, verify:

- [ ] Each requirement uses exactly one EARS pattern
- [ ] THE/WHEN/WHILE/IF/WHERE keywords are capitalized
- [ ] System name is specific (not "it" or "the system")
- [ ] Response is measurable or verifiable
- [ ] No compound requirements (split if "and" appears)

---

## Common Mistakes

### Wrong: Vague Response
```
WHEN user logs in, THE system SHALL handle it appropriately
```

### Right: Specific Response
```
WHEN user logs in, THE system SHALL create session and redirect to dashboard
```

### Wrong: Multiple Actions
```
WHEN form submitted, THE system SHALL validate, save, and send email
```

### Right: Split Into Multiple
```
WHEN form submitted, THE system SHALL validate all required fields
WHEN validation passes, THE system SHALL save to database
WHEN save succeeds, THE system SHALL send confirmation email
```

---

## Applies To

- **Build** builds: discovery.md requirements section
- **Skill** builds: discovery.md requirements section

Other build types use simpler discovery questions.

---

*Reference: EARS (Easy Approach to Requirements Syntax)*
