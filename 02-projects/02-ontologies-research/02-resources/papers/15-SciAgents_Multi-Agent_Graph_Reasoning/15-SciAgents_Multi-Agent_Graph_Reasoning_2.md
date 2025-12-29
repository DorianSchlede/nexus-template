<!-- Source: 15-SciAgents_Multi-Agent_Graph_Reasoning.pdf | Chunk 2/10 -->

|4|Expected Outcomes|~~The expected outcomes include a water contact angle greater than 150 degrees,~~<br>fracture toughness of at least 10 MPa<br>_√_<br>0_._5, self-cleaning capabilities, and detailed<br>AFM images showing the nanoscale hierarchical structure.|
|4|~~Novelty/Feasibility~~|~~7/8~~|
|5|Research idea|Investigating the interaction between graphene and amyloid fbrils to create novel<br>bioelectronic devices with enhanced electrical properties.|
|5|Hypothesis|~~Binding of graphene to amyloid fbrils will result in a composite material with~~<br>superior electrical conductivity and stability, which can be further optimized through<br>engineered gene circuits that regulate the expression, secretion, and assembly of<br>amyloid-forming proteins.|
|5|Expected Outcomes|~~The expected outcomes include high-performance composite materials, detailed~~<br>insights into binding mechanisms, optimized gene circuits, advanced bioelectronic<br>devices, and broader scientifc, technological, and societal impacts.|
|5|~~Novelty/Feasibility~~|~~8/7~~|


The randomly selected nodes for this experiment were “heat transfer performance” and “rhamphotheca” and the
generated graph consists of concepts such as “lamellar structure”, “biomaterials”, “microfluidic chips”, “keratin scales”,
and “biomimetic materials”. The proposed idea involves engineering the lamellar structure of biomaterials, inspired
by keratin scales, into microfluidic chips using soft lithography techniques to improve their mechanical behavior and
heat transfer efficiency under cyclic loading conditions. Expected outcomes of the resulting biomimetic microfluidic
chips include a 20-30% increase in heat transfer efficiency compared to conventional microfluidic chips (the lamellar


14


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**Figure 9: The plan developed by the planner agent in response to the query from the user to generate research**
**hypothesis from random keywords, as developed by the autonomous system.** The process begins with the selection
of random keywords, followed by the generation of a knowledge path that links the selected terms. Each term
along the path is defined by an ontologist, who also elaborates on the relationships between them. Based on these
definitions, a research proposal is crafted by a designated scientist. Subsequently, various specialized agents (hypothesis,
outcome, mechanism, design principles, unexpected properties, comparison, and novelty agents) each expand upon their
respective components of the proposal. The proposal is then critiqued by the critic_agent, who also suggests potential
improvements. As the final step, the novelty and feasibility of the research proposal are assessed using a dedicated
function, ensuring that the proposed ideas are both innovative and actionable.


structure of the biomimetic materials will facilitate efficient heat dissipation), enhanced mechanical stability under
cyclic loading conditions (the layered lamellar structure will provide enhanced mechanical strength and flexibility),
with a failure rate reduced by 15%, and superior biocompatibility (due to the use of biocompatible materials), making
them suitable for prolonged use in biomedical applications.


The design principles for biomimetic microfluidic chips focus on material selection, fabrication, integration, testing,
biocompatibility, modeling, and optimization. Materials such as PDMS and hydrogels, which mimic the lamellar
structure of keratin scales, are chosen for their biocompatibility and mechanical properties, with targeted thermal
conductivity and Young’s modulus ranges. Soft lithography is employed for fabrication, optimizing curing conditions
and structural characterization. Integration with microfluidic technology enhances heat transfer and mechanical stability,
with design optimization via CAD and simulations. Testing includes mechanical and heat transfer assessments, while
biocompatibility is evaluated through in vitro and in vivo tests. Finite Element Analysis (FEA) and Computational
Fluid Dynamics (CFD) simulations help model heat transfer and fluid flow, guiding iterative design optimization based
on performance metrics like heat transfer efficiency, mechanical stability, and biocompatibility.


Moreover, the model predicts that the biomimetic microfluidic chips may exhibit unexpected properties, such as
self-healing capabilities, adaptive heat transfer, enhanced fluid dynamics, and improved chemical resistance. These
properties are primarily attributed to the lamellar structure of the material, and the rationale behind them is summarized
in Table 5.


For the proposed research idea, the critic agent summarizes the overall research hypothesis covering the key features
and highlights strengths such as the innovative integration of biomimetic materials with microfluidic technology,
detailed mechanisms for performance, and potential biomedical applications. It also acknowledges the exploration of
self-healing and adaptive heat transfer. However, weaknesses include the complexity of the fabrication process, a lack
of preliminary data, and concerns about long-term biocompatibility. To improve, the agent recommends conducting
pilot studies, assessing scalability, and performing long-term biocompatibility testing. Moreover, the critic agent
suggests the most impactful scientific questions with molecular modeling ( `How does the lamellar structure of`
`biomimetic materials influence the heat transfer efficiency in microfluidic chips?` ) and synthetic biology and provides the pertinent key steps ( `Can biomimetic materials with a lamellar structure`
`be engineered to exhibit self-healing properties under mechanical stress?` ). These specific directions can be used as springboard for additional _in-situ_ data collection; in the case of the modeling context, this can
be implemented by incorporating a simulation engine, similar to what was done in recent work [37].


15


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**Table 5:** Predicted unexpected properties for biomimetic microfluidic chips. The data summarizes the property,
mechanism, and rationale.


**Unexpected Property** **Mechanism** **Rationale**



Self-Healing Properties The lamellar structure might enable
self-healing capabilities, where minor damages can be repaired autonomously, extending the lifespan
of the chips.


Adaptive Heat Transfer The heat transfer efficiency might
adapt dynamically based on the thermal load, similar to natural biological systems.


