# Batch Extraction: Limitations (Batch 1 of 2)

Field: **limitations**
Description: What the ontology cannot capture (tacit knowledge, improvisation, etc.)

---

## Paper: 02-Knowledge_Graphs (Chunk 9)

### Pattern: Scalability Limitations for Reasoning
- **Source:** 02-Knowledge_Graphs (Chunk 9:19-31)
- **Description:** Knowledge graphs face fundamental scalability challenges particularly for deductive and inductive reasoning operations. These challenges are described as dimensions that will continue to require improvement but are unlikely to ever be completely "solved."
- **Quote:** "Aside from specific topics, more general challenges for knowledge graphs include _scalability_, particularly for deductive and inductive reasoning; _quality_, not only in terms of data, but also the models induced from knowledge graphs; _diversity_, such as managing contextual or multi-modal data; _dynamicity_, considering temporal or streaming data; and finally _usability_, which is key to increasing adoption. Though techniques are continuously being proposed to address precisely these challenges, they are unlikely to ever be completely 'solved'; rather they serve as dimensions along which knowledge graphs, and their techniques, tools, etc., will continue to mature."
- **Context:** This limitation is discussed in the context of future research directions for knowledge graphs, acknowledging that these are persistent challenges rather than problems with definitive solutions.

### Pattern: Data and Model Quality Limitations
- **Source:** 02-Knowledge_Graphs (Chunk 9:21-22)
- **Description:** Quality challenges exist not only in the underlying data but also in the models that are induced from knowledge graphs, suggesting that even sophisticated reasoning may be limited by imperfect inputs.
- **Quote:** "_quality_, not only in terms of data, but also the models induced from knowledge graphs"
- **Context:** Part of the broader discussion on general challenges facing knowledge graph technologies.

### Pattern: Contextual and Multi-Modal Data Diversity
- **Source:** 02-Knowledge_Graphs (Chunk 9:23-24)
- **Description:** Knowledge graphs struggle with managing diverse data types including contextual information and multi-modal data.
- **Quote:** "_diversity_, such as managing contextual or multi-modal data"
- **Context:** Listed as one of the general persistent challenges for knowledge graphs.

### Pattern: Temporal and Streaming Data Dynamicity
- **Source:** 02-Knowledge_Graphs (Chunk 9:24-25)
- **Description:** Handling temporal aspects and streaming data presents ongoing challenges that limit knowledge graph capabilities.
- **Quote:** "_dynamicity_, considering temporal or streaming data"
- **Context:** Part of the enumeration of fundamental challenges in knowledge graph research.

---

## Paper: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1)

### Pattern: LLM Domain Expertise Limitations
- **Source:** 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:87-92)
- **Description:** Despite their successes, LLMs face significant challenges in achieving domain specialist expertise without extensive specialized training. They produce inaccurate responses when dealing with questions outside their training scope, with concerns about accountability, explainability, and transparency.
- **Quote:** "Despite their successes, significant challenges persist regarding their ability to achieve the level of expertise possessed by domain specialists without extensive specialized training. Common issues include their tendency to produce inaccurate responses when dealing with questions that fall outside their initial training scope, and broader concerns about accountability, explainability, and transparency. These problems underscore the potential risks associated with the generation of misleading or even harmful content, requiring us to think about strategies that increase their problem-solving and reasoning capabilities."
- **Context:** This is framed as a challenge that motivates the development of multi-agent systems and in-context learning approaches to enhance LLM performance.

### Pattern: Single-Agent Complexity Limitations
- **Source:** 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:113-121)
- **Description:** Single LLM-based agents fall short for the complex demands of scientific discovery, which involves deep thinking, integration of diverse information, and sometimes conflicting information.
- **Quote:** "While single-LLM-based agents can generate more accurate responses when enhanced with well-designed prompts and context, they often fall short for the complex demands of scientific discovery. Creating new scientific insights involves a series of steps, deep thinking, and the integration of diverse, sometimes conflicting information, making it a challenging task for a single agent."
- **Context:** This limitation motivates the use of multi-agent systems where specialized agents collaborate to overcome individual agent limitations.

