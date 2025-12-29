<!-- Source: 02-ContextSurvey-2507.13334.pdf | Chunk 3/26 -->

integration of task decomposition, multi-plan selection, and iterative refinement capabilities [444, 1192].


Modular RAG architectures enable flexible composition of retrieval components through standardized
interfaces and plug-and-play designs. Graph-Enhanced RAG systems leverage structured knowledge representations for improved information access, while Real-time RAG implementations address dynamic information
requirements in streaming applications [316, 1401].


_**4.1.3. Dynamic Context Assembly**_


Dynamic context assembly represents the sophisticated orchestration of acquired information components
into coherent, task-optimized contexts that maximize language model performance while respecting computational constraints.


**Assembly Functions and Orchestration Mechanisms** The assembly function _A_ encompasses templatebased formatting, priority-based selection, and adaptive composition strategies that must adapt to varying task
requirements, model capabilities, and resource constraints [708, 1142, 575]. Contemporary orchestration
mechanisms manage agent selection, context distribution, and interaction flow control in multi-agent systems,
enabling effective cooperation through user input processing, contextual distribution, and optimal agent
selection based on capability assessment [902, 53, 175].


Advanced orchestration frameworks incorporate intent recognition, contextual memory maintenance,
and task dispatching components for intelligent coordination across domain-specific agents. The Swarm
Agent framework utilizes real-time outputs to direct tool invocations while addressing limitations in static
tool registries and bespoke communication frameworks [814, 267, 250].


15


**Multi-Component Integration Strategies** Context assembly must address cross-modal integration challenges, incorporating diverse data types including text, structured knowledge, temporal sequences, and
external tool interfaces while maintaining coherent semantic relationships [535, 1230, 502]. Verbalization
techniques convert structured data including knowledge graph triples, table rows, and database records
into natural language sentences, enabling seamless integration with existing language systems without
architectural modifications [12, 788, 1072, 13].


Programming language representations of structured data, particularly Python implementations for
knowledge graphs and SQL for databases, outperform traditional natural language representations in
complex reasoning tasks by leveraging inherent structural properties [1175]. Multi-level structurization
approaches reorganize input text into layered structures based on linguistic relationships, while structured
data representations leverage existing LLMs to extract structured information and represent key elements as
graphs, tables, or relational schemas [687, 1134, 1334].


**Automated Assembly Optimization** Automated prompt engineering addresses manual optimization limitations through systematic prompt generation and refinement algorithms. Automatic Prompt Engineer (APE)
employs search algorithms for optimal prompt discovery, while LM-BFF introduces automated pipelines combining prompt-based fine-tuning with dynamic demonstration incorporation, achieving up to 30% absolute
improvement across NLP tasks [311, 421, 596]. Promptbreeder implements self-referential evolutionary
systems where LLMs improve both task-prompts and mutation-prompts governing these improvements
through natural selection analogies [279, 514].


Self-refine enables iterative output improvement through self-critique and revision across multiple
iterations, with GPT-4 achieving approximately 20% absolute performance improvement through this
methodology [741, 676]. Multi-agent collaborative frameworks simulate specialized team dynamics with
agents assuming distinct roles (analysts, coders, testers), resulting in 29.9-47.1% relative improvement in
Pass@1 metrics compared to single-agent approaches [440, 1266].


Tool integration frameworks combine Chain-of-Thought reasoning with external tool execution, automating intermediate reasoning step generation as executable programs strategically incorporating external data.
LangChain provides comprehensive framework support for sequential processing chains, agent development,
and web browsing capabilities, while specialized frameworks like Auto-GPT and Microsoft’s AutoGen facilitate
complex AI agent development through user-friendly interfaces [971, 1095, 25, 875].


**4.2. Context Processing**


Context Processing focuses on transforming and optimizing acquired contextual information to maximize its
utility for LLMs. This component addresses challenges in handling ultra-long sequence contexts, enables
iterative self-refinement and adaptation mechanisms, and facilitates integration of multimodal, relational
and structured information into coherent contextual representations.


_**4.2.1. Long Context Processing**_


Ultra-long sequence context processing addresses fundamental computational challenges arising from
transformer self-attention’s O(n [2] ) complexity, which creates significant bottlenecks as sequence lengths
increase and substantially impacts real-world applications [1067, 737, 299, 272, 420]. Increasing Mistral-7B
input from 4K to 128K tokens requires 122-fold computational increase, while memory constraints during


