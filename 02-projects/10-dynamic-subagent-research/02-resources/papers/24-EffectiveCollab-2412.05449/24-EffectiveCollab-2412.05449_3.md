<!-- Source: 24-EffectiveCollab-2412.05449.pdf | Chunk 3/4 -->

for full results on coordination mode.


We also performed ablation experiments with the payload referencing capability of the supervisor
agent, which is discussed in more detail in Section 6.1.


**5.2** **Routing Mode Experiments**


To benchmark dynamic agent routing, we curated two additional datasets for evaluation from our
original benchmarking data: 1) Mortgage Routing (3 agent layers) and 2) Travel Routing (2 agent
layers), and manually annotated around 100 routing classification labels for each datasets. Intrinsic
evaluation shows that the LLM-based routing solution with Claude 3.0 Haiku achieves more than
90% routing classification accuracy and less than 3% false agent switching rate (Table 7). Average
latency of routing classification is about 350 ms. With end-to-end evaluation, we observe turn-level
routing overhead (time taken by the supervisor agents) in 600 ms to 800ms range (Table 8).


**5.3** **Agreement with Human Evaluation**


Throughout this report, we have used an LLM to provide automatic judgements on assertions. This
has helped scale our experiments so that we can quickly prototype and develop improved multi-agent
systems. What if we ask a human to judge conversation success purely from their own perspective
without any reference to assertions? To understand how well assertion-based evaluation compares
with human evaluation, we deliver a batch of ninety trajectories to human annotators during one of our
milestone checkpoints. For each conversation, we ask three annotators to provide binary judgements
on a different set of guidelines. During this human evaluation, they are never shown assertions or
LLM judgements and only instructed to determine success and efficiency from their own judgements.
Table 9 show the instructions given to human annotators for each success metric.


After the human annotators finish their evaluation, the aggregated majority judgement is used to
compare against LLM evaluations. Note that for this milestone, we use Claude 3.5 Sonnet (20240620)
for supervisor agent and Sonnet 3.0 for specialist agents. See Appendix D for the automatic and
human evaluation results for this set of experiments. We then compute agreement between human and
LLM judges. Since the judgements for automatic and human evaluation are binary, we use agreement
ratio to measure alignment between human and automatic evaluation. The agreement ratio is the
number of conversations with matching judgements (either both 1 or both 0) over the total number of
conversations evaluated.


12


Table 9: The instructions given to annotators when performing human evaluation of conversation
trajectories. Note that humans do not judge assertions and only determine success purely from their
own judgements.


Metric Human annotator instructions


User GSR Evaluate from user’s perspective, whether the conversation with the primary
agent meets the user’s goals and successfully address user’s requests or not.
System GSR From the perspective of the environment, evaluate whether the actual impacts
of all agent actions accurately address and resolve all of the user’s stated tasks,
requests, and expectations within that specific environment or context.
Supervisor Evaluate from user’s perspective whether the primary agent has tried its best to
GSR help the User, regardless of whether task was completed or the agent actions
correctly impacted the environment.


Table 10: The agreement ratios between human annotators and assertion-based benchmarking on
success metrics across 90 conversation trajectories.


Dataset Overall GSR Supervisor GSR User-side GSR System-side GSR


Travel 0.93 0.87 0.93 0.93
Mortgage 0.87 1.00 0.97 0.87
Software 0.97 0.77 1.00 0.90


For success metrics, the agreement is generally above 85% (Table 10). The only exception is on
primary agent success for software, where the agreement is 77%. Here, the automatic evaluation
has overall GSR as 90% but the human annotators only believe the supervisor agent is successful in
87% of the conversations. On the trajectories where the humans disagree with LLM judgements, we
observe a mix of mistakes from both ends. For some trajectories, the human evaluation would mark
that supervisor agent has not make a mistake but LLM judge has captured when the supervisor agent
repeatedly wanting to follow-up with the user rather than delegating tasks to sub-agents. There is
also the reversed case where the LLM judge does not observe any issues with the supervisor agent
but the human annotators detect that the supervisor agent neglects to conduct thorough code review
with the Review agent.


