<!-- Source: 15-SciAgents_Multi-Agent_Graph_Reasoning.pdf | Chunk 1/10 -->

## SCIAGENTS: AUTOMATING SCIENTIFIC DISCOVERY THROUGH
### MULTI-AGENT INTELLIGENT GRAPH REASONING [∗]

**Alireza Ghafarollahi**
Laboratory for Atomistic and Molecular Mechanics (LAMM)
Massachusetts Institute of Technology
77 Massachusetts Ave.
Cambridge, MA 02139, USA


**Markus J. Buehler**
Laboratory for Atomistic and Molecular Mechanics (LAMM)
Center for Computational Science and Engineering
Schwarzman College of Computing
Massachusetts Institute of Technology
77 Massachusetts Ave.
Cambridge, MA 02139, USA


Correspondence: `mbuehler@MIT.EDU`


**ABSTRACT**


A key challenge in artificial intelligence is the creation of systems capable of autonomously advancing
scientific understanding by exploring novel domains, identifying complex patterns, and uncovering
previously unseen connections in vast scientific data. In this work, we present SciAgents, an approach
that leverages three core concepts: (1) the use of large-scale ontological knowledge graphs to
organize and interconnect diverse scientific concepts, (2) a suite of large language models (LLMs)
and data retrieval tools, and (3) multi-agent systems with _in-situ_ learning capabilities. Applied to
biologically inspired materials, SciAgents reveals hidden interdisciplinary relationships that were
previously considered unrelated, achieving a scale, precision, and exploratory power that surpasses
traditional human-driven research methods. The framework autonomously generates and refines
research hypotheses, elucidating underlying mechanisms, design principles, and unexpected material
properties. By integrating these capabilities in a modular fashion, the intelligent system yields material
discoveries, critique and improve existing hypotheses, retrieve up-to-date data about existing research,
and highlights their strengths and limitations. Our case studies demonstrate scalable capabilities to
combine generative AI, ontological representations, and multi-agent modeling, harnessing a ‘swarm
of intelligence’ similar to biological systems. This provides new avenues for materials discovery and
accelerates the development of advanced materials by unlocking Nature’s design principles.


_**K**_ **eywords** Scientific AI _·_ Multi-agent system _·_ Large language model _·_ Natural language processing _·_ Materials
design _·_ Bio-inspired materials _·_ Knowledge graph _·_ Biological design


**1** **Introduction**


One of the grand challenges in the evolving landscape of scientific discovery is finding ways to model, understand,
and utilize information mined from diverse sources as a foundation for further research progress and new science
discovery. Traditionally, this has been the domain of human researchers who review background knowledge, draft
hypotheses, assess and test these hypotheses through various methods ( _in silico_ or _in vitro_ ), and refine them based on


_∗Citation_ : **A. Ghafarollahi, M.J. Buehler. arXiv, DOI:000000/11111., 2024**


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


their findings. While these conventional approaches have led to breakthroughs throughout the history of science, they
are constrained by the researcher’s ingenuity and background knowledge, potentially limiting discovery to the bounds
of human imagination. Additionally, conventional human-driven methods are inadequate for exploring the vast amount
of existing scientific data to extrapolate knowledge toward entirely novel ideas specially for multi-disciplinary areas
like bio-inspired materials design where a common goal is to extract principles from Nature’s toolbox and bring it to
bear towards engineering applications.


The emergence of artificial intelligence (AI) technologies presents a potential promising solution by enabling the
analysis and synthesis of large datasets beyond human capability, which could significantly accelerate discovery by
uncovering patterns and connections that are not immediately obvious to human researchers [1, 2, 3, 4, 5]. Therefore,
there is great interest in developing AI systems that can not only explore and exploit existing knowledge to make
significant scientific discoveries but also automate and replicate the broader research process, including acquiring
relevant knowledge and data [6, 7, 8, 9, 10].


Large language models (LLMs), such as OpenAI’s GPT series [11], have demonstrated remarkable progress in diverse
domains, driven by their robust capabilities [12, 13, 14, 15, 16]. These foundational general-purpose AI models

[17, 18, 19, 11] have been increasingly applied in scientific analysis, where they facilitate the generation of new
ideas and hypotheses, offering solutions to some of the intrinsic limitations of conventional human-driven methods

[20, 21, 22, 23, 24, 25, 26]. Despite their successes, significant challenges persist regarding their ability to achieve the
level of expertise possessed by domain specialists without extensive specialized training. Common issues include their
tendency to produce inaccurate responses when dealing with questions that fall outside their initial training scope, and
broader concerns about accountability, explainability, and transparency. These problems underscore the potential risks
associated with the generation of misleading or even harmful content, requiring us to think about strategies that increase
their problem-solving and reasoning capabilities.


In response to these challenges, in-context learning emerges as a compelling strategy to enhance the performance of
LLMs without the need for costly and time-intensive fine-tuning. This approach exploits the model’s inherent ability to
adapt its responses based on the context embedded within the prompt, which can be derived from a variety of sources.
This capability enables LLMs to execute a wide array of tasks effectively [27, 28, 29]. The potential to construct
powerful generative AI models that integrate external knowledge to provide context and elicit more precise responses
during generation is substantial [30]. The central challenge is to develop robust mechanisms for the accurate retrieval
and integration of relevant knowledge that enables LLMs to interpret and synthesize information pertinent to specific
tasks, particularly in the realm of scientific discovery.