16


prefilling and decoding stages create substantial resource demands, with Llama 3.1 8B requiring up to 16GB
per 128K-token request [1040, 1236, 429].


**Architectural Innovations for Long Context** State Space Models (SSMs) maintain linear computational
complexity and constant memory requirements through fixed-size hidden states, with models like Mamba
offering efficient recurrent computation mechanisms that scale more effectively than traditional transformers

[1267, 351, 350]. Dilated attention approaches like LongNet employ exponentially expanding attentive
fields as token distance grows, achieving linear computational complexity while maintaining logarithmic
dependency between tokens, enabling processing of sequences exceeding one billion tokens [220].


Toeplitz Neural Networks (TNNs) model sequences with relative position encoded Toeplitz matrices,
reducing space-time complexity to log-linear and enabling extrapolation from 512 training tokens to 14,000
inference tokens [876, 877]. Linear attention mechanisms reduce complexity from O(N [2] ) to O(N) by
expressing self-attention as linear dot-products of kernel feature maps, achieving up to 4000 _×_ speedup
when processing very long sequences [528]. Alternative approaches like non-attention LLMs break quadratic
barriers by employing recursive memory transformers and other architectural innovations [553].


**Position Interpolation and Context Extension** Position interpolation techniques enable models to process
sequences beyond original context window limitations by intelligently rescaling position indices rather than
extrapolating to unseen positions [153]. Neural Tangent Kernel (NTK) approaches provide mathematically
grounded frameworks for context extension, with YaRN combining NTK interpolation with linear interpolation
and attention distribution correction [839, 477, 1029].


LongRoPE achieves 2048K token context windows through two-stage approaches: first fine-tuning
models to 256K length, then conducting positional interpolation to reach maximum context length [222].
Position Sequence Tuning (PoSE) demonstrates impressive sequence length extensions up to 128K tokens
by combining multiple positional interpolation strategies [1387]. Self-Extend techniques enable LLMs to
process long contexts without fine-tuning by employing bi-level attention strategies—grouped attention and
neighbor attention—to capture dependencies among distant and adjacent tokens [505].


**Optimization Techniques for Efficient Processing** Grouped-Query Attention (GQA) partitions query heads
into groups that share key and value heads, striking a balance between multi-query attention and multihead attention while reducing memory requirements during decoding [16, 1351]. FlashAttention exploits
asymmetric GPU memory hierarchy to achieve linear memory scaling instead of quadratic requirements,
with FlashAttention-2 providing approximately twice the speed through reduced non-matrix multiplication
operations and optimized work distribution [200, 199].


Ring Attention with Blockwise Transformers enables handling extremely long sequences by distributing
computation across multiple devices, leveraging blockwise computation while overlapping communication
with attention computation [682]. Sparse attention techniques include Shifted sparse attention (S [2] -Attn) in
LongLoRA and SinkLoRA with SF-Attn, which achieve 92% of full attention perplexity improvement with
significant computation savings [1313, 1226].


Efficient Selective Attention (ESA) proposes token-level selection of critical information through query
and key vector compression into lower-dimensional representations, enabling processing of sequences up to
256K tokens [1092]. BigBird combines local attention with global tokens that attend to entire sequences,


17


plus random connections, enabling efficient processing of sequences up to 8 _×_ longer than previously possible

[1294].


**Memory Management and Context Compression** Memory management strategies include Rolling Buffer
Cache techniques that maintain fixed attention spans, reducing cache memory usage by approximately
8 _×_ on 32K token sequences [1351]. StreamingLLM enables processing infinitely long sequences without
fine-tuning by retaining critical “attention sink” tokens together with recent KV cache entries, demonstrating
up to 22.2 _×_ speedup over sliding window recomputation with sequences up to 4 million tokens [1185].


Infini-attention incorporates compressive memory into vanilla attention, combining masked local attention
with long-term linear attention in single Transformer blocks, enabling processing of infinitely long inputs
with bounded memory and computation [798]. Heavy Hitter Oracle (H2O) presents efficient KV cache
eviction policies based on observations that small token portions contribute most attention value, improving
throughput by up to 29 _×_ while reducing latency by up to 1.9 _×_ [1343].


