<!-- Source: 20-Agentic_RAG_Survey.pdf | Chunk 3/3 -->



**Use Case: Twitch Ad Sales Enhancement** [37]
For instance, Twitch leveraged an agentic workflow with RAG on Amazon Bedrock to streamline ad sales. The system
dynamically retrieved advertiser data, historical campaign performance, and audience demographics to generate detailed
ad proposals, significantly boosting operational efficiency.


**Key Benefits:**


    - **Improved Response Quality** : Personalized and context-aware replies enhance user engagement.


    - **Operational Efficiency** : Reduces the workload on human support agents by automating complex queries.


    - **Real-Time Adaptability** : Dynamically integrates evolving data, such as live service outages or pricing
updates.


**7.2** **Healthcare and Personalized Medicine**


In healthcare, the integration of patient-specific data with the latest medical research is critical for informed decisionmaking. Agentic RAG systems enable this by retrieving real-time clinical guidelines, medical literature, and patient
history to assist clinicians in diagnostics and treatment planning.


**Use Case: Patient Case Summary** [38]
Agentic RAG systems have been applied in generating patient case summaries. For example, by integrating electronic
health records (EHR) and up-to-date medical literature, the system generates comprehensive summaries for clinicians
to make faster and more informed decisions.


**Key Benefits:**


    - **Personalized Care** : Tailors recommendations to individual patient needs.


    - **Time Efficiency** : Streamlines the retrieval of relevant research, saving valuable time for healthcare providers.


    - **Accuracy** : Ensures recommendations are based on the latest evidence and patient-specific parameters.


**7.3** **Legal and Contract Analysis**


Agentic RAG systems are redefining how legal workflows are conducted, offering tools for rapid document analysis and
decision-making.


**Use Case: Contract Review** [39]
A legal agentic RAG system can analyze contracts, extract critical clauses, and identify potential risks. By combining
semantic search capabilities with legal knowledge graphs, it automates the tedious process of contract review, ensuring
compliance and mitigating risks.


**Key Benefits:**


    - **Risk Identification** : Automatically flags clauses that deviate from standard terms.


    - **Efficiency** : Reduces the time spent on contract review processes.


    - **Scalability** : Handles large volumes of contracts simultaneously.


**7.4** **Finance and Risk Analysis**


Agentic RAG systems are transforming the finance industry by providing real-time insights for investment decisions,
market analysis, and risk management. These systems integrate live data streams, historical trends, and predictive
modeling to generate actionable outputs.


**Use Case: Auto Insurance Claims Processing** [40]
In auto insurance, Agentic RAG can automate claim processing. For example, by retrieving policy details and combining
them with accident data, it generates claim recommendations while ensuring compliance with regulatory requirements.


**Key Benefits:**


    - **Real-Time Analytics** : Delivers insights based on live market data.


30


    - **Risk Mitigation** : Identifies potential risks using predictive analysis and multi-step reasoning.

    - **Enhanced Decision-Making** : Combines historical and live data for comprehensive strategies.


**7.5** **Education and Personalized Learning**


Education is another domain where Agentic RAG systems are making significant strides. These systems enable adaptive
learning by generating explanations, study materials, and feedback tailored to the learner’s progress and preferences.


**Use Case: Research Paper Generation** [41]
In higher education, Agentic RAG has been used to assist researchers by synthesizing key findings from multiple
sources. For instance, a researcher querying, “What are the latest advancements in quantum computing?” receives a
concise summary enriched with references, enhancing the quality and efficiency of their work.


**Key Benefits:**


    - **Tailored Learning Paths** : Adapts content to individual student needs and performance levels.

    - **Engaging Interactions** : Provides interactive explanations and personalized feedback.

    - **Scalability** : Supports large-scale deployments for diverse educational environments.


**7.6** **Graph-Enhanced Applications in Multimodal Workflows**


Graph-Enhanced Agentic RAG (GEAR) combines graph structures with retrieval mechanisms, making it particularly
effective in multimodal workflows where interconnected data sources are essential.


**Use Case: Market Survey Generation**
GEAR enables the synthesis of text, images, and videos for marketing campaigns. For example, querying, “What
are the emerging trends in eco-friendly products?” generates a detailed report enriched with customer preferences,
competitor analysis, and multimedia content.


**Key Benefits:**


    - **Multi-Modal Capabilities** : Integrates text, image, and video data for comprehensive outputs.

    - **Enhanced Creativity** : Generates innovative ideas and solutions for marketing and entertainment.

    - **Dynamic Adaptability** : Adapts to evolving market trends and customer needs.


The applications of Agentic RAG systems span a wide range of industries, showcasing their versatility and transformative
potential. From personalized customer support to adaptive education and graph-enhanced multimodal workflows, these
systems address complex, dynamic, and knowledge-intensive challenges. By integrating retrieval, generation, and
agentic intelligence, Agentic RAG systems are paving the way for next-generation AI applications.


**8** **Tools and Frameworks for Agentic RAG**


Agentic Retrieval-Augmented Generation (RAG) systems represent a significant evolution in combining retrieval,
generation, and agentic intelligence. These systems extend the capabilities of traditional RAG by integrating decisionmaking, query reformulation, and adaptive workflows. The following tools and frameworks provide robust support for
developing Agentic RAG systems, addressing the complex requirements of real-world applications.


**Key Tools and Frameworks:**


    - **LangChain and LangGraph:** LangChain [42] provides modular components for building RAG pipelines,
