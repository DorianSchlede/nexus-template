<!-- Source: 02-ContextSurvey-2507.13334.pdf | Chunk 1/26 -->

##### **Contents**

**1** **Introduction** **4**


**2** **Related Work** **5**


**3** **Why Context Engineering?** **7**


3.1 Definition of Context Engineering . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8


3.2 Why Context Engineering . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11


3.2.1 Current Limitations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11


3.2.2 Performance Enhancement . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11


3.2.3 Resource Optimization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11


3.2.4 Future Potential . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12


**4** **Foundational Components** **12**


4.1 Context Retrieval and Generation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12


4.1.1 Prompt Engineering and Context Generation . . . . . . . . . . . . . . . . . . . . . . . 13


4.1.2 External Knowledge Retrieval . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14


4.1.3 Dynamic Context Assembly . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15


4.2 Context Processing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16


4.2.1 Long Context Processing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16


4.2.2 Contextual Self-Refinement and Adaptation . . . . . . . . . . . . . . . . . . . . . . . 18


4.2.3 Multimodal Context . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20


4.2.4 Relational and Structured Context . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21


4.3 Context Management . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23


4.3.1 Fundamental Constraints . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23


4.3.2 Memory Hierarchies and Storage Architectures . . . . . . . . . . . . . . . . . . . . . 24


4.3.3 Context Compression . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25


4.3.4 Applications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26


**5** **System Implementations** **27**


5.1 Retrieval-Augmented Generation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27


5.1.1 Modular RAG Architectures . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27


2


5.1.2 Agentic RAG Systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28


5.1.3 Graph-Enhanced RAG . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29


5.1.4 Applications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30


5.2 Memory Systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31


5.2.1 Memory Architectures . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31


5.2.2 Memory-Enhanced Agents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33


5.2.3 Evaluation and Challenges . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35


5.3 Tool-Integrated Reasoning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37


5.3.1 Function Calling Mechanisms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37


5.3.2 Tool-Integrated Reasoning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39


5.3.3 Agent-Environment Interaction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 40


5.4 Multi-Agent Systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42


5.4.1 Communication Protocols . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42


5.4.2 Orchestration Mechanisms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43


5.4.3 Coordination Strategies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 44


**6** **Evaluation** **45**


6.1 Evaluation Frameworks and Methodologies . . . . . . . . . . . . . . . . . . . . . . . . . . . 45


6.1.1 Component-Level Assessment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 45


6.1.2 System-Level Integration Assessment . . . . . . . . . . . . . . . . . . . . . . . . . . . 46


6.2 Benchmark Datasets and Evaluation Paradigms . . . . . . . . . . . . . . . . . . . . . . . . . 47


6.2.1 Foundational Component Benchmarks . . . . . . . . . . . . . . . . . . . . . . . . . . 47


6.2.2 System Implementation Benchmarks . . . . . . . . . . . . . . . . . . . . . . . . . . . 47


6.3 Evaluation Challenges and Emerging Paradigms . . . . . . . . . . . . . . . . . . . . . . . . . 48


6.3.1 Methodological Limitations and Biases . . . . . . . . . . . . . . . . . . . . . . . . . . 49


6.3.2 Emerging Evaluation Paradigms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 49


6.3.3 Safety and Robustness Assessment . . . . . . . . . . . . . . . . . . . . . . . . . . . . 50


**7** **Future Directions and Open Challenges** **50**


7.1 Foundational Research Challenges . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 51


7.1.1 Theoretical Foundations and Unified Frameworks . . . . . . . . . . . . . . . . . . . . 51


7.1.2 Scaling Laws and Computational Efficiency . . . . . . . . . . . . . . . . . . . . . . . 51


3


7.1.3 Multi-Modal Integration and Representation . . . . . . . . . . . . . . . . . . . . . . . 52


7.2 Technical Innovation Opportunities . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 52


7.2.1 Next-Generation Architectures . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 53


7.2.2 Advanced Reasoning and Planning . . . . . . . . . . . . . . . . . . . . . . . . . . . . 53


7.2.3 Complex Context Organization and Solving Graph Problems . . . . . . . . . . . . . . 54


7.2.4 Intelligent Context Assembly and Optimization . . . . . . . . . . . . . . . . . . . . . 54


7.3 Application-Driven Research Directions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 55


7.3.1 Domain Specialization and Adaptation . . . . . . . . . . . . . . . . . . . . . . . . . . 55


7.3.2 Large-Scale Multi-Agent Coordination . . . . . . . . . . . . . . . . . . . . . . . . . . 55


