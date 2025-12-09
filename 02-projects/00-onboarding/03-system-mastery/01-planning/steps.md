# Tasks: System Mastery (Project 03)

**Project ID**: 03-system-mastery
**Onboarding Step**: 4 of 4 (FINAL!)
**Estimated Time**: 16-18 minutes (Expanded with Expert Collaboration Patterns)

---

## Context Loading

**CRITICAL**: Load EVERYTHING for full setup analysis!

```bash
python nexus-loader.py --project 03
```

**This loads**:
- goals.md (role, goals, motivation)
- roadmap.md (milestones, priorities)
- project-map.md (projects tracking, onboarding state)
- Skills metadata (from 03-skills/)
- Workspace structure (04-workspace/)

**Extract for Analysis**:
- USER_GOAL
- USER_DOMAIN
- FIRST_PROJECT (name and status)
- FIRST_SKILL (name)
- WORKSPACE_FOLDERS (list)
- PROJECT_YAML (from first project)

---

## Section 1: Welcome + Load Full Context (1 min)

- [ ] **Task 1.1**: Welcome to final onboarding
  - Say: "Welcome to Project 03—the final onboarding session!"
  - Say: "Let me load YOUR complete setup for review..."
  - Execute: Load all context
  - Time: 30 seconds

- [ ] **Task 1.2**: Summarize what was found
  - Say: "Here's what I found:"
  - List: "Goals: [USER_GOAL]"
  - List: "Workspace: [WORKSPACE_FOLDERS]"
  - List: "Projects: [FIRST_PROJECT]"
  - List: "Skills: [FIRST_SKILL]"
  - Say: "Today we'll review YOUR setup and confirm you're ready for independent use"
  - Time: 30 seconds

---

## Section 2: Pitfall #1 - Projects Instead of Skills (2 min)

- [ ] **Task 2.1**: Analyze user's projects
  - Review: FIRST_PROJECT name and description
  - Check: Does it seem like it should be a skill? (repeatable workflow vs temporal work)
  - Time: 15 seconds (internal)

- [ ] **Task 2.2**: Teach pitfall with THEIR example
  - **If found issue**:
    - Say: "I notice your [FIRST_PROJECT] seems like it might repeat..."
    - Explain: Why it might be better as a skill
    - Suggest: How to restructure
  - **If no issue**:
    - Say: "Your [FIRST_PROJECT] is clearly a Project—it has a defined endpoint"
    - Say: "Great job distinguishing! But watch for this pitfall:"
    - Explain: "Some users create projects like 'weekly-report-week-1', 'weekly-report-week-2'..."
    - Explain: "That's repeating work → Should be ONE skill called 'weekly-report'"
  - Time: 2 minutes

---

## Section 3: Pitfall #2 - Skipping Close-Session (1 min)

- [ ] **Task 3.1**: Review close-session habit
  - Say: "You successfully closed all 3 onboarding sessions ✅"
  - Say: "This is THE critical habit—keep it up!"
  - Reinforce: "Every session should end with 'done'"
  - Time: 1 minute

---

## Section 4: Pitfall #3 - Over-Organizing Upfront (2 min)

- [ ] **Task 4.1**: Analyze workspace structure
  - Count: WORKSPACE_FOLDERS
  - Time: 5 seconds (internal)

- [ ] **Task 4.2**: Teach pitfall with THEIR example
  - **If ≤3 folders**:
    - Say: "Your workspace has [X] folders: [list them]"
    - Say: "Perfect! You followed just-in-time design"
    - Say: "You created only what YOU need for [THEIR_GOAL]"
  - **If 4-5 folders**:
    - Say: "Your workspace has [X] folders—that's okay!"
    - Say: "Just remember: Add folders as work emerges, not before"
  - **If >5 folders**:
    - Say: "I notice you created [X] folders: [list them]"
    - Say: "That's more than I recommended (≤3)"
    - Ask: "Are they all actively used? Or can some be consolidated?"
    - Explain: "Structure should emerge from work, not precede it"
  - Time: 2 minutes

---



## 🤖 PART B: AI BEHAVIORAL AWARENESS (4-5 min)

---

## Section 5: Introduction to AI Behavioral Patterns (1 min)

