<!-- Source: 20-Agentic_RAG_Survey.pdf | Chunk 1/3 -->

## AGENTIC RETRIEVAL-AUGMENTED GENERATION: A SURVEY ON AGENTIC RAG



**Aditi Singh**
Department of Computer Science
Cleveland State University
Cleveland, OH, USA
```
 a.singh22@csuohio.edu

```


**Abul Ehtesham**
The Davey Tree Expert Company
Kent, OH, USA
```
 abul.ehtesham@davey.com

```


**Saket Kumar**
The MathWorks Inc
Natick, MA, USA
```
saketk@mathworks.com

```


**Tala Talaei Khoei**
Khoury College of Computer Science
Roux Institute at Northeastern University
Portland, ME, USA
```
                t.talaeikhoei@northeastern.edu

```

**ABSTRACT**


Large Language Models (LLMs) have revolutionized artificial intelligence (AI) by enabling humanlike text generation and natural language understanding. However, their reliance on static training
data limits their ability to respond to dynamic, real-time queries, resulting in outdated or inaccurate
outputs. Retrieval-Augmented Generation (RAG) has emerged as a solution, enhancing LLMs by
integrating real-time data retrieval to provide contextually relevant and up-to-date responses. Despite
its promise, traditional RAG systems are constrained by static workflows and lack the adaptability
required for multi-step reasoning and complex task management.


Agentic Retrieval-Augmented Generation (Agentic RAG) transcends these limitations by embedding
autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns reflection, planning, tool use, and multi-agent collaboration to dynamically manage retrieval strategies,
iteratively refine contextual understanding, and adapt workflows through clearly defined operational
structures ranging from sequential steps to adaptive collaboration. This integration enables Agentic
RAG systems to deliver unparalleled flexibility, scalability, and context-awareness across diverse
applications.


This survey provides a comprehensive exploration of Agentic RAG, beginning with its foundational
principles and the evolution of RAG paradigms. It presents a detailed taxonomy of Agentic RAG architectures, highlights key applications in industries such as healthcare, finance, and education, and examines practical implementation strategies. Additionally, it addresses challenges in scaling these systems,
ensuring ethical decision-making, and optimizing performance for real-world applications, while
providing detailed insights into frameworks and tools for implementing Agentic RAG [1] . The GitHub
link for this survey is available at: `[https://github.com/asinghcsu/AgenticRAG-Survey](https://github.com/asinghcsu/AgenticRAG-Survey)` .


_**K**_ **eywords** Large Language Models (LLMs) _·_ Artificial Intelligence (AI) _·_ Natural Language Understanding _·_
Retrieval-Augmented Generation (RAG) _·_ Agentic RAG _·_ Autonomous AI Agents _·_ Reflection _·_ Planning _·_ Tool
Use _·_ Multi-Agent Collaboration _·_ Agentic Patterns _·_ Contextual Understanding _·_ Dynamic Adaptability _·_ Scalability _·_
Real-Time Data Retrieval _·_ Taxonomy of Agentic RAG _·_ Healthcare Applications _·_ Finance Applications _·_ Educational
Applications _·_ Ethical AI Decision-Making _·_ Performance Optimization _·_ Multi-Step Reasoning


