<!-- Source: 15-AgentSurvey-2503.21460.pdf | Chunk 4/10 -->



Fig. 4: An overview of real-world issues in LLM agent
systems, organized into three domains: security challenges
(including agent-centric and data-centric threats), privacy
concerns (covering memorization vulnerabilities and intellectual property exploitation), and social impact considerations
(highlighting both benefits and ethical challenges).


building LLM applications that is highly extensible and allows users to create custom modules and workflows to meet
their specific needs. LlamaIndex [171] is a data framework
serving large model applications, allowing users to build
LLM applications based on local data. It also provides a
rich toolbox for accessing and indexing data, retrieving and
reordering, and building custom query engines. Dify [172] is
an open-source LLM application development platform that
differs from other platforms in that it allows users to build
and test powerful AI workflows on canvas.
_**Operation and Maintenance.**_ After deploying LLM agents,
the O&M tool ensures that the model performs well during training and remains reliable during production. Ollama [173] is a platform for building LLM agents that also
offers observability and monitoring support, allowing teams
to track their models’ performance in real-time. Dify [172]
enables users to monitor and analyze application logs and
performance over time, allowing for continuous improvements in prompts, datasets, and models based on production
data and annotations.
_**Model Context Protocol.**_ MCP [3] is an open protocol that
standardizes how applications provide context to LLMs.
It is used to create secure links between LLMs and data
sources as well as to build LLM agents and workflows. MCPAgent [174] is a simple framework to build agents using
MCP. As more services become MCP-aware, users will be
able to take full advantage of them.


**4** **REAL-WORLD ISSUES**


As LLM agents become increasingly integrated into various
aspects of society, they bring forth significant real-world
challenges that must be addressed for responsible deployment. Figure 4 provides an overview of these challenges,
categorized into three primary domains: security, privacy,
and social impact. Security concerns encompass both agentcentric threats (Section 4.1) that target model components and
data-centric threats (Section 4.2) that contaminate input data.
Privacy issues (Section 4.3) include memorization vulnerabilities and intellectual property exploitation. Beyond technical


3. https://modelcontextprotocol.io/introduction


concerns, LLM agents raise important ethical considerations
and have broad societal implications (Section 4.4), including
both potential benefits and risks to society. Understanding
these challenges is crucial for developing robust, trustworthy
agent systems.


**4.1** **Agent-centric Security**


Agent-centric security targets defending different types
of attacks on the agent models, where attacks aim to
manipulate, tamper, and steal critical components of the
weights, architecture, and inference process of the agent
models. These agent-centric attacks may lead to performance degradation, maliciously manipulated outputs, and
privacy leaks within agent systems. Li et al. [175] analyze
the security vulnerabilities of LLM agents under attacks
categorized by threat actors, objectives, entry points, and
so on. They also conduct experiments on certain popular
agents to demonstrate their security vulnerabilities. Agent
security bench [176] introduces a comprehensive framework
to evaluate attacks and defenses for LLM-based agents
across 10 scenarios, 10 agents, 400+ tools, 23 attack/defense
methods, and 8 metrics, revealing significant vulnerabilities
and limited defense effectiveness of current LLM agents.
We summarize the agent-centric security issues in the blow
categories.


_4.1.1_ _Adversarial Attacks and Defense_

Adversarial attacks aim to compromise the reliability of the
agents, rendering them ineffective in specific tasks. Mo et
al. [177] categorize adversarial attacks into three components,
i.e., _Perception, Brain, and Action_ . AgentDojo [178] provides an
evaluation framework designed to measure the adversarial
robustness of AI agents by testing them on 97 realistic tasks
and 629 security test cases. ARE [179] evaluates multimodal
agent robustness under adversarial attacks. For adversarial
attack methods, CheatAgent [180] uses an LLM-based agent
to attack black-box LLM-empowered recommender systems
by identifying optimal insertion positions, generating adversarial perturbations, and refining attacks through iterative
prompt tuning and feedback. GIGA [181] introduces generalizable infectious gradient attacks to propagate adversarial
inputs across multi-agent, multi-round LLM-powered systems by finding self-propagating inputs that generalize well
across contexts. For adversarial attacks defense methods,
LLAMOS [182] introduces a defense technique for adversarial attacks by purifying adversarial inputs using agent
instruction and defense guidance before they are input into
the LLM. Chern et al. [183] introduce a multi-agent debate
method to reduce the susceptibility of agents to adversarial
attacks.


