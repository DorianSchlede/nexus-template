# INCOSE Quality Rules

**Purpose**: Quality standards for requirements in Build and Skill builds

---

## Clarity and Precision

### Active Voice

**Rule**: Clearly state who does what

**Wrong**: "The data should be validated"
**Right**: "THE API SHALL validate input data"

### No Vague Terms

**Rule**: Avoid subjective or unmeasurable terms

**Banned words**:
- quickly, fast, slow
- adequate, sufficient, reasonable
- user-friendly, intuitive, easy
- good, better, best
- approximately, about
- several, many, few

**Wrong**: "THE system SHALL respond quickly"
**Right**: "THE system SHALL respond within 200ms"

### No Pronouns

**Rule**: Don't use it, them, they, this, that - use specific names

**Wrong**: "When it receives the request, it should process it"
**Right**: "WHEN the API receives the request, THE API SHALL process the request"

### Consistent Terminology

**Rule**: Use defined terms consistently throughout

Define once:
```
Definitions:
- User: Person interacting with the interface
- Client: Application making API requests
- Session: Authenticated user context
```

Then use consistently:
```
WHEN User clicks submit...
WHEN Client sends request...
WHILE Session is active...
```

---

## Testability

### Explicit Conditions

**Rule**: All conditions must be measurable or verifiable

**Wrong**: "THE system SHALL handle large files"
**Right**: "THE system SHALL process files up to 100MB"

### Measurable Criteria

**Rule**: Use specific, quantifiable criteria

**Wrong**: "THE API SHALL be fast"
**Right**: "THE API SHALL respond to 95% of requests within 500ms"

### One Thought Per Requirement

**Rule**: Each requirement should test one thing

**Wrong**: "THE system SHALL validate inputs and log errors and retry failures"
**Right**: Split into three requirements:
- "THE system SHALL validate all inputs before processing"
- "THE system SHALL log all validation errors"
- "IF validation fails, THEN THE system SHALL retry up to 3 times"

---

## Completeness

### No Escape Clauses

**Rule**: Avoid wiggle room

**Banned phrases**:
- where possible
- if feasible
- as appropriate
- when practical
- to the extent possible

**Wrong**: "THE system SHALL encrypt data where possible"
**Right**: "THE system SHALL encrypt all data at rest using AES-256"

### No Absolutes (Unless True)

**Rule**: Avoid never/always unless truly absolute

**Usually wrong**: "THE system SHALL never crash"
**Better**: "THE system SHALL handle all expected error conditions gracefully"

**Acceptable absolute**: "THE system SHALL never store plaintext passwords"

### Solution-Free

**Rule**: Focus on what, not how

**Wrong**: "THE API SHALL use Redis for caching"
**Right**: "THE API SHALL cache frequently accessed data with 5-minute TTL"

---

## Quality Checklist

For each requirement, verify:

### Clarity
- [ ] Uses active voice
- [ ] No vague terms (quickly, adequate, etc.)
- [ ] No pronouns (it, them, they)
- [ ] Uses consistent terminology

### Testability
- [ ] All conditions are explicit
- [ ] Criteria are measurable
- [ ] Tests one thing only

### Completeness
- [ ] No escape clauses (where possible, if feasible)
- [ ] Absolutes are truly absolute
- [ ] Focuses on what, not how

---

## Example: Before and After

### Before (Poor Quality)
```
The system should quickly process user requests and handle errors
appropriately when they occur, logging them if needed.
```

### After (INCOSE Compliant)
```
REQ-1: THE API SHALL process requests within 200ms for 95th percentile

REQ-2: IF request processing fails, THEN THE API SHALL return structured
error response with error code and message

REQ-3: THE API SHALL log all errors with timestamp, error code, and
request ID
```

---

## Applies To

- **Build** builds: discovery.md requirements section
- **Skill** builds: discovery.md requirements section

Other build types use simpler discovery questions.

---

*Reference: INCOSE Guide for Writing Requirements*