The construction of knowledge bases and the strategic retrieval of information from them are gaining traction as effective
methods to enhance the generative capabilities of LLMs. Recent advancements in generative AI allow for the efficient
mining of vast scientific datasets, transforming unstructured natural language into structured data such as comprehensive
ontological knowledge graphs [31, 32, 6, 33, 34]. These knowledge graphs not only provide a mechanistic breakdown
of information but also offer an ontological framework that elucidates the interconnectedness of different concepts,
delineated as nodes and edges within the graph.


While single-LLM-based agents can generate more accurate responses when enhanced with well-designed prompts and
context, they often fall short for the complex demands of scientific discovery. Creating new scientific insights involves a
series of steps, deep thinking, and the integration of diverse, sometimes conflicting information, making it a challenging
task for a single agent. To overcome these limitations and fully leverage AI in automating scientific discovery, it’s
essential to employ a team of specialized agents. Multi-agent AI systems are known for their ability to tackle complex
problems across different domains by pooling their capabilities [35, 23, 36, 37, 38]. This collaborative approach allows
the system to handle the intricacies of scientific discovery more effectively, potentially leading to breakthroughs that are
difficult to achieve by single agents alone.


Building on these insights, our study introduces a method that synergizes the strengths of ontological knowledge
graphs [39, 40] with the dynamic capabilities of LLM-based multi-agent systems, setting a robust foundation for
enhancing graph reasoning and automating the scientific discovery process. Within this generative framework, the
discovery workflow is systematically broken down into more manageable subtasks. Each agent in the system is assigned
a distinct role, optimized through complex prompting strategies to ensure that every subtask is tackled with targeted
expertise and precision. This strategic division of labor allows the AI system to proficiently manage the complexities of
scientific research, fostering effective collaboration among agents. This collaboration is crucial for generating, refining,
and critically evaluating new hypotheses against essential criteria like novelty and feasibility.


Central to our hypothesis generation is the utilization of a large ontological knowledge graph, focusing on biological
materials, and developed from around 1,000 scientific papers in this domain [6]. We implemented a novel sampling
strategy to extract relevant sub-graphs from this comprehensive knowledge graph, allowing us to identify and understand


2


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


the key concepts and their interrelationships. This rich, contextually informed backdrop is crucial for guiding the agents
in generating well-informed and innovative hypotheses. Such a method not only improves the accuracy of hypothesis
generation but also ensures that these hypotheses are solidly rooted in a comprehensive knowledge framework. This
structured approach promises to enhance the impact and relevance of scientific discoveries by ensuring they are
well-informed and methodologically sound.


The plan of the paper is as follows. In Section 2, we discuss our proposed LLM-powered multi-agent system for
automated scientific discovery, outlining its main components and constitutive agents. Two approaches are discussed and
compared: One based on pre-programmed AI-AI interactions, and another one utilizing a fully automated framework in
which a set of agents self-organize to solve problems. Several examples are provided to illustrate the different aspects of
our approach, from path generation to research hypothesis generation and critique, demonstrating the system’s potential
to explore novel scientific concepts and produce innovative ideas by synthesizing an iterative prompting strategy during
which multiple LLMs work together. Section 3 then presents the key findings and discussing the implications of our
multi-agent system for future research in scientific discovery.


**2** **Results and discussion**


LLMs have demonstrated a relatively high level of proficiency across a wide range of tasks, including question
answering, hypothesis development, summarizing and contrasting ideas, processing complex information, executing
tasks, and even writing code. However, conventional inference strategies often fail to produce sophisticated reasoning
and detail in the generated data. By using a set of interacting models, and assigning distinct roles to LLM-based
agents, effective multi-agent AI systems can be constructed. When combined with carefully crafted prompts and
in-context learning from graph representation of data, these systems are capable of generating scientific ideas and
hypotheses. We now present results from a several experiments we conducted with our proposed framework (details
about implementation, see Materials and Methods section).


**2.1** **Multi-agent system for graph reasoning and scientific discovery**


Figure 1 illustrates the outline of our proposed multi-agent model designed to automate the scientific discovery process
based on the key concepts and relationships retrieved from a comprehensive knowledge graph developed from scientific
papers (Figure 1a). This figure further showcases two distinct strategies deployed in this study for generating novel
scientific hypotheses, both of which harness the collective intelligence of a team of agents. These strategies integrate
the specialized capabilities of each agent, systematically exploring uncharted research territories to produce innovative
and high-impact scientific hypotheses. The full description of the agents incorporated in SciAgents is listed in Figures
S1-S4 in the Supporting Information.


The key difference between these approaches lies in the nature of the interaction between the agents. In the first approach
(Figure 1b), the interactions between agents are pre-programmed and follow a predefined sequence of tasks that ensure
consistency and reliability in hypothesis generation. In contrast, the second approach features fully automated agent
interactions without any predetermined order of how interactions between agents unfold, providing a more flexible
and adaptive framework that can dynamically respond to the evolving context of the research process. This second
strategy (Figure 1c) also incorporates human-in-the-loop interactions, enabling human intervention at various stages of
research development. Such interventions allow for expert feedback, refinement of hypotheses, or strategic guidance,
specification about certain materials, types or features, ultimately enhancing the quality and relevance of the generated
scientific ideas. Moreover, the second approach provides a more robust framework where additional tools could be
readily incorporated. For instance, we have empowered our automated multi-agent model with the Semantic Scholar
API as a tool that provides it with an ability to check the novelty of the generated hypothesis against the existing
literature.