seamlessly integrating retrievers, generators, and external tools. LangGraph complements this by introducing
graph-based workflows that support loops, state persistence, and human-in-the-loop interactions, enabling
sophisticated orchestration and self-correction mechanisms in agentic systems.

    - **LlamaIndex:** LlamaIndex’s [43] Agentic Document Workflows (ADW) enable end-to-end automation of
document processing, retrieval, and structured reasoning. It introduces a meta-agent architecture where
sub-agents manage smaller document sets, coordinating through a top-level agent for tasks such as compliance
analysis and contextual understanding.

    - **Hugging Face Transformers and Qdrant:** Hugging Face [44] offers pre-trained models for embedding and
generation tasks, while Qdrant [45] enhances retrieval workflows with adaptive vector search capabilities,
allowing agents to optimize performance by dynamically switching between sparse and dense vector methods.


31


    - **CrewAI and AutoGen:** These frameworks emphasize multi-agent architectures. CrewAI [46] supports
hierarchical and sequential processes, robust memory systems, and tool integrations. AG2 [47] (formerly
knows as AutoGen [48, 49]) excels in multi-agent collaboration with advanced support for code generation,
tool execution, and decision-making.


    - **OpenAI Swarm Framework:** An educational framework designed for ergonomic, lightweight multi-agent
orchestration [50], emphasizing agent autonomy and structured collaboration.


    - **Agentic RAG with Vertex AI:** Developed by Google, Vertex AI [51] integrates seamlessly with Agentic
Retrieval-Augmented Generation (RAG), providing a platform to build, deploy, and scale machine learning
models while leveraging advanced AI capabilities for robust, contextually aware retrieval and decision-making
workflows.


    - **Semantic Kernel:** Semantic Kernel [52, 53] is an open-source SDK by Microsoft that integrates large language
models (LLMs) into applications. It supports agentic patterns, enabling the creation of autonomous AI agents
for natural language understanding, task automation, and decision-making. It has been used in scenarios like
ServiceNow’s P1 incident management to facilitate real-time collaboration, automate task execution, and
retrieve contextual information seamlessly


    - **Amazon Bedrock for Agentic RAG:** Amazon Bedrock [37] provides a robust platform for implementing
Agentic Retrieval-Augmented Generation (RAG) workflows.


    - **IBM Watson and Agentic RAG:** IBM’s watsonx.ai [54] supports building Agentic RAG systems, exemplified
by using the Granite-3-8B-Instruct model to answer complex queries by integrating external information and
enhancing response accuracy.


    - **Neo4j and Vector Databases:** Neo4j, a prominent open-source graph database, excels in handling complex
relationships and semantic queries. Alongside Neo4j, vector databases like Weaviate, Pinecone, Milvus, and
Qdrant provide efficient similarity search and retrieval capabilities, forming the backbone of high-performance
Agentic Retrieval-Augmented Generation (RAG) workflows.


**9** **Benchmarks and Datasets**


Current benchmarks and datasets provide valuable insights into evaluating Retrieval-Augmented Generation (RAG)
systems, including those with agentic and graph-based enhancements. While some are explicitly designed for RAG,
others are adapted to test retrieval, reasoning, and generation capabilities in diverse scenarios. Datasets are crucial for
testing the retrieval, reasoning, and generation components of RAG systems. Table 3 discusses some key datasets based
on the dowstream task for RAG Evaluation.


Benchmarks play a critical role in standardizing the evaluation of RAG systems by providing structured tasks and
metrics. The following benchmarks are particularly relevant:


    - **BEIR (Benchmarking Information Retrieval):** A versatile benchmark designed for evaluating embedding
models on a variety of information retrieval tasks, encompassing 17 datasets across diverse domains like
bioinformatics, finance, and question answering [55].


    - **MS MARCO (Microsoft Machine Reading Comprehension):** Focused on passage ranking and question
answering, this benchmark is widely used for dense retrieval tasks in RAG systems [56].


    - **TREC (Text REtrieval Conference, Deep Learning Track):** Provides datasets for passage and document
retrieval, emphasizing the quality of ranking models in retrieval pipelines [57].


    - **MuSiQue (Multihop Sequential Questioning):** A benchmark for multihop reasoning across multiple
documents, emphasizing the importance of retrieving and synthesizing information from disconnected contexts

[58].


    - **2WikiMultihopQA:** A dataset designed for multihop QA tasks over two Wikipedia articles, focusing on the
ability to connect knowledge across multiple sources [59].


    - **AgentG (Agentic RAG for Knowledge Fusion):** Tailored for agentic RAG tasks, this benchmark assesses
dynamic information synthesis across multiple knowledge bases [8].


    - **HotpotQA:** A multi-hop QA benchmark requiring retrieval and reasoning over interconnected contexts, ideal
for evaluating complex RAG workflows[60].


    - **RAGBench:** A large-scale, explainable benchmark featuring 100,000 examples across industry domains, with
a TRACe evaluation framework for actionable RAG metrics [61].


32


   - **BERGEN (Benchmarking Retrieval-Augmented Generation):** A library for systematically benchmarking
RAG systems with standardized experiments [62].


   - **FlashRAG Toolkit:** Implements 12 RAG methods and includes 32 benchmark datasets to support efficient
and standardized RAG evaluation [63].


   - **GNN-RAG:** This benchmark evaluates graph-based RAG systems on tasks like node-level and edge-level
predictions, focusing on retrieval quality and reasoning performance in Knowledge Graph Question Answering
(KGQA) [64].