1 _GitHub link_ [: https://github.com/asinghcsu/AgenticRAG-Survey](https://github.com/asinghcsu/AgenticRAG-Survey)


**1** **Introduction**


Large Language Models (LLMs) [1, 2] [3], such as OpenAI’s GPT-4, Google’s PaLM, and Meta’s LLaMA, have significantly transformed artificial intelligence (AI) with their ability to generate human-like text and perform complex natural
language processing tasks. These models have driven innovation across diverse domains, including conversational
agents [4], automated content creation, and real-time translation. Recent advancements have extended their capabilities
to multimodal tasks, such as text-to-image and text-to-video generation [5], enabling the creation and editing of videos
and images from detailed prompts [6], which broadens the potential applications of generative AI.


Despite these advancements, LLMs face significant limitations due to their reliance on static pre-training data. This
reliance often results in outdated information, hallucinated responses [7], and an inability to adapt to dynamic, real-world
scenarios. These challenges emphasize the need for systems that can integrate real-time data and dynamically refine
responses to maintain contextual relevance and accuracy.


Retrieval-Augmented Generation (RAG) [8, 9] emerged as a promising solution to these challenges. By combining
the generative capabilities of LLMs with external retrieval mechanisms [10], RAG systems enhance the relevance and
timeliness of responses. These systems retrieve real-time information from sources such as knowledge bases [11], APIs,
or the web, effectively bridging the gap between static training data and the demands of dynamic applications. However,
traditional RAG workflows remain limited by their linear and static design, which restricts their ability to perform
complex multi-step reasoning, integrate deep contextual understanding, and iteratively refine responses.


The evolution of agents [12] has significantly enhanced the capabilities of AI systems. Modern agents, including
LLM-powered and mobile agents [13], are intelligent entities capable of perceiving, reasoning, and autonomously
executing tasks. These agents leverage agentic patterns, such as reflection [14], planning [15], tool use, and multi-agent
collaboration [16], to enhance decision-making and adaptability.


Furthermore, these agents employ agentic workflow patterns [12, 13], such as prompt chaining, routing, parallelization,
orchestrator-worker models, and evaluator-optimizer, to structure and optimize task execution. By integrating these
patterns, Agentic RAG systems can efficiently manage dynamic workflows and address complex problem-solving
scenarios. The convergence of RAG and agentic intelligence has given rise to Agentic Retrieval-Augmented Generation
(Agentic RAG) [14], a paradigm that integrates agents into the RAG pipeline. Agentic RAG enables dynamic retrieval
strategies, contextual understanding, and iterative refinement [15], allowing for adaptive and efficient information
processing. Unlike traditional RAG, Agentic RAG employs autonomous agents to orchestrate retrieval, filter relevant
information, and refine responses, excelling in scenarios requiring precision and adaptability. The overview of Agentic
RAG is in figure 1.


This survey explores the foundational principles, taxonomy, and applications of Agentic RAG. It provides a comprehensive overview of RAG paradigms, such as Naïve RAG, Modular RAG, and Graph RAG [16], alongside their evolution
into Agentic RAG systems. Key contributions include a detailed taxonomy of Agentic RAG frameworks, applications
across domains such as healthcare [17, 18], finance, and education [19], and insights into implementation strategies,
benchmarks, and ethical considerations.


The structure of this paper is as follows: Section 2 introduces RAG and its evolution, highlighting the limitations of
traditional approaches. Section 3 elaborates on the principles of agentic intelligence and agentic patterns. Section 4
elaborates agentic workflow patterns. Section 5 provides a taxonomy of Agentic RAG systems, including single-agent,
multi-agent, and graph-based frameworks. Section 6 provides comparative analysis of Agentic RAG frameworks.
Section 7 examines applications of Agentic RAG, while Section 8 discusses implementation tools and frameworks.
Section 9 focuses on benchmarks and dataset, and Section 10 concludes with future directions for Agentic RAG systems.


**2** **Foundations of Retrieval-Augmented Generation**


**2.1** **Overview of Retrieval-Augmented Generation (RAG)**


Retrieval-Augmented Generation (RAG) represents a significant advancement in the field of artificial intelligence,
combining the generative capabilities of Large Language Models (LLMs) with real-time data retrieval. While LLMs
have demonstrated remarkable capabilities in natural language processing, their reliance on static pre-trained data
often results in outdated or incomplete responses. RAG addresses this limitation by dynamically retrieving relevant
information from external sources and incorporating it into the generative process, enabling contextually accurate and
up-to-date outputs.


2


Figure 1: An Overview of Agentic RAG


**2.2** **Core Components of RAG**


The architecture of RAG systems integrates three primary components (Figure2):


    - **Retrieveal** : Responsible for querying external data sources such as knowledge bases, APIs, or vector databases.
Advanced retrievers leverage dense vector search and transformer-based models to improve retrieval precision
and semantic relevance.

    - **Augmentation** : Processes retrieved data, extracting and summarizing the most relevant information to align
with the query context.

    - **Generation** : Combines retrieved information with the LLM’s pre-trained knowledge to generate coherent,
contextually appropriate responses.


**2.3** **Evolution of RAG Paradigms**


The field of Retrieval-Augmented Generation (RAG) has evolved significantly to address the increasing complexity of
real-world applications, where contextual accuracy, scalability, and multi-step reasoning are critical. What began as
simple keyword-based retrieval has transitioned into sophisticated, modular, and adaptive systems capable of integrating
diverse data sources and autonomous decision-making processes. This evolution underscores the growing need for
RAG systems to handle complex queries efficiently and effectively.


This section examines the progression of RAG paradigms, presenting key stages of development—Naïve RAG,
Advanced RAG, Modular RAG, Graph RAG, and Agentic RAG alongside their defining characteristics, strengths, and


3


Figure 2: Core Components of RAG


limitations. By understanding the evolution of these paradigms, readers can appreciate the advancements made in
retrieval and generative capabilities and their application in various domains


**2.3.1** **Naïve RAG**


Naïve RAG [20] represents the foundational implementation of retrieval-augmented generation. Figure 3 illustrates the
simple retrieve-read workflow of Naive RAG, focusing on keyword-based retrieval and static datasets.. These systems
rely on simple keyword-based retrieval techniques, such as TF-IDF and BM25, to fetch documents from static datasets.
The retrieved documents are then used to augment the language model’s generative capabilities.


Figure 3: An Overview of Naive RAG.


Naïve RAG is characterized by its simplicity and ease of implementation, making it suitable for tasks involving
fact-based queries with minimal contextual complexity. However, it suffers from several limitations:


    - **Lack of Contextual Awareness** : Retrieved documents often fail to capture the semantic nuances of the query
due to reliance on lexical matching rather than semantic understanding.


    - **Fragmented Outputs** : The absence of advanced preprocessing or contextual integration often leads to
disjointed or overly generic responses.


    - **Scalability Issues** : Keyword-based retrieval techniques struggle with large datasets, often failing to identify
the most relevant information.


Despite these limitations, Naïve RAG systems provided a critical proof-of-concept for integrating retrieval with
generation, laying the foundation for more sophisticated paradigms.


**2.3.2** **Advanced RAG**


Advanced RAG [20] systems build upon the limitations of Naïve RAG by incorporating semantic understanding and
enhanced retrieval techniques. Figure 4 highlights the semantic enhancements in retrieval and the iterative, contextaware pipeline of Advanced RAG. These systems leverage dense retrieval models, such as Dense Passage Retrieval
(DPR), and neural ranking algorithms to improve retrieval precision.


Key features of Advanced RAG include:


4


Figure 4: Overview of Advanced RAG


    - **Dense Vector Search** : Queries and documents are represented in high-dimensional vector spaces, enabling
better semantic alignment between the user query and retrieved documents.


    - **Contextual Re-Ranking** : Neural models re-rank retrieved documents to prioritize the most contextually
relevant information.


    - **Iterative Retrieval** : Advanced RAG introduces multi-hop retrieval mechanisms, enabling reasoning across
multiple documents for complex queries.


These advancements make Advanced RAG suitable for applications requiring high precision and nuanced understanding,
such as research synthesis and personalized recommendations. However, challenges such as computational overhead
and limited scalability persist, particularly when dealing with large datasets or multi-step queries.


**2.3.3** **Modular RAG**


Modular RAG [20] represents the latest evolution in RAG paradigms, emphasizing flexibility and customization.
These systems decompose the retrieval and generation pipeline into independent, reusable components, enabling
domain-specific optimization and task adaptability. Figure 5 demonstrates the modular architecture, showcasing hybrid
retrieval strategies, composable pipelines, and external tool integration.


Key innovations in Modular RAG include:


    - **Hybrid Retrieval Strategies** : Combining sparse retrieval methods (e.g., a sparse encoder-BM25) with dense
retrieval techniques [21] (e.g., DPR - Dense Passage Retrieval ) to maximize accuracy across diverse query
types.


    - **Tool Integration** : Incorporating external APIs, databases, or computational tools to handle specialized tasks,
such as real-time data analysis or domain-specific computations.


    - **Composable Pipelines** : Modular RAG enables retrievers, generators, and other components to be replaced,
enhanced, or reconfigured independently, allowing high adaptability to specific use cases.


For instance, a Modular RAG system designed for financial analytics might retrieve live stock prices via APIs, analyze
historical trends using dense retrieval, and generate actionable investment insights through a tailored language model.
This modularity and customization make Modular RAG ideal for complex, multi-domain tasks, offering both scalability
and precision.


5


Figure 5: Overview of Modular RAG


**2.3.4** **Graph RAG**


Graph RAG [16] extends traditional Retrieval-Augmented Generation systems by integrating graph-based data structures
as illustrated in Figure 6. These systems leverage the relationships and hierarchies within graph data to enhance multihop reasoning and contextual enrichment. By incorporating graph-based retrieval, Graph RAG enables richer and more
accurate generative outputs, particularly for tasks requiring relational understanding.


Graph RAG is characterized by its ability to:


    - **Node Connectivity** : Captures and reasons over relationships between entities.


    - **Hierarchical Knowledge Management** : Handles structured and unstructured data through graph-based
hierarchies.


    - **Context Enrichment** : Adds relational understanding by leveraging graph-based pathways.


However, Graph RAG has some limitations:


    - **Limited Scalability** : The reliance on graph structures can restrict scalability, especially with extensive data
sources.


    - **Data Dependency** : High-quality graph data is essential for meaningful outputs, limiting its applicability in
unstructured or poorly annotated datasets.


    - **Complexity of Integration** : Integrating graph data with unstructured retrieval systems increases design and
implementation complexity.


Graph RAG is well-suited for applications such as healthcare diagnostics, legal research, and other domains where
reasoning over structured relationships is crucial.


**2.3.5** **Agentic RAG**


Agentic RAG represents a paradigm shift by introducing autonomous agents capable of dynamic decision-making
and workflow optimization. Unlike static systems, Agentic RAG employs iterative refinement and adaptive retrieval
strategies to address complex, real-time, and multi-domain queries. This paradigm leverages the modularity of retrieval
and generation processes while introducing agent-based autonomy.


6


Figure 6: Overview of Graph RAG


Key characteristics of Agentic RAG include:


    - **Autonomous Decision-Making** : Agents independently evaluate and manage retrieval strategies based on
query complexity.


    - **Iterative Refinement** : Incorporates feedback loops to improve retrieval accuracy and response relevance.


    - **Workflow Optimization** : Dynamically orchestrates tasks, enabling efficiency in real-time applications.


Despite its advancements, Agentic RAG faces some challenges:


    - **Coordination Complexity** : Managing interactions between agents requires sophisticated orchestration
mechanisms.


    - **Computational Overhead** : The use of multiple agents increases resource requirements for complex workflows.


    - **Scalability Limitations** : While scalable, the dynamic nature of the system can strain computational resources
for high query volumes.


Agentic RAG excels in domains like customer support, financial analytics, and adaptive learning platforms, where
dynamic adaptability and contextual precision are paramount.


**2.4** **Challenges and Limitations of Traditional RAG Systems**


Traditional Retrieval-Augmented Generation (RAG) systems have significantly expanded the capabilities of Large
Language Models (LLMs) by integrating real-time data retrieval. However, these systems still face critical challenges
that hinder their effectiveness in complex, real-world applications. The most notable limitations revolve around
**contextual integration**, **multi-step reasoning**, and **scalability and latency issues** .


**2.4.1** **Contextual Integration**


Even when RAG systems successfully retrieve relevant information, they often struggle to seamlessly incorporate it
into generated responses. The static nature of retrieval pipelines and limited contextual awareness lead to fragmented,
inconsistent, or overly generic outputs.


**Example:** A query such as, _"What are the latest advancements in Alzheimer’s research and their implications for_
_early-stage treatment?"_ might yield relevant research papers and medical guidelines. However, traditional RAG
systems often fail to synthesize these findings into a coherent explanation that connects the new treatments to specific
patient scenarios. Similarly, for a query like, _"What are the best sustainable practices for small-scale agriculture in_
_arid regions?"_, traditional systems might retrieve documents on general agricultural methods but overlook critical
sustainability practices tailored to arid environments.


7


Table 1: Comparative Analysis of RAG Paradigms





|Paradigm|Key Features|Strengths|
|---|---|---|
|**Naïve RAG**|• Keyword-based retrieval (e.g.,<br>TF-IDF, BM25)|• Simple and easy to implement<br>• Suitable for fact-based queries|
|**Advanced RAG**|• Dense retrieval models (e.g.,<br>DPR)<br>• Neural ranking and re-ranking<br>• Multi-hop retrieval|• High precision retrieval<br>• Improved contextual relevance|
|**Modular RAG**|• Hybrid retrieval (sparse and<br>dense)<br>• Tool and API integration<br>• Composable, domain-specifc<br>pipelines|• High fexibility and customization<br>• Suitable for diverse applications<br>• Scalable|
|**Graph RAG**|• Integration<br>of<br>graph-based<br>structures<br>• Multi-hop reasoning<br>• Contextual<br>enrichment<br>via<br>nodes|• Relational reasoning capabilities<br>• Mitigates hallucinations<br>• Ideal for structured data tasks|
|**Agentic RAG**|• Autonomous agents<br>• Dynamic decision-making<br>• Iterative refnement and work-<br>fow optimization|• Adaptable to real-time changes<br>• Scalable for multi-domain tasks<br>• High accuracy|


**2.4.2** **Multi-Step Reasoning**





Many real-world queries require iterative or multi-hop reasoning—retrieving and synthesizing information across
multiple steps. Traditional RAG systems are often ill-equipped to refine retrieval based on intermediate insights or user
feedback, resulting in incomplete or disjointed responses.


**Example:** A complex query like, _"What lessons from renewable energy policies in Europe can be applied to developing_
_nations, and what are the potential economic impacts?"_ demands the orchestration of multiple types of information,
including policy data, contextualization for developing regions, and economic analysis. Traditional RAG systems
typically fail to connect these disparate elements into a cohesive response.


**2.4.3** **Scalability and Latency Issues**


As the volume of external data sources grows, querying and ranking large datasets becomes increasingly computationally
intensive. This results in significant latency, which undermines the system’s ability to provide timely responses in
real-time applications.


**Example:** In time-sensitive settings such as _financial analytics_ or _live customer support_, delays caused by querying
multiple databases or processing large document sets can hinder the system’s overall utility. For example, a delay in
retrieving market trends during high-frequency trading could result in missed opportunities.


**2.5** **Agentic RAG: A Paradigm Shift**


Traditional RAG systems, with their static workflows and limited adaptability, often struggle to handle dynamic, multistep reasoning and complex real-world tasks. These limitations have spurred the integration of agentic intelligence,


8


resulting in Agentic RAG. By incorporating autonomous agents capable of dynamic decision-making, iterative reasoning,
and adaptive retrieval strategies, Agentic RAG builds on the modularity of earlier paradigms while overcoming their
inherent constraints. This evolution enables more complex, multi-domain tasks to be addressed with enhanced precision
and contextual understanding, positioning Agentic RAG as a cornerstone for next-generation AI applications. In
particular, Agentic RAG systems reduce latency through optimized workflows and refine outputs iteratively, tackling
the very challenges that have historically hindered traditional RAG’s scalability and effectiveness.


**3** **Core Principles and Background of Agentic Intelligence**


Agentic Intelligence forms the foundation of Agentic Retrieval-Augmented Generation (RAG) systems, enabling them
to transcend the static and reactive nature of traditional RAG. By integrating autonomous agents capable of dynamic
decision-making, iterative reasoning, and collaborative workflows, Agentic RAG systems exhibit enhanced adaptability
and precision. This section explores the core principles underpinning agentic intelligence.


**Components of an AI Agent.** In essence, an AI agent comprises (Figure. 7):


    - **LLM (with defined Role and Task):** Serves as the agent’s primary reasoning engine and dialogue interface.
It interprets user queries, generates responses, and maintains coherence.


    - **Memory (Short-Term and Long-Term):** Captures context and relevant data across interactions. Short-term
memory [22] tracks immediate conversation state, while long-term memory [22]stores accumulated knowledge
and agent experiences.


    - **Planning (Reflection & Self-Critique):** Guides the agent’s iterative reasoning process through reflection,
query routing, or self-critique[23], ensuring that complex tasks are broken down effectively [24].


    - **Tools Vector Search, Web Search, APIs, etc.):** Expands the agent’s capabilities beyond text generation,
