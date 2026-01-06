---
description: Created with Workflow Studio
allowed-tools: Task,AskUserQuestion
---
```mermaid
flowchart TD
    start_node_default([Start])
    end_node_default([End])
    prompt_1767284987822[Enter your prompt here.]
    agent_1767285040332[subagent-node]
    ifelse_1767285075049{If/Else:<br/>Conditional Branch}
    switch_1767285098858{Switch:<br/>Conditional Branch}

    start_node_default --> prompt_1767284987822
    prompt_1767284987822 --> ifelse_1767285075049
    ifelse_1767285075049 -->|True| agent_1767285040332
    ifelse_1767285075049 -->|False| switch_1767285098858
```

## Workflow Execution Guide

Follow the Mermaid flowchart above to execute the workflow. Each node type has specific execution methods as described below.

### Execution Methods by Node Type

- **Rectangle nodes**: Execute Sub-Agents using the Task tool
- **Diamond nodes (AskUserQuestion:...)**: Use the AskUserQuestion tool to prompt the user and branch based on their response
- **Diamond nodes (Branch/Switch:...)**: Automatically branch based on the results of previous processing (see details section)
- **Rectangle nodes (Prompt nodes)**: Execute the prompts described in the details section below

### Prompt Node Details

#### prompt_1767284987822(Enter your prompt here.)

```
Enter your prompt here.

You can use variables like {{variableName}}.

{{sheesh}}
```

### If/Else Node Details

#### ifelse_1767285075049(Binary Branch (True/False))

**Branch conditions:**
- **True**: When condition is true
- **False**: When condition is false

**Execution method**: Evaluate the results of the previous processing and automatically select the appropriate branch based on the conditions above.

### Switch Node Details

#### switch_1767285098858(Multiple Branch (2-N))

**Branch conditions:**
- **Case 1**: When condition 1 is met
- **Case 2**: When condition 2 is met
- **default**: Other cases

**Execution method**: Evaluate the results of the previous processing and automatically select the appropriate branch based on the conditions above.