Context compression techniques like QwenLong-CPRS implement dynamic context optimization mechanisms enabling multi-granularity compression guided by natural language instructions [952]. InfLLM stores
distant contexts in additional memory units and employs efficient mechanisms to retrieve token-relevant
units for attention computation, allowing models pre-trained on sequences of a few thousand tokens to
effectively process sequences up to 1,024K tokens [1184].


_**4.2.2. Contextual Self-Refinement and Adaptation**_


Self-refinement enables LLMs to improve outputs through cyclical feedback mechanisms mirroring human
revision processes, leveraging self-evaluation through conversational self-interaction via prompt engineering
distinct from reinforcement learning approaches [741, 924, 25, 1220].


**Foundational Self-Refinement Frameworks** The Self-Refine framework uses the same model as generator,
feedback provider, and refiner, demonstrating that identifying and fixing errors is often easier than producing
perfect initial solutions [741, 1322, 231]. Reflexion maintains reflective text in episodic memory buffers
for future decision-making through linguistic feedback [964], while structured guidance proves essential as
simplistic prompting often fails to enable reliable self-correction [678, 593].


Multi-Aspect Feedback integrates frozen language models and external tools focusing on specific error
categories to enable more comprehensive, independent evaluation [805]. The N-CRITICS framework
implements ensemble-based evaluation where initial outputs are assessed by both generating LLMs and other
models, with compiled feedback guiding refinement until task-specific stopping criteria are fulfilled [795].


The A2R framework adopts explicit evaluation across multiple dimensions including correctness and
citation quality, formulating natural language feedback for each aspect and iteratively refining outputs [583].
ISR-LLM improves LLM-based planning by translating natural language to formal specifications, creating an
initial plan, and then systematically refining it with a validator [1383].


**Meta-Learning and Autonomous Evolution** SELF teaches LLMs meta-skills (self-feedback, self-refinement)
with limited examples, then has the model continuously self-evolve by generating and filtering its own
training data [710]. Self-rewarding mechanisms enable models to improve autonomously through iterative


18


self-judgment, where a single model adopts dual roles as performer and judge, maximizing rewards it assigns
itself [1172, 1287].


The Creator framework extends this paradigm by enabling LLMs to create and use their own tools through
a four-module process encompassing creation, decision-making, execution, and recognition [954, 862]. The
Self-Developing framework represents the most autonomous approach, enabling LLMs to discover, implement,
and refine their own improvement algorithms through iterative cycles generating algorithmic candidates as
executable code [472].


In-context learning fundamentally represents a form of meta-learning where models learn optimization strategies during pre-training that generalize across diverse tasks, enabling rapid adaptation to novel
challenges during inference [183, 1174]. Meta-in-context learning demonstrates that in-context learning
abilities can be recursively improved through in-context learning itself, adaptively reshaping model priors
over expected tasks and modifying in-context learning strategies [181].


**Memory-Augmented Adaptation Frameworks** Memory augmentation represents a powerful approach
for implementing meta-learning through frameworks like Memory of Amortized Contexts, which uses
feature extraction and memory-augmentation to compress information from new documents into compact
modulations stored in memory banks [1019]. Context-aware Meta-learned Loss Scaling addresses outdated
knowledge challenges by meta-training small autoregressive models to dynamically reweight language
modeling loss for each token during online fine-tuning [436].


Decision-Pretrained Transformers demonstrate how transformers can be trained to perform in-context
reinforcement learning, solving previously unseen RL problems by generalizing beyond pretraining distribution [1021, 588]. Context-based meta-reinforcement learning methods enhance performance through direct
supervision of context encoders, improving sample efficiency compared to end-to-end training approaches

[1080].


**Long Chain-of-Thought and Advanced Reasoning** Long Chain-of-Thought has emerged as a significant
evolution characterized by substantially longer reasoning traces enabling thorough problem exploration, as
implemented in advanced models including OpenAI-o1, DeepSeek-R1, QwQ, and Gemini 2.0 Flash Thinking

[148, 724, 1223]. LongCoT effectiveness appears linked to context window capacity, with empirical evidence
suggesting larger context windows often lead to stronger reasoning performance [1238].


Extended reasoning enables self-reflection and error correction mechanisms allowing models to identify
and rectify mistakes during problem-solving processes [1344]. The effectiveness of increasing reasoning
step length, even without adding new information, considerably enhances reasoning abilities across multiple
datasets through test-time scaling [1355].