**6** **Communication Mechanism Ablations**


Section 5 shows the main results of our approach with different models. In this section, we provide
additional ablations to quantify the impact of MAC communication mechanisms. This includes
experiments with and without payload referencing, as well as comparison with open-source frameworks. The additional experiments provide more justification on the utility of MAC for enterprise
applications.


**6.1** **Impact of Payload Referencing**


In Table 11, we report the results of an ablation experiment with Payload Referencing for Software
domain with Claude 3.5 Sonnet (20241022) as the supervisor agent as well as specialist agents. This
experiment reveals that payload referencing significantly improves both the efficiency as well as
effectiveness of multi-agent collaboration, particularly in the code-heavy Software domain. The
impact is most pronounced here as large code blocks are frequently exchanged between agents.


Enabling payload referencing results in a 23% relative improvement in overall GSR as well as a 27%
relative reduction in the average communication overhead per turn. The latter can be attributed to a
30% relative reduction in the average output tokens per communication of the supervisor agent, as
it is able to leverage the payload referencing mechanism to more efficiently reduce the number of
generated tokens required for sharing code blocks, while improving the goal success rate.


When enabling payload referencing, we also observe an increase in the average user-perceived turn
latency. As this also includes the latency of the specialist agents, it suggests that the specialist agents
operating for a smaller number of turns may be detrimental to the overall goal success.


13


Table 11: Impact of payload referencing on GSR and latency for Software



Avg.
user-perceived
turn latency
per session (s)



Avg.
output
tokens per
communication



Overall
GSR



Avg.
communication
overhead per
turn (s)



With Payload Ref. 0.90 35.44 168.73 373.77
Without Payload Ref. 0.73 48.78 159.75 539.21


Table 12: Comparison with a widely adopted open-source framework for task automation (OSF).
Note that the version of Sonnet 3.5 used below refers to an older version.


Setting Dataset Overall GSR Supervisor GSR




[MAC Coordination Mode]
Supervisor: Sonnet 3.5 (20240620)
Specialists: Sonnet 3.0


[OSF]
Supervisor: Sonnet 3.5 (20240620)
Specialists: Sonnet 3.0


[OSF]
Supervisor: GPT-4o (mini)
Specialists: GPT-4o (mini)



Travel 0.87 0.90
Mortgage 0.90 0.97
Software 0.77 0.90


Travel 0.50 0.80
Mortgage 0.63 0.87
Software 0.40 0.63


Travel 0.43 0.63
Mortgage 0.40 0.67
Software 0.33 0.77



In conclusion, payload referencing proves particularly valuable in domains such as Software, as it:


    - Enables precise referencing of payloads without expensive regeneration of tokens


    - Reduces the likelihood of payload corruption during agent-to-agent transmission


    - Maintains formatting and structure of the payload across agent communications


    - Facilitates more efficient parallel inter-agent communication


Our experiments suggest that payload referencing is a crucial optimization for multi-agent systems,
particularly in domains involving structured content exchange. The mechanism not only improves
system performance metrics but also enhances the quality and reliability of agent interactions.


**6.2** **Comparison with Task Automation Framework**


We also conducted a comparative evaluation of our implementation against a widely adopted opensource framework (OSF) for task automation. The OSF implements multi-agent collaboration as
a sequential task-automation workflow, wherein the supervisor agent receives a task from the user
and is responsible for breaking it up into one-time sub-tasks for its sub-agents. However, as our
evaluation is primarily based on more conversational back-and-forth between the specialist agents,
the one-time task assignment may not be sufficient. Therefore, we also expanded the OSF to support
multiple sub-agent interactions. The OSF also enables tool-use for its agents using ReAct-style
prompting [23], as opposed to native function-calling capability of our implementation.