enabling access to external resources, real-time data, or specialized computations.


Figure 7: An Overview of AI Agents


Agentic Patterns [25, 26] provide structured methodologies that guide the behavior of agents in Agentic RetrievalAugmented Generation (RAG) systems. These patterns enable agents to dynamically adapt, plan, and collaborate,
ensuring that the system can handle complex, real-world tasks with precision and scalability. Four key patterns underpin
agentic workflows:


**3.1** **Reflection**


Reflection is a foundational design pattern in agentic workflows, enabling agents to iteratively evaluate and refine their
outputs. By incorporating self-feedback mechanisms, agents can identify and address errors, inconsistencies, and areas
for improvement, enhancing performance across tasks like code generation, text production, and question answering (


9


as shown in Figure 8). In practical use, Reflection involves prompting an agent to critique its outputs for correctness,
style, and efficiency, then incorporating this feedback into subsequent iterations. External tools, such as unit tests or
web searches, can further enhance this process by validating results and highlighting gaps.


In multi-agent systems, Reflection can involve distinct roles, such as one agent generating outputs while another
critiques them, fostering collaborative improvement. For instance, in legal research, agents can iteratively refine
responses by re-evaluating retrieved case law, ensuring accuracy and comprehensiveness. Reflection has demonstrated
significant performance improvements in studies like _Self-Refine_ [27], _Reflexion_ [28], and _CRITIC_ [23].