Table 3: Downstream Tasks and Datasets for RAG Evaluation (Adapted from [20]













|Category|Task Type|Datasets and References|
|---|---|---|
|**QA**|Single-hop QA|Natural Questions (NQ) [65], TriviaQA [66], SQuAD [67],<br>Web Questions (WebQ) [68], PopQA [69], MS MARCO<br>[56]|
|**QA**|Multi-hop QA|HotpotQA [60], 2WikiMultiHopQA [59], MuSiQue [58]|
|**QA**|Long-form QA|ELI5 [70], NarrativeQA (NQA) [71], ASQA [72], QM-<br>Sum [73]|
|**QA**|Domain-specifc QA|Qasper [74], COVID-QA [75], CMB/MMCU Medical<br>[76]|
|**QA**|Multi-choice QA|QuALITY [77], ARC (No reference available), Common-<br>senseQA [78]|
|**Graph-based QA**|Graph QA|GraphQA [79]|
|**Graph-based QA**|Event Argument Extraction|WikiEvent [80], RAMS [81]|
|**Dialog**|Open-domain Dialog|Wizard of Wikipedia (WoW) [82]|
|**Dialog**|Personalized Dialog|KBP [83], DuleMon [84]|
|**Dialog**|Task-oriented Dialog|CamRest [85]|
|**Recommendation**|Personalized Content|Amazon Datasets (Toys, Sports, Beauty) [86]|
|**Reasoning**|Commonsense Reasoning|HellaSwag [87], CommonsenseQA [78]|
|**Reasoning**|CoT Reasoning|CoT Reasoning [88]|
|**Reasoning**|Complex Reasoning|CSQA [89]|
|**Others**|Language Understanding|MMLU (No reference available), WikiText-103 [65]|
|**Others**|Fact Checking/Verifcation|FEVER [90], PubHealth [91]|
|**Others**|Strategy QA|StrategyQA [92]|
|**Summarization**|Text Summarization|WikiASP [93], XSum [94]|
|**Summarization**|Long-form Summarization|NarrativeQA (NQA) [71], QMSum [73]|
|**Text Generation**|Biography|Biography Dataset (No reference available)|
|**Text Classifcation**|Sentiment Analysis|SST-2 [95]|
|**Text Classifcation**|General Classifcation|VioLens[96], TREC [57]|
|**Code Search**|Programming Search|CodeSearchNet [97]|
|**Robustness**|Retrieval Robustness|NoMIRACL [98]|
|**Robustness**|Language Modeling Robustness|WikiText-103 [99]|
|**Math**|Math Reasoning|GSM8K [100]|
|**Machine Translation**|Translation Tasks|JRC-Acquis [101]|


**10** **Conclusion**


Agentic Retrieval-Augmented Generation (RAG) represents a transformative advancement in artificial intelligence,
addressing the limitations of traditional RAG systems through the integration of autonomous agents. By leveraging


33


agentic intelligence, these systems introduce capabilities such as dynamic decision-making, iterative reasoning, and
collaborative workflows, enabling them to tackle complex, real-world tasks with enhanced precision and adaptability.


This survey explored the evolution of RAG systems, from their initial implementations to advanced paradigms like
Modular RAG, highlighting the contributions and limitations of each. The integration of agents into the RAG pipeline
has emerged as a pivotal development, resulting in Agentic RAG systems that overcome static workflows and limited
contextual adaptability. Applications across healthcare, finance, education, and creative industries demonstrate the
transformative potential of these systems, showcasing their ability to deliver personalized, real-time, and context-aware
solutions.


Despite their promise, Agentic RAG systems face challenges that require further research and innovation. Coordination
complexity in multi-agent architectures, scalability, and latency issues, as well as ethical considerations, must be
addressed to ensure robust and responsible deployment. Additionally, the lack of specialized benchmarks and datasets
tailored to evaluate agentic capabilities poses a significant hurdle. Developing evaluation methodologies that capture
the unique aspects of Agentic RAG, such as multi-agent collaboration and dynamic adaptability, will be crucial for
advancing the field.


Looking ahead, the convergence of retrieval-augmented generation and agentic intelligence has the potential to redefine
AI’s role in dynamic and complex environments. By addressing these challenges and exploring future directions,
researchers and practitioners can unlock the full potential of Agentic RAG systems, paving the way for transformative
applications across industries and domains. As AI systems continue to evolve, Agentic RAG stands as a cornerstone for
creating adaptive, context-aware, and impactful solutions that meet the demands of a rapidly changing world.


**References**


[1] Shervin Minaee, Tomas Mikolov, Narjes Nikzad, Meysam Chenaghlu, Richard Socher, Xavier Amatriain, and
Jianfeng Gao. Large language models: A survey, 2024.


[2] Aditi Singh. Exploring language models: A comprehensive survey and analysis. In _2023 International Con-_
_ference on Research Methodologies in Knowledge Management, Artificial Intelligence and Telecommunication_
_Engineering (RMKMATE)_, pages 1–4, 2023.


[3] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang,
Junjie Zhang, Zican Dong, Yifan Du, Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang, Ruiyang Ren,
Yifan Li, Xinyu Tang, Zikang Liu, Peiyu Liu, Jian-Yun Nie, and Ji-Rong Wen. A survey of large language
models, 2024.


[4] Sumit Kumar Dam, Choong Seon Hong, Yu Qiao, and Chaoning Zhang. A complete survey on llm-based ai
chatbots, 2024.


[5] Aditi Singh. A survey of ai text-to-image and ai text-to-video generators. In _2023 4th International Conference_
_on Artificial Intelligence, Robotics and Control (AIRC)_, pages 32–36, 2023.


[6] Aditi Singh, Abul Ehtesham, Gaurav Kumar Gupta, Nikhil Kumar Chatta, Saket Kumar, and Tala Talaei Khoei.
Exploring prompt engineering: A systematic review with swot analysis, 2024.


[7] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua
Peng, Xiaocheng Feng, Bing Qin, and Ting Liu. A survey on hallucination in large language models: Principles,
taxonomy, challenges, and open questions. _ACM Transactions on Information Systems_, November 2024.


[8] Meng-Chieh Lee, Qi Zhu, Costas Mavromatis, Zhen Han, Soji Adeshina, Vassilis N. Ioannidis, Huzefa Rangwala,
and Christos Faloutsos. Agent-g: An agentic framework for graph retrieval augmented generation, 2024.


[9] Penghao Zhao, Hailin Zhang, Qinhan Yu, Zhengren Wang, Yunteng Geng, Fangcheng Fu, Ling Yang, Wentao
Zhang, Jie Jiang, and Bin Cui. Retrieval-augmented generation for ai-generated content: A survey, 2024.


[10] Zhengbao Jiang, Frank F. Xu, Luyu Gao, Zhiqing Sun, Qian Liu, Jane Dwivedi-Yu, Yiming Yang, Jamie Callan,
and Graham Neubig. Active retrieval augmented generation, 2023.


[11] Yikun Han, Chunjiang Liu, and Pengfei Wang. A comprehensive survey on vector database: Storage and retrieval
technique, challenge, 2023.


[12] Anthropic. Building effective agents, 2024. `[https://www.anthropic.com/research/](https://www.anthropic.com/research/building-effective-agents)`
`[building-effective-agents](https://www.anthropic.com/research/building-effective-agents)` . Accessed: February 2, 2025.


[13] LangChain. Langgraph workflows tutorial, 2025. `[https://langchain-ai.github.io/langgraph/](https://langchain-ai.github.io/langgraph/tutorials/workflows/)`
`[tutorials/workflows/](https://langchain-ai.github.io/langgraph/tutorials/workflows/)` . Accessed: February 2, 2025.


34


[14] Chidaksh Ravuru, Sagar Srinivas Sakhinana, and Venkataramana Runkana. Agentic retrieval-augmented
generation for time series analysis, 2024.


[15] Jie Huang and Kevin Chen-Chuan Chang. Towards reasoning in large language models: A survey, 2023.


[16] Boci Peng, Yun Zhu, Yongchao Liu, Xiaohe Bo, Haizhou Shi, Chuntao Hong, Yan Zhang, and Siliang Tang.
Graph retrieval-augmented generation: A survey, 2024.


[17] Aditi Singh, Abul Ehtesham, Saifuddin Mahmud, and Jong-Hoon Kim. Revolutionizing mental health care
through langchain: A journey with a large language model. In _2024 IEEE 14th Annual Computing and_
_Communication Workshop and Conference (CCWC)_, pages 0073–0078, 2024.


[18] Gaurav Kumar Gupta, Aditi Singh, Sijo Valayakkad Manikandan, and Abul Ehtesham. Digital diagnostics: The
potential of large language models in recognizing symptoms of common illnesses. _AI_, 6(1), 2025.


[19] Aditi Singh, Abul Ehtesham, Saket Kumar, Gaurav Kumar Gupta, and Tala Talaei Khoei. Encouraging responsible
use of generative ai in education: A reward-based learning approach. In Tim Schlippe, Eric C. K. Cheng, and
Tianchong Wang, editors, _Artificial Intelligence in Education Technologies: New Development and Innovative_
_Practices_, pages 404–413, Singapore, 2025. Springer Nature Singapore.


[20] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, Meng Wang, and
Haofen Wang. Retrieval-augmented generation for large language models: A survey, 2024.


[21] Vladimir Karpukhin, Barlas O˘guz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen
tau Yih. Dense passage retrieval for open-domain question answering, 2020.


[22] Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu, Zhenhua Dong, and Ji-Rong
Wen. A survey on the memory mechanism of large language model based agents, 2024.


[23] Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen, Yujiu Yang, Nan Duan, and Weizhu Chen. Critic: Large
language models can self-correct with tool-interactive critiquing, 2024.


[24] Xu Huang, Weiwen Liu, Xiaolong Chen, Xingmei Wang, Hao Wang, Defu Lian, Yasheng Wang, Ruiming Tang,
and Enhong Chen. Understanding the planning of llm agents: A survey, 2024.


[25] Aditi Singh, Abul Ehtesham, Saket Kumar, and Tala Talaei Khoei. Enhancing ai systems with agentic workflows
patterns in large language model. In _2024 IEEE World AI IoT Congress (AIIoT)_, pages 527–532, 2024.


[26] DeepLearning.AI. How agents can improve llm performance. `[https://www.deeplearning.ai/the-batch/](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/?ref=dl-staging-website.ghost.io)`
`[how-agents-can-improve-llm-performance/?ref=dl-staging-website.ghost.io](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/?ref=dl-staging-website.ghost.io)`, 2024. Accessed: 2025-01-13.


[27] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha
Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann,
Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. Self-refine: Iterative refinement with self-feedback, 2023.


[28] Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao.
Reflexion: Language agents with verbal reinforcement learning, 2023.


[29] Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang, Shichao Pei, Nitesh V. Chawla, Olaf Wiest, and
Xiangliang Zhang. Large language model based multi-agents: A survey of progress and challenges, 2024.


[30] Weaviate Blog. What is agentic rag? `[https://weaviate.io/blog/what-is-agentic-rag#:~:text=is%](https://weaviate.io/blog/what-is-agentic-rag#:~:text=is%20Agentic%20RAG%3F-,%E2%80%8B,of%20the%20non%2Dagentic%20pipeline.)`
`[20Agentic%20RAG%3F-,%E2%80%8B,of%20the%20non%2Dagentic%20pipeline.](https://weaviate.io/blog/what-is-agentic-rag#:~:text=is%20Agentic%20RAG%3F-,%E2%80%8B,of%20the%20non%2Dagentic%20pipeline.)` Accessed: 2025-01-14.


[31] Shi-Qi Yan, Jia-Chen Gu, Yun Zhu, and Zhen-Hua Ling. Corrective retrieval augmented generation, 2024.


[32] LangGraph CRAG Tutorial. Langgraph crag: Contextualized retrieval-augmented generation tutorial. `[https:](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/)`
`[//langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/)` . Accessed: 2025-01-14.


[33] Soyeong Jeong, Jinheon Baek, Sukmin Cho, Sung Ju Hwang, and Jong C. Park. Adaptive-rag: Learning to adapt
retrieval-augmented large language models through question complexity, 2024.


[34] LangGraph Adaptive RAG Tutorial. Langgraph adaptive rag: Adaptive retrieval-augmented generation tutorial. `[https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_adaptive_rag/)` .
Accessed: 2025-01-14.


[35] Zhili Shen, Chenxin Diao, Pavlos Vougiouklis, Pascual Merita, Shriram Piramanayagam, Damien Graux, Dandan
Tu, Zeren Jiang, Ruofei Lai, Yang Ren, and Jeff Z. Pan. Gear: Graph-enhanced agent for retrieval-augmented
generation, 2024.


[36] LlamaIndex. Introducing agentic document workflows. `[https://www.llamaindex.ai/blog/](https://www.llamaindex.ai/blog/introducing-agentic-document-workflows)`
`[introducing-agentic-document-workflows](https://www.llamaindex.ai/blog/introducing-agentic-document-workflows)`, 2025. Accessed: 2025-01-13.


35


[37] AWS Machine Learning Blog. How twitch used agentic workflow with rag on amazon
bedrock to supercharge ad sales. `[https://aws.amazon.com/blogs/machine-learning/](https://aws.amazon.com/blogs/machine-learning/how-twitch-used-agentic-workflow-with-rag-on-amazon-bedrock-to-supercharge-ad-sales/)`
`[how-twitch-used-agentic-workflow-with-rag-on-amazon-bedrock-to-supercharge-ad-sales/](https://aws.amazon.com/blogs/machine-learning/how-twitch-used-agentic-workflow-with-rag-on-amazon-bedrock-to-supercharge-ad-sales/)`,
2025. Accessed: 2025-01-13.


[38] LlamaCloud Demo Repository. Patient case summary workflow using llamacloud. `[https:](https://github.com/run-llama/llamacloud-demo/blob/main/examples/document_workflows/patient_case_summary/patient_case_summary.ipynb)`
```
  //github.com/run-llama/llamacloud-demo/blob/main/examples/document_workflows/
```

`[patient_case_summary/patient_case_summary.ipynb](https://github.com/run-llama/llamacloud-demo/blob/main/examples/document_workflows/patient_case_summary/patient_case_summary.ipynb)`, 2025. Accessed: 2025-01-13.


[39] LlamaCloud Demo Repository. Contract review workflow using llamacloud. `[https://github.com/](https://github.com/run-llama/llamacloud-demo/blob/main/examples/document_workflows/contract_review/contract_review.ipynb)`
```
  run-llama/llamacloud-demo/blob/main/examples/document_workflows/contract_review/
```

`[contract_review.ipynb](https://github.com/run-llama/llamacloud-demo/blob/main/examples/document_workflows/contract_review/contract_review.ipynb)`, 2025. Accessed: 2025-01-13.


[40] LlamaCloud Demo Repository. Auto insurance claims workflow using llamacloud. `[https:](https://github.com/run-llama/llamacloud-demo/blob/main/examples/document_workflows/auto_insurance_claims/auto_insurance_claims.ipynb)`
```
  //github.com/run-llama/llamacloud-demo/blob/main/examples/document_workflows/auto_
```

`[insurance_claims/auto_insurance_claims.ipynb](https://github.com/run-llama/llamacloud-demo/blob/main/examples/document_workflows/auto_insurance_claims/auto_insurance_claims.ipynb)`, 2025. Accessed: 2025-01-13.


[41] LlamaCloud Demo Repository. Research paper report generation workflow using llamacloud.
```
  https://github.com/run-llama/llamacloud-demo/blob/main/examples/report_generation/
```

`[research_paper_report_generation.ipynb](https://github.com/run-llama/llamacloud-demo/blob/main/examples/report_generation/research_paper_report_generation.ipynb)`, 2025. Accessed: 2025-01-13.


[42] LangGraph Agentic RAG Tutorial. Langgraph agentic rag: Nodes and edges tutorial. `[https://langchain-ai.](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#nodes-and-edges)`
`[github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#nodes-and-edges](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/#nodes-and-edges)` . Accessed:
2025-01-14.


[43] LlamaIndex Blog. Agentic rag with llamaindex. `[https://www.llamaindex.ai/blog/](https://www.llamaindex.ai/blog/agentic-rag-with-llamaindex-2721b8a49ff6)`
`[agentic-rag-with-llamaindex-2721b8a49ff6](https://www.llamaindex.ai/blog/agentic-rag-with-llamaindex-2721b8a49ff6)` . Accessed: 2025-01-14.


[44] Hugging Face Cookbook. Agentic rag: Turbocharge your retrieval-augmented generation with query reformulation and self-query. `[https://huggingface.co/learn/cookbook/en/agent_rag](https://huggingface.co/learn/cookbook/en/agent_rag)` . Accessed: 2025-01-14.


[45] Qdrant Blog. Agentic rag: Combining rag with agents for enhanced information retrieval. `[https://qdrant.](https://qdrant.tech/articles/agentic-rag/)`
`[tech/articles/agentic-rag/](https://qdrant.tech/articles/agentic-rag/)` . Accessed: 2025-01-14.


[46] crewAI Inc. crewai: A github repository for ai projects. `[https://github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)`, 2025.
Accessed: 2025-01-15.


[47] AG2AI Contributors. Ag2: A github repository for advanced generative ai research. `[https://github.com/](https://github.com/ag2ai/ag2)`
`[ag2ai/ag2](https://github.com/ag2ai/ag2)`, 2025. Accessed: 2025-01-15.


[48] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun
Zhang, Jiale Liu, Ahmed Hassan Awadallah, Ryen W White, Doug Burger, and Chi Wang. Autogen: Enabling
next-gen llm applications via multi-agent conversation framework. 2023.


[49] Shaokun Zhang, Jieyu Zhang, Jiale Liu, Linxin Song, Chi Wang, Ranjay Krishna, and Qingyun Wu. Training
language model agents without modifying language models. _ICML’24_, 2024.


[50] OpenAI. Swarm: Lightweight multi-agent orchestration framework. `[https://github.com/openai/swarm](https://github.com/openai/swarm)` .
Accessed: 2025-01-14.


[51] LlamaIndex Documentation. Agentic rag using vertex ai. `[https://docs.llamaindex.ai/en/stable/](https://docs.llamaindex.ai/en/stable/examples/agent/agentic_rag_using_vertex_ai/)`
`[examples/agent/agentic_rag_using_vertex_ai/](https://docs.llamaindex.ai/en/stable/examples/agent/agentic_rag_using_vertex_ai/)` . Accessed: 2025-01-14.


[52] Microsoft. Semantic kernel overview, 2025. `[https://learn.microsoft.com/en-us/semantic-kernel/](https://learn.microsoft.com/en-us/semantic-kernel/overview/)`
`[overview/](https://learn.microsoft.com/en-us/semantic-kernel/overview/)` . Accessed: February 2, 2025.


[53] Microsoft. Semantic kernel github repository, 2025. `[https://github.com/microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel)` .
Accessed: February 2, 2025.


[54] IBM Granite Community. Agentic rag: Ai agents with ibm granite models. `[https://github.com/](https://github.com/ibm-granite-community/granite-snack-cookbook/blob/main/recipes/AI-Agents/Agentic_RAG.ipynb)`
```
  ibm-granite-community/granite-snack-cookbook/blob/main/recipes/AI-Agents/Agentic_
```

`[RAG.ipynb](https://github.com/ibm-granite-community/granite-snack-cookbook/blob/main/recipes/AI-Agents/Agentic_RAG.ipynb)` . Accessed: 2025-01-14.


[55] Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. Beir: A heterogenous
benchmark for zero-shot evaluation of information retrieval models, 2021.


[56] Payal Bajaj, Daniel Campos, Nick Craswell, Li Deng, Jianfeng Gao, Xiaodong Liu, Rangan Majumder, Andrew
McNamara, Bhaskar Mitra, Tri Nguyen, Mir Rosenberg, Xia Song, Alina Stoica, Saurabh Tiwary, and Tong
Wang. Ms marco: A human generated machine reading comprehension dataset, 2018.


[57] Nick Craswell, Bhaskar Mitra, Emine Yilmaz, Daniel Campos, Jimmy Lin, Ellen M. Voorhees, and Ian Soboroff.
Overview of the trec 2022 deep learning track. In _Text REtrieval Conference (TREC)_ . NIST, TREC, March 2023.


36


[58] Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. Musique: Multihop questions
via single-hop question composition, 2022.

[59] Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, and Akiko Aizawa. Constructing a multi-hop qa dataset
for comprehensive evaluation of reasoning steps, 2020.

[60] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. Hotpotqa: A dataset for diverse, explainable multi-hop question answering, 2018.

[61] Robert Friel, Masha Belyi, and Atindriyo Sanyal. Ragbench: Explainable benchmark for retrieval-augmented
generation systems, 2024.

[62] David Rau, Hervé Déjean, Nadezhda Chirkova, Thibault Formal, Shuai Wang, Vassilina Nikoulina, and Stéphane
Clinchant. Bergen: A benchmarking library for retrieval-augmented generation, 2024.

[63] Jiajie Jin, Yutao Zhu, Xinyu Yang, Chenghao Zhang, and Zhicheng Dou. Flashrag: A modular toolkit for efficient
retrieval-augmented generation research, 2024.

[64] Costas Mavromatis and George Karypis. Gnn-rag: Graph neural retrieval for large language model reasoning,
2024.

[65] Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle
Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, Kristina Toutanova, Llion Jones, Matthew Kelcey, Ming-Wei
Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc Le, and Slav Petrov. Natural questions: A benchmark for question
answering research. _Transactions of the Association for Computational Linguistics_, 7:452–466, 2019.

[66] Mandar Joshi, Eunsol Choi, Daniel S. Weld, and Luke Zettlemoyer. Triviaqa: A large scale distantly supervised
challenge dataset for reading comprehension, 2017.

[67] Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and Percy Liang. Squad: 100,000+ questions for machine
comprehension of text, 2016.

[68] Jonathan Berant, Andrew K. Chou, Roy Frostig, and Percy Liang. Semantic parsing on freebase from questionanswer pairs. In _Conference on Empirical Methods in Natural Language Processing_, 2013.

[69] Alex Mallen, Akari Asai, Victor Zhong, Rajarshi Das, Daniel Khashabi, and Hannaneh Hajishirzi. When not to
trust language models: Investigating effectiveness of parametric and non-parametric memories. In Anna Rogers,
Jordan Boyd-Graber, and Naoaki Okazaki, editors, _Proceedings of the 61st Annual Meeting of the Association for_
_Computational Linguistics (Volume 1: Long Papers)_, pages 9802–9822, Toronto, Canada, July 2023. Association
for Computational Linguistics.

[70] Angela Fan, Yacine Jernite, Ethan Perez, David Grangier, Jason Weston, and Michael Auli. Eli5: Long form
question answering, 2019.

[71] Tomáš Koˇciský, Jonathan Schwarz, Phil Blunsom, Chris Dyer, Karl Moritz Hermann, Gábor Melis, and Edward
Grefenstette. The narrativeqa reading comprehension challenge. 2017.

[72] Ivan Stelmakh, Yi Luan, Bhuwan Dhingra, and Ming-Wei Chang. Asqa: Factoid questions meet long-form
answers, 2023.

[73] Ming Zhong, Da Yin, Tao Yu, Ahmad Zaidi, Mutethia Mutuma, Rahul Jha, Ahmed Hassan Awadallah, Asli
Celikyilmaz, Yang Liu, Xipeng Qiu, and Dragomir Radev. QMSum: A new benchmark for query-based
multi-domain meeting summarization. pages 5905–5921, June 2021.

[74] Pradeep Dasigi, Kyle Lo, Iz Beltagy, Arman Cohan, Noah A. Smith, and Matt Gardner. A dataset of informationseeking questions and answers anchored in research papers. In Kristina Toutanova, Anna Rumshisky, Luke
Zettlemoyer, Dilek Hakkani-Tur, Iz Beltagy, Steven Bethard, Ryan Cotterell, Tanmoy Chakraborty, and Yichao
Zhou, editors, _Proceedings of the 2021 Conference of the North American Chapter of the Association for_
_Computational Linguistics: Human Language Technologies_, pages 4599–4610, Online, June 2021. Association
for Computational Linguistics.

[75] Timo Möller, Anthony Reina, Raghavan Jayakumar, and Malte Pietsch. COVID-QA: A question answering
dataset for COVID-19. In _ACL 2020 Workshop on Natural Language Processing for COVID-19 (NLP-COVID)_,
2020.

[76] Xidong Wang, Guiming Hardy Chen, Dingjie Song, Zhiyi Zhang, Zhihong Chen, Qingying Xiao, Feng Jiang,
Jianquan Li, Xiang Wan, Benyou Wang, and Haizhou Li. Cmb: A comprehensive medical benchmark in chinese,
2024.

[77] Richard Yuanzhe Pang, Alicia Parrish, Nitish Joshi, Nikita Nangia, Jason Phang, Angelica Chen, Vishakh
Padmakumar, Johnny Ma, Jana Thompson, He He, and Samuel R. Bowman. Quality: Question answering with
long input texts, yes!, 2022.


37


[78] Alon Talmor, Jonathan Herzig, Nicholas Lourie, and Jonathan Berant. CommonsenseQA: A question answering
challenge targeting commonsense knowledge. In Jill Burstein, Christy Doran, and Thamar Solorio, editors,
_Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational_
_Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)_, pages 4149–4158, Minneapolis,
Minnesota, June 2019. Association for Computational Linguistics.


