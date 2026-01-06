# Synthesis Approach v2: Grounded Discovery

**Purpose**: Generate novel insights through pattern emergence, not hypothesis confirmation.

---

## Philosophy

> "The goal is NOT to prove that X exists across all papers.
> The goal IS to discover what actually exists and synthesize something new."

### Key Differences from v1

| v1 (Hypothesis Validation) | v2 (Grounded Discovery) |
|----------------------------|-------------------------|
| Test 8-entity hypothesis | Discover what entities emerge |
| Count papers supporting each entity | Map the actual landscape |
| Confirm Agent-Activity-Entity triad | See what triads/patterns appear |
| Map to predefined categories | Let categories emerge |
| Validation report | Synthesis of novel insights |

---

## Synthesis Workflow

### Phase 1: Raw Pattern Collection

**Input**: All 22 paper index.md files (v2 extractions)
**Process**:
1. Collect all `ontological_primitives` across papers
2. Collect all `structural_patterns`
3. Collect all `novel_concepts`
4. Collect all `gaps_and_tensions`

**Output**: Raw pattern inventory (no deduplication yet)

---

### Phase 2: Cluster Analysis

**Input**: Raw pattern inventory
**Process**:
1. Group similar primitives WITHOUT forcing predefined categories
2. Identify pattern families (triads, hierarchies, etc.)
3. Map concept genealogies (who cites/extends whom)
4. Note outliers and singletons

**Output**: Emergent clusters with member lists

**Key Question**: What clusters emerge naturally? Don't force 8 categories.

---

### Phase 3: Divergence Mapping

**Input**: Clusters + gaps_and_tensions
**Process**:
1. Where do frameworks DISAGREE on primitives?
2. What concepts appear in some but not others?
3. What semantic commitments conflict?
4. What gaps are consistent vs sporadic?

**Output**: Divergence map showing:
- Universal agreement (rare - note it!)
- Majority patterns (most frameworks agree)
- Contested territory (frameworks disagree)
- Orphan concepts (appear once)

---

### Phase 4: Gap Synthesis

**Input**: Divergence map + gaps_and_tensions
**Process**:
1. What's conspicuously ABSENT from all frameworks?
2. What's needed but not formalized?
3. Where do ALL frameworks fall short?
4. What would fill the gaps?

**Output**: Opportunity map for novel contributions

---

### Phase 5: Novel Synthesis

**Input**: All prior phases
**Process**:
1. Can we synthesize a NEW framework from emerging patterns?
2. What novel combinations are possible?
3. What primitives would address identified gaps?
4. What would a contribution to the field look like?

**Output**: Synthesis proposal (if warranted by data)

---

## Synthesis Report Structure

### 1. Methodology
- Discovery approach (not validation)
- Papers analyzed
- Extraction schema used

### 2. Emergent Taxonomy
- What primitive categories emerged?
- How many? (Don't force a number)
- What are the defining characteristics?
- Where did the expected categories NOT appear?

### 3. Pattern Catalog
- Structural patterns with frequency
- Variations and exceptions
- Genealogy of patterns

### 4. Divergence Map
- Where frameworks agree
- Where frameworks disagree
- Contested concepts
- Orphan concepts

### 5. Gap Analysis
- Universal gaps (all frameworks miss)
- Partial gaps (some address, some don't)
- Emerging gaps (AI era introduces new needs)

### 6. Surprises and Counter-Evidence
- What we expected but didn't find
- What we found but didn't expect
- Counter-examples to "obvious" patterns

### 7. Synthesis Opportunities
- Novel framework possibilities
- Integration opportunities
- Research directions

### 8. Grounded Conclusions
- What we can confidently claim
- What remains uncertain
- What requires further research

---

## Anti-Validation Checks

**Before finalizing synthesis, verify:**

- [ ] Did NOT count "papers supporting X" for predefined X
- [ ] Did NOT claim "universal" without actual universality
- [ ] DID note where expected patterns didn't appear
- [ ] DID preserve disagreement and tension
- [ ] DID include surprises section
- [ ] DID acknowledge limitations

---

## Example: How v2 Differs

### v1 Would Say:
> "The Agent-Activity-Entity triad was validated across 22/23 papers, confirming its universality as a foundational pattern."

### v2 Would Say:
> "A participation pattern involving some actor, some action, and some affected thing appeared in 18 papers, but with significant variation:
> - 6 papers used 3-element triads
> - 8 papers used 4+ element structures
> - 4 papers had fundamentally different structures (e.g., OCEL's object-centric model)
>
> The 'triad' is not universal - it's one pattern among several. OCEL's approach challenges the assumption that cases/processes are primary."

---

## Synthesis Quality Signals

### GOOD synthesis shows:
- Emergent categories (not predefined)
- Acknowledged disagreement
- Identified gaps
- Noted surprises
- Novel combinations
- Honest uncertainty

### WARNING signs:
- All papers "support" expected findings
- Universal claims without caveats
- No surprises section
- No gaps identified
- Categories match exactly what was hypothesized
- No novel synthesis proposed

---

## Output Files

| File | Purpose |
|------|---------|
| `_emergent_taxonomy.yaml` | Categories that emerged from data |
| `_pattern_catalog.yaml` | Structural patterns with frequency |
| `_divergence_map.yaml` | Agreement/disagreement matrix |
| `_gap_analysis.yaml` | What's missing |
| `_synthesis_opportunities.md` | Novel contribution ideas |
| `_synthesis_report_v2.md` | Full discovery report |

---

**Version**: 2.0 (Discovery-oriented)
**Date**: 2025-12-31
**Philosophy**: Discover, don't confirm. Synthesize, don't validate.
