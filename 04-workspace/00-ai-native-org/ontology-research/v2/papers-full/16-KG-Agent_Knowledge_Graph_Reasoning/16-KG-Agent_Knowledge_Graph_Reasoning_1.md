<!-- Source: 16-KG-Agent_Knowledge_Graph_Reasoning.pdf | Chunk 1/2 -->

## **KG-Agent: An Efficient Autonomous Agent Framework for Complex** **Reasoning over Knowledge Graph**

**Jinhao Jiang** **[1,3]** **, Kun Zhou** **[2,3]** **, Wayne Xin Zhao** **[1,3]** _[∗]_ **, Yang Song** **[4]** _[∗]_ **,**
**Chen Zhu** **[5]** **, Hengshu Zhu** **[5]** **, Ji-Rong Wen** **[1,2,3]**

1Gaoling School of Artificial Intelligence, Renmin University of China.
2School of Information, Renmin University of China.
3Beijing Key Laboratory of Big Data Management and Analysis Methods.
4NLP Center, BOSS Zhipin. 5Career Science Lab, BOSS Zhipin.
jiangjinhao@ruc.edu.cn, batmanfly@gmail.com



**Abstract**


In this paper, we aim to improve the reasoning
ability of large language models (LLMs) over
knowledge graphs (KGs) to answer complex
questions. Inspired by existing methods that design the interaction strategy between LLMs and
KG, we propose an autonomous LLM-based
agent framework, called **KG-Agent**, which
enables a small LLM to actively make decisions until finishing the reasoning process over
KGs. In KG-Agent, we integrate the LLM,
multifunctional toolbox, KG-based executor,
and knowledge memory, and develop an iteration mechanism that autonomously selects the
tool then updates the memory for reasoning
over KG. To guarantee the effectiveness, we
leverage program language to formulate the
multi-hop reasoning process over the KG, and
synthesize a code-based instruction dataset to
fine-tune the base LLM. Extensive experiments
demonstrate that only using 10K samples for
tuning LLaMA-7B can outperform state-of-theart methods using larger LLMs or more data, on
both in-domain and out-domain datasets. Our
code and data will be publicly released.


**1** **Introduction**


Despite the remarkable performance on various
NLP tasks (Brown et al., 2020; Zhao et al., 2023),
large language models (LLMs) still have limited capacities in solving complex tasks (Hu et al., 2023b)
solely based on their parametric knowledge, _e.g.,_
multi-hop and knowledge-intensive reasoning (Lan
et al., 2023). Knowledge graph (KG), which stores
massive knowledge triples in a graph-structured format, has been broadly used to complement LLMs
with external knowledge (Pan et al., 2023).
Due to the large volume and structured format of
KG data, it is not easy for LLMs to effectively utilize the information from KG. Recent work mainly
adopts _retrieval-augmented_ (Ye et al., 2022) or
_synergy-augmented_ (Jiang et al., 2023b) methods to


_∗_ Corresponding author.



enhance LLMs with KG data. The former approach
retrieves and serializes the task-related triples as
part of the prompt for LLMs, while the latter approach designs an information interaction mechanism between KG and LLMs to iteratively find
the solution to the question. In particular, synergyaugmented methods can benefit from the structured
search on KG ( _e.g.,_ SPARQL) and the language
understanding capacity of LLMs, achieving comparable or even better performance compared with
previous state-of-the-art methods (Gu et al., 2023).

However, there are still two major limitations
on existing synergy-augmented methods. First,
the information interaction mechanism between
LLM and KG is often pre-defined ( _e.g.,_ following
a human-crafted multi-round plan), which cannot
flexibly adapt to various complex tasks (Luo et al.,
2023; Jiang et al., 2023b). For instance, it would become ineffective to handle the unintended requirements in the reasoning process, _e.g.,_ varied difficulties or constraints. Second, these methods (Wang
et al., 2023a) mostly rely on stronger closed-source
LLM APIs ( _e.g.,_ ChatGPT and GPT-4) to understand or learn to solve complex tasks. However,
the distilled plans or procedures, also limited to
special task settings or capacity levels, may not be
best suited for instructing these weaker models.

To address these issues, in this paper, we propose the **KG-Agent**, an autonomous LLM-based
agent framework for complex reasoning tasks over
KG. The motivations are twofold: (1) designing
autonomous reasoning approaches that can actively
make decisions during reasoning, without human
assistance; (2) enabling relatively small models
( _e.g.,_ 7B LLM) to effectively perform complex reasoning, without reliance on close-sourced LLM
APIs. To achieve this, our approach makes three
major technical contributions. First, we extend the
LLM’s capacity to manipulate structured data by
curating a multifunctional toolbox, enabling LLM
to perform discrete or advanced operations ( _e.g.,_


filtering, counting, and retrieval) on KG data and
intermediate results. Second, we leverage existing
KG reasoning datasets for synthesizing code-based
instruction data to fine-tune the LLM, where we
first generate the program according to the reasoning chain on KG and then synthesize the instruction
data. Third, we propose an autonomous iteration
mechanism based on tool selection and memory
updation that integrates the tuned LLM, multifunctional toolbox, KG-based executor, and knowledge
memory, for autonomously reasoning over KG.