Optimization strategies address computational inefficiencies due to verbose reasoning traces through
self-generated shorter reasoning paths via best-of-N sampling, adaptive reasoning modes including ZeroThinking and Less-Thinking approaches, and explicit compact CoT methods reducing token usage while
maintaining reasoning quality [797, 1358, 703]. Auto Long-Short Reasoning enables dynamic adjustment
of reasoning path length according to question complexity, helping models decide when longer chains are
necessary [721].


19


_**4.2.3. Multimodal Context**_


Multimodal Large Language Models (MLLMs) extend context engineering beyond text by integrating diverse
data modalities including vision, audio, and 3D environments into unified contextual representations. This
expansion introduces new challenges in modality fusion, cross-modal reasoning, and long-context processing
while enabling sophisticated applications that leverage rich multimodal contextual understanding.


**Multimodal Context Integration**


**Foundational Techniques** Multimodal MLLMs expand upon traditional LLMs by integrating data from
diverse modalities like vision, audio, and 3D environments [105, 49, 965]. A primary integration method
converts visual inputs into discrete tokens concatenated with text tokens, conditioning the LLM’s generative
process on a combined representation [1295]. This is often facilitated by Visual Prompt Generators (VPGs)
trained on image-caption pairs to map visual features into the LLM’s embedding space [613]. The dominant
architectural paradigm connects specialized, external multimodal encoders—such as CLIP for vision or CLAP
for audio—to the LLM backbone via alignment modules like Q-Former or simple MLPs [19, 86, 615, 1139],
a modular design that allows for independent encoder updates without retraining the entire model [624].


**Advanced Integration Strategies** More sophisticated approaches enable deeper modality fusion. Crossmodal attention mechanisms learn fine-grained dependencies between textual and visual tokens directly
within the LLM’s embedding space, enhancing semantic understanding for tasks like image editing [570,
909, 102]. To manage lengthy inputs, hierarchical designs process modalities in stages to ensure scalability

[158], while the “browse-and-concentrate” paradigm fuses the contexts of multiple images before LLM
ingestion to overcome the limitations of isolated processing [1143]. Some research bypasses the adaptation
of text-only LLMs, opting for unified training paradigms that jointly pre-train models on multimodal data and
text corpora from the start to mitigate alignment challenges [1391, 1233]. Other methods leverage text as a
universal semantic space, using LLM in-context learning to improve generalization across diverse modality
combinations [1058]. For video, context integration techniques range from prompt tuning to adapter-based
methods that transform video content into a sequence for reasoning [1088]. The development of these
models is often constrained by the need for vast, high-quality multimodal data and significant computational
resources [1304, 615, 215].


**Core Challenges in Multimodal Context Processing**


**Modality Bias and Reasoning Deficiencies** A primary obstacle in MLLM development is modality bias,
where models favor textual inputs, generating plausible but multimodally ungrounded responses by relying
on learned linguistic patterns rather than integrated visual or auditory information [1368, 24, 319, 1335].
This issue is exacerbated by training methodologies; for instance, VPGs trained on simple image-captioning
tasks learn to extract only salient features for captions, neglecting other visual details crucial for more
complex, instruction-based tasks, which fundamentally limits deep multimodal understanding [613, 510].
Consequently, MLLMs frequently struggle with fine-grained spatial or temporal reasoning, such as precise
object localization or understanding detailed event sequences in videos [1039, 965], particularly in complex
domains like social media where interpreting the interplay of text and images to understand misinformation
or sarcasm is difficult [511]. Effective multimodal reasoning requires not just comprehending each modality


20


but also inferring their combined holistic meaning [389]. Compounding these issues is our limited mechanistic understanding of MLLMs themselves; their internal workings are largely a black box, hindering the
development of better architectures [1283].


**Advanced Contextual Capabilities and Future Directions**


**In-Context and Long-Context Learning** A key capability of MLLMs is in-context learning, where models
adapt to new tasks from multimodal examples in the prompt without weight updates [1407, 1408, 557].
Link-context learning (LCL) enhances this by providing demonstrations with explicit causal links, improving
generalization [1020]. However, in-context learning is constrained by fixed context windows, as image
tokens consume significant space, limiting many-shot learning [443]. Performance is also sensitive to input
order and the relative importance of each modality varies by task [1028, 1206]. Processing long multimodal
contexts, crucial for applications like video analysis, remains a major research frontier [1094]. Innovations
include adaptive hierarchical token compression for video [1128], variable visual position encoding (V2PE)