Figure 8: An Overview of Agentic Self- Reflection


**3.2** **Planning**


Planning [24] is a key design pattern in agentic workflows that enables agents to autonomously decompose complex tasks
into smaller, manageable subtasks. This capability is essential for multi-hop reasoning and iterative problem-solving in
dynamic and uncertain scenarios as shown in Figure 9a.


By leveraging planning, agents can dynamically determine the sequence of steps needed to accomplish a larger objective.
This adaptability allows agents to handle tasks that cannot be predefined, ensuring flexibility in decision-making.
While powerful, Planning can produce less predictable outcomes compared to deterministic workflows like Reflection.
Planning is particularly suited for tasks that require dynamic adaptation, where predefined workflows are insufficient.
As the technology matures, its potential to drive innovative applications across domains will continue to grow.


**3.3** **Tool Use**


Tool Use enables agents to extend their capabilities by interacting with external tools, APIs, or computational resources
as illustrated in 9b. This pattern allows agents to gather information, perform computations, and manipulate data beyond
their pre-trained knowledge. By dynamically integrating tools into workflows, agents can adapt to complex tasks and
provide more accurate and contextually relevant outputs.


Modern agentic workflows incorporate tool use for a variety of applications, including information retrieval, computational reasoning, and interfacing with external systems. The implementation of this pattern has evolved significantly
with advancements like GPT-4’s function calling capabilities and systems capable of managing access to numerous
tools. These developments facilitate sophisticated workflows where agents autonomously select and execute the most
relevant tools for a given task.


