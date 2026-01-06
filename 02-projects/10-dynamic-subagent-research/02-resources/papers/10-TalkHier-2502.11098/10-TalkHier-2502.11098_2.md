<!-- Source: 10-TalkHier-2502.11098.pdf | Chunk 2/5 -->


i


from Member nodes to Supervisor nodes. These information are then established as a communication
event _c_ [(] _ij_ _[t]_ [)] _[∈C][p]_ [.]


**3.3** **Collaborative Hierarchy Agent Team**


The entire graph _G_ consists of multiple teams, each
represented as a subset _V_ team _⊆V_ . Each team includes a dedicated supervisor agent _v_ team _[S]_ [and one]
or more member agents _v_ team _[M]_ [. A key feature of the]
hierarchical structure in _TalkHier_ is that a member agent in one team can also act as a supervisor
for another team, creating a nested hierarchy of
agent teams. As shown in the second row of Figure 3, this structure enables the entire graph _G_ to
represent a hierarchical node system, where teams
are recursively linked through supervisor-member
relationships.
Formally, the hierarchical structure of agents
with two teams is defined as:


_V_ main = _{v_ main _[S]_ _[, v]_ main [Gen] _[, v]_ eval _[S]_ _[, v]_ main [Rev] _[}][,]_

_V_ eval = _{v_ eval _[S]_ _[, v]_ eval _[E]_ [1] _[, v]_ eval _[E]_ [2] _[, . . ., v]_ eval _[E][k]_ _[}][,]_

where the Main Supervisor ( _v_ main _[S]_ [) and Evaluation]
Supervisor ( _v_ eval _[S]_ [) oversee their respective team’s]



i


**Algorithm.** Algorithm 1 illustrates the operation
of our hierarchical refinement process within the
collaborative agent framework. The process begins with the main Supervisor ( _v_ main _[S]_ [) assigning]
tasks to the evaluation Supervisor ( _v_ eval _[S]_ [), who then]
distributes evaluation criteria to individual evaluators ( _v_ eval _[E][i]_ [). Each evaluator assesses the gener-]
ated output ( **A** _t−_ 1) based on their assigned criteria,
producing detailed feedback. The evaluation Supervisor aggregates and summarizes this feedback
( **F** [eval] summary [) before passing it to the main Supervi-]
sor. The main Supervisor evaluates whether the
summarized feedback meets the quality threshold
( _M_ threshold). If the threshold is satisfied, the output
is finalized; otherwise, the Revisor ( _v_ main [Rev] [) refines]
the output for further iterations. This iterative refinement ensures accurate and unbiased collaboration across the agent hierarchy.


The main Supervisor evaluates whether the
summarized feedback meets the quality threshold
( _M_ threshold), defined vaguely as “ensuring correctness” or “achieving high relevance.” If satisfied, the
output is finalized; otherwise, the Revisor ( _v_ main [Rev] [)]
refines it. Details of our settings are in Appendix B,
Appendix C, and Appendix D.



i


5


**4** **Experiments**


In this section, we aim to answer the following
research questions across various domains:
**RQ1:** Does _TalkHier_ outperform existing multiagent, single-agent, and proprietary approaches on
general benchmarks?
**RQ2:** How does _TalkHier_ perform on open-domain
question-answering tasks?
**RQ3:** What is the contribution of each component
of _TalkHier_ to its overall performance?
**RQ4:** How well does _TalkHier_ generalize to more
practical but complex generation task?


**4.1** **Experimental Setup**


**Datasets.** We evaluated _TalkHier_ on a diverse collection of datasets to assess its performance across
various tasks. The Massive Multitask Language
Understanding (MMLU) Benchmark (Hendrycks
et al., 2021) tests domain-specific reasoning problems including Moral Scenario, College Physics,
Machine Learning, Formal Logic and US Foreign
Policy. WikiQA (Yang et al., 2017) evaluates opendomain question-answering using real-world questions from Wikipedia. The Camera Dataset (Mita
et al., 2024) focuses on advertisement headline generation, assessing the ability to create high-quality
advertising text.


**Baselines.** To evaluate _TalkHier_, we compared it
against a comprehensive set of baselines including:

  - **GPT-4o** (OpenAI, 2024a), based on OpenAI’s