In Table 12, we present a comparative analysis with the OSF. Due to the prompting style of the agents
in the OSF, they tend to be highly verbose and utilize a much higher number of tokens. To constrain
the experiment to a reasonable budget, we employ Claude 3.5 Sonnet (20240620) as the supervisor
agent and Claude 3.0 Sonnet as the specialist agents. Since the original prompts in the OSF may have
been optimized for GPT-4o (mini), as suggested by the defaults in the code implementation, we also
report the performance of GPT-4o (mini) with the OSF in the conversational setting.


**7** **Discussion**


The results presented in this technical report demonstrate the effectiveness of MAC in enabling
coordinated problem-solving through multiple specialized agents. Across the evaluated domains


14


of Travel, Mortgage, and Software Development, the multi-agent collaboration approach achieved
impressive goal success rates, with the overall GSR reaching as high as 90% when utilizing the
Claude 3.5 Sonnet (20241022) models for both the supervisor agent and specialist agents. This strong
performance is particularly notable when compared to the single-agent setting, where a significant
regression of up to 37% was observed in the Software Development domain. The ability of the
multi-agent collaboration to leverage the specialized expertise of individual agents appears to be a
key factor in this improved effectiveness.


Further analysis of the results highlights the importance of optimizing the inter-agent communication
mechanisms. The impact of the payload referencing feature is most pronounced in the Software
Development domain, where it led to a 23% relative improvement in overall GSR as well as a 27%
relative reduction in the average communication overhead per turn. By allowing the supervisor agent
to more efficiently reference and share large content blocks, such as code snippets, this specialized
mechanism enhances the reliability and speed of the multi-agent interactions. However, the results
also reveal some limitations of the current system. The higher latency observed in the more complex
Software Development scenarios suggests that further optimizations may be needed to reduce the
overhead of multi-agent coordination, particularly in time-sensitive applications.


**8** **Conclusion**


This paper presents a comprehensive evaluation of the multi-agent collaboration framework, demonstrating its effectiveness in enabling coordinated problem-solving across a variety of enterprise
domains. The results highlight the system’s ability to leverage specialized agents to tackle complex
tasks, achieving impressive goal success rates of up to 90% in the evaluated scenarios. A key aspect
of MAC is the focus on optimizing the inter-agent communication mechanisms. The introduction of
the payload referencing feature, for example, was shown to provide significant benefits, particularly
in code-heavy tasks, by allowing the supervisor agent to more efficiently share and reference large
content blocks. This optimization has led to remarkable improvements in both the overall goal success
rate and the communication efficiency of the system.


Furthermore, the evaluation framework that is employed in this study, which combines assertionbased benchmarking with automated LLM-based judgements, has proven to be a reliable and scalable
approach for assessing the performance of multi-agent collaborative systems. During development,
we observe high agreement rates on goal success between human and automated evaluation. This
validates our evaluation framework, which can enable faster prototyping and development of MAC.


One key focus for future work will be on further reducing the latency observed in more complex
scenarios, such as those in the Software Development domain. Exploring additional optimizations to
the inter-agent coordination mechanisms may help to address this challenge and ensure the system
can operate efficiently, even in time-sensitive applications. Additionally, expanding the detection and
handling of different forms of static long-form payloads could lead to additional performance gains.
Investigating automatic prompt optimization techniques may also prove valuable in enhancing the
collaboration capabilities of the individual agents.


Finally, automating the dataset curation process for the benchmarking framework could enable more
scalable and iterative development of the multi-agent system, allowing for faster prototyping and
deployment of improvements. By building on the solid foundations laid out in this technical report,
the future work in these areas promises to further strengthen MAC and its ability to tackle increasingly
complex, real-world challenges.


**Acknowledgments**