To verify the effectiveness, we evaluate KGAgent on both in-domain and out-of-domain tasks
including KG-based question answering (KGQA)
and open domain question answering (ODQA).
With much fewer training data ( _i.e.,_ 10K samples)
for tuning a smaller LLM ( _i.e.,_ LLaMA-7B), our
approach can outperform competitive LLM-based
baselines on in-domain datasets ( _e.g.,_ using about
36% and 23% of the original training set amount
while obtaining 7.5% and 2.7% relative improvement of F1 on CWQ and GrailQA respectively).
On the out-of-domain datasets, the zero-shot performance of our KG-Agent is better than competitive full-data supervised fine-tuning models ( _e.g.,_
9.7% and 8.5% relative improvement of accuracy
on WQ-Freebase and TQ-Wiki, respectively).


**2** **Related Work**


**LLM-based KG Reasoning.** Benefitting from
the powerful zero-shot and few-shot capability, recent studies have leveraged LLMs to perform reasoning over KG. Recent work can be roughly divided into _retrieval-augmented_ (Shu et al., 2022)
and _synergy-augmented_ (Gu et al., 2023) two types.
The retrieval-augmented method is to retrieve and
serialize the triples from the KG, and then feed it
to the LLM to help generate the final results ( _e.g.,_
answers or SPARQL query) (Ye et al., 2022). Such
a way loses the structured information in the original KG and may retrieve redundant knowledge,
limiting LLMs’ understanding. To relieve these
problems, the synergy-augmented methods design
an information interaction mechanism between
LLMs and KGs to enable LLMs to query KGs
multiple times to answer the question (Jiang et al.,
2023b). Specifically, they either first generate the
full plan (Li et al., 2023) and then ground it on KG,
or make a plan step-by-step based on the KG (Luo
et al., 2023). Although obtaining better performance, the information interaction mechanism in



existing methods often follows a pre-defined way,
which cannot flexibly adapt to various complex
tasks. In contrast, our proposed KG-Agent can autonomously make decisions during reasoning over
KG, without human assistance.


**LLM-based Agents.** Recently, LLMs have
shown surprising long-horizon planning and reasoning capabilities (Shinn et al., 2023; Zhong et al.,
2023), and LLM-based agents have gradually become a hot topic for autonomously solving complex interactive tasks (Wang et al., 2023b). A large
number of agents focus on general-purpose task
solving. As the representative projects, ReAct (Yao
et al., 2023) proposes a prompting method to convert LLMs ( _e.g.,_ ChatGPT) as language agents, to
interact with the external environment, receive the
feedback, and then generate the action for next
step reasoning. Then, AutoGPT [1] further empowers LLMs ( _i.e.,_ GPT4) with long/short-term memory management and external tools like search engines to autonomously address a user request. In
addition, several other agents also focus on specific domains, such as WebGPT (Nakano et al.,
2021) for the web-browsing environment, MMREACT (Yang et al., 2023) for the multi-modal
scenario, and ProgPrompt (Singh et al., 2023) for
the real-life environment. However, recent works
involving language agents mostly rely on stronger
closed-source LLM APIs ( _e.g.,_ ChatGPT and GPT4) to understand or learn to solve complex tasks.
Our KG-Agent is the first autonomous agent framework to support complex reasoning over KG only
relying on a relatively smaller 7B LLM.


**3** **Preliminary**


In this section, we first formally define knowledge
graph (KG), and then formalize the complex knowledge reasoning task based on KG.


**Knowledge Graph (KG).** A knowledge graph typically consists of a large number of fact triples,
expressed as _G_ = _{⟨e, r, e_ _[′]_ _⟩|e, e_ _[′]_ _∈E, r ∈R}_,
where _E_ and _R_ denote the entity set and relation
set, respectively. A triple _⟨e, r, e_ _[′]_ _⟩_ describes a factual knowledge that a relation _r_ exists between the
head entity _e_ and tail entity _e_ _[′]_ . Each entity _e_ is
assigned a unique entity ID (or string value), and
belongs to one entity type _t_ such as _Country_ and
_Person_ . Furthermore, we introduce _neighboring_


1https://github.com/Significant-Gravitas/AutoGPT


_relations_ to denote both the incoming and outgoing relations for a set of entities _{e}_, denoted as
_R{e}_ = _{r|⟨e, r, e_ _[′]_ _⟩∈G} ∪{r|⟨e_ _[′]_ _, r, e⟩∈G}_ .


**Problem Formulation.** In this work, we assume
that a KG is available and contains the answer entities for the given natural language question. Our
objective is to develop a LLM-based agent that
can autonomously infer the answer to the question
based on the given KG. As it has been shown that
domain-specific interface is helpful for LLMs to
manipulate the structured data (Jiang et al., 2023b),
we further assume that a toolbox can be provided
to facilitate the access to the information of KG.
Formally, given a natural language question _q_, and
a toolbox _T_ and a KG _G_, we aim to develop a capable agent to deduce the final answers _Aq_ = _{e}_
for the question _q_ by leveraging the tools in _T_ and
the knowledge information in _G_ .


**4** **Approach**


In this part, we present the proposed **KG-Agent**
for autonomously solving complex reasoning tasks
over KG. The core of our KG-Agent framework is
a well-instructed LLM, which can autonomously
make decisions when reasoning over KG. We first
extend the LLM’s capacities by designing a toolbox
with supporting tools to manipulate the KG data or
intermediate results (Section 4.1). To enhance the
step-by-step reasoning capacity, we leverage existing knowlege graph question answering (KGQA)
datasets to synthesize KG reasoning programs and
convert them into formatted instruction tuning data
(Section 4.2). Finally, we design an effective agent
framework based on the knowledge memory to support autonomous reasoning over KG (Section 4.3).
Next, we give the technical details of KG-Agent.


**4.1** **Toolbox for Knowledge Graph**