[79] Xiaoxin He, Yijun Tian, Yifei Sun, Nitesh V. Chawla, Thomas Laurent, Yann LeCun, Xavier Bresson, and Bryan
Hooi. G-retriever: Retrieval-augmented generation for textual graph understanding and question answering,
2024.


[80] Sha Li, Heng Ji, and Jiawei Han. Document-level event argument extraction by conditional generation, 2021.


[81] Seth Ebner, Patrick Xia, Ryan Culkin, Kyle Rawlins, and Benjamin Van Durme. Multi-sentence argument
linking, 2020.


[82] Emily Dinan, Stephen Roller, Kurt Shuster, Angela Fan, Michael Auli, and Jason Weston. Wizard of wikipedia:
Knowledge-powered conversational agents, 2019.


[83] Hongru Wang, Minda Hu, Yang Deng, Rui Wang, Fei Mi, Weichao Wang, Yasheng Wang, Wai-Chung Kwan,
Irwin King, and Kam-Fai Wong. Large language models as source planner for personalized knowledge-grounded
dialogue, 2023.


[84] Xinchao Xu, Zhibin Gou, Wenquan Wu, Zheng-Yu Niu, Hua Wu, Haifeng Wang, and Shihang Wang. Long time
no see! open-domain conversation with long-term persona memory, 2022.


