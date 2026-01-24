# Complete Onboarding Specification - ALL DETAILS

> **Build**: 04-improved-onboarding-design
> **Date**: 2026-01-24
> **Purpose**: COMPLETE specification of all decisions, code, copy, flows - EVERYTHING

---

## 1. HEROIC INTRO - COMPLETE COPY

```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         Welcome to Nexus
         (Powered by Claude Code)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ChatGPT gives you answers.
Nexus and Claude Code build you SYSTEMS.

Here's what people have actually built:

  🔬 "MedScan" - Medical Research Platform
     → My dad connected open-source scientific databases and MRI
       analysis software in one evening
     → We found patterns radiologists missed

  💼 "JobTracker" - Application Automation
     → My girlfriend built a job search system that auto-tracks
       positions, extracts requirements, fills CVs with her stories
     → Her interview rate went up 4x

  🏃 "FitPlan" - Personal Performance Lab
     → She connected her smartwatch (10 minutes, not technical)
     → Gets personalized marathon training plans
     → Also analyzes her financial data

  📝 "ContentEngine" - LinkedIn Production System
     → AI interviews you to collect your stories
     → Plans posting schedule across channels
     → Maintains your voice, 10x your output

  🗺️ "ProductOS" - Strategy & Roadmap System
     → Our PM uses it for product roadmaps
     → Connects research, feedback, and vision
     → Tracks dependencies and releases

Used throughout our entire company. People dropped ChatGPT, Claude,
even when they were required to use those tools.

Why? Because this COMPOUNDS.

You build it once. It works forever.
Every session makes YOUR system smarter.

Ready?
```

**Location**: `.claude/hooks/templates/startup_first_run.md` (lines 1-45)

**Design Notes**:
- Real examples only (no made-up stories)
- Each system has a NAME (MedScan, JobTracker, etc.)
- Personality and realness ("my dad", "my girlfriend")
- Icons for visual scanning (🔬💼🏃📝🗺️)
- "Welcome to Nexus (Powered by Claude Code)" - not "NEW ERA of AI"
- Emphasis on COMPOUNDS (key value prop)

---

## 2. LANGUAGE SELECTION

**Display**:
```
What language do you want to work in?

1. English
2. Deutsch
3. Español
4. Français
5. Italiano
6. 日本語
7. 中文

(All future sessions will use this language)

Type the number (1-7):
```

**State Update**:
```yaml
onboarding:
  language_preference: "en" | "de" | "es" | "fr" | "it" | "ja" | "zh"
```

**Save to**: `01-memory/user-config.yaml`

**Location**: `.claude/hooks/templates/startup_first_run.md` (after heroic intro)

---

## 3. FORK DECISION

**Display**:
```
How do you want to start?

1. Show me how Nexus works (~7 min guided tour)
   → Learn the system, then setup in next session

2. Set up my system now (skip tour, dive in)
   → Quick setup, learn as you go

Choose 1 or 2:
```

**State Update**:
```yaml
onboarding:
  chosen_path: "tour" | "direct"
```

**Routing**:
```python
if user_choice == "1":
    onboarding.chosen_path = "tour"
    onboarding.status = "tour_in_progress"
    load_skill("how-nexus-works")

elif user_choice == "2":
    onboarding.chosen_path = "direct"
    onboarding.status = "setup_in_progress"
    load_skill("setup-system")
```

---

## 4. HOW-NEXUS-WORKS SKILL (Complete Spec)

**File**: `00-system/skills/learning/how-nexus-works/SKILL.md`

**Metadata**:
```yaml
name: how-nexus-works
description: "Learn how Nexus works - the system tour. ~7 min."
onboarding: true
priority: critical
duration: "7 min"
```

**Content Outline** (7 parts):

### Part 1: Two Work Modes (2 min)
```markdown
Nexus has TWO modes of operation:

**BUILD Mode** 🔨
- Create something NEW
- Has a clear END (when it's done, it's done)
- Example: Build a sales playbook, create a proposal generator
- You PLAN it, then you BUILD it

**WORK Mode** 💼
- USE what you've built
- REPEATABLE (use it again and again)
- Example: "proposal [client]" → generates proposal using your playbook

The distinction:
- If it ENDS → BUILD
- If it REPEATS → WORK (via skills)
```

### Part 2: The Four Pillars (2 min)
```markdown
Your Nexus system has 4 core components:

📁 **01-memory/** - Your system's brain
   - goals.md: What you want to achieve
   - Loaded EVERY session (AI never forgets you)

📁 **02-builds/** - Your workshop
   - Projects with clear beginning and end
   - Each build: 4 documents (overview, discovery, plan, steps)

📁 **03-skills/** - Your AI workforce
   - Reusable automations
   - Trigger: "follow-up [client]" → skill runs

📁 **04-workspace/** - Your files
   - Organized by YOUR structure
   - AI navigates via workspace-map.md
```

### Part 3: The Core Innovation (1 min)
```markdown
Three things make Nexus different:

1. **Collaborative Planning**
   AI doesn't just execute vague ideas
   It interviews YOU to extract what you REALLY need

2. **AI Navigates YOUR Structure**
   You design the folders
   AI learns the map, operates within YOUR system

3. **Cross-Session Continuity**
   While building, AI NEVER forgets
   Pick up EXACTLY where you left off
```