### Pattern: Human-Driven Research Constraints
- **Source:** 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:65-70)
- **Description:** Conventional human-driven research methods are constrained by the researcher's ingenuity and background knowledge, potentially limiting discovery to the bounds of human imagination. Human methods are also inadequate for exploring vast amounts of existing scientific data.
- **Quote:** "While these conventional approaches have led to breakthroughs throughout the history of science, they are constrained by the researcher's ingenuity and background knowledge, potentially limiting discovery to the bounds of human imagination. Additionally, conventional human-driven methods are inadequate for exploring the vast amount of existing scientific data to extrapolate knowledge toward entirely novel ideas specially for multi-disciplinary areas like bio-inspired materials design"
- **Context:** Presented as motivation for AI-assisted scientific discovery approaches.

### Pattern: Critic-Identified Limitations (Scalability, Environmental Impact, Data Gaps)
- **Source:** 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:527-529)
- **Description:** The critic agent identifies specific weaknesses including challenges with nanoscale integration, scalability concerns, environmental impacts of solvent use, and lack of quantitative data. Long-term stability under real-world conditions is also a concern.
- **Quote:** "Moreover, the critic identifies areas needing improvement, including challenges with nanoscale integration, scalability, environmental impacts of solvent use, and a lack of quantitative data. Concerns about the long-term stability of the material under real-world conditions are also raised."
- **Context:** These limitations are identified through the adversarial review process of the multi-agent system, demonstrating the system's self-critical capabilities.

---

## Paper: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 2)

### Pattern: Backbone LLM Generalizability Limitation
- **Source:** 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 2:10-20)
- **Description:** The KG-Agent method is limited by being tested only on LLaMA2-7B, requiring more experiments with comparable models like Mistral-7B or CodeLLaMA-7b to establish generalizability.
- **Quote:** "Although KG-Agent demonstrates remarkable performance across various complex factual question answering tasks, there are some limitations of our method. First, we only use the LLaMA2-7B as the backbone LLM, which has a strong capability after instruction tuning. Hence, more experiments are required to evaluate other LLMs with comparable parameter sizes, such as Mistral-7B (Jiang et al., 2023a) or CodeLLaMA-7b (Roziere et al., 2023)."
- **Context:** Explicitly stated in the paper's Limitations section.

### Pattern: Knowledge Source Type Limitation
- **Source:** 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 2:21-24)
- **Description:** The framework is limited to reasoning over knowledge graphs for factual questions and does not extend to other knowledge sources like databases or tables.
- **Quote:** "Second, we focus on reasoning over the KG to answer the factual questions. We should consider extending our framework to deal with more types of knowledge sources, _e.g.,_ databases or tables."
- **Context:** Explicitly stated in the paper's Limitations section, indicating a scope limitation of the current approach.

### Pattern: Evaluation Scenario Limitation
- **Source:** 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 2:25-28)
- **Description:** The method is only evaluated on factual question answering tasks based on KG, lacking evaluation on wider scenarios like data-to-text and formal-language-to-text.
- **Quote:** "Third, we only evaluate factual question answering tasks based on KG. Future work should include wider evaluation scenarios to evaluate the universality of our method, _e.g.,_ data-to-text and formal-language-to-text (Xie et al., 2022)."
- **Context:** Explicitly stated in the paper's Limitations section.

### Pattern: Discriminatory/Risky Response Filtering Limitation
- **Source:** 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 2:28-33)
- **Description:** Despite efforts to tune the LLM to answer based on KG information and avoid discriminatory/risky responses, additional rule-based methods are needed to post-process predictions and filter illegal responses.
- **Quote:** "Finally, we have tried our best to tune the LLM only to answer the questions based on the KG information, and avoid generating discriminatory and risky responses for user questions. However, we should add more rule-based methods to post-process the predictions and filter the illegal responses."
- **Context:** Explicitly stated in the paper's Limitations section, acknowledging safety and ethical concerns that cannot be fully addressed by the current approach.

---

## Paper: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1)

### Pattern: LLM Hallucination and Factual Incorrectness
- **Source:** 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:52-56)
- **Description:** LLMs lack genuine understanding of the real world, leading to outputs that may seem plausible but can be factually incorrect or hallucinated.
- **Quote:** "While LLMs excel at generating outputs based on patterns identified in their training data, they lack a genuine understanding of the real world. Consequently, their outputs might seem plausible on the surface, but can be factually incorrect or even _hallucinated_"
- **Context:** Presented as an inherent limitation of LLMs that motivates the exploration of multi-agent architectures.

