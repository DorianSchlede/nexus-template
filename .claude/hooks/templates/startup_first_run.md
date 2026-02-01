```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              Your AI operating system
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ChatGPT gives you answers. Nexus enables you to build.

What people actually use it for:

  > Job Search
     Search 15 job boards every morning, prioritize matches,
     and generate tailored CVs from your stored stories.

  > Health System
     Talk to your fitness data, log meals from photos,
     get personalized training plans that adapt to your progress.

  > Content Engine
     Interview yourself to capture stories, plan your calendar,
     auto-generate posts that sound like you.

The difference: Everything you build is always remembered.
Context compounds. Every session makes it smarter.

Ready?
```

================================================================================
CLAUDE INSTRUCTIONS - HEROIC INTRO
================================================================================

STATE: First run - fresh installation

After displaying the heroic intro above, proceed to LANGUAGE SELECTION.

================================================================================
LANGUAGE SELECTION
================================================================================

Display:

```
What language do you want to work in?

1. English
2. Deutsch
3. Español
4. Français
5. Italiano
6. 日本語
7. 中文
8. Other (type your language)

(All future sessions will use this language)

Type the number (1-8):
```

**When user responds**:
- If 1-7: Map to language code (en, de, es, fr, it, ja, zh)
- If 8: Ask "Which language?" and accept their input

**State Update**:
```yaml
onboarding:
  language_preference: "<selected language>"
```

Save to user-config.yaml, then proceed to FORK DECISION.

================================================================================
FORK DECISION
================================================================================

Display:

```
═══════════════════════════════════════════════════════════════
How do you want to start?
═══════════════════════════════════════════════════════════════

┌───────────────────────────────────────────────────────────┐
│  1. QUICK START (8-10 minutes)                            │
│                                                           │
│  * Set your goal                                          │
│  * Plan your first project                                │
│  * Ready to execute next session                          │
│                                                           │
│  Best if: You want to jump in now                         │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  2. COMPLETE SETUP (10-12 minutes)                        │
│                                                           │
│  * Import your existing files                             │
│  * AI analyzes your work                                  │
│  * Personalized roadmap                                   │
│                                                           │
│  Best if: You have files to import                        │
└───────────────────────────────────────────────────────────┘

Choose 1 or 2:
```

**Routing**:

If user chooses 1 (Quick Start):
```yaml
onboarding:
  path_chosen: "quick_start"
  status: "in_progress"
  in_progress_skill: "quick-start"
```
Load skill: `quick-start`

If user chooses 2 (Complete Setup):
```yaml
onboarding:
  path_chosen: "complete_setup"
  status: "in_progress"
  in_progress_skill: "complete-setup"
```
Load skill: `complete-setup`

================================================================================
IMPORTANT NOTES
================================================================================

- Display ALL content in the user's selected language (after language selection)
- Do NOT show the old menu format
- This flow replaces the previous 3-step recommendation
- After fork decision, immediately load the chosen skill
- The heroic intro should feel authentic and personal, not like marketing