### Part 4: Session Boundaries (1 min)
```markdown
IMPORTANT: Clean session boundaries matter.

Good practice:
- 1 session = 1 topic
- Planning session → close → New session → Execution
- Each session has clear focus

Why?
- Better AI performance (focused context)
- Cleaner summaries
- Easier to resume later

How:
- When you finish a topic, open a NEW chat/session
- Don't mix multiple topics in one session
```

### Part 5: The Build Workflow (1 min)
```markdown
When you want to BUILD something:

Session 1 (PLANNING):
- Say "build [X]" or "create [Y]"
- AI loads plan-build skill
- You fill 4 documents TOGETHER
- Mental models applied (why this matters)
- End session (planning complete)

Session 2 (EXECUTION):
- Say "continue [build name]"
- AI loads execute-build skill
- AI executes the plan YOU approved
- You review outputs
- End session (build complete)

Why separate sessions?
- Planning = thinking (needs focus)
- Execution = doing (different mindset)
- Clean context = better results
```

**End of Skill Message**:
```
SESSION COMPLETE ✓

You now understand how Nexus works!

Your progress saves automatically.

IMPORTANT: Clean session boundaries matter in Nexus.
Each session = one focus.

This session: System learning (DONE)
Next session: Set up your goals and build your first system

→ Open a NEW chat/session when ready to continue
```

**State Update**:
```yaml
onboarding:
  status: "tour_complete"
  in_progress_skill: null

learning_tracker:
  completed:
    how_nexus_works: true
```

---

## 5. SETUP-SYSTEM SKILL (Complete Specification)

**File**: `00-system/skills/learning/setup-system/SKILL.md`

**Metadata**:
```yaml
name: setup-system
description: "Set up your Nexus system: goals, roadmap, workspace, projects. 10-15 min."
onboarding: true
priority: critical
duration: "10-15 min"
cross_session_continuity: true
```

**Pre-Execution**:
```python
# Create onboarding project automatically
def initialize_setup_system():
    # Create onboarding project
    create_folder("02-builds/00-onboarding-session/01-planning/")
    create_folder("02-builds/00-onboarding-session/02-resources/")
    create_folder("02-builds/00-onboarding-session/03-working/")
    create_folder("02-builds/00-onboarding-session/04-outputs/")

    # Create overview
    write_file("02-builds/00-onboarding-session/01-planning/01-overview.md", """
---
id: 00-onboarding-session
name: Onboarding Session
type: setup
priority: critical
status: IN_PROGRESS
created: {today}
---

# Onboarding Session

## Purpose

Initialize your Nexus system with:
- Your goals and context
- Your roadmap (what you'll build)
- Your workspace structure
- Initial project scaffolds

## Process

1. Context upload (optional)
2. Define goals
3. Generate roadmap
4. Create workspace
5. Initiate projects
""")

    # Create steps tracker
    write_file("02-builds/00-onboarding-session/01-planning/04-steps.md", """
# Onboarding Steps

## Progress

- [ ] Step 1: Context upload
- [ ] Step 2: Goals defined
- [ ] Step 3: Roadmap created
- [ ] Step 4: Workspace structured
- [ ] Step 5: Projects initiated
- [ ] Step 6: Everything saved
- [ ] Step 7: Session ended
""")

    # Symlink input folder
    symlink(
        source="04-workspace/input/",
        target="02-builds/00-onboarding-session/03-working/input/"
    )

    # Set active build
    set_active_build("00-onboarding-session")
```

### STEP 1: Context Upload (Optional, 3-5 min if files)

**Display**:
```
STEP 1/7: Context Upload (Optional)

Want to upload files for me to learn about you?
(Documents, code, data, spreadsheets - anything relevant)

You can:
1. Upload files now
2. Skip this step

If you upload files, I'll analyze them to understand:
- What you work on
- Potential systems to build
- Integration opportunities
- How to organize your workspace

Choose 1 or 2:
```

**If user chooses 1 (upload)**:
```
Great! Upload your files to: 04-workspace/input/

You can drag and drop multiple files.
When you're done, let me know and I'll analyze them.

(This might take 1-2 minutes depending on file count)
```

