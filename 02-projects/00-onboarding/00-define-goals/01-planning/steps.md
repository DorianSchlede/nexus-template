# Tasks: Get Started (Project 00)

**Project ID**: 00-define-goals
**Onboarding Step**: 1 of 4
**Estimated Time**: 8-10 minutes

---

⚠️ **CRITICAL FOR close-session SKILL**:
This file contains **40 REAL TASKS** with checkboxes that MUST be marked complete when work is done!

---

## Design Philosophy

**Key Principle**: CONCRETE BEFORE ABSTRACT

We start by capturing YOUR goals (concrete), create your memory workspace (action), then explain what happened (understanding). You learn by experiencing, not by listening.

---

## Execution Instructions for AI

**Critical Principles**:
- NO system state complexity in first 30 seconds
- Goals and discovery happen FIRST (concrete)
- Memory creation happens SECOND (action)
- Explanation happens THIRD (abstract, now grounded)

**Vocabulary Limit**: Only 4 terms this session (Memory, Goals, Sessions, close-session)

**Context Loading**: None (first project)

**Output**: goals.md, roadmap.md, user-config.yaml, project-map.md, core-learnings.md, session-reports/

---

## Task Execution Flow

**Time Breakdown** (8-10 minutes):

| Section | Focus | Time |
|---------|-------|------|
| 0 | Welcome + Language | 30 sec |
| 1 | Your Goals (Discovery + Definition) | 5 min |
| 2 | Optional Context (FYI only) | 15 sec |
| 3 | Create Your Workspace | 2 min |
| 4 | Understanding Memory | 2 min |
| 5 | Close-Session Habit | 2 min |
| 6 | What's Next | 1 min |

---

## Section 0: Welcome + Language (30 seconds)

- [ ] **Task 0.1**: Aspirational welcome
  - Show Nexus banner
  - Say: "Welcome to Nexus—your AI partner for building the future."
  - Say: "I'm not just a chatbot. I'm a persistent system that learns your goals, remembers your context, and helps you build complex projects."
  - Say: "In the next 10 minutes, we'll create your personalized memory core."
  - **NOTE**: NO system state complexity, NO project/skill lists
  - Time: 15 seconds

- [ ] **Task 0.2**: Language selection
  - Say: "🌍 First, what language do you prefer?"
  - Examples: "English, Deutsch, Español, Français, 中文, 日本語, etc."
  - Wait for answer
  - Capture: USER_LANGUAGE
  - Say: "Perfect! Switching to [USER_LANGUAGE] now..."
  - **CRITICAL**: ALL subsequent messages in USER_LANGUAGE
  - Time: 15 seconds

- [ ] **Task 0.3**: Show onboarding roadmap
  - Say: "Before we dive in, here's your complete onboarding journey:"
  - Display roadmap:
    ```
    ╔══════════════════════════════════════════════════════════╗
    ║          YOUR NEXUS ONBOARDING JOURNEY                   ║
    ╠══════════════════════════════════════════════════════════╣
    ║                                                          ║
    ║  Session 1 (9-11 min) → YOU ARE HERE                    ║
    ║  📝 Define Goals                                         ║
    ║     • Capture your role and goals                       ║
    ║     • Create your memory system                         ║
    ║     • Learn close-session habit                         ║
    ║                                                          ║
    ║  Session 2 (15-18 min)                                  ║
    ║  🚀 Your First Project                                  ║
    ║     • Create your workspace folder structure            ║
    ║     • Build a real project for your work                ║
    ║     • Understand memory persistence                     ║
    ║                                                          ║
    ║  Session 3 (14-16 min)                                  ║
    ║  🔧 Your First Skill                                    ║
    ║     • Create a reusable workflow                        ║
    ║     • Learn the difference: Projects end, Skills repeat ║
    ║     • Master the Nexus system                           ║
    ║                                                          ║
    ║  Session 4 (16-18 min)                                  ║
    ║  🎓 System Mastery                                      ║
    ║     • Full menu and navigation                          ║
    ║     • Advanced features & Expert collaboration          ║
    ║     • You're ready to work independently!               ║
    ║                                                          ║
    ║  Total: 55-65 minutes over 4 short sessions            ║
    ╚══════════════════════════════════════════════════════════╝
    ```
  - Say: "Each session builds on the last, so you learn by doing."
  - Say: "Ready to start Session 1?"
  - Wait for confirmation
  - Time: 45 seconds

---

## Section 1: Your Goals (5 minutes) - CONCRETE FIRST