7.3.3 Human-AI Collaboration and Integration . . . . . . . . . . . . . . . . . . . . . . . . . 56


7.4 Deployment and Societal Impact Considerations . . . . . . . . . . . . . . . . . . . . . . . . . 56


7.4.1 Scalability and Production Deployment . . . . . . . . . . . . . . . . . . . . . . . . . . 56


7.4.2 Safety, Security, and Robustness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 57


7.4.3 Ethical Considerations and Responsible Development . . . . . . . . . . . . . . . . . . 57


**8** **Conclusion** **58**

##### **1. Introduction**


The advent of LLMs has marked a paradigm shift in artificial intelligence, demonstrating unprecedented
capabilities in natural language understanding, generation, and reasoning [103, 1067, 459]. However, the
performance and efficacy of these models are fundamentally governed by the _context_ they receive. This
context—ranging from simple instructional prompts to sophisticated external knowledge bases—serves as
the primary mechanism through which their behavior is steered, their knowledge is augmented, and their
capabilities are unleashed. As LLMs have evolved from basic instruction-following systems into the core
reasoning engines of complex applications, the methods for designing and managing their informational
payloads have correspondingly evolved into the formal discipline of **Context Engineering** [25, 1265, 1068].


The landscape of context engineering has expanded at an explosive rate, resulting in a proliferation
of specialized yet fragmented research domains. We conceptualize this landscape as being composed of
foundational _components_ and their subsequent _implementations_ . The foundational components represent the
systematic pipeline of context engineering through three critical phases: **Context Retrieval and Generation**,
encompassing prompt-based generation and external knowledge acquisition [25, 597, 48]; **Context Process-**
**ing**, involving long sequence processing, self-refinement mechanisms, and structured information integration

[200, 741, 495]; and **Context Management**, addressing memory hierarchies, compression techniques, and
optimization strategies [1372, 1082, 819].


These foundational components serve as the building blocks for more complex, application-oriented implementations that bridge LLMs to external realities. These systems include **Advanced Retrieval-Augmented**
**Generation (RAG)**, which has evolved into modular and agentic architectures for dynamic knowledge


4


injection [597, 316, 973, 315]; explicit **Memory Systems** that mimic human cognitive faculties for persistent
information retention [1191, 943, 1372]; and the entire ecosystem of **Intelligent Agent Systems** . This
latter category represents the pinnacle of context engineering, where agents leverage **Function Calling**
and **Tool-Integrated Reasoning** to interact with the world [939, 864, 669], and rely on sophisticated
**Agent Communication** protocols and **Context Orchestration** to achieve complex goals in multi-agent
configurations [360, 250, 902, 128].


While each of these domains has generated substantial innovation, they are predominantly studied in
isolation. This fragmented development obscures the fundamental connections between techniques and
creates significant barriers for researchers seeking to understand the broader landscape and practitioners
aiming to leverage these methods effectively. The field urgently requires a unified framework that systematically organizes these diverse techniques, clarifies their underlying principles, and illuminates their
interdependencies.


To address this critical gap, this survey provides the first comprehensive and systematic review of
Context Engineering for LLMs. Our primary contribution is a novel, structured taxonomy that classifies
the multifaceted techniques used to design, manage, and optimize context. This taxonomy organizes the
field into coherent categories, distinguishing between foundational _Components_ and their integration into
sophisticated _System Implementations_ . Through this framework, we: (1) provide a clear and structured
overview of the state-of-the-art across each domain; (2) analyze the core mechanisms, strengths, and
limitations of different approaches; and (3) identify overarching challenges and chart promising directions
for future research. This work serves as both a technical roadmap for navigating the complex landscape of
context engineering and a foundation for fostering deeper understanding and catalyzing future innovation.


The remainder of this paper is organized as follows. After discussing related work and formally defining Context Engineering, we first examine the **Foundational Components** of the field, covering Context
Retrieval and Generation, Context Processing, and Context Management. We then explore their **System**
**Implementations**, including Retrieval-Augmented Generation, Memory Systems, Tool-Integrated Reasoning,
and Multi-Agent Systems. Finally, we discuss evaluation methodologies, future research directions, and conclude the survey. Figure 1 provides a comprehensive overview of our taxonomy, illustrating the hierarchical
organization of techniques and their relationships within the Context Engineering landscape.

##### **2. Related Work**


The rapid maturation of LLMs has spurred a significant body of survey literature aiming to map its multifaceted
landscape. This existing work, while valuable, has largely focused on specific vertical domains within the
broader field of what we define as Context Engineering. Our survey seeks to complement these efforts by
providing a horizontal, unifying taxonomy that distinguishes between foundational components and their
integration into complex systems, thereby bridging these specialized areas.