**SubAgent Analysis Triggered**:
```python
def analyze_user_files_detailed():
    # Step 1: Scan input directory
    input_dir = Path("04-workspace/input/")
    files = list(input_dir.glob("**/*"))
    files = [f for f in files if f.is_file()]

    if not files:
        return None

    # Step 2: Calculate sizes and check for large files
    processed_files = []
    for file in files:
        size_kb = file.stat().st_size / 1024

        if size_kb > 2000:  # >2MB = context risk
            # Split into chunks
            chunks = split_file_into_chunks(
                file,
                max_kb=1500,
                overlap_lines=50  # preserve context
            )
            processed_files.extend(chunks)
        else:
            processed_files.append({
                "path": str(file),
                "size_kb": size_kb,
                "is_chunk": False
            })

    # Step 3: Calculate total KB
    total_kb = sum(f["size_kb"] for f in processed_files)

    # Step 4: Thematic clustering by filename patterns
    clusters = {}
    for file in processed_files:
        filename = Path(file["path"]).name.lower()

        # Pattern matching
        if "client" in filename or "customer" in filename:
            theme = "clients"
        elif "sales" in filename or "proposal" in filename:
            theme = "sales"
        elif "research" in filename or "paper" in filename:
            theme = "research"
        elif "financial" in filename or "invoice" in filename:
            theme = "finance"
        elif "code" in filename or filename.endswith((".py", ".js", ".ts")):
            theme = "code"
        else:
            theme = "general"

        if theme not in clusters:
            clusters[theme] = []
        clusters[theme].append(file)

    # Step 5: Show clusters to user for confirmation
    print("I found files about:")
    for theme, files_in_theme in clusters.items():
        count = len(files_in_theme)
        total_kb_theme = sum(f["size_kb"] for f in files_in_theme)
        print(f"  - {theme}: {count} files ({total_kb_theme:.1f} KB)")

    user_confirms = ask_user("Does this clustering make sense? (yes/no/suggest different)")

    if user_confirms == "suggest different":
        # Ask user how to group
        clusters = ask_user_for_clustering(files)

    # Step 6: Calculate agent count (KB-based)
    if total_kb < 1000:
        agent_count = 1
    elif total_kb < 3000:
        agent_count = 2
    elif total_kb < 5000:
        agent_count = 3
    elif total_kb < 10000:
        agent_count = 5
    elif total_kb < 20000:
        agent_count = 8
    else:
        # Every 2.5MB = 1 agent
        agent_count = min(ceil(total_kb / 2500), 10)

    print(f"Analyzing with {agent_count} parallel agents...")

    # Step 7: Distribute files to agents
    # Balance KB + respect theme clusters
    agent_assignments = []
    target_kb_per_agent = total_kb / agent_count

    current_agent = {"files": [], "kb": 0, "themes": set()}

    for theme, files_in_theme in clusters.items():
        for file in files_in_theme:
            current_agent["files"].append(file)
            current_agent["kb"] += file["size_kb"]
            current_agent["themes"].add(theme)

            # If agent is full, start new one
            if current_agent["kb"] >= target_kb_per_agent and len(agent_assignments) < agent_count - 1:
                agent_assignments.append(current_agent)
                current_agent = {"files": [], "kb": 0, "themes": set()}

    # Add final agent
    if current_agent["files"]:
        agent_assignments.append(current_agent)

    # Step 8: Launch SubAgents in parallel
    subagent_prompt_path = "00-system/core/nexus/prompts/subagent-file-analysis.md"

    agents = []
    for i, assignment in enumerate(agent_assignments):
        agent = launch_subagent(
            prompt_file=subagent_prompt_path,
            files=[f["path"] for f in assignment["files"]],
            metadata={
                "agent_id": f"subagent-{i+1}",
                "total_kb": assignment["kb"],
                "themes": list(assignment["themes"])
            },
            run_in_background=False  # Wait for results
        )
        agents.append(agent)

    # Step 9: Wait for all agents (parallel execution)
    results = []
    for agent in agents:
        result = wait_for_agent(agent)
        results.append(result)

    # Step 10: Synthesize results
    unified = {
        "generated_at": datetime.now().isoformat(),
        "total_files": len(files),
        "total_kb": total_kb,
        "agents_used": len(results),
        "file_analyses": [],
        "professional_context": {},
        "integration_opportunities": [],
        "workspace_structure_suggestion": {}
    }

    # Combine all file analyses
    for result in results:
        unified["file_analyses"].extend(result["file_analyses"])

    # Merge professional contexts (take most detailed)
    all_roles = [r["professional_context"]["role"] for r in results if r["professional_context"].get("role")]
    if all_roles:
        unified["professional_context"]["role"] = max(all_roles, key=len)

    all_domains = [r["professional_context"]["domain"] for r in results if r["professional_context"].get("domain")]
    if all_domains:
        unified["professional_context"]["domain"] = max(all_domains, key=len)

    all_skills = []
    for r in results:
        all_skills.extend(r["professional_context"].get("skills", []))
    unified["professional_context"]["skills"] = list(set(all_skills))

    # Dedupe integration opportunities
    seen_integrations = set()
    for result in results:
        for integration in result["integration_opportunities"]:
            key = (integration["name"], integration["type"])
            if key not in seen_integrations:
                unified["integration_opportunities"].append(integration)
                seen_integrations.add(key)

    # Merge workspace suggestions
    all_folders = []
    for result in results:
        all_folders.extend(result["workspace_structure_suggestion"]["folders"])

    # Dedupe folders by path
    folder_map = {}
    for folder in all_folders:
        path = folder["path"]
        if path not in folder_map:
            folder_map[path] = folder
        else:
            # Merge subfolders
            existing_subfolders = set(folder_map[path].get("subfolders", []))
            new_subfolders = set(folder.get("subfolders", []))
            folder_map[path]["subfolders"] = list(existing_subfolders | new_subfolders)

    unified["workspace_structure_suggestion"]["folders"] = list(folder_map.values())

    # Step 11: Save to onboarding project
    save_path = "02-builds/00-onboarding-session/02-resources/file-analysis.json"
    write_file(save_path, json.dumps(unified, indent=2))

    # Also save human-readable summary
    summary_md = generate_summary_markdown(unified)
    write_file("02-builds/00-onboarding-session/02-resources/file-analysis-summary.md", summary_md)

    # Step 12: Update state
    update_config({
        "onboarding.setup_system_state.step_completed": 1,
        "onboarding.setup_system_state.files_uploaded": True,
        "onboarding.setup_system_state.file_analysis_done": True
    })

    return unified
```

**SubAgent Prompt File**: `00-system/core/nexus/prompts/subagent-file-analysis.md`