- [ ] **Task 1.0**: Frame the importance of goals
  - Say: "Now let's capture YOUR goals. This is the most important step."
  - Say: "Whatever we put here gets loaded EVERY session—it's your persistent context."
  - Say: "The more specific you are now, the better I can help you later."
  - Say: "Think of this as telling a smart assistant exactly what you're working toward."
  - Time: 30 seconds

- [ ] **Task 1.1**: Discover their work (WITH AI suggestions)
  - Say: "Let's start with your vision. What would you like to build with your AI companion?"
  - Wait for answer
  - Capture: USER_ROLE (infer from answer)
  - **AI Analysis** (if context document provided in Section 2):
    - Extract role/domain from shared document
    - Use to inform suggestions below
  - **AI Suggestion** (ALWAYS provide, not just questions):
    - Say: "Based on [ROLE], I'm guessing your work might involve:"
    - Suggest 2-3 typical work patterns for their role
    - Example for "Product Manager": "• Defining product roadmaps, • Managing stakeholders, • Prioritizing features"
    - Example for "Consultant": "• Client projects, • Proposals and pitches, • Research and analysis"
  - Ask: "Does that sound right, or is your situation different?"
  - Wait for confirmation/correction
  - Refine understanding based on their response
  - Time: 90 seconds

- [ ] **Task 1.2**: Short-term goals (3 months) (WITH AI suggestions)
  - Say: "What do you want to accomplish in the next 3 months?"
  - Wait for answer
  - Capture: SHORT_TERM_GOAL
  - **AI Analysis** (if context document provided):
    - Extract goals/objectives from shared document
    - Use to validate or enhance their stated goal
  - **AI Suggestion** (ALWAYS provide suggestions + questions):
    - Say: "Got it! For a goal like '[SHORT_TERM_GOAL]', I'd suggest focusing on:"
    - Suggest 2-3 relevant sub-goals or metrics
    - Example for "Launch consulting": "• Define service offering, • Create 3 case studies, • Build pipeline of 5 prospects"
    - Example for "Ship product": "• Complete MVP features, • Get 10 beta users, • Iterate based on feedback"
  - Ask: "Which of these resonates most, or is there something else that's more important?"
  - Wait for answer and refine
  - Time: 120 seconds

- [ ] **Task 1.3**: Long-term vision (1 year) (WITH AI suggestions)
  - Say: "And looking further ahead—what's your 1-year vision?"
  - Wait for answer
  - Capture: LONG_TERM_GOAL
  - **AI Analysis** (if context document provided):
    - Extract long-term strategy from shared document
    - Connect to stated vision
  - **AI Suggestion** (ALWAYS provide vision-building):
    - Say: "A 1-year vision like '[LONG_TERM_GOAL]' typically involves:"
    - Suggest 2-3 milestones or phases
    - Example for "Grow consulting to $500K": "• Q1-Q2: Build foundation, • Q3-Q4: Scale delivery, • Ongoing: Build team"
    - Example for "Launch startup": "• Q1: Product-market fit, • Q2-Q3: Growth engine, • Q4: Fundraising"
  - Ask: "Does that timeline feel realistic, or would you adjust it?"
  - Wait for confirmation/adjustment
  - Time: 120 seconds

- [ ] **Task 1.4**: Confirm understanding
  - Say: "Let me make sure I understand:"
  - Summarize: "You're a [ROLE] who wants to [SHORT_TERM_GOAL] in 3 months and [LONG_TERM_GOAL] within a year."
  - Ask: "Is that right?"
  - Wait for confirmation/corrections
  - Time: 30 seconds

---

## Section 2: Add Context to Understand Your Goals (1 minute) - OPTIONAL BUT HELPFUL

**Purpose**: If you have documents about your work, sharing them now helps me understand your goals better!