- [ ] **Task 5.1**: Introduce AI behavioral awareness
  - Say: "Great! You know the system pitfalls. Now let's talk about AI pitfalls"
  - Say: "AI assistants have predictable failure patterns—knowing them makes you 10x more effective"
  - Say: "I'm going to teach you the top 2 patterns, backed by research from 65+ real AI sessions"
  - Say: "You'll learn to recognize when I'm making these mistakes so you can correct me"
  - Time: 1 minute

- [ ] **Task 5.5**: Workspace map deep dive (NEW - CRITICAL UNDERSTANDING)
  - Say: "Before we continue, let's talk about workspace-map.md—it's more important than you might think."
  - Step 1: Show their current workspace-map
    - Execute: Read 04-workspace/workspace-map.md
    - Display: Current contents to user
  - Step 2: Explain the importance
    - Say: "This file does TWO critical things:"
    - Say: "1. **It helps ME** - When I load your workspace, I read this map to understand your structure"
    - Say: "2. **It helps YOU** - It's your navigation guide when you come back after weeks away"
  - Step 3: Demonstrate staleness impact
    - Say: "Here's what happens when workspace-map gets stale:"
    - Say: "• I suggest putting files in folders that don't exist anymore"
    - Say: "• I can't find your actual folders because they're not documented"
    - Say: "• You waste time explaining your structure every session"
  - Step 4: Maintenance instructions
    - Say: "How to keep it current:"
    - Say: "• The close-session skill now AUTO-CHECKS for mismatches"
    - Say: "• If folders added/removed, I'll prompt you to update the map"
    - Say: "• Takes 30 seconds, saves hours of confusion"
  - Step 5: Show real example
    - Say: "Let me check yours right now..."
    - Execute: List folders in 04-workspace/
    - Compare: Against workspace-map.md
    - Report: "✓ Your map is accurate" OR "⚠ Found [X] mismatches"
  - Time: 2 minutes

---

## Section 6: AI Pattern #1 - False Progress Claims (2 min)

- [ ] **Task 6.1**: Teach False Progress pattern
  - Say: "**Pattern #1: False Progress Claims** (19% of AI failures)"
  - Explain: "AI claims completion without actual proof"
  - Example: "'✅ Complete! All tasks done!' without showing evidence"
  - Detection: "Ask: 'Show me the evidence' or 'What files did you create?'"
  - Example using THEIR project:
    - ❌ WRONG: "Your [THEIR_PROJECT] is 100% complete!"
    - ✅ RIGHT: "Your [THEIR_PROJECT] is complete. Evidence: [lists files created, shows outputs]"
  - Time: 1 minute 30 seconds

- [ ] **Task 6.2**: Practice detection exercise
  - Say: "Practice scenario:"
  - Present:
    - "Scenario: You ask if [THEIR_PROJECT] is ready"
    - "I respond: 'Yes, everything is done! Project is complete!'"
    - Ask: "What should you ask me?"
  - Wait for user answer
  - Confirm correct responses: "Show me proof", "What files exist?", "What evidence validates this?"
  - Time: 30 seconds

---

## Section 7: AI Pattern #2 - Incomplete File Reading (1 min)

- [ ] **Task 7.1**: Teach Incomplete Reading pattern
  - Say: "**Pattern #2: Incomplete File Reading** (Critical directive violation)"
  - Explain: "AI reads only first 100-200 lines of 800-line files, misses critical content"
  - Example: "Reading workflow.md with limit parameter, missing entire architecture in later sections"
  - Detection: "Ask: 'Did you read the entire file?' or 'How many lines did you read?'"
  - Impact: "40% of integration failures come from incomplete file understanding"
  - Time: 1 minute

---

## Section 8: Quick Overview of Other Patterns (1 min)

- [ ] **Task 8.1**: Briefly introduce remaining patterns
  - Say: "A few more patterns to be aware of:"
  - **Complexity Bias** (16%): "AI over-engineers simple solutions—ask 'Can this be simpler?'"
  - **Basic Operations Failure** (21%): "AI makes mistakes with file paths, sequences—always verify filesystem matches claims"
  - Say: "You don't need to memorize all patterns. Just remember:"
    - "Always ask for proof"
    - "Verify files actually exist"
    - "Challenge complexity"
  - Time: 1 minute