GPT-4 model with both single-run and ensemble majority voting (3, 5, or 7 runs).

  - **OpenAI-o1-preview** (OpenAI, 2024b), a beta
model using advanced inference techniques,
though limited by API support.

  - **ReAct** (Yao et al., 2022), a reasoning and action framework in single-run and ensemble
configurations.

  - **AutoGPT** (Gravitas, 2023), an autonomous
agent designed for task execution and iterative
improvement.

  - **AgentVerse** (OpenBMB, 2023), a multi-agent
system framework for collaborative problemsolving.

  - **GPTSwarm** (Zhuge et al., 2024), a swarmbased agent collaboration model utilizing optimizable communication graphs.

  - **AgentPrune** (Zhang et al., 2024a), a model
leveraging pruning techniques for efficient
multi-agent communication and reasoning.



Table 1: General Performance on MMLU Dataset. The
table reports accuracy (%) for various baselines across
Moral Scenario (Moral), College Physics (Phys.), Machine Learning (ML), Formal Logic (FL) and US Foreign Policy (UFP) domains. The notations **3@**, **5@**, and
**7@** represent majority voting results using 3, 5, and 7
independent runs, respectively.


**Models** **Moral** **Phys.** **ML** **FL** **UFP** **Avg.**


GPT4o 64.25 62.75 67.86 63.49 92.00 70.07

GPT4o-3@ 65.70 62.75 66.07 66.67 91.00 70.44

GPT4o-5@ 66.15 61.76 66.96 66.67 92.00 70.71

GPT4o-7@ 65.81 63.73 66.96 68.25 91.00 71.15

ReAct 69.61 72.55 59.82 32.54 58.00 58.50

ReAct-3@ 74.75 83.33 66.07 52.38 53.00 65.91

ReAct-5@ 74.97 82.35 66.96 46.83 63.00 66.82

ReAct-7@ 75.53 84.78 67.86 50.79 57.00 67.19


AutoGPT 66.37 78.43 64.29 60.83 90.00 71.98

AgentVerse 79.11 **93.14** 79.46 78.57 88.00 83.66

GPTSwarm 60.48 67.70 72.32 68.33 57.00 65.17

AgentPrune 70.84 91.18 81.25 81.75 93.00 83.60


o1-preview 82.57 91.17 **85.71** 83.33 **95.00** 87.56


_TalkHier (Ours)_ **83.80** **93.14** 84.68 **87.30** 93.00 **88.38**


  - **OKG** (Wang et al., 2025), A method tailored
specifically for ad text generation tasks and
easily generalizable to ad headlines with minimal prompt redefinition.


**Implementation details.** For fair comparisons,
we use GPT-4o as the backbone across all experiments for the baselines and _TalkHier_, with the
temperature set to 0 in all settings. For the OpenAIo1 baseline, we followed the implementation guide
and the limitations outlined in OpenAI’s documentation [†], and keep the temperature fixed at 1.


**4.2** **Performance on MMLU (RQ1)**


Table 1 reports the average accuracy of various
models on the five domains of MMLU dataset.
_TalkHier_, built on GPT-4o, achieves the highest average accuracy (88.38%), outperforming
open-source multi-agent models (e.g., AgentVerse,
83.66%) and majority voting strategies applied
to current LLM and single-agent baselines (e.g.,
ReAct-7@, 67.19%; GPT-4o-7@, 71.15%). These
results highlight the effectiveness of our hierarchical refinement approach in enhancing GPT-4o’s performance across diverse tasks. Although OpenAIo1 cannot be directly compared to _TalkHier_ and
other baselines—since they are all built on GPT-4o
and OpenAI-o1’s internal design and training data
remain undisclosed— _TalkHier_ achieves a slightly
higher average score (88.38% vs. 87.56%), demon