While tool use significantly enhances agentic workflows, challenges remain in optimizing the selection of tools,
particularly in contexts with a large number of available options. Techniques inspired by retrieval-augmented generation
(RAG), such as heuristic-based selection, have been proposed to address this issue.


**3.4** **Multi-Agent**


Multi-agent collaboration [29] is a key design pattern in agentic workflows that enables task specialization and parallel
processing. Agents communicate and share intermediate results, ensuring the overall workflow remains efficient and
coherent. By distributing subtasks among specialized agents, this pattern improves the scalability and adaptability


10


(a) An Overview of Agentic Planning (b) An Overview of Tool Use


Figure 9: Overview of Agentic Planning and Tool Use


of complex workflows. Multi-agent systems allow developers to decompose intricate tasks into smaller, manageable
subtasks assigned to different agents. This approach not only enhances task performance but also provides a robust
framework for managing complex interactions. Each agent operates with its own memory and workflow, which can
include the use of tools, reflection, or planning, enabling dynamic and collaborative problem-solving (see Figure 10).


While multi-agent collaboration offers significant potential, it is a less predictable design pattern compared to more
mature workflows like Reflection and Tool Use. Nevertheless, emerging frameworks such as AutoGen, Crew AI, and
LangGraph are providing new avenues for implementing effective multi-agent solutions.