```markdown
# FILE ANALYSIS SUBAGENT

You are analyzing user files to understand their context, work patterns, and suggest system organization.

## INPUT

You will receive:
- List of file paths to analyze
- Total KB assigned to you
- Theme cluster (if applicable)

## YOUR TASK

1. Read and analyze each file
2. Extract key information
3. Detect integration opportunities
4. Suggest folder organization

## OUTPUT CONTRACT (JSON)

Return EXACTLY this JSON structure:

{
  "agent_id": "subagent-X",
  "files_analyzed": 8,
  "total_kb": 1250,

  "file_analyses": [
    {
      "filename": "client-acme-proposal.pdf",
      "path": "04-workspace/input/client-acme-proposal.pdf",
      "type": "document|spreadsheet|code|data|image",

      "summary_short": "One sentence describing the file",

      "summary_detailed": "2-4 sentences providing full understanding of content. Include: main purpose, key data points, important entities, structure, how it might be used. Be specific - mention actual values, names, amounts when relevant.",

      "theme": "clients|sales|research|finance|code|general",

      "detected_entities": [
        "Company names",
        "People names",
        "Dollar amounts",
        "Dates",
        "Technical terms",
        "Tools/systems mentioned"
      ],

      "suggested_folder": "clients/acme/"
    }
  ],

  "professional_context": {
    "role": "Best guess of user's role based on files, or null",
    "domain": "Industry/domain inferred from content, or null",
    "skills": ["skills evident from file content"]
  },

  "integration_opportunities": [
    {
      "name": "HubSpot CRM",
      "type": "CRM|Email|Calendar|Database|Analytics|Storage",
      "evidence": "Specific file and what you found (e.g., 'Found config/hubspot.json with API credentials')",
      "suggestion": "What to connect and why it would be useful"
    }
  ],

  "workspace_structure_suggestion": {
    "folders": [
      {
        "path": "clients/",
        "purpose": "Why this folder (based on file content)",
        "subfolders": ["acme/", "beta/"]
      }
    ]
  }
}

## IMPORTANT RULES

1. **summary_detailed** must be 2-4 sentences, NOT one sentence
2. Be SPECIFIC in summaries - mention actual data:
   - ✅ "Proposal for Acme Corp, $50k deal, 6-month timeline, includes Salesforce integration"
   - ❌ "A proposal document"
3. Detect integration opportunities aggressively:
   - Config files with API keys
   - Credential files
   - References to external tools
4. Respect privacy:
   - Don't expose passwords/API keys in summaries
   - Summarize sensitive data generically
5. Theme must be ONE of: clients, sales, research, finance, code, general
6. suggested_folder should match theme structure

## EXAMPLES

### Good summary_detailed:
"Comprehensive sales methodology covering discovery calls using SPIN technique, demo flow with objection handling scripts for 3 main competitors, pricing negotiation strategies with discount approval matrix up to 20%, and closing techniques differentiated for enterprise vs mid-market. Includes 5 real call transcripts as examples."

### Bad summary_detailed:
"A sales document."

### Good integration opportunity:
{
  "name": "HubSpot CRM",
  "type": "CRM",
  "evidence": "Found config/hubspot-credentials.json containing API key and org ID",
  "suggestion": "Connect HubSpot to auto-sync client contact data, deal stages, and pull information for automated proposal generation"
}

### Bad integration opportunity:
{
  "name": "CRM",
  "type": "CRM",
  "evidence": "mentions CRM",
  "suggestion": "connect CRM"
}
```

**If user chooses 2 (skip files)**:
```python
update_config({
    "onboarding.setup_system_state.step_completed": 1,
    "onboarding.setup_system_state.files_uploaded": False
})
# Continue to Step 2
```

### STEP 2: Core Question (2-3 min)

**Display**:
```
STEP 2/7: Define Your Goals

Who are you, OR what do you want to achieve/build with this system?

You can answer:
- Your role: "I'm a sales consultant in B2B SaaS..."
- Your goal: "I want to automate proposal generation..."
- Both: "I'm a PM and I want to build a product roadmap system..."

Tell me about yourself or your goal:
```

**AI Extracts**:
```python
def extract_goals_from_answer(user_answer, file_analysis=None):
    # Use AI to parse user answer
    extraction = {
        "role": None,
        "short_term_goal": None,
        "long_term_vision": None,
        "system_type": None,  # sales, content, research, product, client, etc.
        "work_patterns": []
    }

    # AI analyzes answer
    prompt = f"""
User answer: "{user_answer}"

File analysis available: {file_analysis is not None}
{f"Professional context from files: {file_analysis['professional_context']}" if file_analysis else ""}

Extract:
1. Role (if mentioned or can be inferred)
2. Short-term goal (3-6 months, specific)
3. Long-term vision (1-3 years, if mentioned)
4. System type (sales, content, research, product, client, operations, etc.)
5. Work patterns (what they do regularly)

Be specific. If they said "automate proposals", that's a short-term goal.
If they said "I'm a sales consultant", that's a role.
"""

    extraction = call_ai(prompt)

    # Follow-up questions if needed
    if not extraction["short_term_goal"]:
        short_term = ask_user("What's your main goal for the next 3-6 months?")
        extraction["short_term_goal"] = short_term

    if not extraction["long_term_vision"]:
        # Optional - don't force
        long_term = ask_user("(Optional) What's your 1-3 year vision? (or 'skip')")
        if long_term.lower() != "skip":
            extraction["long_term_vision"] = long_term

    # Update state
    update_config({
        "onboarding.setup_system_state.step_completed": 2,
        "onboarding.setup_system_state.role_captured": True,
        "onboarding.setup_system_state.goals_captured": True
    })

    return extraction
```