[†https://platform.openai.com/docs/guides/](https://platform.openai.com/docs/guides/reasoning/beta-limitations)
[reasoning/beta-limitations](https://platform.openai.com/docs/guides/reasoning/beta-limitations)



6


Table 2: Evaluation Results on WikiQA. The table reports Rouge-1 and BERTScore for various models.


GPT4o 0.2777 0.5856

AutoGPT 0.3286 0.5885

AgentVerse 0.2799 0.5716

AgentPrune 0.3027 0.5788

o1-preview 0.2631 0.5701


strating competitive performance.


**4.3** **Evaluation on WikiQA Benchmark (RQ2)**


We evaluated _TalkHier_ and baselines on the WikiQA dataset, an open-domain question-answering
benchmark. Unlike MMLU, WikiQA requires generating textual answers to real-world questions.
The quality of generated answers was assessed
using two metrics: Rouge-1 (Lin, 2004), which
measures unigram overlap between generated and
reference answers, and BERTScore (Zhang et al.,
2020), which evaluates the semantic similarity between the two.
Table 2 shows that _TalkHier_ outperforms baselines in both Rouge-1 and BERTScore, demonstrating its ability to generate accurate and semantically
relevant answers. While other methods, such as
AutoGPT and AgentVerse, perform competitively,
their scores fall short of _TalkHier_, highlighting its
effectiveness in addressing open-domain questionanswering tasks.


**4.4** **Ablation Study (RQ3)**


To better understand the contribution of individual
components in _TalkHier_, we conducted ablation
studies by removing specific modules and evaluating the resulting performance across the Moral
Scenario, College Physics, and Machine Learning
domains. The results of these experiments are summarized in Table 3.
Table 3 presents the contributions of our ablation
study on the main components in _TalkHier_ . Removing the evaluation Supervisor ( _TalkHier_ w/o Eval.
Sup.) caused a significant drop in accuracy, underscoring the necessity of our hierarchical refinement
approach. Replacing the structured communication
protocol with the text-based protocol ( _TalkHier_ w.
Norm. Comm) resulted in moderate accuracy reductions, while eliminating the entire evaluation



Table 3: Ablative Results on Main Components of
_TalkHier_ : Accuracy (%) across Physics, ML, and Moral
domains. _TalkHier_ w/o Eval. Sup. removes the evaluation supervisor. _TalkHier_ w/o Eval. Team excludes the
evaluation team component. _TalkHier_ w. Norm. Comm
uses a normalized communication protocol.


w/o Eval. Sup. 83.57 87.25 74.77 81.86

w/o Eval. Team 73.54 80.34 74.56 76.15

w. Norm. Comm 82.91 88.24 82.14 84.43

_TalkHier (Ours)_ **83.80** **93.14** **84.68** **87.21**


Table 4: Ablative Results: Accuracy (%) across Physics,
ML, and Moral domains. The study examines the
impact of removing components from the structured
communication protocol: message ( **M** _ij_ ), background
( **B** _ij_ ), and intermediate output ( **I** _ij_ ).


w/o **I** _ij_ 81.56 90.20 75.89 82.55
w/o **B** _ij_ 76.87 87.50 70.54 78.30
w/o **B** _ij,_ **I** _ij_ 77.99 90.20 78.57 82.25


team ( _TalkHier_ w/o Eval.Team) led to substantial
performance declines across all domains. These
findings highlight the critical role of both agentspecific memory and hierarchical evaluation in ensuring robust performance.

Table 4 delves into the impact of individual elements in the communication protocol. Removing
intermediate outputs ( _TalkHier_ w/o **I** _ij_ ) or background information ( _TalkHier_ w/o **B** _ij_ ) lead to inferior performance, with their combined removal
( _TalkHier_ w/o **B** _ij,_ **I** _ij_ ) yielding similar declines.
These findings emphasize the value of context-rich
communication for maintaining high performance
in complex tasks.


**4.5** **Evaluation on Ad Text Generation (RQ4)**


We evaluate _TalkHier_ on the Camera dataset (Mita
et al., 2024) using traditional text generation
metrics (BLEU-4, ROUGE-1, BERTScore) and
domain-specific metrics (Faithfulness, Fluency, Attractiveness, and Character Count Violation) (Mita
et al., 2024). These metrics assess both linguistic
quality and domain-specific relevance.

Setting up baselines like AutoGPT, AgentVerse,
and GPTSwarm for this task was challenging, as
their implementations focus on general benchmarks
like MMLU and require significant customization



7


Table 5: Evaluation Results on Camera Dataset. We report BLEU-4 (B4), ROUGE-1 (R1), BERTScore (BERT),
and domain-specific metrics (Faithfulness, Fluency, Attractiveness, Character Count Violation(CCV)) following
(Mita et al., 2024).


**Models** **B4** (↑) **R1** (↑) **BERT** (↑) **Faithfulness** (↑) **Fluency** (↑) **Attractiveness** (↑) **CCV** (↓)

GPT-4o 0.01 0.02 0.65 4.8 5.9 6.5 16%

ReAct 0.01 0.01 0.70 4.9 6.4 **7.0** 17%

OKG 0.03 0.16 0.73 6.3 8.7 6.1 **4%**

_TalkHier (Ours)_ **0.04** **0.20** **0.91** **8.6** **8.9** 6.2 **4%**



for ad text generation. In contrast, OKG (Wang
et al., 2025), originally for ad keyword generation,
was easier to adapt, making it a more practical
baseline.
Table 5 presents the results. _TalkHier_ outperforms ReAct, GPT-4o, and OKG across most metrics, particularly excelling in Faithfulness, Fluency, and Attractiveness while maintaining a low
Character Count Violation rate. The mean performance gain over the best-performing baseline,
OKG, across all metrics is approximately 17.63%.
To verify whether _TalkHier_ ’s multi-agent evaluations of attractiveness, fluency, and faithfulness are
accurate, we conducted a subjective experiment on
a sub-dataset of Camera, comparing the system’s
automatic ratings to human judgments; details of
this procedure are provided in Appendix E.


**5** **Discussion**


The experimental results across the MMLU, WikiQA, and Camera datasets consistently demonstrate
the superiority of _TalkHier_ . Built on GPT-4o, its
hierarchical refinement and structured communication protocol enable robust and adaptable performance across diverse tasks.


**General and Practical Benchmarks.** _TalkHier_
outperformed baselines across general and practical benchmarks. On MMLU, it achieved the highest accuracy (88.38%), surpassing the best opensource multi-agent baseline, AgentVerse (83.66%),
by 5.64%. On WikiQA, it obtained a ROUGE-1
score of 0.3461 (+5.32%) and a BERTScore of
0.6079 (+3.30%), outperforming the best baseline,
AutoGPT (0.3286 ROUGE-1, 0.5885 BERTScore).
On the Camera dataset, _TalkHier_ exceeded OKG
across almost all metrics, demonstrating superior
Faithfulness, Fluency, and Attractiveness while
maintaining minimal Character Count Violations.
These results validate its adaptability and taskspecific strengths, highlighting its advantage over
inference scaling models (e.g., OpenAI-o1), open


source multi-agent models (e.g., AgentVerse), and
majority voting strategies (e.g., ReAct, GPT-4o).


**Comparative and Ablation Insights.** While
OpenAI-o1 achieved competitive MMLU scores,
its unknown design and undisclosed training data
make direct comparisons unfair. Since _TalkHier_ is
built on the GPT-4o backbone, comparisons with
other GPT-4o-based baselines are fair. Despite
this, _TalkHier_ was competitive with OpenAI-o1 on
MMLU and achieved a significant advantage on
WikiQA. Ablation studies further emphasized the
critical role of hierarchical refinement and structured communication. Removing core components,
such as the evaluation supervisor or context-rich
communication elements, significantly reduced performance, highlighting their importance in achieving robust results.


**6** **Conclusions**


In this paper, we propose _TalkHier_, a novel framework for LLM-MA systems that addresses key challenges in communication and refinement. To the
best of our knowledge, _TalkHier_ is the first framework to integrate a structured communication protocol in LLM-MA systems, embedding _Messages_,
_intermediate outputs_, and _background_ information
to ensure organized and context-rich exchanges. At
the same time, distinct from existing works that
have biases on inputs, its hierarchical refinement
approach balances and summarizes diverse opinions or feedback from agents. _TalkHier_ sets a new
standard for managing complex multi-agent interactions across multiple benchmarks, surpassing the
best-performing baseline by an average of 5.64%
on MMLU, 4.31% on WikiQA, and 17.63% on
Camera benchmarks. Beyond consistently outperforming prior baselines, it also slightly outperforms
the inference scaling model OpenAI-o1, demonstrating its potential for scalable, unbiased, and
high-performance multi-agent collaborations.



8


**Limitations**


One of the main limitations of _TalkHier_ is the relatively high API cost associated with the experiments (see Appendix A for details). This is a tradeoff due to the design of _TalkHier_, where multiple
agents collaborate hierarchically using a specifically designed communication protocol. While this
structured interaction enhances reasoning and coordination, it also increases computational expenses.
This raises broader concerns about the accessibility and democratization of LLM research, as such
costs may pose barriers for researchers with limited
resources. Future work could explore more costefficient generation strategies while preserving the
benefits of multi-agent collaboration.


**References**


Anthony Brohan et al. 2022. Code as policies:
Language model-driven robotics. _arXiv preprint_
_arXiv:2209.07753_ .


Mark Chen et al. 2021. Evaluating large language models trained on code. _arXiv preprint_
_arXiv:2107.03374_ .


Pei Chen, Boran Han, and Shuai Zhang. 2024.
Comm: Collaborative multi-agent, multi-reasoningpath prompting for complex problem solving. _arXiv_
_preprint arXiv:2404.17729_ .


Yuheng Cheng, Ceyao Zhang, Zhengwen Zhang, Xiangrui Meng, Sirui Hong, Wenhao Li, Zihao Wang,
Zekai Wang, Feng Yin, Junhua Zhao, and Xiuqiang
[He. 2024. Exploring large language model based in-](https://arxiv.org/abs/2401.03428)
[telligent agents: Definitions, methods, and prospects.](https://arxiv.org/abs/2401.03428)
_CoRR_, abs/2401.03428.


Eva Eigner and Thorsten Händler. 2024. Determinants
of llm-assisted decision-making. _arXiv preprint_
_arXiv:2402.17385_ .


Federico Errica, Giuseppe Siracusano, Davide Sanvito, and Roberto Bifulco. 2024. What did i
do wrong? quantifying llms’ sensitivity and consistency to prompt engineering. _arXiv preprint_
_arXiv:2406.12334_ .


Jiangnan Fang, Cheng-Tse Liu, Jieun Kim, Yash
Bhedaru, Ethan Liu, Nikhil Singh, Nedim Lipka,
Puneet Mathur, Nesreen K Ahmed, Franck Dernoncourt, et al. 2024. Multi-llm text summarization.
_arXiv preprint arXiv:2412.15487_ .


Chen Gao, Xiaochong Lan, Nian Li, Yuan Yuan, Jingtao
Ding, Zhilun Zhou, Fengli Xu, and Yong Li. 2023.
[Large language models empowered agent-based mod-](https://arxiv.org/abs/2312.11970)
[eling and simulation: A survey and perspectives.](https://arxiv.org/abs/2312.11970)
_CoRR_, abs/2312.11970.



[Significant Gravitas. 2023. Autogpt: An experimental](https://github.com/Torantulino/Auto-GPT)
[open-source application.](https://github.com/Torantulino/Auto-GPT)


Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang,
Shichao Pei, Nitesh V Chawla, Olaf Wiest, and Xiangliang Zhang. 2024. Large language model based
multi-agents: A survey of progress and challenges.
_arXiv preprint arXiv:2402.01680_ .


Shiyang Han, Qian Zhang, Yue Yao, Wenhao Jin, Zhen
Xu, and Cheng He. 2024. Llm multi-agent systems: Challenges and open problems. _arXiv preprint_
_arXiv:2402.03578_ .


Chengbo He, Bochao Zou, Xin Li, Jiansheng Chen,
Junliang Xing, and Huimin Ma. 2024. Enhancing llm
reasoning with multi-path collaborative reactive and
reflection agents. _arXiv preprint arXiv:2501.00430_ .


Dan Hendrycks, Colin Burns, Samuel Basart, Chia Zou,
[David Song, and Thomas G. Dietterich. 2021. Mea-](https://arxiv.org/abs/2110.08307)
[suring massive multitask language understanding.](https://arxiv.org/abs/2110.08307)
_arXiv preprint arXiv:2110.08307_ .


Sirui Hong, Xiawu Zheng, Jonathan Chen, Yuheng
Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven
Ka Shing Yau, Zijuan Lin, Liyang Zhou, et al. 2023.
Metagpt: Meta programming for multi-agent collaborative framework. _arXiv preprint arXiv:2308.00352_ .


Xiaoyu Li, Shuang Wang, Shaohui Zeng, Yucheng Wu,
and Yue Yang. 2024. A survey on llm-based multiagent systems: Workflow, infrastructure, and challenges. _Vicinagearth_, 1(9).