First, we want to thank the AWS Bedrock Agents Science team for their help in the project, notably
Tamer Alkhouli, Renato Negrinho, Veera Raghavendra Elluru, and Yassine Benajiba. We thank
Claudia Zaghi and Nina Rondoni for their substantial support in data collection. We thank the
AWS Bedrock Product team and solution architects for their crucial feedback on enterprise needs
and usecases. Finally, we want to acknowledge the AWS Bedrock Engineering team for diligently
deploying the multi-agents collaboration service and delivering our work on enterprise applications
to AWS customers.


15


**References**


[1] Anthropic. Claude 3.5 Sonnet, 2024. `[https://www.anthropic.com/news/](https://www.anthropic.com/news/claude-3-5-sonnet)`
`[claude-3-5-sonnet](https://www.anthropic.com/news/claude-3-5-sonnet)`, Accessed on 2024-12-06.


[2] Negar Arabzadeh, Siqing Huo, Nikhil Mehta, Qingyun Wu, Chi Wang, Ahmed Hassan Awadallah, Charles L. A. Clarke, and Julia Kiseleva. Assessing and verifying task utility in LLMpowered applications. In _Empirical Methods of Natural Language Processing_, 2024.


[3] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal,
Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel
Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler,
Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott
Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya
Sutskever, and Dario Amodei. Language models are few-shot learners. In _Advances in Neural_
_Information Processing Systems_, 2020.


[4] Weize Chen, Yusheng Su, Jingwei Zuo, Cheng Yang, Chenfei Yuan, Chen Qian, Chi-Min Chan,
Yujia Qin, Yaxi Lu, Ruobing Xie, et al. Agentverse: Facilitating multi-agent collaboration and
exploring emergent behaviors in agents. _arXiv preprint arXiv:2308.10848_, 2023.


[5] CrewAI. CrewAI, 2024. `[https://www.crewai.com/](https://www.crewai.com/)`, Accessed on 2024-12-06.


[6] Luca Gioacchini, Giuseppe Siracusano, Davide Sanvito, Kiril Gashteovski, David Friede,
Roberto Bifulco, and Carolin Lawrence. AgentQuest: A modular benchmark framework to
measure progress and improve LLM agents. In _Annual Conference of the North American_
_Chapter of the Association for Computational Linguistics_, 2024.


[7] Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang, Shichao Pei, Nitesh V Chawla, Olaf
Wiest, and Xiangliang Zhang. Large language model based multi-agents: A survey of progress
and challenges. _arXiv preprint arXiv:2402.01680_, 2024.


[8] Shanshan Han, Qifan Zhang, Yuhang Yao, Weizhao Jin, Zhaozhuo Xu, and Chaoyang He. Llm
multi-agent systems: Challenges and open problems. _arXiv preprint arXiv:2402.03578_, 2024.


[9] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao
Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng
Xiao, Chenglin Wu, and Jürgen Schmidhuber. MetaGPT: Meta programming for a multi-agent
collaborative framework. In _International Conference on Learning Representations_, 2024.


[10] Sayash Kapoor, Benedikt Stroebl, Zachary S Siegel, Nitya Nadgir, and Arvind Narayanan. AI
Agents That Matter. _arXiv preprint arXiv:2407.01502_, 2024.


[11] LangChain. LangGraph, 2024. `[https://www.langchain.com/langgraph](https://www.langchain.com/langgraph)`, Accessed on
2024-12-06.


[12] Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard
Ghanem. Camel: Communicative agents for "mind" exploration of large language model society.
In _Neural Information Processing Systems_, 2023.


[13] Huao Li, Yu Chong, Simon Stepputtis, Joseph Campbell, Dana Hughes, Charles Lewis, and
Katia Sycara. Theory of mind for multi-agent collaboration via large language models. In
_Empirical Methods in Natural Language Processing_, 2023.