Figure 2 shows an overview of the entire process from initial keyword selection to the final document. We employ a
hierarchical expansion strategy where answers are successively refined and improved, enriched with retrieved data,
critiqued and amended by identification or critical modeling, simulation and experimental tasks and adversarial
prompting. The process begins with initial keyword identification or random exploration within a graph, followed by
path sampling to create a subgraph of relevant concepts and relationships. This subgraph forms the basis for generating
structured output in JSON following a specific set of aspects that the model is tasked to develop. These include the
hypothesis, outcome, mechanisms, design principles, unexpected properties, comparison, and novelty. Each component
is subsequently expanded on with individual prompting, to yield significant amount of additional detail, forming a
comprehensive draft. This draft then undergoes a critical review process, including amendments for modeling and
simulation priorities (e.g., molecular dynamics) and experimental priorities (e.g., synthetic biology). The final integrated
draft, along with critical analyses, results in a document that can guide further scientific inquiry.


3


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**Figure 1: Overview of the multi-agent graph-reasoning system developed here** . Panel a, overview of graph
construction, as reported in [6]. The visual shows the progression from scientific papers as data source to graph
construction, with the image on the right showing a zoomed-in view of the graph. Panels b and c: Two distinct
approaches are presented: In b, A multi-agent system based on pre-programmed sequence of interactions between
agents, ensuring consistency and reliability, and in c, a fully automated, flexible multi-agent framework that adapts
dynamically to the evolving research context. Both systems leverage a sampled path within a global knowledge graph
as context to guide the research idea generation process. Each agent plays a specialized role: The Ontologist defines key
concepts and relationships, Scientist 1 crafts a detailed research proposal, Scientist 2 expands and refines the proposal,
and the Critic agent conducts a thorough review and suggests improvements. The Planner in the second approach
develops a detailed plan and the assistant is instructed to check the novelty of the generated research hypotheses. This
collaborative framework enables the generation of innovative and well-rounded scientific hypotheses that extend beyond
conventional human-driven methods.


In the following, we explore the primary components of our multi-agent strategy. For better clarity and understanding,
each section is accompanied by practical examples from a sample hypothesis. This hypothesis was generated using
“silk” and “energy-intensive” as the starting nodes. The outcomes of this experiment are presented in Figure 3. For a
more detailed illustration, see the Supplementary Information.


**1- Path generation.** At the core of our model is an expansive knowledge graph, first introduced in [6], that encompasses the fields of bio-inspired materials and mechanics. This knowledge graph integrates a variety of concepts
and knowledge domains, enabling the exploration of hypotheses that once seemed disconnected. To augment the
capabilities of our underlying large language model (LLM), we provide it with a sub-graph derived from this more
extensive knowledge graph. This sub-graph depicts a pathway that connects two crucial concepts or nodes within the
comprehensive graph. The construction of this path is crucial; Unlike in earlier work [6] where the shortest path was
utilized, our study employs a random path approach. As illustrated in Figure 4, the random approach infuses the path
with a richer array of concepts and relationships, enabling our agents to explore a broader spectrum of domains, as
opposed to the shortest path where only a few concepts are included. This expanded exploration not only enhances
the depth and breadth of insights gained but also fosters the novelty of the hypotheses generated. Initially, the two
concepts can be either specified by the user or selected randomly by the model from the knowledge graph. For instance,


4


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**Figure 2: Overview of the entire process from initial keyword selection to the final document, following a**
**hierarchical expansion strategy where answers are successively refined and improved, enriched with retrieved**
**data, critiqued and amended by identification or critical modeling, simulation and experimental tasks.** The
process begins with initial keyword identification or random exploration within a graph, followed by path sampling
to create a subgraph of relevant concepts and relationships (see, Figure S1, for an illustration of how the path can be
sampled). This subgraph forms the basis for generating structured output in JSON, including the hypothesis, outcome,
mechanisms, design principles, unexpected properties, comparison, and novelty. Each component is subsequently
expanded on with individual prompting, to yield significant amount of additional detail, forming a comprehensive draft.
This draft then undergoes a critical review process, including amendments for modeling and simulation priorities (e.g.,
molecular dynamics) and experimental priorities (e.g., synthetic biology). The final integrated draft, along with critical
analyses, results in a document that guides further scientific inquiry.


the example below demonstrates the path generated by the model between the concepts “silk” and “energy-intensive”.
Figure 8 shows additional knowledge graphs derived from random sampling for randomly chosen concepts to provide
additional examples. We refer the reader to Figure S1 for a visualization of how path sampling can be conducted
between two predetermined nodes, or randomly selected pairs of nodes.


silk –> provides –> biocompatibility –> possess –> biological materials –> has –> multifunctionality –> include
–> self-cleaning –> include –> multifunctionality –> broad applicability in biomaterial design –> silk –> possess
–> biopolymers –> possess –> silk –> is –> fibroin –> is –> silk –> broad applicability in biomaterial design –>
multifunctionality –> include –> structural coloration –> exhibited by –> insects –> are –> energy-intensive