Figure 10: An Overview of MultiAgent


These design patterns form the foundation for the success of Agentic RAG systems. By structuring workflows—from
simple, sequential steps to more adaptive, collaborative processes—these patterns enable systems to dynamically
adapt their retrieval and generative strategies to the diverse and ever-changing demands of real-world environments.
Leveraging these patterns, agents are capable of handling iterative, context-aware tasks that significantly exceed the
capabilities of traditional RAG systems.


**4** **Agentic Workflow Patterns: Adaptive Strategies for Dynamic Collaboration**


Agentic workflow patterns, [12, 13] structure LLM-based applications to optimize performance, accuracy, and efficiency.
Different approaches are suitable depending on task complexity and processing requirements.


11


**4.1** **Prompt Chaining: Enhancing Accuracy Through Sequential Processing**


Prompt chaining [12, 13] decomposes a complex task into multiple steps, where each step builds upon the previous
one. This structured approach improves accuracy by simplifying each subtask before moving forward. However, it may
increase latency due to sequential processing.


Figure 11: Illustration of Prompt Chaining Workflow


**When to Use:** This workflow is most effective when a task can be broken down into fixed subtasks, each contributing
to the final output. It is particularly useful in scenarios where step-by-step reasoning enhances accuracy.


**Example Applications:**


    - Generating marketing content in one language and then translating it into another while preserving nuances.

    - Structuring document creation by first generating an outline, verifying its completeness, and then developing
the full text.


**4.2** **Routing:Directing Inputs to Specialized Processes**


Routing [12, 13] involves classifying an input and directing it to an appropriate specialized prompt or process. This
method ensures distinct queries or tasks are handled separately, improving efficiency and response quality.


Figure 12: Illustration Routing Workflow


**When to Use:** Ideal for scenarios where different types of input require distinct handling strategies, ensuring optimized
performance for each category.


**Example Applications:**


    - Directing customer service queries into categories such as technical support, refund requests, or general
inquiries.


12


    - Assigning simple queries to smaller models for cost efficiency, while complex requests go to advanced models.


**4.3** **Parallelization: Speeding Up Processing Through Concurrent Execution**


Parallelization [12, 13] divides a task into independent processes that run simultaneously, reducing latency and
improving throughput. It can be categorized into sectioning (independent subtasks) and voting (multiple outputs for
accuracy).


Figure 13: Illustration of Parallelization Workflow


**When to Use:** Useful when tasks can be executed independently to enhance speed or when multiple outputs improve
confidence.