Since LLMs struggle to accurately manipulate the
structured data (Jiang et al., 2023b), we construct a
supporting toolbox for easing the utilization of the
KG information. According to existing work (Gu
et al., 2021; Cao et al., 2022), reasoning over KG
( _e.g.,_ Freebase or Wikidata) typically requires three
fundamental operations, namely extracting information from KG, filtering irrelevant information
based on the semantics of the question, and operating on the extracted information. Therefore,
we design three types of tools for LLMs reasoning
over KG, _i.e.,_ extraction, semantic, and logic tools.

_•_ **Extraction tools** aim to facilitate the access to



information from KG. Considering the basic data
types in KG, we design five tools to support the access to the relations ( _get_relation_ ), the head/tail entities ( _get_head_entity_ / _get_tail_entity_ ), and entities
with specific type or constraint ( _get_entity_by_type_ /
_get_entity_by_constraint_ ), _w.r.t._ some entity set or
other input information ( _e.g.,_ relation or type).

_•_ **Logic tools** aim to support basic manipulation
operations on the extracted KG information, including entity counting ( _count_ ), entity set intersection
( _intersect_ ) and union ( _union_ ), condition verification
( _judge_ ), and ending the reasoning process with the
current entity set as the final answer(s) ( _end_ ).

_•_ **Semantic tools** are developed by utilizing pretrained models to implement specific functions, including relation retrieval ( _retrieve_relation_ ) and entity disambiguation ( _disambiguate_entity_ ). These
tools extend the basic operations on KGs and can
support advanced functionalities for KG reasoning.
We summarize the detailed definition and usage
of the tools in Table 8 at the Appendix B. Note that
since the format and usage for each tool have been
defined in a unified way, the toolbox for KG can be
flexibly extended according to the real needs.


**4.2** **KG-Agent Instruction Tuning**


To enable the autonomous reasoning process, we
construct a high-quality instruction dataset for finetuning a small LLM ( _i.e.,_ LLaMA2-7B). For this
purpose, we first leverage existing KG based question answering (KGQA) datasets to generate the
KG reasoning program, and then decompose it into
multiple steps. Finally, each step is formulated as
the instruction data with input and output.


**4.2.1** **KG Reasoning Program Generation**


Instead of distilling from close-sourced LLMs ( _e.g.,_
GPT-4), we propose to leverage existing KGQA
datasets to synthesize the KG reasoning program.
These KGQA datasets contain the annotated SQL
queries that can be executed to directly extract the
answer entities for each question. In particular, the
SQL query generally includes the relation chain,
conditions, or constraints, which are beneficial for
reasoning program synthesis. Concretely, we first
ground the SQL query on the KG to obtain a query
graph, then extract the reasoning chain and constraint conditions from the query graph, and finally
decompose the chain into multiple code snippets
as the reasoning program.


**Reasoning Chain Extraction.** Since the whole


Which sports team for which **Cristiano** **Knowledge Memory Updating** **Autonomous Reasoning**
**Ronaldo** played in 2011 was founded last ? **t=1**


```
get_relation(m.02xt6q)

```




**t=1**



**t=2**


**t=3**


**t=4**





_The answer is_



_Portugal national_

_football team_


```
out:[teams,…] in:[athlete,…]

 v0 = get_tail_entity(
   m.02xt6q,team)

     v0={m.050fh,…}

  get_relation(v0)

 out:[from,…] in:[roster,…]

  v1 = get_entity_by_
constraint(v0,from,=,2011)

     v1={m.06l22,…}

```






**Planner**


**Toolbox** **Executor**
















|Question Toolbox Definition<br>His_ Pro Cur_KG_Info<br>linked_entity<br>t=1 = m.02xt6q t=1 None<br>get_relation<br>teams, athlete<br>t=2 (m.02xt6q) t=2 …<br>v0 = get_tail_<br>entity (m.0xt6q, None<br>t=3 team) t=3<br>get_relation<br>(v0) t=4from …, roster<br>t=4|Col2|Col3|
|---|---|---|
|_Question_<br>_Toolbox Definition_<br>linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>teams, athlete<br>…<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**<br>_His_ Pro_<br>**t=1**<br>None<br>_Cur_KG_Info_<br>**t=2**<br>**t=4**<br>from, roster<br>…<br>None<br>**t=3**|linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**|**t=1**<br>None|
|_Question_<br>_Toolbox Definition_<br>linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>teams, athlete<br>…<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**<br>_His_ Pro_<br>**t=1**<br>None<br>_Cur_KG_Info_<br>**t=2**<br>**t=4**<br>from, roster<br>…<br>None<br>**t=3**|linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**||
|_Question_<br>_Toolbox Definition_<br>linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>teams, athlete<br>…<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**<br>_His_ Pro_<br>**t=1**<br>None<br>_Cur_KG_Info_<br>**t=2**<br>**t=4**<br>from, roster<br>…<br>None<br>**t=3**|linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**|teams, athlete<br>…<br>**t=2**|
|_Question_<br>_Toolbox Definition_<br>linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>teams, athlete<br>…<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**<br>_His_ Pro_<br>**t=1**<br>None<br>_Cur_KG_Info_<br>**t=2**<br>**t=4**<br>from, roster<br>…<br>None<br>**t=3**|linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**||
|_Question_<br>_Toolbox Definition_<br>linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>teams, athlete<br>…<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**<br>_His_ Pro_<br>**t=1**<br>None<br>_Cur_KG_Info_<br>**t=2**<br>**t=4**<br>from, roster<br>…<br>None<br>**t=3**|linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**|None<br>**t=3**|
|_Question_<br>_Toolbox Definition_<br>linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>teams, athlete<br>…<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**<br>_His_ Pro_<br>**t=1**<br>None<br>_Cur_KG_Info_<br>**t=2**<br>**t=4**<br>from, roster<br>…<br>None<br>**t=3**|linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**||
|_Question_<br>_Toolbox Definition_<br>linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>teams, athlete<br>…<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**<br>_His_ Pro_<br>**t=1**<br>None<br>_Cur_KG_Info_<br>**t=2**<br>**t=4**<br>from, roster<br>…<br>None<br>**t=3**|linked_entity<br>= m.02xt6q<br>**t=1**<br>get_relation<br>(m.02xt6q)<br>**t=2**<br>v0 = get_tail_<br>entity (m.0xt6q,<br>team)<br>**t=3**<br>get_relation<br>(v0)<br>**t=4**|**t=4**<br>from, roster<br>…|
