[85] Tsung-Hsien Wen, Milica Gaši´c, Nikola Mrkši´c, Lina M. Rojas-Barahona, Pei-Hao Su, Stefan Ultes, David
Vandyke, and Steve Young. Conditional generation and snapshot learning in neural dialogue systems. In
_Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing_, pages 2153–2162,
Austin, Texas, November 2016. Association for Computational Linguistics.


[86] Ruining He and Julian McAuley. Ups and downs: Modeling the visual evolution of fashion trends with one-class
collaborative filtering. In _Proceedings of the 25th International Conference on World Wide Web_, WWW ’16, page
507–517, Republic and Canton of Geneva, CHE, 2016. International World Wide Web Conferences Steering
Committee.


[87] Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. HellaSwag: Can a machine really
finish your sentence? In Anna Korhonen, David Traum, and Lluís Màrquez, editors, _Proceedings of the 57th_
_Annual Meeting of the Association for Computational Linguistics_, pages 4791–4800, Florence, Italy, July 2019.
Association for Computational Linguistics.


[88] Seungone Kim, Se June Joo, Doyoung Kim, Joel Jang, Seonghyeon Ye, Jamin Shin, and Minjoon Seo. The
cot collection: Improving zero-shot and few-shot learning of language models via chain-of-thought fine-tuning,
2023.


