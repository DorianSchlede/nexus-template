#!/usr/bin/env python3
"""
MetaTuner Dataset Export - NodeTask Level

Exports Airtable test data to MetaTuner-compatible PromptDataset format.
Each dataset item = ONE NodeTask (one prompt execution) with ALL its variable outputs.

Usage:
    python export_dataset.py [OPTIONS]

Options:
    --node NAME        Filter by node name (partial match) - RECOMMENDED
    --agent NAME       Filter by agent name (partial match)
    --tier TIER        Quality tier: gold, silver, bronze (default: gold)
    --limit N          Max records to export
    --output PATH      Output file path
    --format FORMAT    Output format: json, jsonl (default: json)
    --verbose          Show detailed progress

Examples:
    python export_dataset.py --node "Receptionist" --tier gold
    python export_dataset.py --node "Extract All Case" --limit 100
    python export_dataset.py --agent "TZV" --tier gold

Schema: PromptDataset with PromptDatasetItem[] (MetaTuner compatible)
  - id: NodeTask Name (unique identifier for the prompt execution)
  - input: { prompt: FilledPrompt }
  - expectedOutput: { varName1: val1, varName2: val2, ... } (aggregated)
  - actualOutput: { varName1: aiVal1, varName2: aiVal2, ... } (aggregated)
  - metadata: { score, agent, node, variableCount, ... }
"""

import os
import sys
import csv
import json
import argparse
from datetime import datetime
from collections import defaultdict

# Increase CSV field size limit for large cells
csv.field_size_limit(sys.maxsize)

# Find project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
RESOURCES_DIR = os.path.join(PROJECT_DIR, '02-resources')
OUTPUT_DIR = os.path.join(PROJECT_DIR, '04-outputs', 'datasets')


# ============================================================================
# Data Loading
# ============================================================================