Enhanced Fluid Dynamics The lamellar structure might influence fluid dynamics within the microfluidic channels, leading to improved mixing and reduced pressure
drop.


Improved Chemical Resistance The lamellar structure might enhance
the chemical resistance of the microfluidic chips, making them suitable for a wider range of applications.



The layered structure can facilitate
the redistribution of stress and the
healing of minor cracks, similar to
natural biological systems.


The lamellar structure can facilitate
dynamic adaptation to varying thermal loads, enhancing the overall thermal management capabilities.


The layered structure can create
micro-scale vortices and enhance
fluid mixing, which is beneficial for
applications requiring efficient mixing of reagents.


The layered structure can act as a
barrier to chemical penetration, protecting the underlying material from
chemical degradation.



In the end, the assistant agent executes the tool to assess the novelty and feasibility of the proposed research idea
against the literature. It then returns a detailed analysis as depicted in Figure 10 suggesting that the proposed research
hypothesis has a high degree of novelty and a reasonable level of feasibility.


**3** **Conclusion**


We introduced a multi-agent AI framework designed to autonomously generate and refine research hypotheses by
leveraging LLMs and a comprehensive ontological knowledge graph 1, applied here in the context of biologically
inspired materials. Our results demonstrate the significant potential of integrating AI agents with specialized roles
to tackle the complex and interdisciplinary nature of scientific discovery, particularly in the domain of bio-inspired
materials. The automated system effectively navigated the intricate web of relationships within the knowledge graph,
generating diverse and novel hypotheses that align with unmet research needs. The proposed approach, harnessing
a modular, hierarchically organized (Figure 2) swarm of intelligence (Figure 1) similar to biological systems with
multiple iterations to model the process of negotiation a solution during the process of thinking and reflecting about
a problem, offers a much more nuanced reasoning approach than conventional zero-shot answers generated by AI
systems, as shown in Figure 11.


The ontological knowledge graph representation of data plays a crucial role in our approach, as it serves as the
foundational structure that guides the research idea generation, ensuring that the hypotheses proposed by the AI agents
are both informed by and rooted in a vast network of interconnected scientific concepts. By systematically navigating
this graph, our multi-agent system identifies and capitalizes on previously unrecognized relationships, aiming towards
the creation of highly-rated innovative ideas that are as feasible as they are groundbreaking. The incorporation of
assessment strategies is an important strategic aspect that reflects adversarial relationships commonly identified in
conventional research strategies, such as team-based efforts or peer-review. A notable feature was the finding that the
autonomous multi-agent system can develop sophisticated problem solving strategies (see, Figure 7) on its own. These
types of results are expected to improve as more powerful foundation models become available, especially with better
long-term planning and reasoning capabilities.


The multi-agent approach proved particularly effective in decomposing the scientific discovery process into manageable
subtasks, enabling a more systematic exploration of the knowledge landscape. By assigning distinct roles to each
agent—ranging from path generation and deep analysis to hypothesis formulation and critical review, we achieved
a thorough and rigorous development of research ideas. Our experiments showed that the system could consistently


16


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning





**Figure 10: The results of the novelty and feasibility analysis as performed by the assistant agent for the**
**“Biomimetic Microfluidic Chips” hypothesis, based on data collected using the Semantic Scholar API.** As the
analysis shows, the approach is considered unique due to its lack of direct matches in existing literature. Feasibility
is evaluated based on the plausibility of implementing these structures using soft lithography, though challenges in
mechanical behavior and heat transfer efficiency under cyclic loading were identified as potential hurdles requiring
experimental validation.


**Figure 11: SciAgents presents a framework for generative materials informatics, showcasing the iterative process**
**of ideation and reasoning driven by input data, questions, and context.** The cycle of ideation and reasoning
leads to predictive outcomes, offering insights into new material designs and properties. The visual elements on the
edges represent various data modalties such as images, documents, scientific data, DNA sequences, video content, and
microscopy, illustrating the diverse sources of information feeding into this process.


produce hypotheses with high novelty and feasibility, supported by contextually enriched data and iterative feedback
mechanisms that mirrored traditional scientific methodologies. The incorporation of specific priority modeling and
simulation tasks, for instance, offers direct pathways to incorporate additional mechanisms to solicit new physics-based
data (e.g. by running Density Functional Theory models, molecular dynamics, finite element/difference solvers,
etc.) [37, 38]. As such, the approach presented here offers significant potential in not only developing research questions
but also expanding the set of first-principles sourced data. If deployed at scale, this can aid our quest to generate large
materials-focused datasets strategically expanding beyond what is currently know. Based on the execution efficacy, it is
possible to generate thousands or tens of thousands of individual results within days, which if filtered by a set of criteria


17


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


(e.g. novelty, feasibility, or how well it meets a target) can generate a high-efficacy innovation framework for generative
materials informatics.


One of the key contributions of this study is the demonstration of how AI-driven agents can autonomously generate,
critique, and refine scientific hypotheses, offering a scalable and efficient alternative to conventional research approaches.
The integration of tools to assess novelty against existing literature further strengthens the validity of the generated
hypotheses, ensuring that the system not only produces innovative ideas but also eliminates redundancies with prior
research. This capability positions the system as a powerful tool for accelerating discovery and fostering crossdisciplinary innovation.


In fields such as biological materials analysis, identifying common mechanisms that hold for a variety of systems and
that can be applied to solve challenging engineering problems, remains a major challenge. This work underscores
the potential of generative AI in potentially scaling the scientific process, opening new avenues for exploration and
discovery across various fields of study. As we can automate, and hence accelerate the generation of research ideas,
this multi-agent system paves the way for a future where AI could then contribute as an integral player in shaping the
direction and pace of scientific advancement.