The generated path provides an analytical representation of various concepts and their interconnections, which were
previously unrelated. By delineating these relationships, the model gains the ability to perceive and analyze connections
between concepts that have not been explicitly linked before. This innovative mapping approach enables the model to
extrapolate and generate ideas that are both novel and potentially transformative, paving the way for breakthroughs in
understanding and application.


**2- Deep Insights with LLM-Based Analysis** Utilizing our LLM-powered ontologist agent, we move deeper into
the intricacies of the relationships that have been mapped out in the earlier path generation stage. By examining the
connections and nuances among the identified concepts, the agent helps transition from static knowledge retrieval to
dynamic knowledge generation. This crucial shift is what enables the model to identify gaps in existing research and
propose new angles of inquiry, thereby laying the groundwork for novel ideas and hypotheses. In this context, the
role of the ontologist agent is instrumental. It applies advanced reasoning and inference techniques to synthesize and
interpret the complex web of data. This capability allows it to extract significant insights that might not be obvious at
first glance, offering a richer, more detailed understanding of the relationships.


5


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**Figure 3: Results from our multi-agent model, illustrating a novel research hypothesis based on a knowledge**
**graph connecting the keywords “silk” and “energy-intensive”, as an example.** This visual overview shows that the
system produces detailed, well-organized documentation of research development with multiple pages and detailed text
(the example shown here includes 8,100 words). Details of the results are presented in the main text and other figures,
and full conversations generated by the SciAgents model are included as Supplementary Information.

#### a b


**Figure 4: The knowledge graphs connecting the keywords “silk” and “energy-intensive” extracted from the**
**global graph using (a) random path and (b) the shortest path between the concepts.** The difference between nodes
and edges sampled in the two approaches is apparent, where enhanced sampling invokes a host of additional concepts
that will be incorporated into research development. The richer substrate that forms the basis for agentic reasoning yields
more sophisticated research concepts. Agentic reasoning carefully assesses the ideas and negotiate, via adverserial
interactions between the agents, a sound prediction and carefully delineated research ideas [41, 35, 37, 38, 42, 43].


6


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


As an example, here are some of the insights into the relationships as identified by the ontologist for the aforementioned
path, demonstrating how our approach not only maps out but also meaningfully interprets complex datasets to generate
scientific hypotheses.


  - **Silk – possess – biopolymers**: Silk is a type of biopolymer, a natural polymer produced by living organisms.

  - **Biopolymers – possess – silk**: This reiterates that silk is a biopolymer. - **Silk – can be spun into – membranes**:
Silk can be processed and spun into thin layers or sheets known as membranes.

  - **Membranes – can be spun into – silk**: This indicates the reverse process, where membranes can be derived from silk.

  - **Silk – broad applicability in biomaterial design – multifunctionality**: Silk’s multifunctional properties make it highly
applicable in the design of biomaterials.

  - **High adhesion – include – multifunctionality**: This indicates that high adhesion is part of the multifunctional nature of
silk.

  - **Structural coloration – exhibited by – insects**: Insects, such as those that produce silk, often exhibit structural coloration.

  - **Insects – are – energy-intensive**: The processes involving insects, including silk production, can be energy-intensive.


The results demonstrate that the model has developed a reasonably refined understanding of relationships between
seemingly unrelated concepts. This capability enables the model to support reasoning in scientific research and propose
new research hypotheses, which will be further explored in the subsequent stage.


**3- Research Hypothesis Generation and Expansion** This stage is where the effects of our multi-agent system
emerges. The scientist agent harnesses the extensive knowledge parsed from the knowledge graph and further refined
by the ontologist to propose novel research ideas. Through complex prompting, as shown in Figure 5, the agent is
assigned specific roles and is tasked with synthesizing a novel research proposal that integrates all key concepts from
the knowledge graph. The designated agent, Scientist_1, is configured to deliver a detailed hypothesis that is both
innovative and logically grounded, aiming to advance the understanding or application of the provided concepts. The
agent creates a proposal that carefully addresses the following seven key aspects: hypothesis, outcome, mechanisms,
design principles, unexpected properties, comparison, and novelty. This approach ensures a thorough exploration and
evaluation of the new scientific idea, allowing for a detailed assessment of its feasibility, potential impact, and areas of
innovation.


The proficiency of the Scientist_1 LLM agent in generating novel research hypotheses is demonstrated in Figure 3.
The concept involves integrating silk with dandelion-based pigments to create biomaterials with enhanced optical and
mechanical properties. The proposed enhancement in mechanical properties stems from a hierarchical organization
of silk combined with the reinforcing effects of the pigments. According to the model, this proposed composite
material could exhibit significantly improved mechanical strength, reaching up to 1.5 GPa compared to traditional
silk materials, which range from 0.5 to 1.0 GPa. Additionally, the use of low-temperature processing and dandelion
pigments is projected to reduce energy consumption by approximately 30%. This example underscores the potential of
translating knowledge graphs into unprecedented material designs, facilitating a seamless transition from theoretical
data to practical applications in materials science.