[89] Amrita Saha, Vardaan Pahuja, Mitesh M. Khapra, Karthik Sankaranarayanan, and Sarath Chandar. Complex
sequential question answering: Towards learning to converse over linked question answer pairs with a knowledge
graph. 2018.


[90] James Thorne, Andreas Vlachos, Christos Christodoulopoulos, and Arpit Mittal. FEVER: a large-scale dataset for
fact extraction and VERification. In Marilyn Walker, Heng Ji, and Amanda Stent, editors, _Proceedings of the 2018_
_Conference of the North American Chapter of the Association for Computational Linguistics: Human Language_
_Technologies, Volume 1 (Long Papers)_, pages 809–819, New Orleans, Louisiana, June 2018. Association for
Computational Linguistics.


[91] Neema Kotonya and Francesca Toni. Explainable automated fact-checking for public health claims, 2020.


[92] Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot, Dan Roth, and Jonathan Berant. Did aristotle use a laptop?
a question answering benchmark with implicit reasoning strategies, 2021.


[93] Hiroaki Hayashi, Prashant Budania, Peng Wang, Chris Ackerson, Raj Neervannan, and Graham Neubig. Wikiasp:
A dataset for multi-domain aspect-based summarization, 2020.


[94] Shashi Narayan, Shay B. Cohen, and Mirella Lapata. Don’t give me the details, just the summary! topic-aware
convolutional neural networks for extreme summarization, 2018.