---

## Section 9: AI Collaboration Best Practices Summary (1 min)

- [ ] **Task 9.1**: Summarize AI collaboration approach
  - Say: "Here's your AI collaboration toolkit:"
  - Key Questions to Ask:
    - "Show me the evidence/files"
    - "Did you read the complete file?"
    - "Can this be simpler?"
  - Say: "You're not questioning my competence—you're being an effective collaborator"
  - Say: "These questions help me catch my own mistakes"
  - Time: 1 minute

---

## 🤝 PART C: EXPERT COLLABORATION PATTERNS (3-4 min)
 
 ---
 
 ## Section 10: Introduction to Expert Mode (1 min)
 
 - [ ] **Task 10.1**: Introduce mode transition
   - Say: "Great! You now know how to catch AI mistakes (defensive skills)."
   - Say: "But there's another level: Using AI as a PARTNER (offensive skills)."
   - Say: "After onboarding, our interaction changes:"
   - Say: "• **Before**: I guide and teach (onboarding mode)"
   - Say: "• **After**: I challenge and collaborate (expert mode)"
   - Say: "Let me show you 3 patterns you'll experience..."
   - Time: 1 minute
 
 ---
 
 ## Section 11: Pattern #1 - "Yes, And..." Collaboration (1 min)
 
 - [ ] **Task 11.1**: Teach "Yes, And..." pattern
   - Say: "**Pattern #1: 'Yes, And...' Collaboration**"
   - Explain: "I don't just execute—I add proactive value."
   - Example from THEIR work:
     - "You: 'Create skill for [FIRST_SKILL]'"
     - "Me: 'Done. Skill created. **AND** I scanned your [WORKSPACE_FOLDERS]—linked relevant files.'"
   - Say: "Your Role: Evaluate my 'AND' additions. Say yes/no/modify."
   - Time: 1 minute
 
 ---
 
 ## Section 12: Pattern #2 - Intelligent Friction (1 min)
 
 - [ ] **Task 12.1**: Teach Intelligent Friction pattern
   - Say: "**Pattern #2: Intelligent Friction**"
   - Explain: "I stop momentum to force deeper thinking on critical decisions."
   - Example:
     - "You: 'Create project to [USER_GOAL]'"
     - "Me: 'Before we create this, let me challenge you: How will you measure success?'"
   - Say: "Why this helps: Prevents costly rework. Thinking hard now saves hours later."
   - Say: "Your Role: When I challenge, answer the questions. They surface blind spots."
   - Time: 1 minute
 
 ---
 
 ## Section 13: Pattern #3 - Proactive Context Scanning (1 min)
 
 - [ ] **Task 13.1**: Teach Proactive Scanning pattern
   - Say: "**Pattern #3: Proactive Context Scanning**"
   - Explain: "I automatically scan your workspace/codebase BEFORE you ask."
   - Example:
     - "You: 'Create project for [USER_DOMAIN]'"
     - "Me: 'Done. I found existing code in [WORKSPACE_FOLDERS] and linked it.'"
   - Say: "Your Role: Review my context findings. Correct if I linked wrong things."
   - Time: 1 minute
 
 ---
## Section 4: Pitfall #3 - Over-Organizing Upfront (2 min)

- [ ] **Task 4.1**: Analyze workspace structure
  - Count: WORKSPACE_FOLDERS
  - Time: 5 seconds (internal)

- [ ] **Task 4.2**: Teach pitfall with THEIR example
  - **If ≤3 folders**:
    - Say: "Your workspace has [X] folders: [list them]"
    - Say: "Perfect! You followed just-in-time design"
    - Say: "You created only what YOU need for [THEIR_GOAL]"
  - **If 4-5 folders**:
    - Say: "Your workspace has [X] folders—that's okay!"
    - Say: "Just remember: Add folders as work emerges, not before"
  - **If >5 folders**:
    - Say: "I notice you created [X] folders: [list them]"
    - Say: "That's more than I recommended (≤3)"
    - Ask: "Are they all actively used? Or can some be consolidated?"
    - Explain: "Structure should emerge from work, not precede it"
  - Time: 2 minutes

---



## 🤖 PART B: AI BEHAVIORAL AWARENESS (4-5 min)

---