_4.1.2_ _Jailbreaking Attacks and Defense_

Jailbreaking attacks attempt to break through the protection
of the model and obtain unauthorized functionality or
information. For jailbreaking attack methods, RLTA [184]
uses reinforcement learning to automatically generate attacks
that produce malicious prompts, triggering LLM agents’
jailbreaking to produce specific output. These can be adapted
to both white box and black box scenarios. Atlas [185]
jailbreaks text-to-image models with safety filters using a



11


mutation agent and a selection agent, enhanced by in-context
learning and chain-of-thought techniques. RLbreaker [186]
is a black-box jailbreaking attack using deep reinforcement
learning to model jailbreaking as a search problem, featuring
a customized reward function and PPO algorithm. PathSeeker [187] also uses multi-agent reinforcement learning
to guide smaller models in modifying inputs based on the
target LLM’s feedback, with a reward mechanism leveraging
vocabulary richness to weaken security constraints. For
jailbreaking defense methods, AutoDefense [188] proposes a
multi-agent defense framework that uses LLM agents with
specialized roles to collaboratively filter harmful responses,
effectively resisting jailbreak attacks. Guardians [189] uses
three examination methods—reverse Turing Tests, multiagent simulations, and tool-mediated adversarial scenarios—to detect rogue agents and counter jailbreaking attacks.
ShieldLearner [190] proposes a novel defense paradigm for
jailbreak attacks by autonomously learning attack patterns
and synthesizing defense heuristics through trial and error.


_4.1.3_ _Backdoor Attacks and Defense_

Backdoor attacks implant specific triggers to cause the
model to produce preset errors when encountering these
triggers while performing normally under normal inputs.
For backdoor attack methods, DemonAgent [191] proposes a
dynamically encrypted muti-backdoor implantation attack
method by using dynamic encryption to map and decompose
backdoors into multiple fragments to avoid safety audits.
Yang et al. [192] investigate and implement diverse forms
of backdoor attacks on LLM-based agents, demonstrating their vulnerability through experiments on tasks like
web shopping and tool utilization. BadAgent [193] attacks
LLM-based intelligent agents to trigger harmful operations
through specific inputs or environment cues as backdoors.
BadJudge [194] introduces a backdoor threat specific to the
LLM-as-a-judge agent system, where adversaries manipulate
evaluator models to inflate scores for malicious candidates,
demonstrating significant score inflation across various data
access levels. DarkMind [195] is a latent backdoor attack that
exploits the reasoning processes of customized LLM agents
by covertly altering outcomes during the reasoning chain
without requiring trigger injection in user inputs.


_4.1.4_ _Model Collaboration Attacks and Defense_

Model collaboration attack is an emerging type of attack
that mainly targets scenarios where multiple models work
together. In this type of attack, attackers manipulate the
interaction or collaboration mechanisms between multiple
models to disrupt the overall functionality of the system. For
model collaboration attack methods, CORBA [196] introduces
a novel yet simple attack method for the LLM multi-agent
system. It exploits contagion and recursion, which are hard
to mitigate via alignment, disrupting agent interactions.
AiTM [197] introduces an attack method to the LLM multiagent system by intercepting and manipulating inter-agent
messages using an adversarial agent with a reflection mechanism. For the defense methods, Netsafe [198] identifies
critical safety phenomena and topological properties that influence the safety of multi-agent networks against adversarial
attacks. G-Safeguard [199] is also based on topology guidance
and leverages graph neural networks to detect anomalies


TABLE 3: Summary of agent-centric attacks and defense in
LLM agents.


**Reference** **Description**


**Adversarial Attacks and Defense**


Mo et al. [177] **Attack:** Adversarial attack benchmark
AgentDojo [178] **Attack:** Adversarial attack framework
ARE [179] **Attack:** Adversarial attack evaluation for multimodal agents
GIGA [181] **Attack:** Generalizable infectious gradient attacks
CheatAgent [180] **Attack:** Adversarial attack agent for recommender systems
LLAMOS [182] **Defense:** Purifying adversarial attack input
Chern et al. [183] **Defense:** Defense via multi-agent debate