The research idea proposed by Scientist_1 provides a foundational abstract for a more detailed research proposal that is
developed through subsequent agentic interactions. To enhance and deepen this initial concept, Scientist_2 is tasked with
rigorously expanding upon and critically assessing the idea’s various components. This agent is specifically instructed
to integrate, wherever possible, quantitative scientific information such as chemical formulas, numerical values, protein
sequences, and processing conditions, significantly enriching the proposal’s scientific depth and accuracy. Additionally,
Scientist_2 is directed to comment on specific modeling and simulation techniques tailored to the project’s needs, such
as simulations for material behavior analysis or experimental methods. This thorough review and enhancement process,
including clear rationale and step-by-step reasoning, ensures that the research proposal is robust, well-grounded, and
ready for further development. This systematic approach not only solidifies the scientific underpinnings of the proposal
but also prepares it for successful implementation and future exploration.


The expanded research idea provided by Scientist_2 is showcased in the Supplementary Information, revealing a
thorough rationale and sequential reasoning for various aspects of the research proposal. Here are selected key points to
exemplify the model’s contributions:


   - The model suggests using Molecular Dynamics (MD) Simulations to explore interactions at the molecular
level. Specifically, it proposes employing software like GROMACS or AMBER to model how silk fibroin
interacts with dandelion pigments, aiming to understand the self-assembly processes and predict the resulting
microstructures.


7


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning



**Figure 5:** The profile of the Scientist_1 LLM agent implemented in the first proposed multi-agent approach for
automated scientific discovery. The AI agent utilizes the definitions of concepts and relationships between them in the
knowledge graph provided by the Ontologist to generate a novel research hypothesis.


    - For potential applications of the new composite material, the model identifies its suitability for bio-inspired
adhesives. It highlights how the dynamic interactions between silk proteins and pigments may impart selfhealing properties, making these materials ideal for adhesives that can repair themselves after damage.


    - Regarding the mechanisms that contribute to enhanced material properties, the model points out the reinforcing
effect of the pigments. It suggests that these pigments could improve the tensile strength and toughness of the
composite material, with plans to conduct mechanical testing, including tensile and nanoindentation tests, to
quantify these properties.


    - A detailed comparison with existing materials is also provided by the model as summarized in Table 1. It
notes that traditional silk materials typically exhibit tensile strengths ranging from 0.5 to 1.0 GPa, whereas the
proposed composite material aims to achieve up to 1.5 GPa. This enhancement is attributed to the hierarchical
organization of silk proteins and the reinforcing effect of dandelion-derived pigments. Further, it details
how silk fibroin’s molecular structure, with repetitive sequences of glycine and alanine forming _β_ -sheet
crystallites, contributes to its mechanical properties. The integration of dandelion pigments, possibly including
bioactive compounds such as taraxasterol and luteolin, is expected to further enhance these properties through
intermolecular interactions and cross-linking, providing a synergistic effect at multiple scales.


    - As summarized in Table 2, the model proposes the following design principles: It utilizes the natural multiscale organization of silk fibroin to guide the self-assembly of dandelion pigments, leveraging hierarchical
structuring from the nano to the macro scale. This organization is critical for achieving both the desired
mechanical strength and vibrant structural coloration. The model emphasizes the need to control pigment
concentration and distribution to ensure optimal optical properties, such as precise reflectance peaks, while
maintaining flexibility and tensile strength. Moreover, it advocates for low-temperature processing to preserve
the biocompatibility and structural integrity of silk proteins, ensuring energy-efficient production methods.


8


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


These principles collectively contribute to the creation of an advanced bio-inspired material with enhanced
mechanical and optical functionalities.

    - The model predicts unexpected properties including self-healing properties due to the dynamic nature of the
silk-pigment interactions, stimuli-responsive structural colors as the structural colors could change in response
to environmental stimuli, and additional functionalities such as UV protection and antimicrobial properties due
to the bioactive compounds present in dandelions. Scientist 2 provides more details regarding the mechanisms
underlying these properties as tabulated in Table 3.


**Table 1:** Comparison of traditional silk materials vs. proposed composite material, as predicted by our model.


**Feature** **Traditional Silk Materi-** **Proposed Composite Ma-** **Details**
**als** **terial**


Mechanical Strength Tensile strength: 0.5 to 1.0 Aiming for tensile strength Enhanced by hierarchical
GPa. up to 1.5 GPa. organization of silk fibroin
(composed of Gly-Ala
repeats forming _β_ -sheet
crystallites) and dandelionderived pigments like
taraxasterol (C30H50O)
and luteolin (C15H10O6).



Structural Colors Requires synthetic dyes for Utilizes dandelion-derived
color. pigments for structural colors.



Energy Efficiency Energy-intensive, hightemperature processing
(boiling in Na2CO3
solution at 100°C). [˜]



Low-temperature processing below 50°C, reducing energy consumption by
˜30%.



The pigments will selfassemble into nanoscale
structures, such as photonic crystals or Bragg
stacks, which can reflect
specific wavelengths of
light. The concentration
and distribution of pigments will be optimized to
achieve the desired optical
properties


The energy savings can be
quantified by comparing
the energy required for traditional silk degumming
(typically involving boiling in alkaline solutions)
with the energy required
for the proposed lowtemperature extraction and
processing methods.