|Query Graph m.02xt6q KG Reasoning Program Input "!<br>Grounded on KG (Cristiano Ronaldo) Question Toolbox<br>get_relation(m.02xt6q); Current KG Information<br>team v0=get_tail_entity(m.02xt6q, team); History Program<br>get_relation(v0); Output $!<br>from ? # (CVT) v1=get_entity_by_constraint(v0,from,=,2011); get_relation(m.02xt6q)<br>2011 m.050fh, m.03b04g<br>m.02rqxc, m.06l22 get_relation(v1); Input ""<br>constraint 1 v2=get_tail_entity(v1, roster); Question Toolbox<br>roster Current KG Information<br>get_relation(v2);<br>History Program<br>argmax founded ? " v3=get_entity_by_constraint(v2,founded,argmax); Output $"<br>constraint 2 ans=end(v3) v0=get_tail_entity(m.02xt6q, team)|Col2|Col3|
|---|---|---|
|**`get_relation(m.02xt6q);`**<br>**`v0=get_tail_entity(m.02xt6q, team);`**<br>**`get_relation(v0);`**<br>**`v1=get_entity_by_constraint(v0,from,=,2011);`**<br>**`get_relation(v1);`**<br>**`v2=get_tail_entity(v1, roster);`**<br>**`get_relation(v2);`**<br>**`v3=get_entity_by_constraint(v2,founded,argmax);`**<br>**`ans=end(v3)`**<br>**KG Reasoning Program**<br>team<br>roster<br>argmax<br>founded<br>_constraint 2_<br>? "<br>2011<br>from<br>_constraint 1_<br>? # (CVT)<br>m.050fh, m.03b04g<br>m.02rqxc, m.06l22<br>**Query Graph**<br>**Grounded on KG**<br>(Cristiano Ronaldo)<br>m.02xt6q<br>Question<br>Toolbox<br>Current KG Information<br>History Program<br>Input"!<br>Output$!<br>get_relation(m.02xt6q)<br>Question<br>Toolbox<br>Current KG Information<br>History Program<br>Output$"<br>v0=get_tail_entity(m.02xt6q, team)<br>Input""||team|
|2011<br>from<br>_constraint 1_|? # (CVT)<br>m.050fh, m.03b04g<br>m.02rqxc, m.06l22|? # (CVT)<br>m.050fh, m.03b04g<br>m.02rqxc, m.06l22|
|||roster|
|argmax<br>founded<br>_constraint 2_<br>? "|argmax<br>founded<br>_constraint 2_<br>? "|argmax<br>founded<br>_constraint 2_<br>? "|



Figure 1: The overview of our proposed KG-Agent. The top half is the workflow of our agent, and the bottom
half is an example of instruction fine-tuning data synthesis and the prompt template for the input-output pairs. For
brevity, we simplify the relation surface form.



KG is extremely large and contains irrelevant data,
the first step is to acquire a small KG subgraph
related to the question, referred to as _query graph_ .
Following previous work (Yin et al., 2020), we obtain the query graph from the KG via rule match.
As shown in Figure 1 (b), the query graph has a treelike structure that can be directly mapped to a logical form (Yin et al., 2020), and it can clearly depict
the execution flow of the SQL query to obtain the
answer. Second, starting from the mentioned entity
in the question ( _i.e., Cristiano Ronaldo_ ), we adopt
breadth-first search (BFS) to visit all the nodes on
the query graph. This strategy would finally produce a reasoning chain ( _e.g., teams→roster_team_ )
linking the start entity to the answer entity, and the
relevant constraint conditions ( _e.g., roster_from_ =
“2011”) or numerical operation ( _e.g., founded_ must
be last) can be naturally involved in this process.


**Reasoning Program Generation.** After extracting the reasoning chain, we next convert it into
multiple interrelated triples, where each triple generally corresponds to an intermediate reasoning
step. Finally, we reformulate the triples into several function calls with the code format, which
represents the tool invocation and can be executed
to obtain the corresponding triples based on the
KG. Given a triple _⟨e, r, e_ _[′]_ _⟩_, we craft a rule-based



method to synthesize the function calls that represent the information flow from _e_ to _e_ _[′]_ . Specifically,
we start from the _get_relation(e)_ function call to
obtain the current candidate relations _{r}_ associated with _e_ on the KG. Then, we select one relation
_r_ and pass it to other required function calls ( _e.g.,_
_get_tail_entity_ or _get_entity_by_constraint_ ), and
finally obtain new entities. Following the order of
the reasoning chain, we generate all the function
calls to compose the final KG reasoning program
for producing the instruction dataset. We show one
example in Figure 1 (b) to intuitively illustrate the
conversion process from the annotated SQL query
to our required KG reasoning program.


**4.2.2** **KG Reasoning Instruction Synthesis**