**Example Applications:**


    - **Sectioning:** Splitting tasks like content moderation, where one model screens input while another generates a
response.


    - **Voting:** Using multiple models to cross-check code for vulnerabilities or analyze content moderation decisions.


**4.4** **Orchestrator-Workers: Dynamic Task Delegation**


This workflow [12, 13] features a central orchestrator model that dynamically breaks tasks into subtasks, assigns them
to specialized worker models, and compiles the results. Unlike parallelization, it adapts to varying input complexity.


Figure 14: Illustration of Orchestrator-Workers Workflow


**When to Use:** Best suited for tasks requiring dynamic decomposition and real-time adaptation, where subtasks are not
predefined.


13


**Example Applications:**


    - Automatically modifying multiple files in a codebase based on the nature of requested changes.

    - Conducting real-time research by gathering and synthesizing relevant information from multiple sources.


**4.5** **Evaluator-Optimizer: Refining Output Through Iteration**


The evaluator-optimizer [12, 13] workflow iteratively improves content by generating an initial output and refining it
based on feedback from an evaluation model.


Figure 15: Illustration of Evaluator-Optimizer Workflow


**When to Use:** Effective when iterative refinement significantly enhances response quality, especially when clear
evaluation criteria exist.


**Example Applications:**


    - Improving literary translations through multiple evaluation and refinement cycles.

    - Conducting multi-round research queries where additional iterations refine search results.


**5** **Taxonomy of Agentic RAG Systems**


Agentic Retrieval-Augmented Generation (RAG) systems can be categorized into distinct architectural frameworks
based on their complexity and design principles. These include single-agent architectures, multi-agent systems, and hierarchical agentic architectures. Each framework is tailored to address specific challenges and optimize performance for
diverse applications. This section provides a detailed taxonomy of these architectures, highlighting their characteristics,
strengths, and limitations.


**5.1** **Single-Agent Agentic RAG: Router**


A **Single-Agent Agentic RAG:** [30] serves as a centralized decision-making system where a single agent manages the
retrieval, routing, and integration of information (as shown in Figure. 16). This architecture simplifies the system by
consolidating these tasks into one unified agent, making it particularly effective for setups with a limited number of
tools or data sources.


**Workflow**


1. **Query Submission and Evaluation:** The process begins when a user submits a query. A coordinating
agent (or master retrieval agent) receives the query and analyzes it to determine the most suitable sources of
information.

2. **Knowledge Source Selection:** Based on the query’s type, the coordinating agent chooses from a variety of
retrieval options:


14


       - **Structured Databases:** For queries requiring tabular data access, the system may use a _Text-to-SQL_
engine that interacts with databases like PostgreSQL or MySQL.


       - **Semantic Search:** When dealing with unstructured information, it retrieves relevant documents (e.g.,
PDFs, books, organizational records) using vector-based retrieval.


       - **Web Search:** For real-time or broad contextual information, the system leverages a web search tool to
access the latest online data.


       - **Recommendation Systems:** For personalized or contextual queries, the system taps into recommendation
engines that provide tailored suggestions.


3. **Data Integration and LLM Synthesis:** Once the relevant data is retrieved from the chosen sources, it is
passed to a _Large Language Model (LLM)_ . The LLM synthesizes the gathered information, integrating insights
from multiple sources into a coherent and contextually relevant response.


4. **Output Generation:** Finally, the system delivers a comprehensive, user-facing answer that addresses the
original query. This response is presented in an actionable, concise format and may optionally include
references or citations to the sources used.


Figure 16: An Overview of Single Agentic RAG


**Key Features and Advantages.**


    - **Centralized Simplicity:** A single agent handles all retrieval and routing tasks, making the architecture
straightforward to design, implement, and maintain.


    - **Efficiency & Resource Optimization:** With fewer agents and simpler coordination, the system demands
fewer computational resources and can handle queries more quickly.


    - **Dynamic Routing:** The agent evaluates each query in real-time, selecting the most appropriate knowledge
source (e.g., structured DB, semantic search, web search).


    - **Versatility Across Tools:** Supports a variety of data sources and external APIs, enabling both structured and
unstructured workflows.


    - **Ideal for Simpler Systems:** Suited for applications with well-defined tasks or limited integration requirements
(e.g., document retrieval, SQL-based workflows).


15


Use Case: Customer Support


**Prompt:** Can you tell me the delivery status of my order?


**System Process (Single-Agent Workflow):**


1. **Query Submission and Evaluation:**


        - The user submits the query, which is received by the coordinating agent.

       - The coordinating agent analyzes the query and determines the most appropriate sources of
information.