**Foundational Components** Numerous surveys have addressed the foundational **Components** of context
engineering that form the core technical capabilities for effective context manipulation. The challenge of
**Context Retrieval and Generation** encompasses both prompt engineering methodologies and external
knowledge acquisition techniques. Surveys on prompt engineering have cataloged the vast array of techniques
for guiding LLM behavior, from basic few-shot methods to advanced, structured reasoning frameworks

[25, 257, 1322]. External knowledge retrieval and integration techniques, particularly through knowledge
graphs and structured data sources, are reviewed in works that survey representation techniques, integration


5


**Figure** 1: The taxonomy of Context Engineering in Large Language Models is categorized into foundational components, system implementations, evaluation methodologies, and future directions. Each area
encompasses specific techniques and frameworks that collectively advance the systematic optimization of
information payloads for LLMs.


paradigms, and applications in enhancing the factual grounding of LLMs [489, 432, 823, 897].



The domain of **Context Processing** addresses the technical challenges of handling long sequences,
self-refinement mechanisms, and structured information integration. Long context processing is addressed
in surveys analyzing techniques for extending context windows, optimizing attention mechanisms, and
managing memory efficiently [837, 651, 1298, 272]. The internal cognitive processes of LLMs are increasingly


6


surveyed, with works on self-contextualizing techniques and self-improvement paradigms gaining prominence

[1339, 231, 1176, 943].


Finally, **Context Management** literature focuses on memory hierarchies, compression techniques, and
optimization strategies that enable effective information organization and retrieval within computational
constraints. While comprehensive surveys specifically dedicated to context management as a unified domain
remain limited, related work on memory systems and context compression techniques provides foundational
insights into these critical capabilities.


**System Implementation** In parallel, the literature has extensively covered the **System Implementations**
that integrate foundational components into sophisticated architectures addressing real-world application
requirements. The domain of **RAG** has received substantial attention, with foundational surveys tracing its
development and impact on mitigating hallucinations [315, 257, 1140]. More recent work has surveyed the
evolution towards modular, agentic, and graph-enhanced RAG architectures [166, 628, 120, 316, 1401].


**Memory Systems** that enable persistent interactions and cognitive architectures have been explored
through surveys focusing on memory-enhanced agents and their applications. The broader category of
**LLM-based Agents** serves as a foundational area, with comprehensive overviews of autonomous agents,
their architecture, planning, and methodologies [1099, 725, 281, 849, 1350, 504, 1281].


**Tool-Integrated Reasoning** encompassing function calling mechanisms and agent-environment interaction are well-documented, exploring the evolution from single-tool systems to complex orchestration
frameworks [669, 864, 777, 875]. The evolution towards **Multi-Agent Systems (MAS)** represents another
focal point, with surveys detailing MAS workflows, infrastructure, communication protocols, and coordination
mechanisms [631, 360, 250, 1244, 38, 509, 191, 464].


**Evaluation** The critical aspect of **evaluating** these complex systems has been thoroughly reviewed, with
works analyzing benchmarks and methodologies for assessing component-level and system-level capabilities
and performance [1268, 384, 841, 314]. This evaluation literature spans both foundational component
assessment and integrated system evaluation paradigms.


**Our Contribution** While these surveys provide indispensable, in-depth analyses of their respective domains,
they inherently present a fragmented view of the field. The connections between RAG as a form of external
memory, tool use as a method for context acquisition, and prompt engineering as the language for orchestrating these components are often left implicit. Our work distinguishes itself by proposing _Context Engineering_
as a unifying abstraction that explicitly separates foundational components from their integration in complex
implementations. By organizing these disparate fields into a single, coherent taxonomy, this survey aims to
elucidate the fundamental relationships between them, providing a holistic map of how context is generated,
processed, managed, and utilized to steer the next generation of intelligent systems.

##### **3. Why Context Engineering?**


As Large Language Models (LLMs) evolve from simple instruction-following systems into the core reasoning
engines of complex, multi-faceted applications, the methods used to interact with them must also evolve. The
term “prompt engineering,” while foundational, is no longer sufficient to capture the full scope of designing,
managing, and optimizing the information payloads required by modern AI systems. These systems do not


7


**Figure** 2: Context Engineering Evolution Timeline: A comprehensive visualization of the development trajectory of Context Engineering implementations from 2020 to 2025, showing the evolution from foundational
RAG systems to sophisticated multi-agent architectures and tool-integrated reasoning systems.