After obtaining the reasoning program on KG, we
further utilize it for synthesizing instruction data
for supervised fine-tuning (SFT). As discussed in
Section 4.2.1, our instruction data is highly based
on the reasoning program, which is aligned with
the intermediate reasoning steps for KGQA.


**Input-Output Pair Construction.** The synthetic
KG reasoning program consists of multiple function calls in a sequence. For each function call, we
aim to construct an input-output pair as the instruction. Specifically, the input contains the question,
toolbox definition, current KG information ( _i.e.,_ the


**Work**
**Method**
**Flow**



**Base** **Tool Memory** **[Multi]**
**Model** **Task**



Pangu pd T5-3B ✗ ✗ ✗
StructGPT pd ChatGPT ✓ ✗ ✗
RoG pd LLaMA-7B ✗ ✗ ✗
ChatDB auto ChatGPT ✗ ✓ ✗
KB-BINDER pd CodeX ✗ ✗ ✗


KG-Agent auto LLaMA2-7B ✓ ✓ ✓


Table 1: Comparison of different methods. _**Work Flow**_
describes that the interaction way between the LLM and
KG is pre-defined (“pd”) or autonomous (“auto”). _**Multi**_
_**Task**_ means whether to support generalization across
different KGs via multi-task learning.


next candidate relations of the current entity set),
and history reasoning program before the current
step; and the output is the function call at the current step. Next, after executing the function call
at the current reasoning step, the history reasoning program and current KG information in the
input will be accordingly updated, and the output
will be updated as the function call at the next
step. By iterating the above process, for each sample in the KGQA datasets, we can obtain multiple
input-output pairs derived from the corresponding
reasoning program, which depict the complete reasoning trajectory on the KG. To help LLMs better
understand, we further utilize a unified prompt, as
shown in Figure 1 (c), to format each input-output
pair and obtain the final instruction tuning data.


**Agent Instruction Tuning.** Based on the above
formatted instruction tuning data, we perform supervised fine-tuning on a small LLM ( _i.e.,_ LLaMA7B), which is much smaller than the backbone models in previous work (Jiang et al., 2023b). Formally,
for each sample, we formulate all input-output
pairs of the complete trajectory in the format of
_{⟨x_ 1 _, y_ 1 _⟩, ..., ⟨xt, yt⟩, ..., ⟨xn, yn⟩}_, where _⟨xt, yt⟩_
represent the input and ground-truth response in
the _t_ -th step and _n_ represents the total steps. For
simplicity, we denote each input and output as _x_
and _y_ below. During the instruction tuning process,
we feed the input _x_ and output _y_ into the decoderonly LLM and minimize the cross-entropy loss on
the ground-truth response _y_ as:



**4.3** **Autonomous Reasoning over KG**


After instruction tuning, we further design an effective agent framework that enables KG-Agent to autonomously perform multi-step reasoning over KG
for answer finding. The overall illustration of KGAgent is shown in Figure 1 (a). It mainly contains
four components, _i.e.,_ the core instruction-tuned
LLM (Section 4.2), referred to as the _LLM-based_
_planner_, the multifunctional _toolbox_ (Section 4.1),
the _KG-based executor_ for executing the tool invocation, and the _knowledge memory_ to record
the context and currently useful information in the
whole process. Next, we introduce how KG-Agent
performs autonomous reasoning over KG.


**Knolwedge Memory Initialization.** The knowledge memory preserves the currently useful information to support the LLM-based planner for making decisions. It mainly contains four parts of information, _i.e.,_ natural language question, toolbox
definition, current KG information, and history reasoning program. The former two parts are initialized with the given question and toolbox definition,
which remain unchanged during the reasoning process. The later two parts are initialized as an empty
list, which will be constantly updated at each step
after LLM generating the function call and executor
invoking the corresponding tool.


**Planner for Tool Selection.** Based on the current
knowledge memory, the LLM-based planner selects a tool to interact with KG at each step. Specifically, all the parts in the current knowledge memory will be formatted with corresponding prompt
template to compose the input (used in Agent Instruction Tuning in Section 4.2.2), and then the
LLM will generate one function call by selecting
a tool and its arguments from the input. Generally, the planner needs to invoke tools from the
pre-defined toolbox to address four types of task
requirements, _i.e.,_ linking the mentioned entity
to KG ( _e.g.,_ “ _get_candidate_entity_ ” and “ _disam-_
_biguate_entity_ ”), accessing the KG information
( _e.g., “get_relation”_ and _“get_head_entity”_ ), processing the intermediate results ( _e.g., “count”_ and
_“intersect”_ ), or returning the final answer to end the
reasoning process ( _e.g., “end”_ ).


**Executor for Memory Updation.** After the planner generates the function call, the KG-based executor will execute it using a program compiler. It
can cache or operate the intermediate variables, and



_L_ = _−_



_m_


log Pr( _yk|x, y<k_ ) _,_ (1)

_k_ =1



where _m_ denotes the number of tokens in _y_, _yk_ and
_y<k_ are the _k_ -th and previous tokens in the output.


**WebQSP** **CWQ** **GrailQA (F1)**
**Model**

**Hits@1** **F1** **Hits@1** **F1** **Overall** **I.I.D.** **Compositional** **Zero-shot**


GraftNet 66.4 60.4 36.8 32.7  -  -  -  NSM 68.7 62.8 47.6 42.4 - - - SubgraphRetrieval 69.5 64.1 49.3 46.3  -  -  -  UniKGQA 75.1 70.2 50.7 48.0 - - - ReasoningLM 78.5 71.0 69.0 64.9 - - - 

