================================================================================
CLAUDE INSTRUCTIONS - ONBOARDING RESUME
================================================================================

STATE: Resuming onboarding skill after session compaction/resume

You were in the middle of onboarding. Resume seamlessly without re-displaying content the user already saw.

**Skill to Resume**: {skill}
**Resume From**: {resume_info}

================================================================================
RESUMPTION LOGIC
================================================================================

**For how-nexus-works**:
- Ask user: "We were going through the system tour. Continue?"
- If yes, continue from current part
- Don't restart from Part 1

**For complete-setup**:
- Resume from Step {resume_from_step}/7
- Don't re-do previous steps (user already completed them)
- Show: "Continuing setup from Step {resume_from_step}..."
- Reference 02-builds/00-onboarding-session/ for saved state

================================================================================
USER EXPERIENCE
================================================================================

1. Acknowledge the resume: "Welcome back! Picking up where we left off..."
2. Brief reminder of context (1 sentence max)
3. Continue with next step/part
4. Don't ask "want to continue?" - just do it (user can say stop if needed)

================================================================================
IMPORTANT
================================================================================

- DO NOT restart the skill from the beginning
- DO NOT re-display content user already saw
- Respect language_preference for all text
- State is preserved in user-config.yaml
- Onboarding project files in 02-builds/00-onboarding-session/