At the final stage of our research development process is the Critic agent, responsible for thoroughly reviewing the
research proposal, summarizing its key points, and recommending improvements. This agent delivers a comprehensive
scientific critique, highlighting both the strengths and weaknesses of the research idea while suggesting areas for
refinement. Additionally, the Critic agent is tasked to identify the most impactful scientific question that can be
addressed through molecular modeling (e.g., molecular dynamics) and experimentation (e.g., synthetic biology), and to
outline the critical steps for setting up and conducting these molecular and experimental priorities.


For our model example involving the silk-pigment composite material, the full response from the Critic is detailed in the
Supplementary Information (SI). It provides a comprehensive evaluation of the proposed research methodology and its
potential impact. The critic agent commends the integration of silk-derived biological materials with dandelion-based
pigments for creating energy-efficient, structurally colored biomaterials, noting the project’s interdisciplinary approach
and innovative use of natural hierarchical structures to enhance mechanical and optical properties. The agent also
recognizes the robustness added by the combined use of modeling techniques and experimental methods.


Moreover, the critic identifies areas needing improvement, including challenges with nanoscale integration, scalability,
environmental impacts of solvent use, and a lack of quantitative data. Concerns about the long-term stability of the


9


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**Table 2:** Summary of design principles for energy-efficient, structurally colored silk composites.


**Stage** **Process Details** **Methods**



Low-Temperature Processing for Maintain temperatures below 50°C
Silk during silk protein extraction and
processing. Use aqueous solutions
with a mild pH (6.5-7.5) to avoid denaturation. Monitor thermal stability
with DSC


Self-Assembly of Dandelion Pig- Utilize the alignment of silk nanofibments rils and microfibrils to guide the organization of dandelion-derived pigments. Predict interactions using
MD simulations. Visualize with
AFM and SEM.


Pigment Concentration Optimization Control pigment concentration
within 0.1-1.0 wt% to achieve
desired optical properties. Use
FDTD simulations to model light
interaction. Verify reflectance peaks
with UV-Vis spectroscopy.


Hierarchical Structuring for Strength Align and cross-link silk nanofibrils
and microfibrils. Introduce crosslinking agent genipin (C11H14O5).
Analyze mechanical properties with
FEA and DMA. Target tensile
strength of 1.5 GPa.


Energy-Efficient Production Implement enzymatic extraction
methods for silk proteins and pigments at low temperatures. Monitor
energy usage with calorimetry. Evaluate sustainability with LCA. Aim
for 30% energy reduction.



Differential scanning calorimetry
(DSC) and circular dichroism (CD)
spectroscopy to monitor the thermal
stability of silk proteins.


Molecular dynamics (MD) simulations to predict the interaction energies between silk proteins and
dandelion-derived pigments. Atomic
force microscopy (AFM) and scanning electron microscopy (SEM) to
visualize the hierarchical organization of pigments within the silk.


Use UV-Vis spectroscopy to analyze
the optical properties and confirm
the presence of desired reflectance
peaks.


Use FEA to simulate the mechanical behavior of the composite under
different loading conditions. Use dynamic mechanical analysis (DMA)
to study the viscoelastic properties and ensure a balance between
strength and flexibility.


Use life cycle assessment (LCA) to
evaluate the environmental impact
and energy efficiency of the production process.



material under real-world conditions are also raised. To address these issues, the critic suggests conducting pilot studies
for process validation, exploring green chemistry for pigment extraction, developing detailed scalability plans, and
performing rigorous analyses of energy consumption and material durability. These suggestions aim to refine the
research direction, making the hypotheses generated by the AI system not only innovative but also practical, thereby
enhancing the potential for significant scientific advancements.


Lastly, the critic proposes the most impactful scientific questions related to molecular modeling, simulation, and
synthetic biology experiments as shown in in Figure S7.


For each aspect, the critic agent provides detailed responses, outlining the key steps for setting up and conducting
atomistic simulations and experimental work. To perform the molecular modeling and simulation, the critic describes the
process of simulating the interaction and self-assembly of silk fibroin and dandelion-derived pigments using molecular
dynamics (MD) simulations. This begins by defining the molecular structures of silk fibroin, rich in glycine and
alanine, and key pigments like luteolin and taraxanthin, sourced from protein and chemical databases. Appropriate
force fields, such as CHARMM or AMBER, are selected, with parameters defined using tools like CGenFF. The system
is then prepared by placing the molecules in a solvated environment, adding ions for neutralization, and using VMD
or GROMACS for setup. After energy minimization and equilibration under constant temperature and pressure, MD
simulations are run for 100-500 ns, using periodic boundary conditions. Post-simulation analysis includes calculating


10


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**Table 3:** Unexpected properties predicted for the silk-pigment composite material.


**Self-Healing Properties** **Mechanism** **Details**



Self-Healing Properties Silk proteins (fibroin) re-form hydrogen bonds and _β_ -sheet structures.
Bioactive compounds in dandelionderived pigments (e.g., taraxasterol)
enhance self-healing through hydrogen bonding and hydrophobic interactions.


Stimuli-Responsive Structural Col- The hygroscopic nature of silk and
ors the responsive behavior of dandelion
pigments cause swelling or contraction, altering the spacing between
pigment nanoparticles and shifting
the reflectance peak in response to
humidity and temperature changes.