**Jailbreaking Attacks and Defense**


RLTA [184] **Attack:** Produce jailbreaking prompts via reinforcement learning
Atlas [185] **Attack:** Jailbreaks text-to-image models with safety filters
RLbreaker [186] **Attack:** Model jailbreaking as a search problem
PathSeeker [187] **Attack:** Use multi-agent reinforcement learning to jailbreak
AutoDefense [188] **Defense:** Multi-agent defense to filter harmful responses
Guardians [189] **Defense:** Detect rogue agents to counter jailbreaking attacks.
ShieldLearner [190] **Defense:** Learn attack jailbreaking patterns.


**Backdoor Attacks and Defense**


DemonAgent [191] **Attack:** Encrypted muti-backdoor implantation attack
Yang et al. [192] **Attack:** Backdoor attacks evaluations on LLM-based agents
BadAgent [193] **Attack:** Inputs or environment cues as backdoors
BadJudge [194] **Attack:** Backdoor to the LLM-as-a-judge agent system
DarkMind [195] **Attack:** latent backdoor attack to customized LLM agents


**Agent Collaboration Attacks and Defense**


CORBA [196] **Attack:** Multi-agent attack via multi-agent
AiTM [197] **Attack:** Intercepte and manipulate inter-agent messages
Netsafe [198] **Defense:** Identify critical safety phenomena in multi-agent networks
G-Safeguard [199] **Defense:** leverages graph neural networks to detect anomalies
Trustagent [200] **Defense:** Agent constitution in task planning.
PsySafe [201] **Defense:** Mitigate safety risks via agent psychology


in the LLM multi-agent system. Trustagent [200] aims to
enhance the planning safety of LLM agentic framework in
three different planning stages. PsySafe [201] is grounded in
agent psychology to identify, evaluate, and mitigate safety
risks in multi-agent systems by analyzing dark personality
traits, assessing psychological and behavioral safety, and
devising risk mitigation strategies.


**4.2** **Data-centric Security**


The goal of data-centric attacks is to contaminate the input
data of LLM agents, ultimately leading to unreasonable tool
calling, aggressive outputs and resource depletion, etc [202].
In data-centric attacks, any components in LLM agent
systems or default parameters are not allowed to be modified.
Based on the data type, we categorize attacks into external
data attacks and execution data attacks. Corresponding
defense strategies are summarized to counter these agent
attacks.


_4.2.1_ _External Data Attack and Defense_


_**User Input Falsifying.**_ Modifying the user input is the most
straightforward and widely used data-centric attacks. These
injections [176] can lead to uncontrolled and dangerous
outputs. Though it is simple, it always achieves the highest
Attack Success Rate (ASR) [176], [203]. Li et al. [204] propose
malicious prefix prompts, such as “ignore the document”.
InjectAgent [205] and Agentdojo [203] are two prompt
injection benchmarks, which test the single and multi-turn
attacks in LLM agents. As the widespread effect of injections
on user inputs increases, various defense models have
been designed. Mantis [206] defenses through hacking back
to attackers’ own systems. [207] offers a defense module
called the Input Firewall, which extracts key points from
users’ natural language and converts them into a structured
JSON format. RTBAS [208] and TaskShield [209] check the



12


every step of information flow and agent process, including
function calls and tool execution, to make sure the execution
aligns with the original instructions and intentions. In the
ASB [176] benchmark, a sandwich defend strategy adds
additional guarding instructions to help LLM agents ignore
malicious injections.
_**Dark Psychological Guidance.**_ Attackers can carry out dark
psychological guidance in the prompts, _e.g.,_ use “cheating”
instead of “care”, “betrayal” instead of “fairness”, “subversion” instead of “authority”. Then LLM agents are guided
to be aggressive and antisocial, which may cause serious
social impacts. [210] proposes the “Evil Geniuses” to generate
prompts to put agents into specific role-playing states. Its
prompts are optimized through the red-blue exercises. [201]
injects the dark psychological traits into the user inputs.
To defense dark psychological injections, doctor and police
agents [201] are incorporated into the agents systems. The
doctor agents conduct the psychological assessment, while
the police agents supervise the safety of agent systems. They
work together to guard the healthy psychology at any time.
_**External Source Poisoning.**_ Many attackers pay their attention to the RAG-based LLM agents, as they have been
proven to be more reliable than general memory-based
LLM agents [211]. The attackers inject poisoning samples
into the knowledge databases [175], [212]. Based on this,
the Indirect Prompt Injection (IPI) attack embeds malicious
instructions into other external knowledge sources [213],
such as the websites, support literature, emails, online BBS,
which can manipulate agents and cause them to deviate
from the original intentions. WIPI [214] controls the agents
through a public web page to indirectly poison instructions.