## Section 5: Introduction to AI Behavioral Patterns (1 min)

- [ ] **Task 5.1**: Introduce AI behavioral awareness
  - Say: "Great! You know the system pitfalls. Now let's talk about AI pitfalls"
  - Say: "AI assistants have predictable failure patterns—knowing them makes you 10x more effective"
  - Say: "I'm going to teach you the top 2 patterns, backed by research from 65+ real AI sessions"
  - Say: "You'll learn to recognize when I'm making these mistakes so you can correct me"
  - Time: 1 minute

- [ ] **Task 5.5**: Workspace map deep dive (NEW - CRITICAL UNDERSTANDING)
  - Say: "Before we continue, let's talk about workspace-map.md—it's more important than you might think."
  - Step 1: Show their current workspace-map
    - Execute: Read 04-workspace/workspace-map.md
    - Display: Current contents to user
  - Step 2: Explain the importance
    - Say: "This file does TWO critical things:"
    - Say: "1. **It helps ME** - When I load your workspace, I read this map to understand your structure"
    - Say: "2. **It helps YOU** - It's your navigation guide when you come back after weeks away"
  - Step 3: Demonstrate staleness impact
    - Say: "Here's what happens when workspace-map gets stale:"
    - Say: "• I suggest putting files in folders that don't exist anymore"
    - Say: "• I can't find your actual folders because they're not documented"
    - Say: "• You waste time explaining your structure every session"
  - Step 4: Maintenance instructions
    - Say: "How to keep it current:"
    - Say: "• The close-session skill now AUTO-CHECKS for mismatches"
    - Say: "• If folders added/removed, I'll prompt you to update the map"
    - Say: "• Takes 30 seconds, saves hours of confusion"
  - Step 5: Show real example
    - Say: "Let me check yours right now..."
    - Execute: List folders in 04-workspace/
    - Compare: Against workspace-map.md
    - Report: "✓ Your map is accurate" OR "⚠ Found [X] mismatches"
  - Time: 2 minutes

---

## Section 6: AI Pattern #1 - False Progress Claims (2 min)

- [ ] **Task 6.1**: Teach False Progress pattern
  - Say: "**Pattern #1: False Progress Claims** (19% of AI failures)"
  - Explain: "AI claims completion without actual proof"
  - Example: "'✅ Complete! All tasks done!' without showing evidence"
  - Detection: "Ask: 'Show me the evidence' or 'What files did you create?'"
  - Example using THEIR project:
    - ❌ WRONG: "Your [THEIR_PROJECT] is 100% complete!"
    - ✅ RIGHT: "Your [THEIR_PROJECT] is complete. Evidence: [lists files created, shows outputs]"
  - Time: 1 minute 30 seconds

- [ ] **Task 6.2**: Practice detection exercise
  - Say: "Practice scenario:"
  - Present:
    - "Scenario: You ask if [THEIR_PROJECT] is ready"
    - "I respond: 'Yes, everything is done! Project is complete!'"
    - Ask: "What should you ask me?"
  - Wait for user answer
  - Confirm correct responses: "Show me proof", "What files exist?", "What evidence validates this?"
  - Time: 30 seconds

---

## Section 7: AI Pattern #2 - Incomplete File Reading (1 min)

- [ ] **Task 7.1**: Teach Incomplete Reading pattern
  - Say: "**Pattern #2: Incomplete File Reading** (Critical directive violation)"
  - Explain: "AI reads only first 100-200 lines of 800-line files, misses critical content"
  - Example: "Reading workflow.md with limit parameter, missing entire architecture in later sections"
  - Detection: "Ask: 'Did you read the entire file?' or 'How many lines did you read?'"
  - Impact: "40% of integration failures come from incomplete file understanding"
  - Time: 1 minute

---

## Section 8: Quick Overview of Other Patterns (1 min)

- [ ] **Task 8.1**: Briefly introduce remaining patterns
  - Say: "A few more patterns to be aware of:"
  - **Complexity Bias** (16%): "AI over-engineers simple solutions—ask 'Can this be simpler?'"
  - **Basic Operations Failure** (21%): "AI makes mistakes with file paths, sequences—always verify filesystem matches claims"
  - Say: "You don't need to memorize all patterns. Just remember:"
    - "Always ask for proof"
    - "Verify files actually exist"
    - "Challenge complexity"
  - Time: 1 minute