RNG-KBQA - 75.6 - - 76.8 89.0 68.9 74.7
Uni-Parser  - 75.8  -  - 76.5 88.3 71.4 73.4
ArcaneQA - 75.6 - - 76.9 89.2 73.9 72.8
PanGu w/ T5-3B - 79.6 - - 83.4 - - TIARA 75.2 78.9 - - 81.9 91.2 74.8 80.7
FC-KBQA - 76.9 - 56.4 83.8 91.5 77.3 83.1


ROG **85.7** 70.8 62.6 56.2 - - - ChatGPT 67.4 59.3 47.5 43.2 25.3 19.6 17.0 31.2
Davinci-003 70.8 63.9 51.4 47.6 30.1 23.5 22.0 36.4
GPT-4 73.2 62.3 55.6 49.9 31.7 25.0 20.6 39.2
StructGPT 72.6 63.7 54.3 49.6 54.6 70.4 44.3 50.5


Ours 83.3 **81.0** **72.2** **69.8** **86.1** **92.0** **80.0** **86.3**


Table 2: The results on the test set of WebQSP and CWQ, and dev set of GrailQA, which are based on Freebase
KG. We copy part of the results from Jiang et al. (2023b); Gu et al. (2023); Luo et al. (2023) and evaluate
ChatGPT,Davinci-003, GPT-4, and StructGPT with OpenAI API. Bold font denotes the best performance.



extract new entities or relations from the KG. After
execution, the knowledge memory will be accordingly updated. First, the current function call will
be added to the history reasoning program. Second,
if the invoked tool is to obtain the new information
from the KG ( _e.g.,_ “ _get_relation_ ”), the executor
will add it to the KG information for updating the
knowledge memory.


**Iterative Autonomous KG-Agent.** The KG-Agent
framework autonomously iterates the above tool
selection and memory updation process to perform
step-by-step reasoning, where the knowledge memory is used to maintain the accessed information
from KG. In this way, the multi-turn decisionmaking process of the agent is like walking on the
KG along relations. Once reaching the answer entities, the agent will automatically stop the iterative
process. Note that the whole process is agnostic to
the task types ( _e.g.,_ question answering) and some
specific KGs. Therefore, our approach is a general framework that can be applied to a variety of
complex tasks that require reasoning over any KGs.


**4.4** **Comparison to Previous Work**


Existing methods of reasoning over KG can be categorized into two classes based on their workflow.
The first line of research, such as KB-BINDER (Li
et al., 2023), Pangu (Gu et al., 2023), StructGPT (Jiang et al., 2023b), and RoG (Luo et al.,
2023), crafted a pre-defined interaction way be


tween LLM and KG, which cannot flexibly adapt
to various complex tasks. Another line of research,
such as ChatBD (Hu et al., 2023a), conducted
autonomous reasoning with chain-of-thought and
memory augmented. However, it relies on the
strong closed-source LLM APIs ( _e.g.,_ ChatGPT)
and cannot use tools to implement some specialized operations ( _e.g.,_ count). Our KG-Agent is the
first autonomous agent framework to support the
complex interaction between LLM and KG with
tool and memory augmented. Furthermore, we
implement this autonomous agent by instruction
tuning a smaller 7B open-source LLM compared
to the backbone LLM in KB-BINDER, StructGPT, and ChatDB. At the same time, the agent
instruction tuning data is constructed from various
KGs ( _e.g.,_ Wikidata and Freebase), which helps
our KG-Agent to learn the general autonomous
decision making capabilities over various KGs.


**5** **Experiment**


**5.1** **Experimental Setup**


We select four commonly-used KGQA datasets
as in-domain datasets, _i.e., WebQSP_, _CWQ_, and
_GrailQA_, which are based on Freebase, and _KQA_
_Pro_, which is based on Wikidata. And we select
three ODQA datasets as out-of-domain datasets,
_i.e., WQ_, _NQ_, and _TQ_ . Further, we consider three
types of baseline methods, _i.e., subgraph-based_
_reasoning_, _LM-based seq2seq generation_, and


**Model** **Overall** **Multi-hop** **Qualifier** **Comparison** **Logical** **Count** **Verify** **Zero-shot**


KVMemNet 16.61 16.50 18.47 1.17 14.99 27.31 54.70 0.06
EmbedKGQA 28.36 26.41 25.20 11.93 23.95 32.88 61.05 0.06
RGCN 35.07 34.00 27.61 30.03 35.85 41.91 65.88 0.00


RNN SPARQL 41.98 36.01 19.04 66.98 37.74 50.26 58.84 26.08
BART SPARQL 89.68 88.49 83.09 96.12 88.67 85.78 92.33 87.88


ChatGPT 24.96 24.22 26.37 39.15 25.51 10.76 54.70 15.67
Davinci-003 31.02 29.58 31.58 49.8 29.62 16.70 65.54 21.83
GPT-4 37.43 34.82 37.15 55.75 36.81 15.27 72.93 27.28


Ours **92.15** **91.03** **87.90** **96.32** **91.28** **88.21** **92.86** **91.40**


Table 3: The accuracy on the test set of KQA Pro, which is based on Wikidata KG. The results of Davinci-002,
GPT-4, and ChatGPT are evaluated by us and the results of other baselines are copied from Cao et al. (2022).



**Models** **NQ-Wiki** **TQ-Wiki** **WQ-Freebase**


T5-Base 30.94 27.63 24.06
T5-Large 31.21 29.40 24.70
BART-Base 29.47 25.43 21.95
BART-Large 32.60 33.05 26.33


