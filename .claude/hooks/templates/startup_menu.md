================================================================================
MANDATORY: STARTUP SEQUENCE
================================================================================

STEP 1 - MANDATORY: Display Nexus menu
- Show ASCII banner
- Show active projects with progress
- Show suggested next actions

STEP 2 - MANDATORY: Adjust suggestions based on state
- If onboarding incomplete → Prioritize onboarding
- If has_active_projects → Prioritize: "Continue project at X%"
- If no_projects → Prioritize: "Start your first project"

STEP 3 - MANDATORY: Route user input correctly
- New work request → ALWAYS suggest plan-project first
- Project reference → Load execute-project skill
- Skill trigger → Load matched skill

================================================================================
Wait for user input after displaying menu.
================================================================================