[14] Jiarui Lu, Thomas Holleis, Yizhe Zhang, Bernhard Aumayer, Feng Nan, Felix Bai, Shuang Ma,
Shen Ma, Mengyu Li, Guoli Yin, et al. Toolsandbox: A stateful, conversational, interactive
evaluation benchmark for llm tool use capabilities. _arXiv preprint arXiv:2408.04682_, 2024.


[15] OpenAI. Hello GPT-4o, 2024. `[https://openai.com/index/hello-gpt-4o/](https://openai.com/index/hello-gpt-4o/)`, Accessed
on 2024-12-06.


[16] Joon Sung Park, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and
Michael S. Bernstein. Generative agents: Interactive simulacra of human behavior. In _ACM_
_Symposium on User Interface Software and Technology_, 2023.


16


[17] Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize
Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, and Maosong Sun. ChatDev:
Communicative agents for software development. In _Annual Meeting of the Association for_
_Computational Linguistics_, 2024.


[18] Munindar P Singh. _Multiagent systems_ . Springer, 1994.


[19] Andries Petrus Smit, Nathan Grinsztajn, Paul Duckworth, Thomas D Barrett, and Arnu Pretorius.
Should we be going mad? a look at multi-agent debate strategies for llms. In _International_
_Conference on Machine Learning_, 2024.


[20] Katia P Sycara. Multiagent systems. _AI magazine_, 19(2):79–79, 1998.


[21] Yashar Talebirad and Amirhossein Nadiri. Multi-agent collaboration: Harnessing the power of
intelligent llm agents. _arXiv preprint arXiv:2306.03314_, 2023.


[22] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun
Zhang, Shaokun Zhang, Jiale Liu, Ahmed Hassan Awadallah, Ryen W White, Doug Burger,
and Chi Wang. AutoGen: Enabling next-gen llm applications via multi-agent conversation
framework. In _COLM_, 2024.


[23] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan
Cao. ReAct: Synergizing reasoning and acting in language models. In _International Conference_
_on Learning Representations_, 2023.


[24] Jintian Zhang, Xin Xu, Ningyu Zhang, Ruibo Liu, Bryan Hooi, and Shumin Deng. Exploring
collaboration mechanisms for LLM agents: A social psychology view. In _Annual Meeting of_
_the Association for Computational Linguistics_, 2024.


[25] Yang Zhang, Shixin Yang, Chenjia Bai, Fei Wu, Xiu Li, Zhen Wang, and Xuelong Li.
Towards efficient LLM grounding for embodied multi-agent collaboration. _arXiv preprint_
_arXiv:2405.14314_, 2024.


17


**Appendix**


**A** **Benchmarking Data Artifacts**


Table 13: Example artifacts from benchmarking data collection


Artifact Example


Scenario Goals:
```
          * User needs to book a ticket for a round-trip economy
          flight from DEN to RST, departing on June 23, and returning
          on June 30.
          * User needs to book a room in Rochester, Minnesota from
          June 23 to June 30.
          * User needs to obtain total estimated cost of flight,
          hotel, food, and local transportation for their 7-day trip,
          given their $2,500 weekly budget.

```

Background:
```
          * User’s full name is Gregory James Anderson.
          * Gregory is 36 years old.
          * Gregory resides in Denver, Colorado.
          * Gregory’s preferred class for flights is economy.

```

Input Problem `Please book a ticket for a round-trip economy flight from`
```
          DEN to RST, departing on June 23.

```

Assertions User-side assertions:
```
          * User is informed that a ticket for an economy flight from
          DEN to RST departing on June 23 have been booked.
          * User is informed that a ticket for an economy flight from
          RST to DEN have been booked. The flight from DEN to RST
          departs on June 30.
          * User is informed that a room in a hotel in Rochester,
          Minnesota from June 23 to June 30 has been booked
          * User is informed of the total estimated cost including
          flight, hotel, food, and local transportation for their
          7-day trip from Denver to Minnesota, given their $2,500
          weekly budget.