Additional Functionalities Dandelion pigments introduce UV
protection (via luteolin and caffeic
acid) and antimicrobial properties
(via taraxacin and sesquiterpene lactones), which absorb UV light and
inhibit microbial growth.



Recovery of mechanical strength can
reach up to 80% within 24 hours
at ambient conditions after damage. Self-healing efficiency is measured by the recovery of mechanical
strength.


The reflectance peak shifts by 10-50
nm for a 10% change in relative humidity. This is measured using spectrophotometry and modeled using finite element analysis (FEA).


UV protection efficiency exceeds
90%, and antimicrobial properties exhibit inhibition zones of 10-15 mm
against E. coli and S. aureus. Measured through UV-Vis spectroscopy
and antimicrobial assays.







**Figure 6: Most impactful questions raised by the critic agent for the generated research hypothesis on integrating**
**silk with dandelion-based pigments to create biomaterials with enhanced optical and mechanical properties.**


interaction energies, identifying binding sites, and performing cluster analysis of self-assembled structures, focusing on
nanoscale formations like _β_ -sheets in silk fibroin using tools like PyMOL, Chimera, and GROMACS.


We find that the critic agent plays a crucial role in guiding these efforts by posing probing scientific questions
that challenge the assumptions and focus of the research, ensuring that the simulations and experiments target key
mechanisms and outcomes. By doing so, the critic not only helps refine the research direction but also enhances the
potential for discovering novel biomaterials with optimized mechanical and optical properties. This iterative feedback
loop between hypothesis generation and critical evaluation strengthens the overall scientific process.


**2.2** **Autonomous agentic modeling**


The experiments so far were conducted using the non-automated multi-agent system (see Figure 1), whereas the second
approach described in this section uses an automated way to generate a research hypothesis from a knowledge graph
that facilitates dynamic interactions.


The automated multi-agent system consists of a team of AI agents, each powered by a state-of-the-art general purpose
large language model from the GPT-4 family [11], accessed via the OpenAI API [44]. Each agent has a specific role and
focus in the system which is described by a unique profile. Our team of agents with the following entities collaborate in
a dynamic environment to create a research proposal:


11


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


    - “Human”: human user that poses the task and can intervene at various stages of the problem solving process.

    - “Planner”: suggests a detailed plan to solve the task.

    - “Ontologist”: who is responsible to define the relationships and concepts within the knowledge graph.

    - “Scientist 1”: crafts the initial draft of a detailed research hypothesis with seven key items based on the
definitions provided by Ontologist.

    - “Scientist 2”: who expands and refines the different key aspects of the research proposal created by Scientist 1.

    - “Critic”: conducts a thorough review and suggests improvements.

    - “Assistant”: has access to external tools including a function to generate a knowledge path from two keywords
and a function to assess the novelty and feasibility of the research idea.

    - “Group chat manager”: chooses the next speaker based on the context and agent profiles and broadcasts the
message to the whole group.


Despite the varied dynamics in agentic AI-AI interactions, the overall pipeline of the two proposed agent-based systems
to generate research hypotheses from concepts and relationships derived from a knowledge graph is similar. As
illustrated in Figure 7 the automated multi-agent collaboration starts with a plan from the planner detailing the steps
required to accomplish the task posed by the human which involves creating a research hypothesis from given keywords
or randomly selected by the model. Next, the assistant agent calls the appropriate function to establish a pathway which
serves as the foundational knowledge graph for subsequent analysis. The ontologist agent then discusses definitions and
relationships. This sets the stage for scientist_1 to generate a research idea, which is then expanded by scientist_2. The
sequence concludes with a summary, critical review, and suggestions for improvement by the critic agent. Finally, the
assistant agent executes another tool to analyze and score the novelty and feasibility of the proposed research idea.





















**Figure 7: Flowchart illustrating the dynamic interactions as developed autonomously by the multi-agent team**
**members, coordinated by the group chat manager, to generate research hypotheses through graph reasoning.**
The manager selects the working agents to collaborate based on the current chat context, fostering cooperation and
enabling mutual adjustments to solve the problem.


Despite the similarity in the steps followed by the agents in each approach, the results show that while the generated
hypotheses share overall concepts and methodologies, they differ in the details. For example, in the analysis of the
research hypothesis highlighted earlier, both models emphasize integrating silk with dandelion pigments, but they
differ in specifics such as their scope of application and the depth of technical aspects regarding material fabrication
and potential uses. For comparison, the full document created by the automated multi-agent model using the same
knowledge graph between “silk” and “energy-intensive” is provided in Section S2 of the Supplementary Material.


The difference stems from the subtle differences in how the data is propagated between the agents in the two approaches.
In the first approach, during the generation process, the agents receive only a filtered subset of information from
previous interactions (see 4.3 for more details). In contrast, the second approach allows agents to share memory, giving
them access to all the content generated in previous interactions. This means they operate with full visibility of the
history of their collaboration. Another difference between the two models is that the second approach benefits from the


12


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


integration of a tool that assesses the novelty of the proposed research ideas against current literature, using Semantic
Scholar API. This feature enables us to effectively measure the novelty of the research and proactively eliminate any
ideas that are too similar to existing work.