Future work could explore a variety of additional directions, for instance, the addition of agents that are able to conduct
experimentation or solicit data from simulation studies. The modular approach provides a flexible strategy to accomplish
this. Hence, we believe that the framework presented here offers a blueprint for next-generation of AI-driven research
tools, capable of synthesizing vast amounts of data into actionable insights, ultimately leading to breakthroughs that
might otherwise remain undiscovered.


**4** **Materials and methods**


**4.1** **Ontological knowledge graph**


We use a large graph generated as part of earlier work [6] in this research.


The graph utilized here includes 33,159 nodes and 48,753 edges and represents the giant component of the graph
generated from around 1,000 papers with 92 communities. We use the `BAAI/bge-large-en-v1.5` embedding model.


**4.2** **Heuristic pathfinding algorithm with random waypoints**


The algorithm presented in this work combines heuristic-based pathfinding with node embeddings and randomized
waypoints to discover diverse paths in a graph. The primary goal is to find a path between a source and a target node by
estimating distances using node embeddings. The embeddings are generated using a pre-trained model and are crucial
for the heuristic function, which estimates the distance between the current node and the target node. By relying on these
embeddings, the algorithm adapts to the topological structure of the graph, allowing it to effectively traverse complex
networks. Additionally, the algorithm uses a modified version of Dijkstra’s algorithm that introduces a randomness
factor to the priority queue, creating paths that are not strictly deterministic [45]. We chose the randomness factor to be
0.2 in our experiments.


An additional feature of the algorithm is the introduction of random waypoints to diversify the pathfinding process.
These waypoints are selected from neighboring nodes that are not part of the initial path, enabling the algorithm to
explore alternative routes. The randomization factor controls the balance between heuristic-driven search and stochastic
exploration, making it flexible for different use cases. After the path is found, a subgraph consisting of the path nodes
and their second-hop neighbors is generated, providing a broader context for the discovered route. The resulting paths
are then used as substrate for graph reasoning.


The overall approach is as follows:


18


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning



**4.3** **Graph reasoning**


**4.3.1** **Initial ideation**


The initial step in the approach develops a scientific hypothesis based on a knowledge graph derived from a heuristic
path in a given graph _G_ as described in Section 4.2. Here the graph _G_ represents a set of interconnected nodes, where
each node can represent an entity or concept, and edges represent relationships between these nodes. The algorithm
begins by identifying two key nodes, `keyword_1` and `keyword_2`, which can either be explicitly specified or randomly
selected from _G_ . If the `shortest_path` flag is set to `True`, the function computes the shortest path between these
nodes by using embeddings to estimate the best-fitting nodes, leveraging a pre-existing function called `find_path` . If
`shortest_path` is set to `False`, a heuristic pathfinding approach is employed, which incorporates randomization and
potentially random waypoints to explore more diverse paths. The graph structure is used not only for identifying the
connectivity between the nodes but also for guiding the algorithm’s search for the most relevant or exploratory paths
based on the node embeddings.


Once a path between `keyword_1` and `keyword_2` is established, the function constructs a knowledge graph from
the path and its relationships. This knowledge graph consists of the nodes traversed and the relationships (edges)


19


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


between them. The graph’s structure is vital as it is used to form the input for a generative model, which expands on the
graph’s nodes and relationships by providing definitions and explanations. The function also generates a novel research
hypothesis by analyzing the graph, synthesizing a hypothesis based on the relationships and concepts discovered along
the path. The structure of the graph helps to frame the scientific inquiry, with the hypothesis leveraging the graph’s
connections to predict outcomes, explore mechanisms, and propose innovative ideas. This output is formatted as a JSON
object with fields like `“hypothesis”`, `“outcome”`, and `“design_principles”`, each reflecting different aspects of
the potential research grounded in the graph’s topology.


A key aspect of the process is the use of natural language generation to dynamically expand on the concepts represented
by the nodes and edges of the knowledge graph. For each node, the generative model provides detailed definitions and
explanations of the scientific concepts it represents. The relationships between the nodes, represented by the edges,
are also expanded to give context to how these concepts are interconnected. This approach not only builds a deeper
understanding of individual components of the graph but also enhances the user’s ability to interpret the complex
interrelations between them, thereby setting the foundation for novel scientific inquiry. The response generated by the
model includes comprehensive descriptions of these relationships, ensuring that the resulting graph becomes a robust
substrate for knowledge synthesis.


After the knowledge graph is expanded, the algorithm generates a structured scientific hypothesis that leverages each
of the nodes and relationships in the graph. The output, in JSON format, provides key fields such as `"mechanisms"`,
`"unexpected_properties"`, and `"comparison"`, offering a highly detailed analysis. The `"mechanisms"` field
discusses predicted chemical, biological, or physical interactions, while `"unexpected_properties"` anticipates
emergent behaviors from novel combinations of concepts in the graph. This comprehensive hypothesis formulation
process allows for the exploration of unexplored areas of study, providing an innovative and grounded approach to
scientific discovery based on the structure of the graph and its conceptual relationships.


**4.3.2** **Expansion of the initial concepts**


The final phase of the methodology focuses on leveraging the expanded research concept to identify key scientific
questions and prioritize actionable research directions, particularly in the domains of molecular modeling and synthetic
biology. This phase employs a generative model to analyze the complete research document, which includes the
knowledge graph, expanded concepts, and critical reviews, with the goal of extracting the most impactful scientific
questions. These questions are then further expanded into detailed experimental and simulation plans, or other specific
aspects that a user wants to explore in detail.


Using the JSON developed as described in Section 4.3.1 we conduct several systematic steps.


**Step 1: Prompt-Driven Expansion of Key Research Aspects**


The next phase involves systematically expanding specific aspects of the hypothesis using a series of targeted prompts.
For each aspect of the research, a detailed prompt is constructed to critically assess and improve the scientific content of
that aspect. The primary aspects are drawn from the JSON dictionary, where we iterate over all elements in that data
structure.