2. **Knowledge Source Selection:**


        - Retrieves tracking details from the order management database.

        - Fetches real-time updates from the shipping provider’s API.

        - Optionally conducts a web search to identify local conditions affecting delivery, such as weather
or logistical delays.

3. **Data Integration and LLM Synthesis:**


        - The relevant data is passed to the LLM, which synthesizes the information into a coherent
response.

4. **Output Generation:**


        - The system generates an actionable and concise response, providing live tracking updates and
potential alternatives.

**Response:**
_Integrated Response:_ “Your package is currently in transit and expected to arrive tomorrow evening. The live
tracking from UPS indicates it is at the regional distribution center.”


**5.2** **Multi-Agent Agentic RAG Systems:**


**Multi-Agent RAG** [30] represents a modular and scalable evolution of single-agent architectures, designed to handle
complex workflows and diverse query types by leveraging multiple specialized agents (as shown in Figure 17). Instead
of relying on a single agent to manage all tasks—reasoning, retrieval, and response generation—this system distributes
responsibilities across multiple agents, each optimized for a specific role or data source.


**Workflow**


1. **Query Submission** : The process begins with a user query, which is received by a _coordinator agent_ or master
retrieval agent. This agent acts as the central orchestrator, delegating the query to specialized retrieval agents
based on the query’s requirements.

2. **Specialized Retrieval Agents** : The query is distributed among multiple retrieval agents, each focusing on a
specific type of data source or task. Examples include:


       - **Agent 1** : Handles structured queries, such as interacting with SQL-based databases like PostgreSQL or
MySQL.

       - **Agent 2** : Manages semantic searches for retrieving unstructured data from sources like PDFs, books, or
internal records.

       - **Agent 3** : Focuses on retrieving real-time public information from web searches or APIs.

       - **Agent 4** : Specializes in recommendation systems, delivering context-aware suggestions based on user
behavior or profiles.

3. **Tool Access and Data Retrieval** : Each agent routes the query to the appropriate tools or data sources within
its domain, such as:


       - _Vector Search_ : For semantic relevance.

       - _Text-to-SQL_ : For structured data.

       - _Web Search_ : For real-time public information.

       - _APIs_ : For accessing external services or proprietary systems.

The retrieval process is executed in parallel, allowing for efficient processing of diverse query types.


16


Figure 17: An Overview of Multi-Agent Agentic RAG Systems


4. **Data Integration and LLM Synthesis** : Once retrieval is complete, the data from all agents is passed to a
_Large Language Model (LLM)_ . The LLM synthesizes the retrieved information into a coherent and contextually
relevant response, integrating insights from multiple sources seamlessly.


5. **Output Generation** : The system generates a comprehensive response, which is delivered back to the user in
an actionable and concise format.


**Key Features and Advantages.**


    - **Modularity** : Each agent operates independently, allowing for seamless addition or removal of agents based on
system requirements.


    - **Scalability** : Parallel processing by multiple agents enables the system to handle high query volumes efficiently.


    - **Task Specialization** : Each agent is optimized for a specific type of query or data source, improving accuracy
and retrieval relevance.


    - **Efficiency** : By distributing tasks across specialized agents, the system minimizes bottlenecks and enhances
performance for complex workflows.


    - **Versatility** : Suitable for applications spanning multiple domains, including research, analytics, decisionmaking, and customer support.


**Challenges**


    - **Coordination Complexity** : Managing inter-agent communication and task delegation requires sophisticated
orchestration mechanisms.


    - **Computational Overhead** : Parallel processing of multiple agents can increase resource usage.


    - **Data Integration** : Synthesizing outputs from diverse sources into a cohesive response is non-trivial and
requires advanced LLM capabilities.


17


Use Case: Multi-Domain Research Assistant


**Prompt:** What are the economic and environmental impacts of renewable energy adoption in Europe?


**System Process (Multi-Agent Workflow):**


      - **Agent 1:** Retrieves statistical data from economic databases using SQL-based queries.

      - **Agent 2:** Searches for relevant academic papers using semantic search tools.

      - **Agent 3:** Performs a web search for recent news and policy updates on renewable energy.

      - **Agent 4:** Consults a recommendation system to suggest related content, such as reports or expert
commentary.

**Response:**
_Integrated Response:_ “Adopting renewable energy in Europe has led to a 20% reduction in greenhouse gas
emissions over the past decade, according to EU policy reports. Economically, renewable energy investments
have generated approximately 1.2 million jobs, with significant growth in solar and wind sectors. Recent
academic studies also highlight potential trade-offs in grid stability and energy storage costs.”


**5.3** **Hierarchical Agentic RAG Systems**