### STEP 3: Generate Roadmap (3-4 min)

**Display**:
```
STEP 3/7: Your Roadmap

Based on what you've told me, here's what I think you should build:
```

**AI Generates Roadmap**:
```python
def generate_roadmap(goals, file_analysis=None):
    prompt = f"""
User goals:
- Role: {goals["role"]}
- Short-term goal: {goals["short_term_goal"]}
- Long-term vision: {goals["long_term_vision"]}
- System type: {goals["system_type"]}

{f"File analysis insights: {file_analysis}" if file_analysis else ""}

Generate a roadmap of 3-7 items (builds, skills, integrations) that would help achieve these goals.

For each item:
1. Name (clear, actionable)
2. Type (build, skill, integration)
3. Priority (high, medium, low)
4. Dependencies (which items must be done first)
5. Rationale (why this matters for their goal)

Order by dependencies (foundational items first).

Example output:
[
  {
    "name": "Sales Playbook",
    "type": "build",
    "priority": "high",
    "dependencies": [],
    "rationale": "Foundation for all sales automation - captures your methodology"
  },
  {
    "name": "Proposal Generator",
    "type": "skill",
    "priority": "high",
    "dependencies": ["Sales Playbook"],
    "rationale": "Automates proposal creation using your playbook as template"
  },
  {
    "name": "HubSpot CRM Integration",
    "type": "integration",
    "priority": "medium",
    "dependencies": ["Proposal Generator"],
    "rationale": "Pulls client data automatically for proposals"
  }
]
"""

    roadmap_items = call_ai(prompt)

    # Show to user
    print("\nROADMAP:")
    print("━" * 60)
    for i, item in enumerate(roadmap_items, 1):
        deps_text = f" (after: {', '.join(item['dependencies'])})" if item['dependencies'] else ""
        print(f"\n{i}. {item['name']} ({item['type'].upper()})")
        print(f"   Priority: {item['priority']}{deps_text}")
        print(f"   → {item['rationale']}")
    print("\n" + "━" * 60)

    # Ask for confirmation/refinement
    user_input = ask_user("\nLooks good? (yes/add item/remove item/change priority)")

    if user_input.startswith("add"):
        # Ask what to add
        new_item_name = ask_user("What do you want to add?")
        new_item = create_roadmap_item(new_item_name, goals)
        roadmap_items.append(new_item)

    elif user_input.startswith("remove"):
        # Ask what to remove
        remove_name = ask_user("Which item to remove?")
        roadmap_items = [item for item in roadmap_items if item["name"] != remove_name]

    # etc.

    return roadmap_items
```

### STEP 4: Create Workspace Structure (2-3 min)

```python
def create_workspace_structure(roadmap, file_analysis=None):
    # Generate folder structure from roadmap + file themes

    if file_analysis:
        # Use file themes as base
        suggested_folders = file_analysis["workspace_structure_suggestion"]["folders"]
    else:
        # Generate from roadmap
        suggested_folders = []

        # Extract themes from roadmap
        themes = set()
        for item in roadmap:
            if "sales" in item["name"].lower():
                themes.add("sales")
            elif "client" in item["name"].lower():
                themes.add("clients")
            elif "content" in item["name"].lower():
                themes.add("content")
            # etc.

        for theme in themes:
            suggested_folders.append({
                "path": f"{theme}/",
                "purpose": f"{theme.capitalize()} related files and deliverables",
                "subfolders": []
            })

    # Show to user
    print("\nWORKSPACE STRUCTURE:")
    print("━" * 60)
    print("\n04-workspace/")
    for folder in suggested_folders:
        print(f"├── {folder['path']}")
        if folder.get("subfolders"):
            for subfolder in folder["subfolders"]:
                print(f"│   ├── {subfolder}")
        print(f"│   → {folder['purpose']}")
    print("\n" + "━" * 60)

    user_confirms = ask_user("Good? (yes/modify)")

    if user_confirms == "modify":
        # Allow user to add/remove folders
        pass

    # Create folders
    for folder in suggested_folders:
        create_folder(f"04-workspace/{folder['path']}")
        for subfolder in folder.get("subfolders", []):
            create_folder(f"04-workspace/{folder['path']}{subfolder}")

    # Move files from input/ to organized folders (if files were uploaded)
    if file_analysis:
        for file_data in file_analysis["file_analyses"]:
            source = file_data["path"]
            target = f"04-workspace/{file_data['suggested_folder']}{file_data['filename']}"
            move_file(source, target)

    # Generate workspace-map.md
    workspace_map = generate_workspace_map(suggested_folders)
    write_file("04-workspace/workspace-map.md", workspace_map)

    update_config({
        "onboarding.setup_system_state.step_completed": 4,
        "onboarding.setup_system_state.workspace_created": True
    })
```

### STEP 5: Initiate Projects (2-3 min)