---

## Section 9: AI Collaboration Best Practices Summary (1 min)

- [ ] **Task 9.1**: Summarize AI collaboration approach
  - Say: "Here's your AI collaboration toolkit:"
  - Key Questions to Ask:
    - "Show me the evidence/files"
    - "Did you read the complete file?"
    - "Can this be simpler?"
  - Say: "You're not questioning my competence—you're being an effective collaborator"
  - Say: "These questions help me catch my own mistakes"
  - Time: 1 minute

---

## 🤝 PART C: EXPERT COLLABORATION PATTERNS (3-4 min)
 
 ---
 
 ## Section 10: Introduction to Expert Mode (1 min)
 
 - [ ] **Task 10.1**: Introduce mode transition
   - Say: "Great! You now know how to catch AI mistakes (defensive skills)."
   - Say: "But there's another level: Using AI as a PARTNER (offensive skills)."
   - Say: "After onboarding, our interaction changes:"
   - Say: "• **Before**: I guide and teach (onboarding mode)"
   - Say: "• **After**: I challenge and collaborate (expert mode)"
   - Say: "Let me show you 3 patterns you'll experience..."
   - Time: 1 minute
 
 ---
 
 ## Section 11: Pattern #1 - "Yes, And..." Collaboration (1 min)
 
 - [ ] **Task 11.1**: Teach "Yes, And..." pattern
   - Say: "**Pattern #1: 'Yes, And...' Collaboration**"
   - Explain: "I don't just execute—I add proactive value."
   - Example from THEIR work:
     - "You: 'Create skill for [FIRST_SKILL]'"
     - "Me: 'Done. Skill created. **AND** I scanned your [WORKSPACE_FOLDERS]—linked relevant files.'"
   - Say: "Your Role: Evaluate my 'AND' additions. Say yes/no/modify."
   - Time: 1 minute
 
 ---
 
 ## Section 12: Pattern #2 - Intelligent Friction (1 min)
 
 - [ ] **Task 12.1**: Teach Intelligent Friction pattern
   - Say: "**Pattern #2: Intelligent Friction**"
   - Explain: "I stop momentum to force deeper thinking on critical decisions."
   - Example:
     - "You: 'Create project to [USER_GOAL]'"
     - "Me: 'Before we create this, let me challenge you: How will you measure success?'"
   - Say: "Why this helps: Prevents costly rework. Thinking hard now saves hours later."
   - Say: "Your Role: When I challenge, answer the questions. They surface blind spots."
   - Time: 1 minute
 
 ---
 
 ## Section 13: Pattern #3 - Proactive Context Scanning (1 min)
 
 - [ ] **Task 13.1**: Teach Proactive Scanning pattern
   - Say: "**Pattern #3: Proactive Context Scanning**"
   - Explain: "I automatically scan your workspace/codebase BEFORE you ask."
   - Example:
     - "You: 'Create project for [USER_DOMAIN]'"
     - "Me: 'Done. I found existing code in [WORKSPACE_FOLDERS] and linked it.'"
   - Say: "Your Role: Review my context findings. Correct if I linked wrong things."
   - Time: 1 minute
 
 ---
 
 ## 📋 PART D: MASTERY CONFIRMATION (5 min)

---

## Section 14: Decision Framework Practice (3 min)

- [ ] **Task 14.1**: Present 3 scenarios from THEIR domain
  - Say: "Let's practice the Project vs Skill framework one last time"
  - Say: "3 scenarios from YOUR [USER_DOMAIN] work. Project or Skill?"
  - Time: 30 seconds

- [ ] **Task 14.2**: Scenario 1
  - Present: Scenario from their domain
  - Ask: "Project or Skill?"
  - Wait for answer
  - Explain: Why correct/incorrect
  - Time: 45 seconds

- [ ] **Task 14.3**: Scenario 2
  - [Same pattern]
  - Time: 45 seconds

- [ ] **Task 14.4**: Scenario 3 (tricky)
  - [Same pattern]
  - Time: 45 seconds

- [ ] **Task 14.5**: Assess mastery
  - If 3/3: "Perfect! You've mastered the distinction"
  - If 2/3: "Almost there! Remember: [clarify]"
  - Success: User demonstrates solid understanding
  - Time: 15 seconds

