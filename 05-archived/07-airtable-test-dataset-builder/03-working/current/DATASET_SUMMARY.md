# MetaTuner Dataset Collection Summary

**Generated**: 2026-01-02
**Total Datasets**: 8
**Total NodeTasks**: 415
**Total Variables**: 2,949
**Quality Tier**: Gold (Human Reviewed)
**Format**: MetaTuner PromptDataset (NodeTask level)
**Parsing Status**: ✅ All datasets have proper input/template separation

---

## Dataset Overview

### Phase 5.2 - Initial Priority Nodes

| Dataset | Node | Agent | Tasks | Vars | Avg Score | Version | Use Case |
|---------|------|-------|-------|------|-----------|---------|----------|
| metatuner-1-schreiben-bank-gold.json | 1. Schreiben Bank | TZV Agent 03.09 | 60 | 114 | 0.88 | 2025-10-10 | Medium accuracy, room for improvement |
| metatuner-2-tzv-gold.json | 2. TZV Zurück | TZV Agent 03.09 | 42 | 301 | 0.68 | 2025-10-17 | Lower accuracy, needs optimization |
| metatuner-extract-all-case-info-gold.json | Extract All Case Info | Ops Case Handler | 73 | 998 | 0.57 | 2025-09-18 | Complex extraction, many variables |
| metatuner-receptionist-gold.json | 0. Receptionist | TZV Agent 03.09 | 42 | 544 | 0.80 | Latest | Entry point node, good baseline |

**Subtotal**: 217 tasks, 1,957 variables

### Phase 6.1 - Additional High-Quality Nodes

| Dataset | Node | Agent | Tasks | Vars | Avg Score | Version | Use Case |
|---------|------|-------|-------|------|-----------|---------|----------|
| metatuner-30-ss-grouping-gold.json | 3.0 SS Grouping | TZV Agent 03.09 | 70 | 717 | 0.99 | 2025-10-09 | High accuracy, regression testing |
| metatuner-31-group-a-gold.json | 3.1 Group A: Complex Overlaps | TZV Agent 03.09 | 26 | 73 | 0.91 | 2025-10-09 | Complex cases, good accuracy |
| metatuner-extract-data-gold.json | Extract Data | Deal Breaker | 10 | 110 | 0.93 | 2025-12-18 | Small dataset, high quality |
| metatuner-classify-incoming-email-gold.json | Classify Incoming Email | Email Mgmt Assistant | 92 | 92 | 0.96 | 2025-09-30 | Classification task, simple output |

**Subtotal**: 198 tasks, 992 variables

---

## Data Quality

- **Input Coverage**: 100% (all tasks have filled prompts)
- **Score Coverage**: 100% (all tasks have TaskNodeAccuracy)
- **Version Filtering**: Latest version only (no mixing)
- **Expected Output**: 100% (gold tier requirement)
- **Actual Output**: 100% (all tasks executed)

---

## Agent Distribution

| Agent | Datasets | NodeTasks | Variables | Avg Score |
|-------|----------|-----------|-----------|-----------|
| TZV Agent 03.09 | 5 | 240 | 1,749 | 0.85 |
| Ops Case Handler | 1 | 73 | 998 | 0.57 |
| Deal Breaker | 1 | 10 | 110 | 0.93 |
| Email Mgmt Assistant | 1 | 92 | 92 | 0.96 |

**Total**: 4 agents across 8 datasets

---

## Use Case Recommendations

### For Prompt Optimization
1. **metatuner-2-tzv-gold.json** - Most room for improvement (0.68 accuracy)
2. **metatuner-extract-all-case-info-gold.json** - Complex, many variables (0.57 accuracy)
3. **metatuner-1-schreiben-bank-gold.json** - Medium complexity (0.88 accuracy)

### For Regression Testing
1. **metatuner-30-ss-grouping-gold.json** - High baseline (0.99 accuracy)
2. **metatuner-classify-incoming-email-gold.json** - Simple, stable (0.96 accuracy)
3. **metatuner-extract-data-gold.json** - Small, high quality (0.93 accuracy)

### For Edge Case Testing
1. **metatuner-extract-all-case-info-gold.json** - Lowest accuracy (0.57)
2. **metatuner-receptionist-gold.json** - Entry point complexity (0.80)

---

## Technical Details

### Schema Compliance
All datasets validated against MetaTuner PromptDataset interface:

```typescript
interface PromptDataset {
  name: string;
  description: string;
  items: PromptDatasetItem[];
  metadata: {
    prompt: string;          // Original prompt template (shared)
    agent: string;           // Agent name (shared)
    node: string;            // Node name (shared)
    tier: string;            // Quality tier
    generated_at: string;
    source: string;
  };
  tags: string[];
}

interface PromptDatasetItem {
  id: string;                           // NodeTask UUID
  input: Record<string, any>;           // Varying input data (format varies by agent)
  // TZV Agent: { task, beamAgentOSTaskID, beamTaskId, beamTaskTimestamp, attachments }
  // Deal Breaker: { document, task_query }
  // Email Mgmt: { email_content }
  // Ops Case: { ADM_Email, Optional, ... }
  expectedOutput: Record<string, any>;  // { varName: expectedValue, ... }
  actualOutput: Record<string, any>;    // { varName: actualValue, ... }
  metadata?: {
    score: number;                      // TaskNodeAccuracy (0-1 scale)
  };
}
```

**✅ Input Parsing Achievements (2026-01-02)**:
- ALL 8 datasets have separated inputs (no filled prompts in input field)
- Prompt templates stored in `dataset.metadata.prompt` (shared across all items)
- Input data properly extracted and structured per agent format
- Ready for MetaTuner template optimization

### Export Command Reference

```bash
# Export additional node
python export_dataset.py --node "Node Name" --tier gold --verbose

# Export with limit
python export_dataset.py --node "Node Name" --tier gold --limit 100

# Export silver tier
python export_dataset.py --node "Node Name" --tier silver --verbose
```

---

## Next Steps

1. **Expand Collection**
   - Export silver/bronze tiers for wider coverage
   - Export low-accuracy nodes for stress testing

2. **MetaTuner Integration**
   - Load datasets into MetaTuner
   - Run optimization experiments
   - Compare before/after metrics

3. **Analysis**
   - Identify patterns in successful optimizations
   - Document best practices
   - Create export skill for reusability

---

*Generated by Project 07 - Airtable Test Dataset Builder*