### Pattern: Extended Reasoning Chain Consistency Limitation
- **Source:** 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:57-60)
- **Description:** Despite proficiency with vast textual information and rapid processing, LLMs struggle to maintain consistent logic across extended chains of reasoning, hindering deliberate, in-depth, iterative thought processes (slow thinking).
- **Quote:** "Moreover, despite their proficiency in handling vast amounts of textual information and their rapid processing and pattern recognition capabilities, LLMs struggle with maintaining consistent logic across extended chains of reasoning. This deficiency hinders their ability to engage in a deliberate, in-depth, and iterative thought process (aka _slow thinking_)"
- **Context:** This limitation is presented as a key motivation for multi-agent systems that can decompose complex tasks.

### Pattern: Complex and Interconnected Task Handling Limitation
- **Source:** 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:59-60)
- **Description:** As a result of reasoning limitations, LLMs encounter difficulties when handling more complex and interconnected tasks.
- **Quote:** "As a result, LLMs encounter difficulties when it comes to handling more complex and interconnected tasks"
- **Context:** Direct consequence of the extended reasoning chain consistency limitation.

### Pattern: Autonomy-Alignment Balancing Challenge
- **Source:** 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:83-91)
- **Description:** A central challenge for effective operation lies in finding the optimal balance between autonomy and alignment. High autonomy systems may stray from intended purposes, while highly aligned systems may lack flexibility for novel situations.
- **Quote:** "One of the central challenges for the effective operation of LLM-powered multi-agent architectures (as with many AI systems) lies in finding the optimal _balance between autonomy and alignment_. On the one hand, the systems should be aligned to the goals and intentions of human users; on the other hand, the systems should accomplish the user-prompted goal in a self-organizing manner. However, a system with high autonomy may handle complex tasks efficiently, but risks straying from its intended purpose if not sufficiently aligned, resulting in unexpected consequences and uncontrollable side effects. Conversely, a highly aligned system may adhere closely to its intended purpose but may lack the flexibility and initiative to respond adequately to novel situations."
- **Context:** Framed as a cross-cutting concern that traverses all architectural components and mechanisms.

### Pattern: User Goal-Intention Mismatch
- **Source:** 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:381-383)
- **Description:** The specified and prompted user goal might not exactly represent the user's intentions, resulting in unexpected consequences and uncontrollable side effects.
- **Quote:** "This especially proves challenging, since the specified and prompted user goal might not exactly represent the user's intentions, resulting in unexpected consequences and uncontrollable side effects."
- **Context:** Discussed as a challenge in balancing autonomy and alignment in LLM-powered multi-agent systems.

### Pattern: Existing Taxonomy Inadequacy
- **Source:** 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:94-96)
- **Description:** Existing taxonomies for autonomous systems and multi-agent systems fall short in providing means to categorize and understand challenges and architectural complexities posed by LLM-powered multi-agent systems.
- **Quote:** "However, existing taxonomies and analysis frameworks for autonomous systems and multi-agent systems fall short in providing means to categorize and understand these challenges and involved architectural complexities posed by LLM-powered multi-agent systems."
- **Context:** Presented as motivation for developing a new taxonomy specifically for LLM-powered multi-agent systems.

### Pattern: Pre-LLM Taxonomy Limitations
- **Source:** 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:286-293)
- **Description:** Previous multi-agent taxonomies were developed before LLMs and don't capture characteristic challenges associated with LLM-based multi-agent architectures. The advent of LLMs introduced a new degree of reasoning capabilities not accounted for in earlier frameworks.
- **Quote:** "While these taxonomies have contributed significantly to our understanding of communication protocols and agent constellation within multi-agent systems, they were developed prior to the advent of large language models (LLMs), and thus do not encapsulate the characteristic challenges associated with LLM-based multi-agent architectures. In this context, autonomous agents, also as members of multi-agent networks, often have been used as a kind of metaphor for intelligent and interacting components following rule-based communication protocols and bundling a set of specific skills to interact with their environment... LLMs have introduced a new degree of reasoning capabilities, enabling the creation of genuinely intelligent agents operating within collaborative networks in an autonomous manner."
- **Context:** Analysis of existing taxonomies in the related work section.

---

## Paper: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1)

### Pattern: Tree Structure Limitation on Reasoning
- **Source:** 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:59-61)
- **Description:** Tree of Thoughts (ToT) approaches fundamentally limit reasoning abilities within a prompt by imposing a rigid tree structure on the thought process.
- **Quote:** "Unfortunately, the ToT approaches still fundamentally limit the reasoning abilities within a prompt by imposing the rigid tree structure on the thought process."
- **Context:** Presented as motivation for developing Graph of Thoughts (GoT), which allows arbitrary graph structures for more flexible reasoning.