The following steps summarize how the model expands each research aspect:


    - A prompt is created for each field in the JSON data structure, asking the model to **expand upon the original**
**content** by adding quantitative details such as chemical formulas, material properties, or specific experimental
methods.


The model is also instructed to provide a step-by-step rationale for the proposed scientific improvements.

    - For example, the prompt format includes:

```
      Expand on the following aspect: {field}.
      Critically assess the original content, add specifics, such as chemical formulas,
      sequences, microstructures, and rational improvements:
      {JSON_dictionary[field]}

```

   - The model generates expanded content under a heading such as `### Expanded Mechanisms` or `###`
`Expanded Outcomes` . Each response is added to `res_data_expanded` to track the expanded fields.

    - The iterative process is repeated for each of the first seven fields in `res_data`, ensuring that every major
aspect of the research concept is thoroughly evaluated and improved upon.


20


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**Step 2: Compilation and Summary of Expanded Content**


After the expansion phase, the system compiles the results into a structured document, starting with the original
knowledge graph and hypothesis, followed by the expanded research aspects. This forms a cohesive research narrative.
The complete document includes sections such as:

```
# Research concept between {start_node} and {end_node}
### KNOWLEDGE GRAPH:
{path_string}

### EXPANDED GRAPH:
{res_data[’expanded’]}

### PROPOSED RESEARCH:
{formatted_text}

### EXPANDED DESCRIPTIONS:
{expanded_text}

```

**Step 3: Scientific Critique and Review**


Following the expansion, a prompt is issued to the model to **critically review the entire document** . The review is
designed to evaluate both the strengths and weaknesses of the proposed research and to suggest improvements. This
step is crucial in ensuring that the expanded content is scientifically rigorous and logical. The prompt asks for:

```
Provide a thorough critical scientific review with strengths, weaknesses, and suggested improvements.

```

The result is a critical review that is appended to the final document as `"SUMMARY, CRITICAL REVIEW, AND`
`IMPROVEMENTS"` .


**Step 4: Identification of Modeling and Experimental Priorities**


Finally, the model is prompted to identify the **most impactful scientific questions** related to molecular modeling and
synthetic biology.


Separate prompts are issued for each domain, asking the model to:


    - Identify a key research question that can be tackled using **molecular modeling**, and outline steps to conduct
such modeling, including any specific tools or techniques.

    - Similarly, for **synthetic biology**, the model is prompted to outline an experimental plan, detailing unique
aspects such as gene-editing protocols, biological sequences, or organism-specific techniques.


Examples of these prompts:

```
Identify the single most impactful scientific question that can be tackled with molecular modeling.
Outline key steps for conducting such modeling.

Identify the most impactful question for synthetic biology and provide an experimental setup.

```

The responses are appended to the final document under `"MODELING AND SIMULATION PRIORITIES"` and
`"SYNTHETIC BIOLOGY EXPERIMENTAL PRIORITIES"` .


**Final Document and Output**


The entire research concept, expanded and reviewed, is then compiled into a final document which is saved as both a
PDF and CSV file for further analysis. The final document contains:


    - The original knowledge graph and proposed research hypothesis.

    - Expanded descriptions of key research aspects.

    - A critical review of the proposal.

    - Research priorities for molecular modeling and synthetic biology.


This provides a comprehensive output that transitions the generated hypothesis into a detailed, actionable research plan.


21


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**4.4** **Agentic modeling**


We design AI agents using the general-purpose LLM GPT-4 family models. The automated multi-agent collaboration is
implemented in the AutoGen framework [46], an open-source ecosystem for agent-based AI modeling.


In our multi-agent system, the human agent is constructed using UserProxyAgent class from Autogen, and Assistant,
Planner, Ontologist, Scientist 1, Scientist 2, and Critic agents are created via AssistantAgent class from Autogen; and
the group chat manager is created using GroupChatManager class. Each agent is assigned a role through a profile
description included as system_message at their creation. The full profile of the agents is provided in Figure S2 for
the planner, Figure S3 for the assistant, Figure S4 for the Ontologist, Figure S5 for the Scientist 1, Figure S6 for the
Scientist 2, and Figure S7 for the Critic.


**4.5** **Function and tool design**


All the tools implemented in this work are defined as python functions. Each function is characterized by a name, a
description, and input properties which have a proper description.


**4.6** **Semantic Scholar analysis**


We use the Semantic Scholar API, an AI-powered search engine for academic resources, to search for related publications
using a set of keywords. To ensure a thorough assessment of the research idea, we have implemented a tool featuring an
AI agent named the “novelty assistant”, which calls the Semantic Scholar API three times using different combinations
of keywords selected based on the research hypothesis. The profile of this agent is shown in Figure 12. For each
function call, the ten most relevant publications are returned, including their titles and abstracts. The novelty assistant
agent then thoroughly analyzes the abstracts and provides a review describing the novelty of the research idea.





**Figure 12: The profile of the novelty assistant LLM agent implemented in the automated multi-agent approach**
**for rating the novelty of the research idea.**


**Conflict of interest**


The author declares no conflict of interest.


**Data and code availability**


All data and codes are available on GitHub at `[https://github.com/lamm-mit/SciAgentsDiscovery](https://github.com/lamm-mit/SciAgentsDiscovery)` and `[https:](https://github.com/lamm-mit/GraphReasoning/)`
`[//github.com/lamm-mit/GraphReasoning/](https://github.com/lamm-mit/GraphReasoning/)` .


**Supplementary Materials**


Additional materials are provided as Supplementary Materials, including fully detailed output provided by the agentic
systems.


22


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**Acknowledgements**