---

## Section 15: Best Practices Using THEIR Setup (2 min)

- [ ] **Task 15.1**: Highlight what they did well
  - Say: "Let's review what YOU did well:"
  - Workspace: "Your [folders] workspace shows good just-in-time design"
  - Project: "Your [FIRST_PROJECT] connects directly to your goal: '[USER_GOAL]'"
  - Alignment: "I see clear alignment between your goal, workspace, and project"
  - Patterns: "You created [X] projects and [Y] skills—good balance!"
  - Time: 2 minutes

---

## Section 16: Two-Layer Mastery Confirmation (3 min)

- [ ] **Task 16.1**: Review system mastery checklist (Layer 1)
  - Say: "Let's confirm you're ready for independent use:"
  - Say: "**Layer 1: System Mastery**"
  - Checklist:
    - "✅ Can explain Projects vs Skills?"
    - "✅ Uses close-session consistently?"
  - Confirm: User agrees with all items
  - Time: 1 minute

- [ ] **Task 16.2**: Review AI collaboration mastery (Layer 2)
  - Say: "**Layer 2: AI Collaboration Mastery**"
  - Checklist:
    - "✅ Can detect False Progress claims?"
    - "✅ Knows when to ask for proof?"
    - "✅ Understands file reading completeness?"
  - Confirm: User demonstrates awareness
  - Time: 1 minute

- [ ] **Task 16.3**: Declare two-layer mastery
  - Say: "✅ TWO-LAYER MASTERY CONFIRMED!"
  - Say: "You understand BOTH the system AND how to collaborate effectively with AI"
  - Say: "You've completed all 4 onboarding projects"
  - Say: "Your Nexus system is now operational!"
  - Time: 30 seconds

- [ ] **Task 16.4**: Explain what's next
  - Say: "From now on:"
  - Say: "Create projects for temporal work (use create-project skill)"
  - Say: "Create skills for repeatable workflows (use create-skill skill)"
  - Say: "Remember to verify my work using the detection questions"
  - Say: "Your system will remember everything—just start working!"
  - Time: 30 seconds

---

## Section 18: Your New Normal - The Full Menu (4 min) (NEW - GRADUATION)

- [ ] **Task 18.1**: Frame the transition
  - Say: "Congratulations! You've completed all 4 onboarding sessions."
  - Say: "You're now graduating from guided mode to independent mode."
  - Say: "That means: No more structured projects. YOU decide what to work on next."
  - Say: "To help you navigate, let me show you the FULL Nexus menu."
  - Time: 30 seconds

- [ ] **Task 18.2**: Display complete menu
  - Show full menu with all sections:
    ```
    ╔════════════════════════════════════════════════════╗
    ║             NEXUS SYSTEM MENU                      ║
    ╠════════════════════════════════════════════════════╣
    ║                                                    ║
    ║  📋 MEMORY & NAVIGATION                            ║
    ║    • Show menu                                     ║
    ║    • Load goals                                    ║
    ║    • Load project [name/ID]                        ║
    ║    • Load skill [name]                             ║
    ║    • Show workspace                                ║
    ║                                                    ║
    ║  🚀 PROJECT MANAGEMENT                             ║
    ║    • Create project                                ║
    ║    • List projects                                 ║
    ║    • Work on [project-name]                        ║
    ║    • Archive project [name]                        ║
    ║                                                    ║
    ║  🔧 SKILL MANAGEMENT                               ║
    ║    • Create skill                                  ║
    ║    • List skills                                   ║
    ║    • Use [skill-name]                              ║
    ║                                                    ║
    ║  💾 SESSION MANAGEMENT                             ║
    ║    • Done / Close session                          ║
    ║    • Validate system                               ║
    ║                                                    ║
    ║  📂 WORKSPACE                                      ║
    ║    • Organize workspace                            ║
    ║    • Validate workspace-map                        ║
    ║    • Clean temp files                              ║
    ║                                                    ║
    ╚════════════════════════════════════════════════════╝
    ```
  - Time: 30 seconds