### Pattern: Chain-Based Thought Exploration Limitation
- **Source:** 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:63-72)
- **Description:** Chain-of-Thought and Tree-of-Thought approaches do not naturally enable complex networked thought patterns that humans use, such as merging ideas from different reasoning chains or forming recurrent patterns.
- **Quote:** "When working on a novel idea, a human would not only follow a chain of thoughts (as in CoT) or try different separate ones (as in ToT), but would actually form a more complex network of thoughts. For example, one could explore a certain chain of reasoning, backtrack and start a new one, then realize that a certain idea from the previous chain could be combined with the currently explored one, and merge them both into a new solution, taking advantage of their strengths and eliminating their weaknesses."
- **Context:** Illustrates the limitation of existing prompting schemes by contrasting with human reasoning patterns.

### Pattern: Graph-Enabled Transformations Not Expressible in CoT/ToT
- **Source:** 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:70-72)
- **Description:** Graph-enabled transformations that promise more powerful prompting are not naturally expressible with Chain-of-Thought or Tree-of-Thought approaches.
- **Quote:** "The corresponding _graph-enabled transformations_ bring a promise of more powerful prompting when applied to LLM thoughts, but they are not naturally expressible with CoT or ToT."
- **Context:** Directly states the limitation that GoT aims to address.

### Pattern: Low Volume in Tree-Based Reasoning
- **Source:** 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:743-753)
- **Description:** ToT has low volume (number of preceding thoughts that could have impacted a final thought) of O(log_k N), while GoT achieves volume N through aggregation capabilities.
- **Quote:** "CoT offers a large volume of up to _N_, but at the cost of a high latency of _N_. CoT-SC reduces the latency by a factor of _k_ (which corresponds to its branching factor), but it simultaneously decreases the volume by _k_ as well. ToT offers a latency of log_k N but also has low volume. GoT is the only scheme to come with both a low latency of log_k N and a high volume _N_. This is enabled by the fact that GoT harnesses aggregations of thoughts, making it possible to reach the final thought from any other intermediate thought in the graph decomposition."
- **Context:** Formal analysis comparing the latency-volume tradeoff of different prompting schemes.

---

## Paper: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1)

### Pattern: LLM Non-Deterministic Output Limitation
- **Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:67-68)
- **Description:** LLM outputs are inherently non-deterministic, making them unreliable for consistent behavior in applications requiring perfect reliability.
- **Quote:** "LLM outputs are inherently non-deterministic, making them unreliable for consistent behaviour."
- **Context:** Listed as one of the significant challenges with LLM-based code generation.

### Pattern: Security Vulnerability Introduction
- **Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:66-67)
- **Description:** LLM-based code generation tools like GitHub Copilot can introduce numerous security vulnerabilities into generated code.
- **Quote:** "For instance, GitHub Copilot can introduce numerous security vulnerabilities into generated code"
- **Context:** Cited as a concrete example of LLM code generation limitations.

### Pattern: Ethical Bias Reproduction
- **Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:68-69)
- **Description:** Generated code may reproduce ethically concerning biases, such as gender-related ones.
- **Quote:** "Furthermore, Huang et al. show that generated code may reproduce ethically concerning biases, such as gender-related ones."
- **Context:** Part of the discussion on challenges beyond hallucination in LLM code generation.

### Pattern: Hallucination/Confabulation Limitation
- **Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:64-65)
- **Description:** LLM-based code generation suffers from the well-known hallucination issue (confabulation).
- **Quote:** "significant challenges remain—extending even beyond the well-known hallucination issue (or more precisely: confabulation)"
- **Context:** Acknowledged as a known limitation that other challenges extend beyond.

### Pattern: Perfect Reliability Impossibility with Current LLM Architecture
- **Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:113-116)
- **Description:** The stochastic nature of LLMs makes output imperfect and unreliable. For blockchain smart contracts which require perfect reliability, this is a fundamental issue that cannot be overcome by current LLM architectures.
- **Quote:** "Due to the stochastic nature of LLMs, output remains imperfect and unreliable. While such performance may be acceptable in other contexts, blockchain is an unforgiving environment—on public blockchains developers should assume that any weakness will be exploited. As such, we believe this is a fundamental issue of the chosen approach to have LLMs generate smart contract code, which cannot be overcome by LLMs based on the current architectures."
- **Context:** Core finding of the empirical study on LLM-generated smart contracts.