[95] Richard Socher, Alex Perelygin, Jean Wu, Jason Chuang, Christopher D. Manning, Andrew Ng, and Christopher
Potts. Recursive deep models for semantic compositionality over a sentiment treebank. In David Yarowsky,
Timothy Baldwin, Anna Korhonen, Karen Livescu, and Steven Bethard, editors, _Proceedings of the 2013_
_Conference on Empirical Methods in Natural Language Processing_, pages 1631–1642, Seattle, Washington,
USA, October 2013. Association for Computational Linguistics.


38


[96] Sourav Saha, Jahedul Alam Junaed, Maryam Saleki, Arnab Sen Sharma, Mohammad Rashidujjaman Rifat,
Mohamed Rahouti, Syed Ishtiaque Ahmed, Nabeel Mohammed, and Mohammad Ruhul Amin. Vio-lens: A novel
dataset of annotated social network posts leading to different forms of communal violence and its evaluation. In
Firoj Alam, Sudipta Kar, Shammur Absar Chowdhury, Farig Sadeque, and Ruhul Amin, editors, _Proceedings_
_of the First Workshop on Bangla Language Processing (BLP-2023)_, pages 72–84, Singapore, December 2023.
Association for Computational Linguistics.

[97] Hamel Husain, Ho-Hsiang Wu, Tiferet Gazit, Miltiadis Allamanis, and Marc Brockschmidt. Codesearchnet
challenge: Evaluating the state of semantic code search, 2020.

[98] Nandan Thakur, Luiz Bonifacio, Xinyu Zhang, Odunayo Ogundepo, Ehsan Kamalloo, David Alfonso-Hermelo,
Xiaoguang Li, Qun Liu, Boxing Chen, Mehdi Rezagholizadeh, and Jimmy Lin. "knowing when you don’t know":
A multilingual relevance assessment dataset for robust retrieval-augmented generation, 2024.

[99] Stephen Merity, Caiming Xiong, James Bradbury, and Richard Socher. Pointer sentinel mixture models, 2016.

[100] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert,
Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training verifiers to
solve math word problems, 2021.

[101] Ralf Steinberger, Bruno Pouliquen, Anna Widiger, Camelia Ignat, Tomaž Erjavec, Dan Tufi¸s, and Dániel Varga.
The JRC-Acquis: A multilingual aligned parallel corpus with 20+ languages. In Nicoletta Calzolari, Khalid
Choukri, Aldo Gangemi, Bente Maegaard, Joseph Mariani, Jan Odijk, and Daniel Tapias, editors, _Proceedings of_
_the Fifth International Conference on Language Resources and Evaluation (LREC‘06)_, Genoa, Italy, May 2006.
European Language Resources Association (ELRA).


39