- [ ] **Task 18.3**: Explain menu sections
  - **Memory & Navigation**: "These load context. Start here each session."
  - **Project Management**: "Create and manage finite work (things that END)"
  - **Skill Management**: "Create and use repeatable workflows (things that REPEAT)"
  - **Session Management**: "Always end with 'done' to save progress"
  - **Workspace**: "Organize your 04-workspace/ folder"
  - Time: 2 minutes

- [ ] **Task 18.4**: Practice using the menu
  - Say: "Let's practice. Try asking me to:"
  - Say: "• 'Show projects' - See all your projects"
  - Say: "• 'Load goals' - Refresh your goals in context"
  - Say: "• 'Create project' - Start something new"
  - Wait for user to try one command
  - Execute the command they request
  - Say: "Perfect! You'll get comfortable with these over time."
  - Time: 1 minute

**Section Time**: 4 minutes
**Value Delivered**: ✅ Full system navigation confidence

---

## Section 17: Final Close-Session (1 min)

- [ ] **Task 17.1**: Close final onboarding session
  - Say: "Ready to close the final onboarding session?"
  - Say: "When you say 'done', onboarding will be marked complete"
  - Wait for user to say "done"
  - Execute close-session
  - Time: 30 seconds

- [ ] **Task 17.2**: Celebrate completion!
  - Say: "🎉 ONBOARDING COMPLETE! 🎉"
  - Say: "You're now ready for independent use—with AI awareness superpowers!"
  - Say: "Next session: Real work begins. I'll be here to help!"
  - Say: "See you soon! 👋"
  - Time: 30 seconds

---

## Completion Checklist

**System Mastery (Layer 1)**:
- [ ] Full context loaded (goals, roadmap, projects, skills, workspace)
- [ ] 3 system pitfalls reviewed using user's actual setup
- [ ] Decision framework practiced (3/3 scenarios)
- [ ] Best practices highlighted with user's examples

**AI Collaboration Mastery (Layer 2 - NEW)**:
- [ ] False Progress pattern taught with exercises
- [ ] Incomplete File Reading pattern explained
- [ ] Complexity Bias and Basic Operations overview provided
- [ ] AI collaboration toolkit summarized

**Graduation Requirements**:
- [ ] Two-layer mastery checklist confirmed
- [ ] User understands what to do next
- [ ] User knows how to verify AI work
- [ ] close-session executed
- [ ] Onboarding marked COMPLETE in project-map.md
- [ ] System switched to operational mode

---

## Time Breakdown

| Section | Time | Tasks |
|---------|------|-------|
| **PART A: SYSTEM REVIEW** | **4 min** | |
| 1. Welcome + Load | 1 min | 1.1-1.2 |
| 2. Pitfall #1 (Projects vs Skills) | 2 min | 2.1-2.2 |
| 3. Pitfall #2 (Close-session) | 1 min | 3.1 |
| 4. Pitfall #3 (Over-organizing) | 2 min | 4.1-4.2 |
| **PART B: AI BEHAVIORAL AWARENESS** | **4-5 min** | |
| 5. Introduction to AI patterns | 1 min | 5.1 |
| 6. False Progress + exercise | 2 min | 6.1-6.2 |
| 7. Incomplete File Reading | 1 min | 7.1 |
| 8. Other patterns overview | 1 min | 8.1 |
| 9. AI Collaboration summary | 1 min | 9.1 |
| **PART C: EXPERT COLLABORATION PATTERNS** | **3-4 min** | |
| 10. Intro to Expert Mode | 1 min | 10.1 |
| 11. "Yes, And..." Pattern | 1 min | 11.1 |
| 12. Intelligent Friction | 1 min | 12.1 |
| 13. Proactive Scanning | 1 min | 13.1 |
| **PART D: MASTERY CONFIRMATION** | **5 min** | |
| 14. Framework Practice | 3 min | 14.1-14.5 |
| 15. Best Practices Review | 2 min | 15.1 |
| 16. Two-Layer Mastery | 3 min | 16.1-16.4 |
| 17. Final Close-Session | 1 min | 17.1-17.2 |
| **TOTAL** | **16-18 min** | **25 tasks** |

---

**Status**: Ready for Execution
**This is the FINAL onboarding project - Enhanced with AI Behavioral Awareness!**
**Research-Backed**: Patterns from 65+ real AI session learnings