```python
def initiate_projects(roadmap, goals, file_analysis=None):
    print("\nSTEP 5/7: Initiating Projects")
    print("Creating project scaffolds...")

    for i, item in enumerate(roadmap, 1):
        project_id = f"{i:02d}-{slugify(item['name'])}"

        # Create full folder structure
        base_path = f"02-builds/{project_id}/"
        create_folder(f"{base_path}01-planning/")
        create_folder(f"{base_path}02-resources/")
        create_folder(f"{base_path}03-working/")
        create_folder(f"{base_path}04-outputs/")

        # Generate overview.md (FILLED)
        overview_content = generate_overview(item, goals, file_analysis)
        write_file(f"{base_path}01-planning/01-overview.md", overview_content)

        # Create empty planning docs
        write_file(f"{base_path}01-planning/02-discovery.md", DISCOVERY_TEMPLATE)
        write_file(f"{base_path}01-planning/03-plan.md", PLAN_TEMPLATE)
        write_file(f"{base_path}01-planning/04-steps.md", STEPS_TEMPLATE)

        # Create resume-context.md
        resume_context = f"""---
session_id: null
build_id: {project_id}
build_name: {item['name']}
build_type: {item['type']}
current_phase: "planned"
next_action: "start-planning"
---

## Progress Summary

**Status**: Project initialized, planning not started

**Next**: Say "continue {item['name']}" or "work on {project_id}" to begin planning
"""
        write_file(f"{base_path}01-planning/resume-context.md", resume_context)

        print(f"  ✓ Created: {project_id}")

    update_config({
        "onboarding.setup_system_state.step_completed": 5,
        "onboarding.setup_system_state.projects_initiated": True
    })
```

**overview.md Template Generation**:
```python
def generate_overview(item, goals, file_analysis):
    # AI generates purpose and success criteria

    prompt = f"""
Roadmap item:
- Name: {item['name']}
- Type: {item['type']}
- Priority: {item['priority']}
- Rationale: {item['rationale']}

User goals:
- Role: {goals['role']}
- Goal: {goals['short_term_goal']}

{f"File insights: {file_analysis}" if file_analysis else ""}

Generate:
1. Purpose (2-3 sentences: what and why)
2. Success criteria (3 measurable outcomes)
3. Context (how this relates to user goal + file insights)
"""

    ai_generated = call_ai(prompt)

    # Build overview content
    content = f"""---
id: {project_id}
name: {item['name']}
type: {item['type']}
priority: {item['priority']}
status: PLANNED
created: {today()}
---

# {item['name']}

## Purpose

{ai_generated['purpose']}

## Success Criteria

**Must achieve**:
- [ ] {ai_generated['criteria'][0]}
- [ ] {ai_generated['criteria'][1]}
- [ ] {ai_generated['criteria'][2]}

## Context

**User Goal**: {goals['short_term_goal']}

{ai_generated['context']}

**Dependencies**: {', '.join(item['dependencies']) if item['dependencies'] else 'None - can start immediately'}

## Next Steps

When ready to start:
1. Say "continue {item['name']}" or "work on {project_id}"
2. I'll load this build and guide you through planning
3. We'll fill in discovery, plan, and steps together
"""

    return content
```

### STEP 6: Save Everything (1 min)

```python
def save_onboarding_outputs(goals, roadmap, workspace_folders):
    # Save goals.md
    goals_content = f"""---
personalized: true
created: {today()}
---

# Your Goals

## Current Role

{goals['role'] or '[Your role]'}

## Short-Term Goal (3-6 months)

{goals['short_term_goal']}

**Success Metrics**:
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Long-Term Vision (1-3 years)

{goals['long_term_vision'] or '[Your vision]'}

## Work Style & Preferences

**System Type**: {goals['system_type']}
**Work Patterns**: {', '.join(goals['work_patterns'])}

---

**Last Updated**: {today()}
"""

    write_file("01-memory/goals.md", goals_content)

    # Save roadmap.md
    roadmap_content = generate_roadmap_md(roadmap)
    write_file("01-memory/roadmap.md", roadmap_content)

    # workspace-map.md already created in Step 4

    # Copy outputs to onboarding project
    copy_file("01-memory/goals.md", "02-builds/00-onboarding-session/04-outputs/goals.md")
    copy_file("01-memory/roadmap.md", "02-builds/00-onboarding-session/04-outputs/roadmap.md")
    copy_file("04-workspace/workspace-map.md", "02-builds/00-onboarding-session/04-outputs/workspace-map.md")

    # Update final state
    update_config({
        "onboarding.status": "system_setup_complete",
        "onboarding.setup_system_state.step_completed": 6,
        "onboarding.in_progress_skill": null,
        "learning_tracker.completed.setup_memory": true,
        "learning_tracker.completed.create_folders": true,
        "learning_tracker.completed.create_roadmap": true
    })

    # Mark steps complete
    edit_file(
        "02-builds/00-onboarding-session/01-planning/04-steps.md",
        mark_all_steps_complete()
    )

    # Archive onboarding project
    move_folder(
        "02-builds/00-onboarding-session/",
        "05-archived/00-onboarding-session/"
    )
```

### STEP 7: End Session

**Display**:
```
SETUP COMPLETE ✓

Your Nexus system is initialized!

Created:
✓ goals.md (your context, loaded every session)
✓ roadmap.md (your plan with {len(roadmap)} projects)
✓ workspace-map.md (your folder structure)
✓ {len(roadmap)} project scaffolds (ready to start)

Your progress saves automatically.

IMPORTANT: Clean session boundaries matter in Nexus.
Each session = one focus.

This session: System setup (DONE)
Next session: Start your first build

→ Open a NEW chat/session when ready to continue
```

**State at End**:
```yaml
onboarding:
  status: "system_setup_complete"
  in_progress_skill: null
  language_preference: "en"
  chosen_path: "direct"

learning_tracker:
  completed:
    setup_memory: true
    create_folders: true
    create_roadmap: true  # NEW
```