def load_csv(filename, key_field=None):
    """Load CSV file into list of dicts or dict keyed by field."""
    filepath = os.path.join(RESOURCES_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    if key_field:
        # Return as dict keyed by field
        return {r.get(key_field, ''): r for r in records if r.get(key_field)}

    return records


def load_all_data(verbose=False):
    """Load all CSV data files."""
    if verbose:
        print("Loading CSV data...")

    data = {}

    if verbose:
        print("  Loading DatasetVariables...")
    data['dataset_variables'] = load_csv('DatasetVariables-FULL.csv')

    if verbose:
        print("  Loading VariableTasks...")
    data['variable_tasks'] = load_csv('VariableTasks-WithExpected.csv')

    if verbose:
        print("  Loading DatasetNodes...")
    data['dataset_nodes'] = load_csv('DatasetNodes-ALL.csv')

    if verbose:
        print("  Loading NodeTasks...")
    data['node_tasks'] = load_csv('NodeTasks-ALL.csv')

    if verbose:
        print(f"  Loaded: {len(data['dataset_variables'])} DatasetVariables")
        print(f"  Loaded: {len(data['variable_tasks'])} VariableTasks")
        print(f"  Loaded: {len(data['dataset_nodes'])} DatasetNodes")
        print(f"  Loaded: {len(data['node_tasks'])} NodeTasks")

    return data


# ============================================================================
# Filtering (NodeTask level)
# ============================================================================

def filter_node_tasks_by_node(node_tasks, node_name):
    """Filter NodeTasks by node name (partial match, case-insensitive)."""
    node_lower = node_name.lower()
    result = []
    for nt in node_tasks:
        # Check Name (from Node) field
        node_field = nt.get('Name (from Node)', '').lower()
        if node_lower in node_field:
            result.append(nt)
    return result


def filter_node_tasks_by_agent(node_tasks, agent_name):
    """Filter NodeTasks by agent name (partial match, case-insensitive)."""
    agent_lower = agent_name.lower()
    return [nt for nt in node_tasks if agent_lower in nt.get('Agent (from Node)', '').lower()]


def filter_node_tasks_with_prompt(node_tasks):
    """Filter NodeTasks to only those with a filled prompt."""
    return [nt for nt in node_tasks if nt.get('Filled Prompt', '').strip()]


def filter_node_tasks_latest_version(node_tasks, verbose=False):
    """Filter to only the latest version for each node.

    Node Version format: "NodeName|YYYY-MM-DD|recordID"
    We group by node name and keep only the latest version by date.
    """
    from collections import defaultdict
    from datetime import datetime

    # Group by node name
    by_node = defaultdict(list)
    for nt in node_tasks:
        node_name = nt.get('Name (from Node)', '')
        if node_name:
            by_node[node_name].append(nt)

    latest_tasks = []

    for node_name, tasks in by_node.items():
        # Find latest version
        latest_version = None
        latest_date = None

        for task in tasks:
            version = task.get('Node Version', '')
            if not version or '|' not in version:
                continue

            # Parse version: "NodeName|YYYY-MM-DD|recordID"
            parts = version.split('|')
            if len(parts) >= 2:
                try:
                    date_str = parts[1]
                    date = datetime.strptime(date_str, '%Y-%m-%d')

                    if latest_date is None or date > latest_date:
                        latest_date = date
                        latest_version = version
                except ValueError:
                    continue

        # Keep only tasks with latest version
        if latest_version:
            latest_tasks.extend([t for t in tasks if t.get('Node Version') == latest_version])
            if verbose:
                count = len([t for t in tasks if t.get('Node Version') == latest_version])
                print(f"    {node_name}: {count} tasks from version {latest_version}")

    return latest_tasks


# ============================================================================
# Data Joining
# ============================================================================

def build_variable_tasks_by_node_task(variable_tasks):
    """Build index of VariableTasks grouped by NodeTask Name.

    Returns: dict[NodeTaskName -> list[VariableTask]]
    """
    index = defaultdict(list)
    for vt in variable_tasks:
        node_task_name = vt.get('NodeTask Name (from NodeTask)', '').strip()
        if node_task_name:
            index[node_task_name].append(vt)
    return index


def filter_variable_tasks_with_expected(variable_tasks, tier='gold'):
    """Filter VariableTasks that have expected values (based on tier).

    tier='gold': Expected Output Status = Done
    tier='silver': Has any expected value
    tier='bronze': Has any expected value
    """
    result = []
    for vt in variable_tasks:
        expected = vt.get('Expected Value', '').strip() or vt.get('Expected Value (from DatasetVariable)', '').strip()
        if not expected:
            continue

        if tier == 'gold':
            status = vt.get('Expected Output Status (from DatasetTask) (from DatasetVariables)', '').strip()
            if status == 'Done':
                result.append(vt)
        else:
            result.append(vt)

    return result


# ============================================================================
# Input Extraction from Filled Prompt
# ============================================================================

import re
import json

def parse_filled_prompt(filled_prompt):
    """Parse the filled prompt into its components.

    Attempts to parse structured prompts for multiple agent formats:
    - Deal Breaker: # Data + task_query + extraction instructions
    - TZV Agent: # Role + # Document Context + @ parameters
    - Email Mgmt: ## ROLE + ## CATEGORIES + @EmailContent
    - Ops Case Handler: # Role & Task + Inputs: + structured data

    Falls back to using the filled prompt as-is if parsing fails.

    Returns:
        {
            'input': dict,            # Varying input data extracted from prompt
            'prompt_template': str,   # Static prompt template (without varying data)
            'parsed': bool            # True if successfully parsed, False if fallback
        }
    """
    if not filled_prompt:
        return {'input': {}, 'prompt_template': '', 'parsed': False}

    # ===== TRY 1: Deal Breaker Format (Extract Data) =====
    # Pattern: # Data ```{document}``` + ```{task_query}``` + ```{instructions}```
    if '# Data' in filled_prompt and '------' in filled_prompt:
        document_match = re.search(r'# Data\s*\n\s*```(.+?)```', filled_prompt, re.DOTALL)
        task_query_match = re.search(r'---\s*\n\s*```(.+?)```\s*\n\s*all content in task_query', filled_prompt, re.DOTALL)
        prompt_match = re.search(r'------\s*\n\s*```(.+?)```\s*$', filled_prompt, re.DOTALL)

        if document_match and prompt_match:
            document = document_match.group(1).strip()
            task_query = {}
            if task_query_match:
                try:
                    import ast
                    task_query = ast.literal_eval(task_query_match.group(1).strip())
                except:
                    pass

            return {
                'input': {'document': document, 'task_query': task_query},
                'prompt_template': prompt_match.group(1).strip(),
                'parsed': True
            }

    # ===== TRY 2: TZV Agent Format (Group A, Receptionist, Schreiben Bank, etc.) =====
    # Structure:
    #   # Role + # Rules + # Document Context + # Variables = Static template
    #   # Data section containing:
    #     ## Classification Context '''```{JSON}```''' = Pre-classification reasoning
    #     ## PDF attachment: '''```{document}```''' = Actual PDF content
    #     ## input '''```{task_metadata}```''' = Task metadata (beamTaskId, etc.)
    if '# Document Context' in filled_prompt and '# Data' in filled_prompt:
        # Find where # Data section starts - everything before is the template
        # IMPORTANT: Find the LAST standalone "# Data" that's a section header
        # (not the one in middle of text like "extract from # Data. To do that...")
        # The real # Data section header is at the end of the template, followed by ## subsections
        data_matches = list(re.finditer(r'^# Data\s*$', filled_prompt, re.MULTILINE))
        if data_matches:
            # Use the last match (the actual section header)
            data_idx = data_matches[-1].start()
        else:
            # Fallback: find # Data followed by ## subsection or '''
            data_match = re.search(r'# Data\s*\n\s*(?:##|\'\'\')', filled_prompt)
            data_idx = data_match.start() if data_match else filled_prompt.find('# Data')

        if data_idx > 0:
            template = filled_prompt[:data_idx].strip()
            data_section = filled_prompt[data_idx:]

            input_data = {}

            # Extract Classification Context JSON
            class_match = re.search(
                r"## Classification Context\s*'''\s*```(.+?)```\s*'''",
                data_section, re.DOTALL
            )
            if class_match:
                try:
                    import ast
                    classification = ast.literal_eval(class_match.group(1).strip())
                    input_data['classification_context'] = classification
                except:
                    # Keep as string if parsing fails
                    input_data['classification_context'] = class_match.group(1).strip()

            # Extract PDF attachment content
            pdf_match = re.search(
                r"## PDF attachment:\s*'''\s*```(.+?)```\s*'''",
                data_section, re.DOTALL
            )
            if pdf_match:
                pdf_content = pdf_match.group(1).strip()
                # Check if there's embedded JSON at the end (task metadata in PDF section)
                # Pattern: document text followed by {"task": ...} JSON
                json_in_pdf = re.search(r'(\{"task":.+\})$', pdf_content, re.DOTALL)
                if json_in_pdf:
                    # Split PDF content from embedded task metadata
                    json_start = json_in_pdf.start()
                    input_data['pdf_content'] = pdf_content[:json_start].strip()
                    try:
                        import ast
                        task_meta = ast.literal_eval(json_in_pdf.group(1))
                        input_data['task'] = task_meta.get('task', '')
                        input_data['beamAgentOSTaskID'] = task_meta.get('beamAgentOSTaskID', '')
                        input_data['beamTaskId'] = task_meta.get('beamTaskId', '')
                        input_data['beamTaskTimestamp'] = task_meta.get('beamTaskTimestamp', '')
                        input_data['attachments'] = task_meta.get('attachments', [])
                    except:
                        pass
                else:
                    input_data['pdf_content'] = pdf_content

            # Extract ## input OR ## Email input section (task metadata) if not already extracted from PDF
            # Different TZV nodes use different section names:
            #   - Group A, SS Grouping: ## input
            #   - Schreiben Bank, TZV Zurück, Receptionist: ## Email input
            if 'beamTaskId' not in input_data:
                # Try both patterns
                input_match = re.search(
                    r"##\s*(?:Email\s+)?input\s*'''\s*```(.+?)```\s*'''",
                    data_section, re.DOTALL
                )
                if input_match:
                    try:
                        import ast
                        task_meta = ast.literal_eval(input_match.group(1).strip())
                        input_data['task'] = task_meta.get('task', '')
                        input_data['beamAgentOSTaskID'] = task_meta.get('beamAgentOSTaskID', '')
                        input_data['beamTaskId'] = task_meta.get('beamTaskId', '')
                        input_data['beamTaskTimestamp'] = task_meta.get('beamTaskTimestamp', '')
                        input_data['attachments'] = task_meta.get('attachments', [])
                    except:
                        pass

            if input_data:
                return {
                    'input': input_data,
                    'prompt_template': template,
                    'parsed': True
                }

    # ===== TRY 2b: TZV Agent Format WITHOUT # Data section (older format) =====
    # Pattern: # Document Context + ''' section ''' ```{task_data}``` ''' [optional footer]
    # The task data is in a Python dict between triple backticks near the end
    if '# Document Context' in filled_prompt and '# Data' not in filled_prompt:
        # Find all triple-backtick blocks
        backtick_blocks = list(re.finditer(r'```(.+?)```', filled_prompt, re.DOTALL))

        if backtick_blocks:
            # Try parsing blocks from the end (task data is usually last or second-to-last)
            for block_match in reversed(backtick_blocks):
                block_content = block_match.group(1).strip()

                # Try to parse as Python dict (task data)
                try:
                    import ast
                    task_data = ast.literal_eval(block_content)

                    # Verify it looks like task data (has typical keys)
                    if isinstance(task_data, dict) and any(k in task_data for k in ['task', 'beamAgentOSTaskID', 'beamTaskId']):
                        # Found the task data block
                        # Template is everything before the ''' that precedes this ```
                        block_start = block_match.start()
                        template_section = filled_prompt[:block_start]

                        # Find the last ''' before the block
                        last_triple_quote = template_section.rfind("'''")
                        if last_triple_quote > 0:
                            template = filled_prompt[:last_triple_quote].strip()

                            return {
                                'input': task_data,
                                'prompt_template': template,
                                'parsed': True
                            }
                except:
                    # Not valid Python dict, try next block
                    continue

    # ===== TRY 3: Email Mgmt Format (Classify Incoming Email) =====
    # Pattern: ## ROLE + ## CATEGORIES + ## Parameter Context @EmailContent:
    if '## ROLE' in filled_prompt and '## Parameter Context' in filled_prompt:
        # Find where parameter context starts
        param_context_match = re.search(r'## Parameter Context\s*\n(.+)', filled_prompt, re.DOTALL)
        if param_context_match:
            template_end = param_context_match.start()
            template = filled_prompt[:template_end].strip()
            params_text = param_context_match.group(1)

            # Extract @EmailContent value
            email_match = re.search(r'@EmailContent:\s*\n(.+?)(?=\n@|\Z)', params_text, re.DOTALL)
            if email_match:
                email_content = email_match.group(1).strip()
                return {
                    'input': {'email_content': email_content},
                    'prompt_template': template,
                    'parsed': True
                }

    # ===== TRY 4: Ops Case Handler Format (Extract All Case Info) =====
    # Pattern: # Role & Task + # Objective + Inputs: + field_name ```{data}``` blocks
    if '# Role & Task' in filled_prompt and 'Inputs:' in filled_prompt:
        # Find where Inputs: section starts
        inputs_idx = filled_prompt.find('Inputs:')
        if inputs_idx > 0:
            template = filled_prompt[:inputs_idx].strip()
            inputs_section = filled_prompt[inputs_idx + len('Inputs:'):]

            # Parse input fields - each field has: FieldName \n ```{json_data}```
            # Common fields: ADM_Email, Optional, etc.
            input_data = {}

            # Find all ``` code blocks in the inputs section
            # Pattern: optional field name line, then ```...``` block
            blocks = re.finditer(r'(?:^|\n)([A-Z]\w+(?:_\w+)*)\s*\n\s*```(.+?)```', inputs_section, re.DOTALL)

            for match in blocks:
                field_name = match.group(1).strip()
                field_value = match.group(2).strip()

                # Try to parse as Python/JSON
                try:
                    import ast
                    import json
                    # Try ast first (for Python dict syntax)
                    try:
                        parsed_value = ast.literal_eval(field_value)
                    except:
                        # Try JSON
                        parsed_value = json.loads(field_value)
                    input_data[field_name] = parsed_value
                except:
                    # Keep as string if parsing fails
                    input_data[field_name] = field_value

            if input_data:
                return {
                    'input': input_data,
                    'prompt_template': template,
                    'parsed': True
                }

    # ===== FALLBACK: Use entire filled prompt =====
    # For nodes with unparsed structures, use filled prompt as-is
    return {
        'input': {},
        'prompt_template': filled_prompt,
        'parsed': False
    }


# ============================================================================
# MetaTuner Format Transformation (NodeTask Level)
# ============================================================================

def transform_node_task_to_metatuner(node_task, variable_tasks):
    """Transform a NodeTask with its VariableTasks to MetaTuner format.

    Each NodeTask = one prompt execution
    variable_tasks = list of all VariableTasks for this NodeTask

    Note: We parse the filled prompt to separate input data from prompt template.
    MetaTuner needs the actual varying inputs (document, task_query) separate from
    the prompt template so it can optimize the template.

    Output:
        {
            id: NodeTask Name,
            input: { document, task_query },  # Actual varying input data
            expectedOutput: { varName1: val1, varName2: val2, ... },
            actualOutput: { varName1: aiVal1, varName2: aiVal2, ... },
            metadata: { score }
        }

    Returns: (item, prompt_template)
        item: PromptDatasetItem dict
        prompt_template: str (extracted from filled prompt, shared across dataset)
    """
    node_task_name = node_task.get('NodeTask Name', '')
    original_prompt = node_task.get('Original Prompt Lookup', '')
    filled_prompt = node_task.get('Filled Prompt', '') or original_prompt

    # Parse filled prompt to separate input data from prompt template
    parsed = parse_filled_prompt(filled_prompt)

    # Input data is extracted by parser (or empty dict if fallback)
    if parsed['parsed']:
        # Successfully parsed: Use extracted input data
        input_data = parsed['input']
    else:
        # Fallback: Use filled prompt as input (for nodes with unparsed structures)
        input_data = {'prompt': filled_prompt}

    # Prompt template is extracted separately (will be stored in dataset.metadata.prompt)
    prompt_template = parsed['prompt_template']

    # Aggregate expected and actual outputs from all VariableTasks
    # Also build per-variable evaluation results (PromptEvaluationMetricResult)
    expected_output = {}
    actual_output = {}
    scores = []
    evaluation_metrics = []  # Per-variable evaluation results

    for vt in variable_tasks:
        var_name = vt.get('Variable Name', '') or vt.get('DatasetVariable', '')
        if not var_name:
            continue

        # Get expected value
        expected = vt.get('Expected Value', '').strip() or vt.get('Expected Value (from DatasetVariable)', '').strip()
        if expected:
            expected_output[var_name] = expected

        # Get actual AI value
        actual = vt.get('AIValue', '').strip()
        if actual:
            actual_output[var_name] = actual

        # Calculate accuracy from expected vs actual comparison
        # Note: VariableTaskAccuracy field is often 0 regardless of match, so we compute it ourselves
        var_success = None
        var_score = None
        failure_mode = ''

        if expected and actual:
            # Normalize for comparison (handle boolean strings, numbers, etc.)
            exp_norm = expected.lower().strip()
            act_norm = actual.lower().strip()

            # Direct string match
            var_success = exp_norm == act_norm

            # Try numeric comparison for numbers
            if not var_success:
                try:
                    exp_num = float(expected.replace(',', '.'))
                    act_num = float(actual.replace(',', '.'))
                    var_success = abs(exp_num - act_num) < 0.001
                except (ValueError, TypeError):
                    pass

            var_score = 1.0 if var_success else 0.0
            scores.append(var_score)

            if not var_success:
                failure_mode = 'value_mismatch'
        elif expected and not actual:
            var_success = False
            var_score = 0.0
            failure_mode = 'missing_output'
            scores.append(var_score)
        elif not expected and actual:
            # Has output but no expected value - can't evaluate
            var_success = None
            var_score = None
            failure_mode = ''

        # Build PromptEvaluationMetricResult per MetaTuner interface:
        # interface PromptEvaluationMetricResult {
        #   id: string;
        #   name: string;
        #   reasoning: string;
        #   evaluatedChecklist: string[];
        #   score: number;
        #   llmScore: number;
        #   success: boolean;
        #   failureMode: string;
        #   systemFeedback: string;
        #   error?: string;
        # }
        metric_result = {
            'id': vt.get('VariableTask UID', '') or f"{node_task_name}_{var_name}",
            'name': var_name,
            'reasoning': f"Compared expected '{expected}' with actual '{actual}'" if expected else "No expected value available",
            'evaluatedChecklist': [],  # Not available from Airtable data
            'score': var_score if var_score is not None else 0.0,
            'llmScore': var_score if var_score is not None else 0.0,  # Same as score for exact match evaluation
            'success': var_success if var_success is not None else False,
            'failureMode': failure_mode,
            'systemFeedback': f"Expected: {expected}" if failure_mode == 'value_mismatch' else ("Missing AI output" if failure_mode == 'missing_output' else ""),
            # Additional fields for debugging (not in interface but useful)
            'expected': expected,
            'actual': actual,
        }

        evaluation_metrics.append(metric_result)

    # Calculate average score from VariableTasks
    avg_score = sum(scores) / len(scores) if scores else None

    # Get TaskNodeAccuracy from NodeTask if available (more accurate)
    # Format is "91%" - need to strip the % suffix
    task_node_accuracy = node_task.get('TaskNodeAccuracy', '').strip()
    if task_node_accuracy and task_node_accuracy != 'NaN':
        try:
            # Remove % suffix and convert to 0-1 scale
            acc_value = task_node_accuracy.replace('%', '').strip()
            if acc_value:
                avg_score = float(acc_value) / 100.0  # Convert 91% to 0.91
        except (ValueError, TypeError):
            pass

    # Get full Node Output (complete actual output from the node execution)
    full_actual_output = None
    node_output_raw = node_task.get('Node Output', '').strip()
    if node_output_raw:
        try:
            import ast
            full_actual_output = ast.literal_eval(node_output_raw)
        except:
            try:
                full_actual_output = json.loads(node_output_raw)
            except:
                # Keep as string if parsing fails
                full_actual_output = node_output_raw

    # Build PromptEvaluationResult for this execution
    # interface PromptEvaluationResult {
    #   id: string;
    #   success: boolean;
    #   score: number;
    #   llmScore?: number;
    #   successRate?: number;
    #   evaluations: PromptEvaluationMetricResult[];
    # }
    success_count = sum(1 for m in evaluation_metrics if m.get('success'))
    total_count = len(evaluation_metrics)
    success_rate = success_count / total_count if total_count > 0 else 0.0

    evaluation_result = {
        'id': f"eval_{node_task_name}",
        'success': avg_score == 1.0 if avg_score is not None else success_rate == 1.0,
        'score': avg_score if avg_score is not None else success_rate,
        'successRate': success_rate,
        'evaluations': evaluation_metrics,
    }

    # Build MetaTuner item (matches PromptDatasetItem TypeScript interface exactly)
    # interface PromptDatasetItem {
    #   id: string;
    #   input: Record<string, any>;
    #   actualOutput?: string | Record<string, any>;
    #   expectedOutput?: string | Record<string, any>;
    #   userFeedback?: string;
    #   metadata?: Record<string, any>;
    # }
    item = {
        'id': node_task_name,
        'input': input_data,
        'expectedOutput': expected_output,
        'actualOutput': actual_output,
    }

    # Build metadata with score, evaluation, and full output
    item_metadata = {}
    if avg_score is not None:
        item_metadata['score'] = avg_score
    if evaluation_result:
        item_metadata['evaluation'] = evaluation_result
    if full_actual_output is not None:
        item_metadata['fullActualOutput'] = full_actual_output

    if item_metadata:
        item['metadata'] = item_metadata

    return item, prompt_template  # Return parsed prompt template for dataset metadata


# ============================================================================
# Export Functions (NodeTask Level)
# ============================================================================

def export_dataset(data, node=None, agent=None, tier='gold', limit=None, verbose=False):
    """Export filtered dataset in MetaTuner format at NodeTask level.

    Each output item = ONE NodeTask (one prompt execution) with ALL its variable outputs.

    Process:
    1. Start with NodeTasks
    2. Filter by node/agent
    3. Build index of VariableTasks by NodeTask
    4. Filter VariableTasks by tier (gold = Done status)
    5. For each NodeTask with qualifying VariableTasks, create one item
    """
    if verbose:
        print(f"\nNodeTask-level export mode...")

    # Step 1: Start with NodeTasks
    node_tasks = data['node_tasks']
    if verbose:
        print(f"  Total NodeTasks: {len(node_tasks)}")

    # Step 2a: Filter by node name
    if node:
        node_tasks = filter_node_tasks_by_node(node_tasks, node)
        if verbose:
            print(f"  After node filter '{node}': {len(node_tasks)}")

    # Step 2b: Filter by agent
    if agent:
        node_tasks = filter_node_tasks_by_agent(node_tasks, agent)
        if verbose:
            print(f"  After agent filter '{agent}': {len(node_tasks)}")

    # Step 2c: Filter to latest version only (CRITICAL for accuracy)
    if verbose:
        print(f"  Filtering to latest version per node...")
    node_tasks = filter_node_tasks_latest_version(node_tasks, verbose=verbose)
    if verbose:
        print(f"  After latest version filter: {len(node_tasks)}")

    # Step 2d: Filter to only those with prompts
    node_tasks = filter_node_tasks_with_prompt(node_tasks)
    if verbose:
        print(f"  With filled prompt: {len(node_tasks)}")

    if not node_tasks:
        print("No NodeTasks match the filter criteria.")
        return []

    # Step 3: Build index of VariableTasks by NodeTask Name
    if verbose:
        print("\nBuilding VariableTask index...")
    all_variable_tasks = data['variable_tasks']

    # Step 4: Filter VariableTasks by tier (before indexing)
    filtered_variable_tasks = filter_variable_tasks_with_expected(all_variable_tasks, tier)
    if verbose:
        print(f"  VariableTasks with expected ({tier}): {len(filtered_variable_tasks)}")

    # Build index from filtered VariableTasks
    vt_by_node_task = build_variable_tasks_by_node_task(filtered_variable_tasks)
    if verbose:
        print(f"  NodeTasks with VariableTasks: {len(vt_by_node_task)}")

    # Step 5: Transform each NodeTask that has VariableTasks
    if verbose:
        print(f"\nTransforming NodeTasks to MetaTuner format...")

    items = []
    prompt_template = None  # Collect prompt template (shared across items)
    agent_name = None  # Collect agent name (shared across items)
    node_name = None  # Collect node name (shared across items)
    skipped = 0
    for i, nt in enumerate(node_tasks):
        node_task_name = nt.get('NodeTask Name', '')

        # Get VariableTasks for this NodeTask
        var_tasks = vt_by_node_task.get(node_task_name, [])

        # Skip NodeTasks without any qualifying VariableTasks
        if not var_tasks:
            skipped += 1
            continue

        # Transform to MetaTuner format
        item, item_prompt = transform_node_task_to_metatuner(nt, var_tasks)
        items.append(item)

        # Capture shared metadata from first item
        if not prompt_template and item_prompt:
            prompt_template = item_prompt
        if not agent_name:
            agent_name = nt.get('Agent (from Node)', '').strip()
        if not node_name:
            node_name = nt.get('Name (from Node)', '').strip()

        if verbose and (len(items)) % 50 == 0:
            print(f"  Processed {len(items)} items...")

        # Apply limit
        if limit and len(items) >= limit:
            if verbose:
                print(f"  Reached limit of {limit}")
            break

    if verbose:
        print(f"  Skipped {skipped} NodeTasks (no qualifying VariableTasks)")
        print(f"  Final items: {len(items)}")

    # Return items and shared metadata
    shared_metadata = {
        'prompt': prompt_template,
        'agent': agent_name,
        'node': node_name,
    }
    return items, shared_metadata


# ============================================================================
# Schema & Evaluation Generation
# ============================================================================

def generate_input_schema(items):
    """Generate JSON Schema for input variables based on dataset items.

    Analyzes all input keys across items and infers types.

    Returns: JSON Schema dict
    """
    # Collect all input keys and sample values
    all_keys = set()
    samples = defaultdict(list)

    for item in items:
        input_data = item.get('input', {})
        for key, value in input_data.items():
            all_keys.add(key)
            samples[key].append(value)

    # Build schema properties
    properties = {}
    required = []

    for key in sorted(all_keys):
        sample_values = samples[key]

        # Infer type from samples
        prop_type = 'string'  # Default
        prop_desc = ''

        # Check if all samples are the same type
        non_empty = [v for v in sample_values if v]
        if non_empty:
            first = non_empty[0]
            if isinstance(first, dict):
                prop_type = 'object'
                prop_desc = f"Object with {len(first)} keys" if first else "Object"
            elif isinstance(first, list):
                prop_type = 'array'
                prop_desc = f"Array with {len(first)} items" if first else "Array"
            elif isinstance(first, bool):
                prop_type = 'boolean'
            elif isinstance(first, (int, float)):
                prop_type = 'number'
            else:
                prop_type = 'string'

        # Generate descriptions based on key name
        key_descriptions = {
            'pdf_content': 'The PDF document content (markdown converted)',
            'task': 'Task metadata including clientId, case_id, subfolder',
            'beamTaskId': 'Beam task identifier',
            'beamAgentOSTaskID': 'Beam AgentOS task identifier',
            'beamTaskTimestamp': 'Timestamp of task creation',
            'attachments': 'List of file attachments',
            'classification_context': 'Pre-classification reasoning from previous nodes',
            'document': 'Document content for extraction',
            'task_query': 'Query parameters for the task',
            'email_content': 'Email message content',
            'prompt': 'Full prompt text (fallback when parsing fails)',
        }
        prop_desc = key_descriptions.get(key, prop_desc or f'{key} input field')

        properties[key] = {
            'type': prop_type,
            'description': prop_desc,
        }

        # Mark as required if present in most items
        presence_rate = len(non_empty) / len(items) if items else 0
        if presence_rate > 0.9:
            required.append(key)

    return {
        'type': 'object',
        'properties': properties,
        'required': required,
    }


def generate_output_schema(items):
    """Generate JSON Schema for output variables based on dataset items.

    Analyzes all expectedOutput keys across items and infers types.

    Returns: JSON Schema dict
    """
    # Collect all output keys and sample values
    all_keys = set()
    samples = defaultdict(list)
    enum_values = defaultdict(set)

    for item in items:
        expected = item.get('expectedOutput', {})
        for key, value in expected.items():
            all_keys.add(key)
            samples[key].append(value)
            if isinstance(value, str):
                enum_values[key].add(value)

    # Build schema properties
    properties = {}
    required = []

    for key in sorted(all_keys):
        sample_values = samples[key]
        unique_values = enum_values.get(key, set())

        # Infer type from samples
        prop = {'type': 'string'}

        # If limited unique values, treat as enum
        if unique_values and len(unique_values) <= 10:
            prop['enum'] = sorted(list(unique_values))

        # Generate description from key name
        prop['description'] = f'{key} output variable'

        properties[key] = prop

        # All output variables are required
        required.append(key)

    return {
        'type': 'object',
        'properties': properties,
        'required': required,
    }


def generate_input_parameters(input_schema):
    """Generate human-readable input parameter descriptions.

    Returns: dict[key -> description string]
    """
    params = {}
    props = input_schema.get('properties', {})
    for key, prop in props.items():
        params[key] = prop.get('description', f'{key} input field')
    return params


def generate_output_parameters(output_schema):
    """Generate human-readable output parameter descriptions.

    Returns: dict[key -> description string]
    """
    params = {}
    props = output_schema.get('properties', {})
    for key, prop in props.items():
        desc = prop.get('description', f'{key} output')
        enum_vals = prop.get('enum', [])
        if enum_vals:
            desc += f" (values: {', '.join(enum_vals[:5])}{'...' if len(enum_vals) > 5 else ''})"
        params[key] = desc
    return params


def generate_prompt_evaluations(output_schema):
    """Generate PromptEvaluation criteria - one per output parameter.

    interface PromptEvaluation {
        id: string;
        name: string;
        criteria: string;
        threshold: number;
        evaluationChecklist?: string[];
        evaluationParams: string[];
        model?: string;
    }

    Returns: list[PromptEvaluation] - one eval per output parameter
    """
    output_props = output_schema.get('properties', {})

    if not output_props:
        return []

    # One evaluation per output parameter
    evals = []
    for key, prop in output_props.items():
        desc = prop.get('description', f'{key} output')
        enum_vals = prop.get('enum', [])

        # Build criteria based on type
        if enum_vals:
            criteria = f"Value must be one of: {', '.join(enum_vals)}"
        else:
            criteria = f"Value must exactly match expected {key}"

        evals.append({
            'id': f'eval-{key}',
            'name': f'{key} Evaluation',
            'criteria': criteria,
            'threshold': 1.0,
            'evaluationParams': [key],
        })

    return evals


def build_prompt_executions(items, dataset_id):
    """Build PromptExecutions bundle from dataset items.

    interface PromptExecutions {
        id: string;
        executions: PromptExecution[];
    }

    interface PromptExecution {
        id: string;
        prompt?: string;
        input?: Record<string, any>;
        output: string | Record<string, any>;
        expectedOutput?: string | Record<string, any>;
        systemFeedback?: string;
        userFeedback?: string;
        evaluation?: PromptEvaluationResult;
        metadata?: Record<string, any>;
    }

    Returns: PromptExecutions dict
    """
    executions = []

    for item in items:
        execution = {
            'id': item.get('id', ''),
            'input': item.get('input', {}),
            'output': item.get('actualOutput', {}),
            'expectedOutput': item.get('expectedOutput', {}),
        }

        # Copy evaluation from item metadata if present
        item_meta = item.get('metadata', {})
        if 'evaluation' in item_meta:
            execution['evaluation'] = item_meta['evaluation']

        executions.append(execution)

    return {
        'id': f'exec-{dataset_id}',
        'executions': executions,
    }


def add_placeholders_to_prompt(prompt_template, input_schema):
    """Add {variable} placeholders to prompt template for MetaTuner.

    MetaTuner needs placeholders like {pdf_content}, {task}, etc. to know
    where to inject input variables. The original prompt has a static # Data
    section that was filled with actual values - we replace it with placeholders.

    Returns: prompt string with # Data section containing placeholders
    """
    if not prompt_template:
        return prompt_template

    # Get input variable names from schema
    input_keys = list(input_schema.get('properties', {}).keys())
    if not input_keys:
        return prompt_template

    # Build placeholder section
    placeholder_lines = ['# Data']
    for key in input_keys:
        # Use curly brace placeholders that MetaTuner can fill
        placeholder_lines.append(f'## {key}')
        placeholder_lines.append('{' + key + '}')
        placeholder_lines.append('')

    placeholder_section = '\n'.join(placeholder_lines)

    # The template already ends with # Data section or has it removed
    # We need to append the placeholder section
    if prompt_template.rstrip().endswith('---'):
        # Template ends with separator, add placeholders after
        return prompt_template + '\n' + placeholder_section
    else:
        # Template doesn't have # Data section, add it
        return prompt_template + '\n\n' + placeholder_section


def save_output(items, output_path, format='json', tier='gold', shared_metadata=None):
    """Save items to file in COMPLETE MetaTuner format.

    Complete export structure:
    {
        datasetName: string,
        metadata: {...},
        promptDataset: PromptDataset,
        metatunerPromptInput: MetaTunerPromptInput,
        executions: PromptExecutions
    }

    PromptDatasetItem = { id, input, expectedOutput, actualOutput, metadata? }
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    shared_metadata = shared_metadata or {}

    if format == 'jsonl':
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
    else:
        node = shared_metadata.get('node', '')
        agent = shared_metadata.get('agent', '')
        prompt = shared_metadata.get('prompt', '')

        # Build dataset name
        name_parts = []
        if node:
            name_parts.append(node)
        name_parts.append(tier)
        dataset_name = '-'.join(name_parts) if name_parts else 'dataset'

        # Build description
        desc_parts = []
        if node:
            desc_parts.append(f"Node: {node}")
        if agent:
            desc_parts.append(f"Agent: {agent}")
        desc_parts.append(f"Quality tier: {tier}")
        desc_parts.append(f"Total items: {len(items)}")
        description = '. '.join(desc_parts)

        # Build tags
        tags = [tier]
        if node:
            tags.append(node.lower().replace(' ', '-'))

        # Calculate summary statistics
        scores = []
        succeeded = 0
        failed = 0
        for item in items:
            item_meta = item.get('metadata', {})
            score = item_meta.get('score')
            if score is not None:
                scores.append(score)
            ev = item_meta.get('evaluation', {})
            if ev.get('success'):
                succeeded += 1
            else:
                failed += 1

        avg_score = sum(scores) / len(scores) if scores else 0.0

        # =====================================================
        # Generate schemas and evaluations
        # =====================================================
        input_schema = generate_input_schema(items)
        output_schema = generate_output_schema(items)
        prompt_evals = generate_prompt_evaluations(output_schema)

        # Add {variable} placeholders to prompt template for MetaTuner
        prompt_with_placeholders = add_placeholders_to_prompt(prompt, input_schema)

        # =====================================================
        # Build PromptDataset (core dataset)
        # =====================================================
        # interface PromptDataset {
        #   name: string;
        #   description: string;
        #   items: PromptDatasetItem[];
        #   metadata?: Record<string, any>;
        #   tags?: string[];
        # }
        #
        # interface PromptDatasetItem {
        #   id: string;
        #   input: Record<string, any>;
        #   actualOutput?: string | Record<string, any>;
        #   expectedOutput?: string | Record<string, any>;
        #   userFeedback?: string;
        #   metadata?: Record<string, any>;
        # }
        dataset_items = []
        for item in items:
            dataset_item = {
                'id': item.get('id', ''),
                'input': item.get('input', {}),
                'expectedOutput': item.get('expectedOutput', {}),
                'actualOutput': item.get('actualOutput', {}),
            }
            # Add metadata with score and evaluation
            item_meta = item.get('metadata', {})
            if item_meta:
                dataset_item['metadata'] = item_meta
            dataset_items.append(dataset_item)

        prompt_dataset = {
            'name': dataset_name,
            'description': description,
            'items': dataset_items,
            'metadata': {
                'agent': agent,
                'node': node,
                'tier': tier,
                'itemCount': len(dataset_items),
            },
            'tags': tags,
        }

        # =====================================================
        # Build MetaTunerPromptInput (tuning configuration)
        # =====================================================
        # interface MetaTunerPromptInput {
        #   prompt: string;
        #   inputSchema: Record<string, any>;
        #   dataset: PromptDataset;
        #   evals: PromptEvaluation[];
        #   outputSchema?: Record<string, any>;
        #   executions?: PromptExecutions;
        # }
        metatuner_input = {
            'prompt': prompt_with_placeholders,  # Prompt with {variable} placeholders
            'inputSchema': input_schema,
            'outputSchema': output_schema,
            'evals': prompt_evals,
            # Note: dataset is the same as promptDataset at top level
            # MetaTuner can reference either location
        }

        # =====================================================
        # Build PromptExecutions bundle
        # =====================================================
        executions = build_prompt_executions(items, dataset_name)

        # =====================================================
        # Build COMPLETE export structure
        # =====================================================
        # Count total output variables
        output_variable_count = len(output_schema.get('properties', {}))

        complete_export = {
            'metadata': {
                'datasetName': dataset_name,
                'agent': agent,
                'node': node,
                'promptType': '',  # To be set: extraction, classification, generation, routing
                'tier': tier,
                'itemCount': len(items),
                'outputVariableCount': output_variable_count,
                'averageScore': round(avg_score, 4),
                'succeededCount': succeeded,
                'failedCount': failed,
                'generated_at': datetime.now().isoformat(),
                'source': 'airtable-export',
            },
            'metatunerPromptInput': metatuner_input,
            'promptDataset': prompt_dataset,
            'PromptExecutions': executions,
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(complete_export, f, indent=2, ensure_ascii=False)


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Export Airtable data to MetaTuner format')
    parser.add_argument('--node', '-n', help='Filter by node name (partial match)')
    parser.add_argument('--agent', '-a', help='Filter by agent name (partial match)')
    parser.add_argument('--tier', '-t', choices=['gold', 'silver', 'bronze'], default='gold',
                        help='Quality tier (default: gold)')
    parser.add_argument('--limit', '-l', type=int, help='Max records to export')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', '-f', choices=['json', 'jsonl'], default='json',
                        help='Output format (default: json)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed progress')
    args = parser.parse_args()

    # Load data
    data = load_all_data(args.verbose)

    # Export
    items, shared_metadata = export_dataset(
        data,
        node=args.node,
        agent=args.agent,
        tier=args.tier,
        limit=args.limit,
        verbose=args.verbose
    )

    if not items:
        return

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        # Build slug from node or agent filter
        if args.node:
            slug = args.node.lower().replace(' ', '-').replace('.', '')[:30]
        elif args.agent:
            slug = args.agent.lower().replace(' ', '-')
        else:
            slug = 'all'
        filename = f"metatuner-{slug}-{args.tier}.{args.format}"
        output_path = os.path.join(OUTPUT_DIR, filename)

    # Save with MetaTuner PromptDataset format
    save_output(items, output_path, args.format, tier=args.tier, shared_metadata=shared_metadata)

    # Summary
    print(f"\n{'=' * 60}")
    print("EXPORT SUMMARY (NodeTask Level)")
    print('=' * 60)
    print(f"NodeTasks exported: {len(items)}")
    print(f"Node: {shared_metadata.get('node', 'All')}")
    print(f"Agent: {shared_metadata.get('agent', 'All')}")
    print(f"Quality tier: {args.tier}")
    print(f"Output format: {args.format}")
    print(f"Output file: {output_path}")
    print(f"Prompt template: {'Yes' if shared_metadata.get('prompt') else 'No'}")

    # Stats for NodeTask-level export
    with_input_vars = sum(1 for i in items if i.get('input'))
    with_score = sum(1 for i in items if i.get('metadata', {}).get('score') is not None)
    total_expected = sum(len(i.get('expectedOutput', {})) for i in items)
    avg_expected = total_expected / len(items) if items else 0

    print(f"\nData quality:")
    print(f"  With input variables: {with_input_vars} ({100*with_input_vars/len(items):.1f}%)")
    print(f"  With score: {with_score} ({100*with_score/len(items):.1f}%)")
    print(f"  Total expected outputs: {total_expected}")
    print(f"  Avg outputs/item: {avg_expected:.1f}")


if __name__ == '__main__':
    main()