Davinci-003 51.94 88.57 23.81
ChatGPT **57.49** **88.68** 23.23


Ours 33.00 35.89 **28.90**


Table 4: The results on the subsets of the dev sets from
the out-of-domain ODQA datasets.


_LLM-based methods_ for comparison on in-domain
datasets, and _Fine-tune based_ and _LLM-based_
methods for out-of-domain datasets. We show the
details of the above datasets, baselines, evaluation
protocol, and implementation in Appendix A.


**5.2** **Main Results**


**Results on In-domain Datasets.** Table 2 and Table 3 show the results on in-domain datasets based
on Freebase and Wikidata, respectively. First, LMbased seq2seq generation methods can achieve better F1 score compared to the subgraph-based reasoning methods on the WebQSP and KQA Pro.
It indicates that the SPARQL query generated by
the LM can obtain a more complete answer set,
and the structured query can better support some
complex operations ( _e.g.,_ maximum, count) than
the traditional subgraph-based reasoning methods.
Second, although LLMs are powerful, directly using Davinci-003, ChatGPT, and even GPT-4 still
has a large performance gap compared with the
best fine-tuned methods in WebQSP, GrailQA, and
KQA Pro, indicating the difficulty of answering
complex questions solely by LLMs.
Finally, our KG-Agent is substantially better
than all other competitive baselines in all datasets
after instructing tuning on the mixed data. With the



**Models** **MQA-1hop** **MQA-2hop** **MQA-3hop**


GraftNet 82.5 - EmbedKGQA 92.0 40.7 34.6
NSM 94.8 97.0 91.0
TransferNet 96.5 97.5 90.1


ChatGPT 61.9 31.0 43.2
StructGPT 94.2 93.9 80.2


Ours **97.1** **98.0** **92.1**


Table 5: The results on the three subsets of MetaQA. We
copy the results of baselines from Jiang et al. (2023b).


mutual augmentation between different datasets,
our approach achieves 1.7%, 7.5%, and 2.7% improvements of F1 on WebQSP, CWQ, and Grailqa,
respectively. Benefiting from the autonomous reasoning mechnism, our approach can perform reasoning on the two KGs and obtain consistent improvement on all datasets.


**Results on Out-of-domain Datasets.** After instruction tuning, we directly evaluate the zeroshot performance of our KG-Agent on the out-ofdomain datasets. As shown in Table 4, although
fine-tuned with full data, the small pre-trained language models ( _e.g.,_ T5 and BART) can not effectively answer these factual questions. Owing to
the large-scale parameters, Davinci-003 and ChatGPT performs well on NQ and TQ, which are constructed based on Wikipedia, the corpus that they
may have been pre-trained on. However, they perform not well on WQ, which is constructed based
on Freebase KG. In contrast, our KG-Agent only
needs to learn how to interact with KG instead of
memorizing the specific knowledge. Thus, it can
utilize the external KG in zero-shot setting, and
achieve consistent improvement compared to finetuned pre-trained language models.


Proportion WebQSP CWQ GrailQA Average


1:10:5 80.0 69.8 86.1 **78.6**
2:10:5 81.2 68.7 83.3 77.8
1:20:5 78.9. 73.6 78.8 77.1
1:10:10 80.8 66.9 84.3 77.3


Table 6: The F1 scores on three in-domain datasets after
instruction tuning under different sampling proportions.
We highlight the changed proportion with an underline.


**5.3** **Further Analysis**


**Transfer to Domain-specific KG.** To evaluate
the transferability of our approach on other KGs,
we test our KG-Agent on the MetaQA dataset
which is based on a movie domain KG. Following existing work (He et al., 2021; Jiang et al.,
2023b), we show the one-shot results on the test
set in Table 5. ChatGPT performs not well when
directly answering these domain-specific questions,
where the performance drops 45% absolutely on
the MQA-3hop subset compared to the supervised
fine-tuned TransferNet model. After equipping the
LLM with the KG, StructGPT can greatly outperform ChatGPT with about 37% improvement. In
contrast, our KG-Agent can obtain consistent performance improvement compared to the competitive supervised fine-tuning baselines on all subsets.
It indicates that the agent indeed learns the general ability about reasoning on KG, which can be
efficiently transferred to other KGs.


**Effect of Instruction Amount.** We explore how
the amount of instructions affects the performance
of KG-Agent and show the results in Figure 2. With
a constant sampling proportion, we scale the total
amount from 2k to 64k in an exponential way and
evaluate the F1 and Hist@1 scores on WebQSP and
CWQ datasets. As we can see, the performance
increases with more instruction tuning data, and
eventually reaches a stable state, which indicates
the importance of data amount. At the same time,
with the data amount increasing from 16k to 64k,
the KG-Agent doesn’t obtain a remarkable performance improvement. We think this is relevant to
the variety of our instruction tuning data, which
is illustrated in existing work (Chung et al., 2022;
Aribandi et al., 2022). Therefore, we will construct
more diverse samples in the future to further boost
the performance.


**Effect of Tuning Data Proportion.** Our experiment finds that only sampling 10K samples from
existing datasets is enough for backbone LLM to



Figure 2: The F1 (Left) and Hits@1 (Right) scores of
KG-Agent on the test set of WebQSP and CWQ with a
various amount of instruction tuning data.


learn the autonomous decision making capability.
Here, we conduct a further ablation study to explore
the impact of sampling proportion on the agent’s
performance when keeping the total amount of instruction tuning data constant. Specifically, we
evaluate the agent performance of WebQSP, CWQ,
and GrailQA when doubling the proportion of one
dataset while maintaining the other two dataset
proportions. We show the results in Table 6. We
can see that as the sampling proportion of a certain dataset increases, the agent performance on it
consistently improves. However, for the average
performance on all three datasets, all variants are
lower than our selected proportion, indicating that
the proportion we chose is suitable for the LLM
to balance and master more comprehensive and
general abilities.