---

## 6. SESSION 2: FIRST BUILD

**SessionStart Detection**:
```python
if onboarding.status == "system_setup_complete":
    # Show roadmap, suggest first build
    roadmap = load_file("01-memory/roadmap.md")

    print("Welcome back!")
    print("\nYour roadmap:")
    display_roadmap(roadmap)

    first_item = get_first_non_dependent_item(roadmap)

    print(f"\nRECOMMENDATION: Start with '{first_item['name']}'")
    print("(It has no dependencies, so you can start immediately)")

    user_input = ask_user("Ready to start? (yes/different item)")

    if user_input == "yes":
        # Load plan-build + first-time explanation
        load_skill("plan-build")
        inject_learn_builds_explanation_inline()
```

**learn-builds Explanation (Inline)**:
```markdown
FIRST BUILD - How This Works

You're about to plan your first build!

Quick context:
- BUILD = work with a clear END
- You'll fill 4 documents WITH me (not alone)
- Mental models will be applied (helps avoid mistakes)

The process:
1. Overview: What and why
2. Discovery: Gather info
3. Plan: Decide how
4. Steps: Create task list

After planning complete:
- Open NEW session
- Say "continue [build name]"
- I'll execute the plan

Let's start!
```

---

## 7. STATE MANAGEMENT (Complete Schema)

```yaml
# user-config.yaml

onboarding:
  # Overall status
  status: "not_started" | "tour_in_progress" | "tour_complete" | "setup_in_progress" | "system_setup_complete" | "first_build_started" | "complete"

  # Current in-progress skill (for resume)
  in_progress_skill: null | "how-nexus-works" | "setup-system"

  # User choices
  language_preference: null | "en" | "de" | "es" | "fr" | "it" | "ja" | "zh"
  chosen_path: null | "tour" | "direct"

  # setup-system progress (for cross-session continuity)
  setup_system_state:
    step_completed: 0  # 0-7
    files_uploaded: false
    file_analysis_done: false
    role_captured: false
    goals_captured: false
    roadmap_created: false
    workspace_created: false
    projects_initiated: false

  # Timestamps (for analytics)
  started_at: null
  completed_at: null

learning_tracker:
  session_count: 0
  completed:
    how_nexus_works: false
    setup_memory: false
    create_roadmap: false  # NEW
    create_folders: false
    learn_builds: false
    learn_skills: false
    learn_integrations: false
    learn_nexus: false
  dismissed: []
  last_suggested: null
  suggestion_preference: "normal"
```

---

## 8. SESSIONSTART ROUTING (Complete Logic)

```python
def determine_onboarding_action(session_source, onboarding_state):
    """
    Determine what to show user based on onboarding state.

    Args:
        session_source: "new" | "compact" | "resume"
        onboarding_state: dict from user-config.yaml

    Returns:
        action: "show_heroic_intro" | "resume_skill" | "load_setup_system" | "show_roadmap" | "normal_menu"
    """

    # Check if in-progress skill (cross-session continuity)
    if onboarding_state["in_progress_skill"]:
        if session_source == "compact":
            # Resume skill
            skill_name = onboarding_state["in_progress_skill"]

            if skill_name == "setup-system":
                # Resume from specific step
                step = onboarding_state["setup_system_state"]["step_completed"]
                return {
                    "action": "resume_skill",
                    "skill": "setup-system",
                    "resume_from_step": step + 1
                }
            else:
                return {
                    "action": "resume_skill",
                    "skill": skill_name
                }

    # Route based on status
    status = onboarding_state["status"]

    if status == "not_started":
        # First session ever
        return {
            "action": "show_heroic_intro",
            "template": "startup_first_run"
        }

    elif status == "tour_complete":
        # Completed tour, need setup
        return {
            "action": "load_setup_system",
            "message": "Welcome back! Ready to set up your system?"
        }

    elif status == "system_setup_complete":
        # Setup done, ready for first build
        return {
            "action": "show_roadmap",
            "message": "Welcome back! Time to start your first build."
        }

    elif status == "first_build_started":
        # First build in progress
        # Check if build exists in active builds
        if has_active_builds():
            return {
                "action": "resume_build",
                "build_id": get_first_active_build()
            }
        else:
            # Build complete, onboarding done
            update_config({"onboarding.status": "complete"})
            return {
                "action": "normal_menu"
            }

    elif status == "complete":
        # Onboarding complete, normal operation
        return {
            "action": "normal_menu"
        }

    else:
        # Unknown state, default to normal menu
        return {
            "action": "normal_menu"
        }
```

---

## 9. PROJECT SCAFFOLDING (Complete Templates)

### DISCOVERY_TEMPLATE
```markdown
# {build_name} - Discovery

*This will be filled when you start planning this build*

---

## Current State

*Where are we now?*

### Existing Assets

- [ ] Asset 1
- [ ] Asset 2

### Current Pain Points

1. Pain point 1
2. Pain point 2

---

## Desired State

*What are we trying to achieve?*

### Target Outcomes

- [ ] Outcome 1
- [ ] Outcome 2

### Success Looks Like

Description of success state...

---

## Resources & References

### Relevant Files

- `file-path.md` - Description

### External Resources

- [Resource name](url) - Description

### Similar Work

- Previous build: XX-name
- Reference: link

---

## Stakeholders

| Person/Group | Interest | Input Needed |
|--------------|----------|--------------|
| User | Primary | Requirements |

---

## Constraints & Risks

### Constraints

- Time: [timeline]
- Resources: [what's available]

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Risk 1 | High | How to address |

---
```