[1391], specialized modules like ContextQFormer for conversational memory [595], and dynamic, queryaware frame selection for video [587]. MLLMs also show emergent communication efficiency over extended
interactions, a phenomenon still under investigation [442].


**Emerging Applications** The ability to process rich multimodal context is unlocking new applications.
MLLMs are used for predictive reasoning, such as forecasting human activity from visual scenes [1392], and
have demonstrated impressive perception and cognitive capabilities across various multimodal benchmarks

[294]. In VQA, context is leveraged for more precise answers, for instance, by prompting the MLLM to
generate its own descriptive text context of an image [1356] or by integrating external knowledge via RAG

[1001, 105]. Other applications include planning digital actions based on sensory inputs [611], enhancing
surgical decision support through memory-augmented context comprehension [422], and enabling nuanced
video understanding by integrating visual information with speech and audio cues [648, 1202, 7]. Researchers
have also extended MLLMs to emerging modalities like tactile information, event data, and graph structures

[1368, 1031, 1222]. The growing importance of these real-world use cases has spurred the development of
comprehensive evaluation frameworks to assess contextual comprehension [1118]. These advancements
enable applications previously impossible with text-only models, such as image captioning and sophisticated
multimodal reasoning [1182, 683, 139].


_**4.2.4. Relational and Structured Context**_


Large language models face fundamental constraints processing relational and structured data including
tables, databases, and knowledge graphs due to text-based input requirements and sequential architecture
limitations [495, 47, 1145]. Linearization often fails to preserve complex relationships and structural
properties, with performance degrading when information is dispersed throughout contexts [592, 591, 946].


**Knowledge Graph Embeddings and Neural Integration** Advanced encoding strategies address structural
limitations through knowledge graph embeddings that transform entities and relationships into numerical
vectors, enabling efficient processing within language model architectures [12, 1259, 938, 1203]. Graph
neural networks capture complex relationships between entities, facilitating multi-hop reasoning across


21


knowledge graph structures through specialized architectures like GraphFormers that nest GNN components
alongside transformer blocks [982, 408, 1230, 489].


GraphToken demonstrates substantial improvements by explicitly representing structural information,
achieving up to 73 percentage points enhancement on graph reasoning tasks through parameter-efficient
encoding functions [842]. Heterformer and other hybrid GNN-LM architectures perform contextualized text
encoding and heterogeneous structure encoding in unified models, addressing the computational challenges
of scaling these integrated systems [502, 471, 757].

|Method|Approach|Performance|Key Innovation|
|---|---|---|---|
|**ODA** [1009]|Observation-driven agent framework|12.87% and 8.9% improvements|Recursive observation with action-refection|
|**RAG-KG** [1215]|Historical issue KG construction|77.6% MRR, 0.32 BLEU improvement|Query parsing and sub-graph retrieval|
|**KARPA** [262]|Training-free KG adaptation|State-of-the-art KGQA performance|Pre-planning relation paths|
|**Faithful Reasoning** [726]|Planning-retrieval-reasoning framework|N/A|LLM-KG synergy with relation paths|



Table 3: Knowledge graph integration methods for enhanced reasoning in large language models.


**Verbalization and Structured Data Representations** Verbalization techniques convert structured data
including knowledge graph triples, table rows, and database records into natural language sentences, enabling
seamless integration with existing language systems without architectural modifications [12, 788, 1072, 13].
Multi-level structurization approaches reorganize input text into layered structures based on linguistic
relationships, while structured data representations leverage existing LLMs to extract structured information
and represent key elements as graphs, tables, or relational schemas [687, 1134, 1334, 1043, 608].


Programming language representations of structured data, particularly Python implementations for
knowledge graphs and SQL for databases, outperform traditional natural language representations in
complex reasoning tasks by leveraging inherent structural properties [1175]. Resource-efficient approaches
using structured matrix representations offer promising directions for reducing parameter counts while
maintaining performance on structured data tasks [347].