**6** **Conclusion**


In this work, we proposed an autonomous agent
framework to synergize LLMs and KGs to perform
complex reasoning over KG, namely KG-Agent.
In our approach, we first curated a toolbox for KG,
consisting of three types of tools to support the
typical operations when reasoning on KG. Then,
we developed an autonomous iteration mechanism
based on tool selection and memory updation that
integrates the LLM, multifunctional toolbox, KGbased executor, and knowledge memory, for reasoning over KG. Next, we leveraged existing KGQA
datasets to synthesize the code-based instruction
tuning dataset. Finally, with only 10K tuning samples, we implemented the autonomous agent relying on the smaller 7B LLM, which mostly outperforms state-of-the-art baselines based on full-data
tuning or larger LLMs. In future work, we will consider extending our framework to deal with more
types of structured data, _e.g.,_ databases and tables.
















**Limitations**


Although KG-Agent demonstrates remarkable performance across various complex factual question
answering tasks, there are some limitations of our
method. First, we only use the LLaMA2-7B as the
backbone LLM, which has a strong capability after
instruction tuning. Hence, more experiments are
required to evaluate other LLMs with comparable
parameter sizes, such as Mistral-7B (Jiang et al.,
2023a) or CodeLLaMA-7b (Rozière et al., 2023).
Second, we focus on reasoning over the KG to
answer the factual questions. We should consider
extending our framework to deal with more types of
knowledge sources, _e.g.,_ databases or tables. Third,
we only evaluate factual question answering tasks
based on KG. Future work should include wider
evaluation scenarios to evaluate the universality of
our method, _e.g.,_ data-to-text and formal-languageto-text (Xie et al., 2022). Finally, we have tried our
best to tune the LLM only to answer the questions
based on the KG information, and avoid generating
discriminatory and risky responses for user questions. However, we should add more rule-based
methods to post-process the predictions and filter
the illegal responses.


**References**


Vamsi Aribandi, Yi Tay, Tal Schuster, Jinfeng Rao,
Huaixiu Steven Zheng, Sanket Vaibhav Mehta, Honglei Zhuang, Vinh Q. Tran, Dara Bahri, Jianmo Ni,
Jai Prakash Gupta, Kai Hui, Sebastian Ruder, and
Donald Metzler. 2022. Ext5: Towards extreme multitask scaling for transfer learning. In _ICLR_ . OpenReview.net.


Jonathan Berant, Andrew Chou, Roy Frostig, and Percy
[Liang. 2013. Semantic parsing on freebase from](https://aclanthology.org/D13-1160/)
[question-answer pairs. In](https://aclanthology.org/D13-1160/) _Proceedings of the 2013_
_Conference on Empirical Methods in Natural Lan-_
_guage Processing, EMNLP 2013, 18-21 October_
_2013, Grand Hyatt Seattle, Seattle, Washington, USA,_
_A meeting of SIGDAT, a Special Interest Group of the_
_ACL_, pages 1533–1544. ACL.


Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind
Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Askell, Sandhini Agarwal, Ariel Herbert-Voss,
Gretchen Krueger, Tom Henighan, Rewon Child,
Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,
Clemens Winter, Christopher Hesse, Mark Chen, Eric
Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
Jack Clark, Christopher Berner, Sam McCandlish,
Alec Radford, Ilya Sutskever, and Dario Amodei.
2020. Language models are few-shot learners. In _Ad-_
_vances in Neural Information Processing Systems 33:_



_Annual Conference on Neural Information Process-_
_ing Systems 2020, NeurIPS 2020, December 6-12,_
_2020, virtual_ .


Shulin Cao, Jiaxin Shi, Liangming Pan, Lunyiu Nie,
Yutong Xiang, Lei Hou, Juanzi Li, Bin He, and Hanwang Zhang. 2022. KQA pro: A dataset with explicit
compositional programs for complex question answering over knowledge base. In _Proceedings of the_
_60th Annual Meeting of the Association for Compu-_
_tational Linguistics (Volume 1: Long Papers), ACL_
_2022, Dublin, Ireland, May 22-27, 2022_, pages 6101–
6119. Association for Computational Linguistics.


Danqi Chen, Adam Fisch, Jason Weston, and Antoine
Bordes. 2017. Reading wikipedia to answer opendomain questions. In _Proceedings of the 55th Annual_
_Meeting of the Association for Computational Lin-_
_guistics, ACL 2017, Vancouver, Canada, July 30 -_
_August 4, Volume 1: Long Papers_, pages 1870–1879.
Association for Computational Linguistics.


Hyung Won Chung, Le Hou, Shayne Longpre, Barret
Zoph, Yi Tay, William Fedus, Eric Li, Xuezhi Wang,
Mostafa Dehghani, Siddhartha Brahma, Albert Webson, Shixiang Shane Gu, Zhuyun Dai, Mirac Suzgun, Xinyun Chen, Aakanksha Chowdhery, Sharan
Narang, Gaurav Mishra, Adams Yu, Vincent Y. Zhao,
Yanping Huang, Andrew M. Dai, Hongkun Yu, Slav
Petrov, Ed H. Chi, Jeff Dean, Jacob Devlin, Adam
Roberts, Denny Zhou, Quoc V. Le, and Jason Wei.
2022. Scaling instruction-finetuned language models.
_CoRR_, abs/2210.11416.