[215] describes a Foot-in-the-Door (FITD) attack, which
begins with inconspicuous, unrelated requests and gradually
incorporates harmless ones. This approach increases the
likelihood of the agent executing subsequent actions, leading
to resource consumption that could have been avoided.
AgentPoison [216] is a typical red teaming work, which
achieves a high success rate in knowledge-intensive QA
agent. [183] employs a multi-agent debate for defense, where
each agent acts as a domain expert to verify the facticity of
external knowledge.


_4.2.2_ _Interaction Attack and Defense_


_**Interaction between user and agent interface.**_ Some LLM
agents store the private user-agent interactions in users’
computer memory to enhance dialogue performance. During
these interactions, LLM agents are usually black-box to
attackers. [217] is a private memory extraction attack that
aggregates multiple levels of knowledge from the stored
memory. [218] presents an attack that occurs at the interface
between users and LLM agents, where it solicits information
from users.
_**Interaction among LLM agents.**_ In multi-agent LLM systems,
the interactions among agents are frequent and essential [12].
Attackers poison a single agent, which then infects other
agents [219]. This recursive attack can ultimately deplete
the computational resources. AgentSmith [220] concludes
that the infectious spread occurs exponentially fast. The
Contagious Recursive Blocking Attack (CORBA) [196] is
designed to disrupt the communications among agents,


TABLE 4: Summary of data-centric attack and defense in
LLM agents.


**Reference** **Description**


**External Data Attacks and Security**


Li et al. [204] **Attack:** Malicious prefix injection
Psysafe [201] **Attack:** A dark psychological injection benchmark
Tian et al. [210] **Attack:** Guide agents into specific role-playing states
InjectAgent [205] **Attack:** A prompting injection benchmark
Agentdojo [203] **Attack:** A user injection benchmark
AgentPoison [216] **Attack:** Poisoning samples in knowledge databases
Nakash et al. [215] **Attack:** Indirect prompt injection through FITD attack
WIPI [214] **Attack:** control agents through a public web page
ASB [176] **Attack:** A multi-type attack benchmark
AgentHarm [223] **Attack:** A multi-type attack benchmark
Mantis [206] **Defense:** Hacking back to attackers
Chern et al. [183] **Defense:** Employ multi-agent debate to verify external knowledge
RTBAS [208] **Defense:** Check every step of agent information flow
TaskShield [209] **Defense:** Check every step of agent process
Zhang et al. [201] **Defense:** Doctor and police agents guard the healthy psychology


**Interaction Attacks and Security**


Wang et al. [217] **Attack:** Private memory extraction attack
CORBA [196] **Attack:** Disrupt the communications among agents
AgentSmith [220] **Attack:** Poison one agent to infectious other agents
Lee et al. [221] **Attack:** Conduct injections to self-replicate among agents
He et al. [197] **Attack:** Inject semantic disruptions to agent communications
BlockAgents [222] **Defense:** Incorporate blockchain and PoT against byzantine attacks
Abdelnabi et al. [207] **Defense:** A multi-layer agent firewall