### PLAN_TEMPLATE
```markdown
# {build_name} - Plan

*This will be filled during planning phase*

---

## Approach

*How will we do this?*

### Option 1: [Name]

**Description**: ...

**Pros**:
- Pro 1
- Pro 2

**Cons**:
- Con 1
- Con 2

**Effort**: Low/Medium/High

### Recommended Approach

We'll go with Option X because...

---

## Key Decisions

### Decision 1: [Topic]

**Question**: What should we do about X?

**Options Considered**:
1. Option A - ...
2. Option B - ...

**Decision**: Option A

**Rationale**: Because...

---

## Technical Architecture

(If applicable)

### Components

1. Component 1
2. Component 2

### Flow

```
Step 1 → Step 2 → Step 3
```

---

## Dependencies

### Internal Dependencies

- Depends on: XX-other-build
- Blocks: YY-future-build

### External Dependencies

- Tool: [name] - Purpose
- Data: [source] - What we need

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | Medium | High | Strategy |

---
```

### STEPS_TEMPLATE
```markdown
# {build_name} - Execution Steps

*This will be filled at the end of planning*

---

## Phase 1: [Phase Name]

**Goal**: What this phase achieves

**Tasks**:
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Checkpoint**: How to verify phase complete

---

## Phase 2: [Phase Name]

**Goal**: What this phase achieves

**Tasks**:
- [ ] Task 1
- [ ] Task 2

**Checkpoint**: ...

---

## Completion Checklist

Before marking build complete:

- [ ] All phases executed
- [ ] Outputs reviewed
- [ ] Documentation updated
- [ ] Build archived

---
```

---

## 10. WORKSPACE-MAP.MD FORMAT

```markdown
# Workspace Map

> Last updated: {date}
> Your file organization in 04-workspace/

---

## Folder Structure

📁 **clients/**
   Purpose: Client project files organized by company

   ├── acme/ - Acme Corp project files and deliverables
   ├── beta/ - Beta Inc implementation materials
   └── prospects/ - Potential client outreach and proposals

📁 **sales/**
   Purpose: Sales materials, playbooks, and templates

   ├── playbooks/ - Sales methodology and frameworks
   ├── templates/ - Proposal and email templates
   └── presentations/ - Demo decks and pitch materials

📁 **research/**
   Purpose: Market research and competitive intelligence

   ├── market/ - Industry analysis and trends
   └── competitors/ - Competitive analysis documents

📁 **finance/**
   Purpose: Financial documents and analysis

   └── invoices/ - Client invoicing

---

## Organization Principle

**Entity-based** (organized by clients and business domains)

Files are grouped by the entity they relate to (clients, sales assets, research topics) rather than by process stage.

---

## Usage Notes

- Original file analysis stored in: `05-archived/00-onboarding-session/02-resources/file-analysis.json`
- To update this map: "update workspace map"
- AI reads this map every session to know where files are

---

## File Count

Total files: 45
Total size: 8.5 MB

Last scan: {date}

---
```

---

## 11. ROADMAP.MD FORMAT

```markdown
# Your System Roadmap

> Last updated: {date}
> Status: 35% complete (3 of 9 items done)

---

## BUILDS (In dependency order)

### 1. ✅ Sales Playbook
   - **Type**: Build
   - **Priority**: HIGH
   - **Status**: COMPLETE
   - **Location**: `02-builds/01-sales-playbook/`
   - **Dependencies**: None
   - **Purpose**: Foundation for all sales automation

### 2. 🔵 Proposal Generator
   - **Type**: Skill
   - **Priority**: HIGH
   - **Status**: PLANNING
   - **Location**: `02-builds/02-proposal-generator/`
   - **Dependencies**: Sales Playbook ✅
   - **Purpose**: Auto-generate proposals from templates
   - **Next**: Continue planning in next session

### 3. ⚪ Follow-up Email Automation
   - **Type**: Skill
   - **Priority**: MEDIUM
   - **Status**: PLANNED
   - **Location**: `02-builds/03-follow-up-automation/`
   - **Dependencies**: Proposal Generator
   - **Purpose**: Automated follow-up sequences

### 4. ⚪ HubSpot CRM Integration
   - **Type**: Integration
   - **Priority**: LOW
   - **Status**: PLANNED
   - **Location**: `02-builds/04-hubspot-integration/`
   - **Dependencies**: None (can start anytime)
   - **Purpose**: Auto-sync client data for proposals

---

## PROGRESS

```
Foundation:    [████████████████████████] 100% (Sales Playbook)
Automation:    [████████░░░░░░░░░░░░░░░] 33%  (Proposal Generator in progress)
Integrations:  [░░░░░░░░░░░░░░░░░░░░░░░] 0%   (HubSpot planned)
```

**Next Recommended**: Continue Proposal Generator (already started)

---

## HOW TO USE

To start/continue a build:
- "continue Proposal Generator" (resume current)
- "work on Follow-up Automation" (start new)
- "show roadmap" (see this again)

To update roadmap:
- "add to roadmap [new item]"
- "remove from roadmap [item name]"
- "change priority [item] to high/medium/low"

---
```

---

*This is the COMPLETE specification with ALL details discussed*
*Every code snippet, template, copy, and flow is documented*
*Ready for implementation*