- [ ] **Task 2.1**: Offer to add context documents (WITH pause + clear instructions)
  - Step 1: Frame the purpose (15 sec)
    - Say: "Before we dive into goals, quick question:"
    - Say: "Do you have any documents about your work that could help me understand your goals better?"
    - Say: "• Business plans, project docs, strategy memos, etc."
    - Say: "This is 100% optional, but can help me give better suggestions!"
  - Step 2: Explain HOW to share files (30 sec)
    - Say: "If you want to share context, here's how:"
    - Say: "**Option 1: @ attachment (easiest)**"
    - Say: "• Type '@' and select a file from the picker"
    - Say: "• ⚠️ IMPORTANT: The file must be in your active folder (where you opened this chat)"
    - Say: ""
    - Say: "**Option 2: Create input folder**"
    - Say: "• Create a folder: `04-workspace/input/` in your Nexus-v3 folder"
    - Say: "• Place files there, and I can access them automatically"
  - Step 3: Pause and wait (15 sec)
    - Say: "Want to share any context documents now, or should we continue?"
    - Say: "• Type '@filename' to share (I'll wait!)"
    - Say: "• Or say 'continue' to move on"
    - **WAIT** for user response
    - IF user shares file:
      - Read and analyze the file
      - Say: "Great! I can see [filename]. I'll use this to better understand your goals."
      - Extract relevant context (role, domain, goals, challenges)
      - Store for use in Section 1 suggestions
    - IF user says "continue" or "skip":
      - Say: "No problem! We'll capture your goals through conversation."
      - Say: "You can always share documents later with @filename."
  - Time: 1 minute total

---

## Section 2.5: MCP Server Setup (2 minutes) - OPTIONAL API CONFIGURATION

**Purpose**: Configure external API access for Airtable, Beam Studio, and Slack

- [ ] **Task 2.5.1**: Introduce MCP server setup
  - Say: "Before we create your workspace, let's set up API access for external tools."
  - Say: "This is optional but recommended—it lets me access Airtable, Beam Studio, and Slack on your behalf."
  - Say: "This takes 2 minutes now, or you can skip and set it up later."
  - Ask: "Would you like to set up API keys now?"
  - IF user says "yes" → Continue to Task 2.5.2
  - IF user says "skip" or "later" → Say "No problem! You can set this up later by running the commands in Section 2.5.2 manually." → Skip to Section 3
  - Time: 30 seconds

- [ ] **Task 2.5.2**: Copy configuration templates to root
  - Execute commands:
    ```bash
    # Copy .env template
    cp 02-projects/00-onboarding/00-define-goals/02-resources/env-template.txt .env.example
    cp .env.example .env
    
    # Copy MCP config
    cp 02-projects/00-onboarding/00-define-goals/02-resources/mcp-config.json .mcp.json
    
    # Copy gitignore (if doesn't exist)
    if [ ! -f .gitignore ]; then
      cp 02-projects/00-onboarding/00-define-goals/02-resources/gitignore-template.txt .gitignore
    fi
    ```
  - Say: "✅ Configuration files created in your Nexus-v3 root directory"
  - Time: 15 seconds

- [ ] **Task 2.5.3**: Guide user to add API keys
  - Say: "Now, open the `.env` file in your Nexus-v3 root directory"
  - Say: "You'll see placeholders for:"
  - List:
    - "• **AIRTABLE_API_KEY** - Get from: https://airtable.com/account"
    - "• **BEAM_API_TOKEN** - Get from: https://app.beam.ai → Personal settings → API Keys"
    - "• **SLACK_BOT_TOKEN** (optional) - Get from: https://api.slack.com/apps"
  - Say: "Replace the placeholder values with your actual API keys"
  - Say: "Take your time—I'll wait. Type 'done' when you've added your keys (or 'skip' to do this later)"
  - Wait for user response
  - IF user says "done" → Continue to Task 2.5.4
  - IF user says "skip" → Say "No problem! Files are ready in root—just edit .env when you're ready" → Skip to Section 3
  - Time: 60 seconds

- [ ] **Task 2.5.4**: Verify and explain
  - Say: "Perfect! Your MCP servers are now configured."
  - Say: "What this means:"
  - List:
    - "• I can now access your Airtable bases"
    - "• I can interact with Beam Studio on your behalf"
    - "• I can send/read Slack messages (if configured)"
  - Say: "⚠️ **Security note**: Your `.env` file is in `.gitignore`—it will NEVER be committed to Git"
  - Say: "You'll need to restart Claude Code for MCP servers to activate (we'll do this after onboarding)"
  - Time: 30 seconds

---

## Section 3: Create Your Workspace (2 minutes) - ACTION

- [ ] **Task 3.1**: Announce creation
  - Say: "Perfect! Let me create your personalized workspace..."
  - Say: "This will take about 10 seconds."
  - Time: 5 seconds

- [ ] **Task 3.2**: Run init-memory.py with user data
  - Execute: `python 00-system/core/init-memory.py --language "[USER_LANGUAGE]" --role "[USER_ROLE]" --short-goal "[SHORT_TERM_GOAL]" --long-goal "[LONG_TERM_GOAL]"`
  - Use actual values collected in Section 0, 1, and 2
  - Creates personalized files:
    - 01-memory/goals.md (with actual user data)
    - 01-memory/roadmap.md (template)
    - 01-memory/user-config.yaml (with language set)
    - 01-memory/core-learnings.md (empty template)
    - 01-memory/session-reports/ (folder)
  - Validation: Read 01-memory/goals.md after creation to confirm it has actual data (not [TODO])
  - Time: 10 seconds