allowing the infection to propagate across the entire communication network. [197] incorporates a reflection mechanism
to finish disruptions based on the semantic understanding of communications. [221] injects malicious instructions
into one agent, enabling them to self-replicate across the
agent network, resembling the spread of a computer virus.
Additionally, [221] develops a tagging strategy to control
the infection spread. To defend against Byzantine attacks
during the agent interactions, BlockAgents [222] introduces
a consensus mechanism based on blockchain and proofof-thought (PoT) techniques. The agent that contributes the
most to the planning process is granted the accounting rights.
_**Interaction between agents and tools.**_ To call appropriate tools, the agents first make a plan, and then finish
the action. The interaction between agents and tools is
vulnerable. Some attackers maliciously modify planning
thoughts, and thus alter the agent actions. The agent may
call unconvincing or harmful tools to complete the task, and
further cause unexpected consequences. AgentHarm [223]
adds harmful distractions during multi-step execution tasks.
InjectAgent [205] conducts attacks during the agent planning
process. The multi-layer agent firewall [207] incorporates a
self-correction mechanism, known as the trajectory firewall
layer, to correct the deviated trajectory of agents. This firewall
layer verifies the generated responses to ensure compliance
with security rules.


**4.3** **Privacy**


The widespread use of LLMs in multi-agent systems has
also raised several privacy concerns. These issues are mainly
caused by the memory capacity of LLMs, which may lead
to the leakage of private information during conversations
or when completing tasks. In addition, LLM agents are vulnerable to attacks involving model and prompt theft, along
with other forms of intellectual property theft. This section
explores the privacy threats posed by **LLM Memorization**
**Vulnerabilities** and **LLM Intellectual Property Exploitation**
emphasizing the importance of ensuring the safe and secure
deployment of LLMs in collaborative environments. Addi


13


tionally, it discusses potential countermeasures to mitigate
these risks.


_4.3.1_ _LLM Memorization Vulnerabilities_


It has been shown that LLMs are able to generate text similar
to humans. However, such generated text may be retained
training data, which poses serious privacy protection issues.
These risks are particularly severe in multi-agent systems,
where LLMs may leak sensitive information when collaborating to solve complex tasks. This section explores the privacy
threats posed by LLM memory and discusses protection
measures against these threats.


_**Data Extraction Attacks.**_ They exploit the memory capacity
of LLMs to extract sensitive information from training
data. Carlini et al. [224] show that an attacker can extract
personally identifiable information (PII) such as name, email,
and phone number from a GPT-2 model through specific
queries. The risk of data extraction increases with model size,
frequency of repeated data, and context length [225]. Huang
et al. [226] further study data extraction attacks against pretrained LLMs such as GPT-neo, highlighting the feasibility
of such attacks in practical applications.


_**Member Inference Attacks.**_ Their purpose is to determine
whether a particular data sample has been part of the LLM
training data. Mireshghallah et al. [227] empirically analyze
the vulnerability of fine-tuned LLMs to membership inference attacks and find that fine-tuning the model head makes
it more vulnerable to such attacks. Fu et al. [228] propose a
self-calibrated membership inference attack method based
on probability changes, which provides a more reliable
membership signal through these variations. This type of
attack is particularly dangerous in multi-agent systems, as
the training data may originate from multiple sources of
sensitive information. In response to these risks, protection
strategies such as differential privacy (DP) and knowledge
distillation have been developed [229], [230].


_**Attribute Inference Attacks.**_ The goal of attribute inference
attacks is to infer a certain feature or characteristic of a
data sample using training data. To confirm the existence of
sensitive attribute inference in LLMs, Pan et al. [231] conduct
an in-depth study of privacy issues related to attribute
inference attacks in LLMs. Wang et al. [232] study attribute
existence inference attacks on generative models and find
that most generative models are vulnerable to such attacks.


_**Protective Measures.**_ Several protective strategies have been
proposed to reduce the chance of LLM memorization. Data
cleaning strategies can successfully reduce the risk of memorization by locating and eliminating sensitive information
in training data [233]. Another effective way to minimize
privacy leakage is to introduce differential privacy noise
into model gradients and training data [229] during pretraining and fine-tuning. Knowledge distillation techniques
have become an intuitive means of privacy protection by
transferring knowledge from private teacher models to
public student models [230]. In addition, privacy leakage
detection tools such as ProPILE can help service providers
assess the extent of their PII leakage before deploying LLM
agents [234].


TABLE 5: Summary of privacy threats and countermeasures
in LLM agents.


**Reference** **Description**


**LM Memorization Vulnerabilities**

