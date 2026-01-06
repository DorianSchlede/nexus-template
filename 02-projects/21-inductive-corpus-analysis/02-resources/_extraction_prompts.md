# Unprimed Extraction Prompts

These prompts intentionally avoid theoretical framing.

---

## Prompt 1: Raw Entity Extraction

```
Read this paper excerpt carefully.

List every concept, entity, or term that the author:
1. Explicitly defines
2. Introduces as important
3. Uses as a category or type

For each, provide:
- The exact term used
- The author's definition (quote directly)
- Any examples given

Do NOT:
- Map to external frameworks
- Use terminology not in the text
- Interpret or categorize

Just extract what is there.
```

---

## Prompt 2: Raw Relationship Extraction

```
Read this paper excerpt carefully.

List every relationship the author describes between concepts:
1. What connects to what?
2. What verb or phrase describes the connection?
3. Is the relationship directional?

For each, provide:
- Source concept (author's term)
- Target concept (author's term)
- Relationship description (quote the connecting phrase)

Do NOT:
- Infer relationships not stated
- Use standard relationship names unless author uses them
- Add relationships from other sources

Just extract what is there.
```

---

## Prompt 3: Raw Problem/Gap Extraction

```
Read this paper excerpt carefully.

List every problem, limitation, or gap the author mentions:
1. What does the author say is difficult?
2. What do they say cannot be captured?
3. What future work do they identify?

For each, provide:
- The problem as stated (quote)
- The context (what were they discussing?)

Do NOT:
- Add problems you think exist
- Interpret vague statements as problems
- Bring in external critiques

Just extract what is there.
```

---

## Prompt 4: Raw Pattern Extraction (for AI/workflow papers)

```
Read this paper excerpt carefully.

List every pattern, architecture, or workflow the author describes:
1. What do they call it?
2. What are its components?
3. How do they say it works?

For each, provide:
- Pattern name (author's term)
- Components listed (quote)
- How it operates (quote description)

Do NOT:
- Rename patterns to standard terminology
- Add components not mentioned
- Combine with patterns from other sources

Just extract what is there.
```