operate on a single, static string of text; they leverage a dynamic, structured, and multifaceted information
stream. To address this, we introduce and formalize the discipline of **Context Engineering** .


**3.1. Definition of Context Engineering**


To formally define Context Engineering, we begin with the standard probabilistic model of an autoregressive
LLM. The model, parameterized by _θ_, generates an output sequence _Y_ = ( _y_ 1, . . ., _yT_ ) given an input context
_C_ by maximizing the conditional probability:



_Pθ_ ( _Y|C_ ) =



_T_
∏︁ _Pθ_ ( _yt|y<t_, _C_ ) (1)

_t_ =1



Historically, in the paradigm of prompt engineering, the context _C_ was treated as a monolithic, static string
of text, i.e., _C_ = prompt. This view is insufficient for modern systems.


Context Engineering re-conceptualizes the context _C_ as a dynamically structured set of informational
components, _c_ 1, _c_ 2, . . ., _cn_ . These components are sourced, filtered, and formatted by a set of functions, and
finally orchestrated by a high-level assembly function, _A_ :


_C_ = _A_ ( _c_ 1, _c_ 2, . . ., _cn_ ) (2)


The components _ci_ are not arbitrary; they map directly to the core technical domains of this survey:


8


 - _c_ instr: System instructions and rules ( **Context Retrieval and Generation**, Sec. 4.1).

 - _c_ know: External knowledge, retrieved via functions like RAG or from integrated knowledge graphs
( **RAG**, Sec. 5.1; **Context Processing**, Sec. 4.2).

 - _c_ tools: Definitions and signatures of available external tools ( **Function Calling** & **Tool-Integrated**
**Reasoning**, Sec. 5.3).

 - _c_ mem: Persistent information from prior interactions ( **Memory Systems**, Sec. 5.2; **Context Manage-**
**ment**, Sec. 4.3).

 - _c_ state: The dynamic state of the user, world, or multi-agent system ( **Multi-Agent Systems** & **Orchestra-**
**tion**, Sec. 5.4).

 - _c_ query: The user’s immediate request.


**The Optimization Problem of Context Engineering.** From this perspective, Context Engineering is the
formal optimization problem of finding the ideal set of context-generating functions (which we denote
collectively as _F_ = _{A_, Retrieve, Select, . . . _}_ ) that maximizes the expected quality of the LLM’s output.
Given a distribution of tasks _T_, the objective is:

_F_ _[∗]_ = arg max **E** _τ∼T_ [Reward( _Pθ_ ( _Y|CF_ ( _τ_ )), _Yτ_ _[∗]_ [)]] (3)
_F_


where _τ_ is a specific task instance, _CF_ ( _τ_ ) is the context generated by the functions in _F_ for that task, and
_Yτ_ _[∗]_ [is the ground-truth or ideal output. This optimization is subject to hard constraints, most notably the]
model’s context length limit, _|C| ≤_ _L_ max.


**Mathematical Principles and Theoretical Frameworks.** This formalization reveals deeper mathematical
principles. The assembly function _A_ is a form of **Dynamic Context Orchestration**, a pipeline of formatting
and concatenation operations, _A_ = Concat _◦_ (Format1, . . ., Format _n_ ), where each function must be optimized
for the LLM’s architectural biases (e.g., attention patterns).


The retrieval of knowledge, _c_ know = Retrieve(. . . ), can be framed as an **Information-Theoretic Optimal-**
**ity** problem. The goal is to select knowledge that maximizes the mutual information with the target answer
_Y_ _[∗]_, given the query _c_ query:
Retrieve _[∗]_ = arg max (4)
Retrieve _[I]_ [(] _[Y][∗]_ [;] _[ c]_ [know] _[|][c]_ [query][)]

This ensures that the retrieved context is not just semantically similar, but maximally informative for solving
the task.


Furthermore, the entire process can be viewed through the lens of **Bayesian Context Inference** . Instead of
deterministically constructing the context, we infer the optimal context posterior _P_ ( _C|c_ query, History, World).
Using Bayes’ theorem, this posterior is proportional to the likelihood of the query given the context and the
prior probability of the context’s relevance:


_P_ ( _C|c_ query, . . . ) ∝ _P_ ( _c_ query _|C_ ) _· P_ ( _C|_ History, World) (5)


The decision-theoretic objective is then to find the context _C_ _[∗]_ that maximizes the expected reward over the
distribution of possible answers:



_C_ _[∗]_ = arg max
_C_



∫︁
_P_ ( _Y|C_, _c_ query) _·_ Reward( _Y_, _Y_ _[∗]_ ) _dY · P_ ( _C|c_ query, . . . ) (6)