We acknowledge support from USDA (2021-69012-35978), DOE-SERDP (WP22-S1-3475), ARO (79058LSCSB,
W911NF-22-2-0213 and W911NF2120130) as well as the MIT-IBM Watson AI Lab, MIT’s Generative AI Initiative,
and Google. Additional support from NIH (U01EB014976 and R01AR077793) is acknowledged. AG gratefully
acknowledges the financial support from the Swiss National Science Foundation (project #P500PT_214448).


**References**


[1] van der Zant, T., Kouw, M. & Schomaker, L. Generative artificial intelligence. _Studies in Applied Philosophy,_
_Epistemology and Rational Ethics_ **5**, 107–120 (2013). URL `[https://link.springer.com/chapter/10.](https://link.springer.com/chapter/10.1007/978-3-642-31674-6_8)`
`[1007/978-3-642-31674-6_8](https://link.springer.com/chapter/10.1007/978-3-642-31674-6_8)` .


[2] Guo, K., Yang, Z., Yu, C.-H. & Buehler, M. J. Artificial intelligence and machine learning in design of mechanical
materials. _Materials Horizons_ **8**, 1153–1172 (2021).


[3] Liu, Y., Zhao, T., Ju, W. & Shi, S. Materials discovery and design using machine learning. _Journal of Materiomics_
**3**, 159–177 (2017).


[4] Hu, Y. & Buehler, M. J. Deep language models for interpretative and predictive materials science. _APL Machine_
_Learning_ **1**, 010901 (2023). URL `[https://aip.scitation.org/doi/abs/10.1063/5.0134317](https://aip.scitation.org/doi/abs/10.1063/5.0134317)` .


[5] Matsumoto, M. Materials exploration: The next generation. _MRS Bulletin 2022_ 1–2 (2022). URL `[https:](https://link.springer.com/article/10.1557/s43577-022-00435-x)`
`[//link.springer.com/article/10.1557/s43577-022-00435-x](https://link.springer.com/article/10.1557/s43577-022-00435-x)` .


[6] Buehler, M. J. Accelerating scientific discovery with generative knowledge extraction, graph-based representation,
and multimodal intelligent graph reasoning. _Machine Learning: Science and Technology_ (2024). URL `[http:](http://iopscience.iop.org/article/10.1088/2632-2153/ad7228)`
`[//iopscience.iop.org/article/10.1088/2632-2153/ad7228](http://iopscience.iop.org/article/10.1088/2632-2153/ad7228)` .


[7] Zhang, Q. _et al._ Large-language-model-based ai agent for organic semiconductor device research. _Ad-_
_vanced Materials_ **36**, 2405163 (2024). URL `[https://onlinelibrary.wiley.com/doi/abs/10.1002/adma.](https://onlinelibrary.wiley.com/doi/abs/10.1002/adma.202405163)`
`[202405163](https://onlinelibrary.wiley.com/doi/abs/10.1002/adma.202405163)` . `[https://onlinelibrary.wiley.com/doi/pdf/10.1002/adma.202405163](https://onlinelibrary.wiley.com/doi/pdf/10.1002/adma.202405163)` .


[8] Lu, C. _et al._ The AI Scientist: Towards fully automated open-ended scientific discovery. _arXiv preprint_
_arXiv:2408.06292_ (2024).


[9] Ng, W. L., Goh, G. L., Goh, G. D., Ten, J. S. J. & Yeong, W. Y. Progress and opportunities for machine
learning in materials and processes of additive manufacturing. _Advanced Materials_ **36**, 2310006 (2024). URL
`[https://onlinelibrary.wiley.com/doi/abs/10.1002/adma.202310006](https://onlinelibrary.wiley.com/doi/abs/10.1002/adma.202310006)` . `[https://onlinelibrary.](https://onlinelibrary.wiley.com/doi/pdf/10.1002/adma.202310006)`
`[wiley.com/doi/pdf/10.1002/adma.202310006](https://onlinelibrary.wiley.com/doi/pdf/10.1002/adma.202310006)` .


[10] Lei, G., Docherty, R. & Cooper, S. J. Materials science in the era of large language models: a perspective. _Digital_
_Discovery_ (2024).


[11] OpenAI. GPT-4 technical report (2024). URL `[https://arxiv.org/abs/2303.08774](https://arxiv.org/abs/2303.08774)` . `2303.08774` .


[12] Vaswani, A. _et al._ Attention is all you need. _Advances in neural information processing systems_ **30** (2017).


[13] Wei, J. _et al._ Emergent abilities of large language models. _arXiv preprint arXiv:2206.07682_ (2022).


[14] Touvron, H. _et al._ Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_
(2023).


[15] Teubner, T., Flath, C. M., Weinhardt, C., van der Aalst, W. & Hinz, O. Welcome to the era of chatgpt et al. the
prospects of large language models. _Business & Information Systems Engineering_ **65**, 95–101 (2023).


[16] Zhao, W. X. _et al._ A survey of large language models. _arXiv preprint arXiv:2303.18223_ (2023).


[17] Chowdhery, A. _et al._ Palm: Scaling language modeling with pathways. _Journal of Machine Learning Research_
**24**, 1–113 (2023).


[18] Gunasekar, S. _et al._ Textbooks are all you need. _arXiv preprint arXiv:2306.11644_ (2023).


[19] Jiang, A. Q. _et al._ Mistral 7b. _arXiv preprint arXiv:2310.06825_ (2023).


[20] Girotra, K., Meincke, L., Terwiesch, C. & Ulrich, K. T. Ideas are dimes a dozen: Large language models for idea
generation in innovation. _Available at SSRN 4526071_ (2023).


[21] Buehler, M. J. Generative retrieval-augmented ontologic graph and multi-agent strategies for interpretive large
language model-based materials design. _ACS Engineering AU_ (2023). URL `[https://doi.org/10.1021/](https://doi.org/10.1021/acsengineeringau.3c00058)`
`[acsengineeringau.3c00058](https://doi.org/10.1021/acsengineeringau.3c00058)` .


23


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


[22] Jablonka, K. M. _et al._ 14 examples of how llms can transform materials science and chemistry: a reflection on a
large language model hackathon. _Digital Discovery_ **2**, 1233–1250 (2023).

[23] M. Bran, A. _et al._ Augmenting large language models with chemistry tools. _Nature Machine Intelligence_ 1–11
(2024).

[24] Luu, R. K. & Buehler, M. J. Bioinspiredllm: Conversational large language model for the mechanics of biological
and bio-inspired materials. _Advanced Science_ **11**, 2306724 (2024).

[25] Lu, W., Luu, R. K. & Buehler, M. J. Fine-tuning large language models for domain adaptation: Exploration of
training strategies, scaling, model merging and synergistic capabilities (2024). URL `[https://arxiv.org/abs/](https://arxiv.org/abs/2409.03444)`
`[2409.03444](https://arxiv.org/abs/2409.03444)` . `2409.03444` .

[26] Buehler, M. J. Cephalo: Multi-modal vision-language models for bio-inspired materials analysis and design.
_Advanced Functional Materials_ **n/a**, 2409531. URL `[https://onlinelibrary.wiley.com/doi/abs/10.](https://onlinelibrary.wiley.com/doi/abs/10.1002/adfm.202409531)`
`[1002/adfm.202409531](https://onlinelibrary.wiley.com/doi/abs/10.1002/adfm.202409531)` . `[https://onlinelibrary.wiley.com/doi/pdf/10.1002/adfm.202409531](https://onlinelibrary.wiley.com/doi/pdf/10.1002/adfm.202409531)` .

[27] Wei, J. _et al._ Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural_
_information processing systems_ **35**, 24824–24837 (2022).

[28] White, J. _et al._ A prompt pattern catalog to enhance prompt engineering with chatgpt. _arXiv preprint_
_arXiv:2302.11382_ (2023).

[29] Zhou, Y. _et al._ Large language models are human-level prompt engineers. _arXiv preprint arXiv:2211.01910_
(2022).

[30] Sun, J. _et al._ Think-on-graph: Deep and responsible reasoning of large language model with knowledge graph.
_arXiv preprint arXiv:2307.07697_ (2023).

[31] Shetty, P. _et al._ A general-purpose material property data extraction pipeline from large polymer corpora using
natural language processing. _npj Computational Materials_ **9**, 52 (2023).

[32] Pan, S. _et al._ Unifying large language models and knowledge graphs: A roadmap. _IEEE Transactions on_
_Knowledge and Data Engineering_ (2024).

[33] Dagdelen, J. _et al._ Structured information extraction from scientific text with large language models. _Nature_
_Communications_ **15**, 1418 (2024).

[34] Schilling-Wilhelmi, M. _et al._ From text to insight: Large language models for materials science data extraction.
_arXiv preprint arXiv:2407.16867_ (2024).

[35] Ni, B. & Buehler, M. J. MechAgents: Large language model multi-agent collaborations can solve mechanics
problems, generate new data, and integrate knowledge. _Extreme Mechanics Letters_ **67**, 102131 (2024).

[36] Stewart, I. & Buehler, M. Molecular analysis and design using multimodal generative artificial intelligence via
multi-agent modeling. _ChemRxiv, 10.26434/chemrxiv-2024-nwm7n_ (2024).

[37] Ghafarollahi, A. & Buehler, M. J. ProtAgents: Protein discovery via large language model multi-agent collaborations combining physics and machine learning. _Digital Discovery_ 1389–1409 (2024).

[38] Ghafarollahi, A. & Buehler, M. J. Atomagents: Alloy design and discovery through physics-aware multi-modal
multi-agent artificial intelligence. _arXiv preprint arXiv:2407.10022_ (2024).

[39] Giesa, T., Spivak, D. & Buehler, M. Category theory based solution for the building block replacement problem in
materials design. _Advanced Engineering Materials_ **14** (2012).

[40] Spivak, D., Giesa, T., Wood, E. & Buehler, M. Category theoretic analysis of hierarchical protein materials and
social networks. _PLoS ONE_ **6** (2011).

[41] Wu, Q. _et al._ AutoGen: Enabling next-gen llm applications via multi-agent conversation framework. _arXiv_
_preprint arXiv:2308.08155_ (2023).

[42] Wu, Y., Yue, T., Zhang, S., Wang, C. & Wu, Q. Stateflow: Enhancing llm task-solving through state-driven
workflows (2024). `2403.11322` .

[43] Wu, Y. _et al._ An empirical study on challenging math problem solving with gpt-4. In _ArXiv preprint_
_arXiv:2306.01337_ (2023).

[44] OpenAI API. URL `[https://openai.com/blog/openai-api](https://openai.com/blog/openai-api)` .

[45] Dijkstra, E. W. A note on two problems in connexion with graphs. _Numerische Mathematik_ **1**, 269–271 (1959).

[46] Wu, Q. _et_ _al._ Autogen: Enabling next-gen LLM applications via multi-agent conversation.
_https://arxiv.org/abs/2308.08155_ (2023).


24


**Supplementary Materials**

## **SciAgents: Automating Scientific Discovery through Multi-Agent** **Intelligent Graph Reasoning**


Alireza Ghafarollahi and Markus J. Buehler


**Correspondence:** `mbuehler@MIT.EDU`


**Figure S1: Different strategies for path sampling.** Left: Identifying multiple paths between two pretermined concepts.
Right: Selection of random pairs of concepts, resulting in diverse ideation processes through an unbiased selection
process.





**Figure S2: The profile of the Planner LLM agent implemented in the automated multi-agent approach for**
**automated scientific discovery.**





**Figure S3: The profile of the Assistant LLM agent implemented in the automated multi-agent approach for**
**automated scientific discovery.**


**Figure S4: The profile of the Ontologist LLM agent implemented in the automated multi-agent approach for**
**automated scientific discovery.**


**Figure S5: The profile of the Scientist 1 LLM agent implemented in the automated multi-agent approach for**
**automated scientific discovery.**


**Figure S6: The profile of the Scientist 2 LLM agent implemented in the first proposed multi-agent approach for**
**automated scientific discovery.**


**Figure S7: Profile of the Critic LLM agent implemented in the automated multi-agent approach for automated**
**scientific discovery.**


**S1** **Research idea created by our multi-agent approach based on pre-programmed**
**interactions using the knowledge graph between ’silk’ and ’energy-intensive’.**


**Research concept between 'silk' and 'energy-intensive'**


**KNOWLEDGE GRAPH:**


silk -- provide functionalities -- biological materials -- can be integrated -- novel functionalities -- can be integrated -- biological materials -- uses for creating -- low-temperature processing -uses for creating -- biological materials -- have -- multi-scale organization -- have -- biological materials -- provide functionalities -- dandelion -- provide functionalities -- biological materials -can guide nanoscale organization via -- pigments -- do not use -- insects -- are -- energy-intensive


**EXPANDED GRAPH:**


Here is an analysis of the concepts and relationships in the graph:


**Definitions:**


1. **Silk** : A natural protein fiber produced by certain insects, most notably silkworms, which is used to create textiles and other materials due to its strength, flexibility, and

biocompatibility.
2. **Biological materials** : Substances that are produced by living organisms, including proteins, polysaccharides, and other complex molecules, which can be used in various applications

due to their unique properties.
3. **Novel functionalities** : New and innovative features or capabilities that are not typically found in existing materials or systems.
4. **Low-temperature processing** : Manufacturing or synthesis methods that occur at relatively low temperatures, which can be beneficial for preserving the integrity of sensitive

materials.
5. **Multi-scale organization** : The hierarchical structuring of materials at various scales, from the molecular level to the macroscopic level, which can influence their properties and

functionalities.
6. **Dandelion** : A common flowering plant known for its distinctive yellow flowers and seed heads, which has various uses in traditional medicine and as a food source.
7. **Pigments** : Substances that provide color to materials by absorbing certain wavelengths of light and reflecting others.
8. **Insects** : A class of invertebrates within the arthropod phylum, characterized by a three-part body, compound eyes, and six legs.
9. **Energy-intensive** : Processes or activities that require a significant amount of energy to perform.


**Relationships:**


1. **Silk -- provide functionalities -- biological materials** : Silk, as a biological material, offers various functionalities such as high tensile strength, elasticity, and biocompatibility,

making it useful in textiles, medical sutures, and other applications.
2. **Biological materials -- can be integrated -- novel functionalities** : Biological materials can be engineered or combined with other substances to introduce novel functionalities,

such as enhanced mechanical properties, self-healing capabilities, or responsive behaviors.
3. **Novel functionalities -- can be integrated -- biological materials** : The integration of novel functionalities into biological materials can lead to the development of advanced

materials with unique properties, such as bio-inspired adhesives or smart textiles.
4. **Biological materials -- uses for creating -- low-temperature processing** : Biological materials often require low-temperature processing techniques to maintain their structural

integrity and functional properties, which is crucial for applications in biotechnology and materials science.
5. **Low-temperature processing -- uses for creating -- biological materials** : Low-temperature processing methods are employed to fabricate or modify biological materials without

degrading their sensitive components, enabling the production of high-quality biomaterials.
6. **Biological materials -- have -- multi-scale organization** : Biological materials exhibit multi-scale organization, meaning their structure is organized at multiple levels, from the

molecular to the macroscopic, which contributes to their unique mechanical and functional properties.
7. **Multi-scale organization -- have -- biological materials** : The multi-scale organization inherent in biological materials is a key factor in their performance, influencing properties

such as strength, flexibility, and responsiveness.
8. **Biological materials -- provide functionalities -- dandelion** : Dandelions, as biological materials, offer functionalities such as medicinal properties, nutritional value, and ecological

benefits, which can be harnessed for various applications.
9. **Dandelion -- provide functionalities -- biological materials** : The dandelion plant itself provides functionalities that can be considered biological materials, such as latex for rubber

production and compounds with therapeutic effects.
10. **Biological materials -- can guide nanoscale organization via -- pigments** : Biological materials can influence the nanoscale organization of pigments, leading to the creation of

materials with specific optical properties, such as structural colors found in butterfly wings.
11. **Pigments -- do not use -- insects** : Pigments in biological materials can achieve coloration without relying on insects, instead using structural or chemical means to produce vibrant

colors.
12. **Insects -- are -- energy-intensive** : The production of materials by insects, such as silk, can be energy-intensive, requiring significant metabolic energy to produce the raw materials

and construct the final product.


**PROPOSED RESEARCH/MATERIAL:**


**Hypothesis**


Integrating silk-derived biological materials with dandelion-based pigments through low-temperature processing to create multi-scale organized, energy-efficient, and structurally colored
biomaterials with novel functionalities for advanced optical and mechanical applications.


**Outcome**


The research is expected to yield a new class of biomaterials that exhibit enhanced mechanical strength (up to 1.5 GPa tensile strength), vibrant structural colors (reflectance peaks at specific
wavelengths, e.g., 450 nm for blue), and energy-efficient production processes (reducing energy consumption by 30% compared to traditional silk production). These materials could be used in
smart textiles, bio-inspired adhesives, and eco-friendly coatings.


**Mechanisms**


1. Silk proteins will be extracted and processed at low temperatures (below 50Â°C) to preserve their structural integrity. 2. Dandelion-derived pigments will be integrated into the silk

matrix, guided by the natural multi-scale organization of the silk fibers. 3. The pigments will self-assemble into nanoscale structures, creating structural colors through interference and
diffraction. 4. The resulting composite material will exhibit enhanced mechanical properties due to the hierarchical organization of silk and the reinforcing effect of the pigments.


**Design Principles**


1. Utilize low-temperature processing to maintain the biocompatibility and structural integrity of silk proteins. 2. Leverage the natural multi-scale organization of silk to guide the

self-assembly of dandelion-derived pigments. 3. Optimize the concentration and distribution of pigments to achieve desired optical properties. 4. Engineer the composite
material to balance mechanical strength and flexibility by controlling the hierarchical structuring at multiple scales. 5. Ensure energy-efficient production by minimizing the
metabolic energy required for silk production and pigment extraction.


**Unexpected Properties**


1. The composite material may exhibit self-healing properties due to the dynamic nature of the silk-pigment interactions. 2. The structural colors could change in response to

environmental stimuli (e.g., humidity, temperature), leading to smart, responsive materials. 3. The integration of dandelion-derived pigments may introduce additional functionalities,
such as UV protection or antimicrobial properties, due to the bioactive compounds present in dandelions.


**Comparison**


Compared to traditional silk materials, the proposed composite material will have significantly improved mechanical strength (up to 1.5 GPa vs. 0.5-1.0 GPa) and vibrant structural colors
without the need for synthetic dyes. Unlike conventional energy-intensive silk production, the low-temperature processing and use of dandelion pigments will reduce energy consumption by
approximately 30%. Additionally, the multi-scale organization will provide superior performance compared to single-scale materials.


**Novelty**


The proposed research advances existing knowledge by combining silk and dandelion-derived pigments to create a new class of biomaterials with unique optical and mechanical properties. The
use of low-temperature processing and multi-scale organization represents a novel approach to material design, offering energy-efficient production and enhanced functionalities. This
interdisciplinary integration of biological materials, structural coloration, and energy efficiency opens new avenues for sustainable and advanced material applications.


**EXPANDED DESCRIPTIONS:**


**Expanded Hypothesis**


Integrating silk-derived biological materials with dandelion-based pigments through low-temperature processing (below 50Â°C) to create multi-scale organized, energy-efficient, and
structurally colored biomaterials with novel functionalities for advanced optical and mechanical applications. The integration aims to leverage the hierarchical organization of silk fibroin
(C15H25N5O6) and the unique optical properties of dandelion-derived flavonoids (e.g., luteolin, C15H10O6) to achieve enhanced mechanical strength, vibrant structural colors, and reduced
energy consumption.


**Rationale and Step-by-Step Reasoning:**


1. **Silk Protein Extraction and Processing** :


**Rationale** : Silk fibroin is known for its remarkable mechanical properties and biocompatibility. Preserving its structural integrity during processing is crucial for maintaining
these properties.
**Step-by-Step** :

Extract silk fibroin from Bombyx mori cocoons using a degumming process with a mild alkaline solution (e.g., 0.02 M Na2CO3) at 90Â°C for 30 minutes.
Dissolve the degummed silk in a 9.3 M LiBr solution at 60Â°C for 4 hours.
Dialyze the silk solution against distilled water for 72 hours to remove LiBr, resulting in an aqueous silk fibroin solution.


2. **Dandelion-Derived Pigment Integration** :


**Rationale** : Dandelion pigments, particularly flavonoids like luteolin, exhibit strong UV absorption and potential antimicrobial properties. Their integration into the silk matrix
can enhance the material's functionality.
**Step-by-Step** :

Extract dandelion pigments using ethanol (70% v/v) at room temperature for 24 hours.
Concentrate the pigment extract using rotary evaporation at 40Â°C.
Mix the concentrated pigment extract with the silk fibroin solution at varying concentrations (e.g., 0.1%, 0.5%, 1% w/v) to study the effect on optical and mechanical
properties.


3. **Low-Temperature Processing** :


**Rationale** : Low-temperature processing (below 50Â°C) is essential to maintain the biocompatibility and structural integrity of silk proteins and to facilitate the self-assembly of
pigments.
**Step-by-Step** :

Cast the silk-pigment mixture into molds and allow it to dry at room temperature.
Post-process the dried films by annealing at 40Â°C in a humid environment (70% relative humidity) for 24 hours to induce Î²-sheet formation in silk fibroin, enhancing
mechanical strength.


4. **Multi-Scale Organization and Structural Coloration** :


**Rationale** : The hierarchical organization of silk fibroin can guide the self-assembly of dandelion pigments into nanoscale structures, creating structural colors through
interference and diffraction.
**Step-by-Step** :

Characterize the microstructure of the composite material using scanning electron microscopy (SEM) and transmission electron microscopy (TEM).
Analyze the optical properties using UV-Vis spectroscopy to identify reflectance peaks corresponding to structural colors (e.g., 450 nm for blue).
Use atomic force microscopy (AFM) to study the nanoscale organization of pigments within the silk matrix.


5. **Mechanical and Optical Property Analysis** :


**Rationale** : Quantifying the mechanical and optical properties is crucial to validate the hypothesis and assess the material's potential applications.
**Step-by-Step** :

Measure the tensile strength of the composite material using a universal testing machine (UTM) to determine if it reaches the target of 1.5 GPa.
Conduct dynamic mechanical analysis (DMA) to evaluate the material's flexibility and viscoelastic properties.
Perform environmental stability tests to assess the responsiveness of structural colors to stimuli such as humidity and temperature.


6. **Energy-Efficient Production** :


**Rationale** : Reducing energy consumption is a key goal of this research. Quantifying energy savings compared to traditional silk production methods is necessary.
**Step-by-Step** :

Monitor the energy consumption during each processing step using a power meter.
Compare the total energy consumption with that of conventional silk production, aiming for a 30% reduction.


**Modeling and Simulation Techniques:**