To demonstrate the efficacy of the automated multi-agent model in generating novel research ideas and evaluating their
novelty and feasibility, we conducted five experiments, tasking the automated multi-agent model with constructing
research ideas. We summarized these hypotheses in Table 4, which includes details about each research idea, the
proposed hypotheses, expected outcomes, and assessments of novelty and feasibility. These research ideas are generated
based on randomly selected concepts from the knowledge graph. Figure 8 displays the generated knowledge graphs,
showcasing a diverse array of concepts and relationships. Some nodes like “biomaterials”, “hierarchical structure”, and
“mechanical properties” show high node degree and serve as central hubs, indicating their pivotal roles in interconnecting
various scientific disciplines within the graph. The results highlight the diversity of the research hypotheses, which
stems from both the random selection of endpoint nodes and the paths between them. Moreover, the results showcase
varying levels of novelty and feasibility, as assessed against current literature, underscoring the critical role of comparing
with existing knowledge. The process of exploring a variety of paths, scoring the results, and identifying the most
promising directions could easily be scaled over thousands of iterations, yielding a very large ideation database.


a b c


d e


**Figure 8: Knowledge graphs derived from random sampling for randomly chosen concepts from the global**
**knowledge graph.** Panel a: “heat transfer performance” connecting “rhamphotheca”, panel b: “theoretically reversible
or partially reversible” connecting “mechanical stiffness”, panel c: “tunable processability" connecting “vanadium(v)”,
and panel d: “hexagonally packed” connecting “self-cleaning coating”, and panel e: “graphene” connecting “proteins”.


Below, we provide additional details on the various aspects of the research hypotheses for a selected sample. The
complete documents for the five hypotheses can be found in Sections S3-S7 of the Supplementary Information.


An example of a research hypothesis generated with the knowledge graph depicted in Figure 8(a) is provided in
Section S3 in the Supplementary Information. The process demonstrates dynamic collaboration between the AI agents
in constructing the research hypothesis. Initially, the planner proposes a comprehensive plan to accomplish the task,
as shown in Figure 9. Following this, various agents execute the plan, starting with the generation of a knowledge
graph, followed by the definition of key concepts and relationships by Ontologist agent. Scientist 1 then drafts the
initial research proposal, which is further expanded by Scientist 2. Finally, the critic conducts a review, and the process
concludes with an assessment of novelty and feasibility.


13


SciAgents: Automating scientific discovery through multi-agent intelligent graph reasoning


**Table 4:** Examples of research ideas generated by SciAgents using automated approach featuring underlying hypothesis,
expected outcomes, and novelty and feasibility scores. Novelty was assessed by a tool based on the results from the
Semantic Scholar API. Idea 1 is described in Section S3, Idea 2 in Section S4, Idea 3 in Section S5, Idea 4 in Section S6,
and Idea 5 in Section S7. The corresponding knowledge graphs are showing in Fig. 8.



































|1|Research idea|Development of biomimetic microfluidic chips with enhanced heat transfer perfor-<br>mance for biomedical applications|
|---|---|---|
|1|Hypothesis|Integrating biomimetic materials, inspired by the lamellar structure of keratin scales,<br>into microfuidic chips using soft lithography techniques will improve their mechani-<br>cal behavior and heat transfer effciency under cyclic loading conditions.|
|1|Expected Outcomes|~~A 20-30% increase in heat transfer effciency, a 15% reduction in failure rate under~~<br>cyclic loading, and superior biocompatibility.|
|1|~~Novelty/Feasibility~~|~~8/7~~|
|2|Research idea|Developing a novel collagen-based material with a hierarchical, interconnected 3D<br>porous architecture to enhance crashworthiness, stiffness memory, and dynamic<br>adaptability.|
|2|Hypothesis|~~The hierarchical structure of collagen, when engineered into dynamic 3D archi-~~<br>tectures, can signifcantly improve these properties due to the interplay between<br>biological interactions, cell signaling, and mechanical forces.|
|2|Expected Outcomes|~~A 30% increase in crashworthiness, an 85% recovery rate of stiffness after deforma-~~<br>tion, a 25% increase in Young’s modulus, and dynamic adaptability in response to<br>biological and mechanical stimuli.|
|2|~~Novelty/Feasibility~~|~~8/7~~|
|3|Research idea|Enhancing the mechanical properties of collagen-based scaffolds through a combina-<br>tion of tunable processability and nanocomposite integration adaptability.|
|3|Hypothesis|optimizing material extrusion and electrospinning parameters, along with incorporat-<br>ing nanocomposites like graphene oxide, hydroxyapatite, and carbon nanotubes, will<br>result in scaffolds with superior tensile strength, elasticity, and controlled pore sizes.|
|3|Expected Outcomes|~~The expected outcomes include a 50% increase in tensile strength, a 40% improve-~~<br>ment in elasticity, and enhanced base bite force metrics.|
|3|~~Novelty/Feasibility~~|~~6/8~~|
|4|Research idea|Development of a novel biomimetic material by mimicking the hierarchical structure<br>of nacre and incorporating amyloid fbrils.|
|4|Hypothesis|~~The hierarchical structure of biomaterials, specifcally nacre, enhances both super-~~<br>hydrophobic properties and mechanical robustness. By mimicking this structure<br>and incorporating amyloid fbrils, advanced self-cleaning coatings with superior<br>mechanical properties can be developed.|
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