- [ ] **Task 3.3**: Show what was created
  - Say: "✅ Done! Here's what I created for you:"
  - Show file tree:
    ```
    01-memory/
      ├── goals.md          ← Your goals and work context
      ├── roadmap.md        ← Your milestones and next steps
      ├── user-config.yaml  ← Your language and preferences
      ├── core-learnings.md ← For capturing insights
      ├── memory-map.md     ← System navigation for memory
      └── session-reports/  ← Session summaries
    ```
  - Time: 30 seconds

- [ ] **Task 3.4**: Brief file explanations
  - Say: "Let me explain each file:"
  - **goals.md**: "Your role, work pattern, and goals—everything we just discussed"
  - **roadmap.md**: "Your milestones, metrics, and priorities"
  - **user-config.yaml**: "Your language preference (so I always speak [USER_LANGUAGE])"
  - **core-learnings.md**: "Where we'll capture insights as you work"
  - **memory-map.md**: "Helps me navigate your memory system"
  - **session-reports/**: "Automatic summaries of our sessions"
  - Time: 45 seconds

---

## Section 4: Understanding Memory (2 minutes) - EXPLANATION

- [ ] **Task 4.0**: Show folder structure and boundaries
  - Say: "Let's look at what we just created. Here's your complete workspace:"
  - Display folder tree:
    ```
    Nexus-v3/
    ├── 00-system/          ← SYSTEM (I manage this - don't modify)
    │   ├── core/           ← Core scripts and infrastructure
    │   ├── skills/         ← System skills (close-session, etc.)
    │   └── ...
    ├── 01-memory/          ← YOUR MEMORY (always loaded)
    │   ├── goals.md        ← Your role and goals
    │   ├── roadmap.md      ← Your milestones
    │   ├── user-config.yaml ← Your language preference
    │   └── ...
    ├── 02-projects/        ← YOUR PROJECTS (you create these)
    │   └── (empty for now)
    ├── 04-workspace/       ← YOUR WORKSPACE (organize how you want)
    │   └── (empty for now)
    └── README.md
    ```
  - Say: "Important boundaries:"
  - Say: "• **00-system/**: This is mine—I'll manage it for you"
  - Say: "• **01-memory/**: This is OURS—your context, always loaded"
  - Say: "• **02-projects/**: This is YOURS—you'll create projects here"
  - Say: "• **04-workspace/**: This is YOURS—organize however you want"
  - Say: "This structure keeps everything organized and prevents confusion."
  - Time: 1 minute

- [ ] **Task 4.1**: Explain what just happened
  - Say: "🧠 Here's what makes this special:"
  - Say: "What I just created is YOUR MEMORY."
  - Say: "Normal AI conversations are stateless—every chat starts from scratch."
  - Say: "But Nexus is different: these files persist across sessions."
  - Time: 30 seconds

- [ ] **Task 4.2**: Show the value
  - Say: "Tomorrow, when you return, I'll automatically load these files."
  - Say: "I'll remember that you're a [USER_ROLE]"
  - Say: "I'll remember your goal to [SHORT_TERM_GOAL]"
  - Say: "You'll never have to re-explain yourself."
  - Time: 30 seconds

- [ ] **Task 4.3**: Connect to their goal
  - Say: "This memory is the foundation for everything else."
  - Say: "Next session, we'll use these goals to create your workspace structure."
  - Say: "Everything we build will serve YOUR goal: [SHORT_TERM_GOAL]"
  - Time: 30 seconds

- [ ] **Task 4.4**: Introduce terminology (4 terms only)
  - Say: "Quick vocabulary:"
  - **Memory**: "These files that persist across sessions"
  - **Goals**: "What you want to accomplish (we just defined yours)"
  - **Sessions**: "Each time we work together (like right now)"
  - **close-session**: "How we end sessions properly (you'll learn this next)"
  - Say: "That's all the vocabulary for today—just 4 terms!"
  - Time: 30 seconds

- [ ] **Task 4.5**: Explain session concept
  - Say: "Let's clarify what a 'session' means in Nexus."
  - Say: "A session = one conversation with me, from start to finish."
  - Say: "When do you start a NEW Nexus session?"
  - Say: "• Tomorrow when you come back"
  - Say: "• When you switch to different work"
  - Say: "• After closing your previous session"
  - Say: "Each session loads YOUR memory fresh, so I always remember you."
  - Time: 30 seconds

- [ ] **Task 4.6**: Explain living documents
  - Say: "Important: These memory files are LIVING documents."
  - Say: "They're not 'set it and forget it'—they grow with you."
  - Say: "As your goals evolve, you update goals.md"
  - Say: "As you learn patterns, core-learnings.md grows"
  - Say: "Think of them as your persistent knowledge base that improves over time."
  - Time: 30 seconds

- [ ] **Task 4.7**: Explain scope concept
  - Say: "One last concept: Your memory defines your SCOPE."
  - Say: "If you're working on your SaaS product → load this Nexus instance"
  - Say: "If you're working on a different client → create a separate Nexus instance"
  - Say: "Each major context gets its own memory. This prevents mixing unrelated work."
  - Say: "But within ONE context (like your SaaS), memory persists across all sessions."
  - Time: 30 seconds

---

## Section 5: The Close-Session Habit (2 minutes) - CRITICAL

- [ ] **Task 5.1**: Introduce the habit
  - Say: "🔚 Before we finish, there's ONE critical habit to learn:"
  - Say: "How to end sessions properly."
  - Say: "This is the MOST IMPORTANT habit in Nexus."
  - Time: 20 seconds

- [ ] **Task 5.2**: Explain close-session
  - Say: "When you're done working, say 'done'"
  - Say: "This triggers close-session—a skill that:"
  - List:
    - "✅ Saves all your progress"
    - "✅ Updates your memory files"
    - "✅ Creates a session summary"
    - "✅ Prepares for next session"
  - Say: "Think of it like saving your game before quitting."
  - Time: 40 seconds

- [ ] **Task 5.3**: Practice right now
  - Say: "Let's practice it right now!"
  - Say: "When you're ready to end this session, just say 'done'"
  - Say: "I'll show you what happens..."
  - Wait for user to say "done"
  - Time: 30 seconds

- [ ] **Task 5.4**: Execute close-session
  - User says "done"
  - **CRITICAL**: Load and execute close-session skill
  - Show the process:
    - "🔄 Running close-session..."
    - "✅ Progress saved"
    - "✅ Memory updated"
    - "✅ Session report created"
  - Time: 30 seconds

---

## Section 6: What's Next (1 minute)

- [ ] **Task 6.1**: Preview the journey
  - Say: "🎉 Great! You've completed the first step."
  - Say: "Here's what's ahead:"
  - Say: "**Next session (10-12 min)**: Create your workspace + first project using YOUR goals"
  - Say: "**Session 3 (15 min)**: Learn automation by creating your first reusable workflow"
  - Say: "**Session 4 (10 min)**: Review everything and graduate!"
  - Say: "Total onboarding: 3 more sessions (35-40 min), then you're fully operational."
  - Time: 40 seconds

- [ ] **Task 6.2**: Final message
  - Say: "🎯 What you accomplished today:"
  - List:
    - "✅ Defined your goals"
    - "✅ Created your memory"
    - "✅ Learned close-session habit"
  - Say: "Next time, we'll build your workspace. See you soon! 👋"
  - Time: 20 seconds

---

## Completion Checklist

- [ ] User selected language (all communication in USER_LANGUAGE)
- [ ] User defined role, work pattern, short-term goal, long-term goal
- [ ] Optional input folder mentioned (FYI only, no stopping)
- [ ] init-memory.py executed successfully
- [ ] All 6 memory files created with USER's actual content
- [ ] User understands Memory concept (persistence across sessions)
- [ ] User learned 4 terms: Memory, Goals, Sessions, close-session
- [ ] User practiced close-session successfully
- [ ] User understands what happens next (Project 01)

---

## Time Breakdown

| Section | Time | Tasks |
|---------|------|-------|
| 0. Welcome + Language | 30 sec | 0.1-0.2 |
| 1. Your Goals | 5 min | 1.1-1.4 |
| 2. Optional Context | 15 sec | 2.1 |
| 3. Create Workspace | 2 min | 3.1-3.4 |
| 4. Understanding Memory | 2 min | 4.1-4.4 |
| 5. Close-Session Habit | 2 min | 5.1-5.4 |
| 6. What's Next | 1 min | 6.1-6.2 |
| **TOTAL** | **8-10 min** | **16 tasks** |

---

**Status**: Ready for Execution
**Date**: 2025-11-04