**Integration Frameworks and Synergized Approaches** The integration of knowledge graphs with language
models follows distinct paradigms characterized by different implementation strategies and performance
trade-offs [823, 1149]. Pre-training integration methods like K-BERT inject knowledge graph triples during
training to internalize factual knowledge, while inference-time approaches enable real-time knowledge
access without requiring complete model retraining [696, 1246, 718].


KG-enhanced LLMs incorporate structured knowledge to improve factual grounding through retrievalbased augmentation methods like KAPING, which retrieves relevant facts based on semantic similarities
and prepends them to prompts without requiring model training [48, 679, 597]. More sophisticated
implementations embed KG-derived representations directly into model latent spaces through adapter
modules and cross-attention mechanisms, with Text2Graph mappers providing linking between input text
and KG embedding spaces [132, 1074, 432].


Synergized approaches create unified systems where both technologies play equally important roles,
addressing fundamental limitations through bidirectional reasoning driven by data and knowledge [823,
859, 1120]. GreaseLM facilitates deep interaction across all model layers, allowing language context
representations to be grounded by structured world knowledge while linguistic nuances inform graph


22


representations [1330]. QA-GNN implements bidirectional attention mechanisms connecting questionanswering contexts and knowledge graphs through joint graph formation and mutual representation updates
via graph-based message passing [1259, 982].


**Applications and Performance Enhancement** Structured data integration significantly enhances LLM
capabilities across multiple dimensions, with knowledge graphs providing structured information that reduces
hallucinations by grounding responses in verifiable facts and improving factual accuracy through clearly
defined information sources [1010, 1352, 204, 571]. Knowledge graphs enhance reasoning capabilities by
providing structured entity relationships that enable complex multi-hop reasoning and logical inferences, with
their rich repository of hierarchical knowledge significantly improving precision and reliability of inferences

[1175, 212, 1026].


Real-world applications demonstrate substantial improvements across specialized domains. Healthcare
systems combine structured medical knowledge with contextual understanding through Retrieval-Augmented
Generation frameworks to improve disease progression modeling and clinical decision-making [848, 589].
Scientific research platforms organize findings into structured knowledge supporting hypothesis generation
and research gap identification, while business analytics systems balance rule-based precision with AI pattern
recognition for more actionable insights [1336, 1070].


Question answering systems benefit from natural language interfaces over structured data sources, with
integration creating more robust systems capable of handling multimodal queries and providing personalized
responses that overcome static knowledge base limitations [1326, 1125, 922, 1215]. Research demonstrates
that structured knowledge representations can improve summarization performance by 40% and 14%
across public datasets compared to unstructured memory approaches, with Chain-of-Key strategies providing
additional performance gains through dynamic structured memory updates [465].

|Method|Data Type|Integration Method|Key Innovation|Task Scope|
|---|---|---|---|---|
|**K-LAMP** [48]|Knowledge graphs|Retrieval-based augmentation|KAPING framework|Zero-shot QA|
|**Pan et al.** [823]|Knowledge graphs|Pre-training & inference integration|Synergized LLMs + KGs|Multi-domain reasoning|
|**StructLM** [1402]|Tables, graphs, databases|Instruction tuning|1.1M example dataset|18 datasets, 8 SKG tasks|
|**Shao et al.** [946]|Tables, databases, KGs|Linearization methods|Schema linking & syntax prediction|Text-to-SQL tasks|



Table 4: Representative approaches for structured data integration in large language models.


**4.3. Context Management**


Context Management addresses the efficient organization, storage, and utilization of contextual information
within LLMs. This component tackles fundamental constraints imposed by finite context windows, develops
sophisticated memory hierarchies and storage architectures, and implements compression techniques to
maximize information density while maintaining accessibility and coherence.


_**4.3.1. Fundamental Constraints**_


LLMs face fundamental constraints in context management stemming from finite context window sizes inherent in most architectures, which significantly reduce model efficacy on tasks requiring deep understanding
of lengthy documents while imposing substantial computational demands that hinder applications requiring
quick responses and high throughput [1082]. Although extending context windows enables models to handle


23


entire documents and capture longer-range dependencies, traditional transformer architectures experience
quadratic computational complexity growth as sequence length increases, making processing extremely long
texts prohibitively expensive [1007]. While innovative approaches like LongNet have reduced this complexity
to linear, balancing window size and generalization capabilities remains challenging [1007, 220].