### Pattern: Sub-Perfect F1 Score Inadequacy for Blockchain
- **Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:638-648)
- **Description:** Even achieving 98% F1 score would be inadequate for blockchain-based smart contracts, where the financial risks and immutable nature of transactions mean even small error rates could lead to significant vulnerabilities or losses.
- **Quote:** "F1 scores that do not reliably achieve 100% would not be suitable for this context. Say, the approaches would be improved to achieving an average F1 score of 98%; while this would be impressive in many domains, it falls short of the perfect reliability required for blockchain-based smart contracts. Given the financial risks and immutable nature of blockchain transactions, even such a 2% error rate could lead to significant vulnerabilities or losses, making such performance inadequate for real-world deployment. We do not see a way in which this fundamental issue could be resolved with current LLM architectures."
- **Context:** Discussion section analyzing the practical implications of benchmark results.

### Pattern: Confidentiality, Privacy, and Autonomy Concerns
- **Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:71-75)
- **Description:** Proprietary models raise concerns about confidentiality, privacy, and autonomy due to deployment on centralized platforms, which may not fit blockchain-based processes where decentralization is a goal.
- **Quote:** "Furthermore, proprietary models raise concerns about confidentiality, privacy, and autonomy (c.f. [4,18]). These AI models are often deployed on large, centralised platforms provided by hyperscalers like _AWS_, _Azure_, or _GCP_. Open-source models running on these platforms face the same security concerns. Relying on central deployments may not be a good fit for blockchain-based processes, where decentralisation is a goal"
- **Context:** Discussion of challenges specific to using LLMs in blockchain contexts.

### Pattern: Evaluation Challenge - Manual Inspection Requirement
- **Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:79-81)
- **Description:** Evaluation of LLM outputs poses a significant challenge as it often requires manual human investigation and large volumes of labelled or parallel data.
- **Quote:** "However, evaluation poses a significant challenge, as it often requires manual human investigation and large volumes of labelled or parallel data"
- **Context:** Motivation for developing an automated evaluation framework.

### Pattern: Rule-Based Transformation Tool Limitations
- **Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:54-57)
- **Description:** Traditional rule-based transformation tools for blockchain-based business process execution exhibit various limitations such as inflexibility in supported process modelling constructs, output targets, and blockchain-specific features.
- **Quote:** "These tools, however, exhibit various limitations such as in their flexibility, e.g., in terms of supported process modelling constructs, their supported output targets, or their support of blockchain-specific features."
- **Context:** Presented as motivation for exploring LLM-based approaches as alternatives, though LLMs have their own limitations.

---

## Summary of Limitation Patterns by Category

### Tacit Knowledge and Improvisation
- LLMs lack genuine understanding of the real world (18-Multi-Agent_Architecture)
- Domain expertise limitations without specialized training (15-SciAgents)
- Human-driven research constrained by individual imagination (15-SciAgents)

### Structural/Architectural Constraints
- Tree structure limits reasoning flexibility (19-Graph_of_Thoughts)
- Chain-based approaches cannot express networked thought patterns (19-Graph_of_Thoughts)
- Extended reasoning chain consistency problems (18-Multi-Agent_Architecture)
- Knowledge source type limitations (16-KG-Agent)

### Reliability and Consistency
- Non-deterministic LLM outputs (21-LLM_Smart_Contracts)
- Perfect reliability impossibility with current LLM architectures (21-LLM_Smart_Contracts)
- Hallucination/confabulation issues (18-Multi-Agent_Architecture, 21-LLM_Smart_Contracts)

### Scalability and Performance
- Scalability challenges for deductive/inductive reasoning (02-Knowledge_Graphs)
- Complex and interconnected task handling difficulties (18-Multi-Agent_Architecture)
- Single-agent complexity limitations (15-SciAgents)

### Data Quality and Diversity
- Data and model quality limitations (02-Knowledge_Graphs)
- Contextual and multi-modal data management challenges (02-Knowledge_Graphs)
- Temporal/streaming data dynamicity (02-Knowledge_Graphs)

### Safety and Ethics
- Security vulnerability introduction in code generation (21-LLM_Smart_Contracts)
- Ethical bias reproduction (21-LLM_Smart_Contracts)
- Discriminatory/risky response filtering gaps (16-KG-Agent)
- Confidentiality/privacy/autonomy concerns (21-LLM_Smart_Contracts)

### Alignment and Intent
- Autonomy-alignment balancing challenge (18-Multi-Agent_Architecture)
- User goal-intention mismatch (18-Multi-Agent_Architecture)
- Accountability, explainability, transparency concerns (15-SciAgents)
