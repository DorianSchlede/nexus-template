<!-- Source: 03-ClaudeCode-2508.08322.pdf | Chunk 2/2 -->

integration: after Claude’s changes, the CI pipeline would run again to double-check tests
and then could auto-merge the changes if all checks passed.


Throughout this process, the structured layering of context is key (see Figure 4). At any
given time, an agent is working with a manageable slice of information: its role-specific prompt +
CLAUDE.md context + task-specific instructions + relevant code/knowledge snippets. This helps
maintain coherence even for very large tasks. We also observed that dividing the work among
agents reduced prompt tokens per agent, which mitigates context window issues. While our system
currently executes largely in a sequential manner (one sub-task at a time), it is straightforward
to parallelize independent sub-tasks by spawning agents concurrently – an approach suggested by
Anthropic’s experiments with multi-agent research systems [7]. In our case study tasks, parallelism
was less a priority because many steps had inherent dependencies (you can’t test before code is
written, etc.), but as AI agents become more adept at coordination, parallel execution could speed
up complex multi-component feature implementations.

### **5 Results**


We evaluated our context-engineered assistant on several non-trivial development tasks in the
RainMakerz codebase. Table 1 provides a summary of outcomes on a sample of 5 tasks, comparing
our system to a baseline single-agent Claude (with only a CLAUDE.md context and direct user
prompts). In brief, our multi-agent approach succeeded in more tasks and required fewer iterations.
It often produced working solutions _on the first attempt_, whereas the baseline frequently needed
follow-up prompts or developer intervention to correct mistakes.


**Case Study: Adding a New Feature.** One test involved implementing a new _”CustomBlock”_
in the RainMakerz pitch-deck module (a feature analogous to creating a new content block type in
a presentation). This task spanned front-end and back-end changes: creating a React component
for the block, adding corresponding options UI, updating TypeScript types, and registering the
block in a manager so it could be recognized and saved. Our system handled this end-to-end. The
Planner agent broke the task into 4 steps aligned with these requirements. The Frontend specialist
agent created the new component and its options popup, correctly following the patterns in existing
blocks (likely aided by the retrieved code context of similar blocks). The Backend agent updated
the data model and API endpoints where necessary (though in this case, most logic was front-end,
the agent double-checked if any server changes were needed for persistence). After code generation,
tests were executed; an initial failure occurred because the new block type was not added to a
serialization whitelist. The orchestrator immediately flagged this and tasked the Backend agent
with updating the serialization config. The second test run passed all unit and integration tests.
Finally, the Reviewer agent made a minor suggestion to refactor a hard-coded string into a constant,
which was applied. The entire feature was completed in one automated session. In contrast, when
we tried prompting a single Claude instance for the same task (with the project README and an
excerpt of a similar block as context), the assistant produced only the React component and forgot


9


to update the registry and type definitions, resulting in runtime errors. This highlights how our
system’s comprehensive approach (particularly, planning and retrieving scattered context) leads to
more thorough solutions.


**Improved Context Adherence.** We observed that the multi-agent system was far less prone
to hallucinating irrelevant code or inventing functions. Every function or class used by the generated code existed in the repository, which we attribute to the semantic code retrieval providing
real definitions to the agents. The baseline often guessed function or variable names (e.g. referring to a non-existent getEvents() API) which then caused failures. By having access to actual
API documentation from AllianceCoder-like retrieval and the code index, our agents stuck to the
truth of the codebase and documentation. For example, in a bug-fix task concerning authentication, the baseline assistant attempted to use a refreshToken() call that did not exist, whereas our
system consulted the project docs (via CLAUDE.md context) and correctly utilized the existing
renewSession() function.


**Single-Shot Success Rate.** Out of 5 tasks attempted (including feature additions and bug fixes
of varying complexity), our system achieved a successful outcome (defined by passing all tests and
meeting the acceptance criteria) on 4 tasks (80%) without any human corrections. The singleagent baseline succeeded on only 2 tasks (40%), with the others requiring significant manual fixes
or additional prompting. While this is a small sample, it aligns with the qualitative improvements
noted in prior multi-agent studies (e.g., DARS and HyperAgent). Notably, even on the one task
where our approach did not fully succeed on the first try, it made partial progress and identified an
environmental issue (a misconfigured library) that a developer then easily fixed before re-running
the agent.


**Efficiency and Cost.** The richer context and multi-step reasoning come with a cost in LLM
usage. On average, our system exchanged around 30-40 messages across all agents for a single
task and consumed roughly 100k tokens in total (input + output). In contrast, the single-agent
approach might use 10k-20k tokens for a few prompt-response turns. In our evaluation, the multiagent method used about 3–5 _×_ more tokens on successful tasks. However, the baseline often
needed multiple attempts or lengthy debugging chats which, if counted, push its token count closer
to 50k for a complex task. Thus, the overhead of our approach is justified by getting the job done
largely autonomously. In a team setting, the value of saving developer time by achieving a correct
solution outweighs the additional compute cost. We also note that the modular design allowed us
to parallelize certain steps (though in our tests we ran sequentially); in future, this could further
improve wall-clock efficiency.

### **6 Discussion**


**Effect of Context Engineering.** The case studies and results illustrate how each element of our
context engineering approach contributes to the overall performance. The intent translation step
(GPT-5) proved particularly useful in breaking down ambiguous requests. We found that when
the initial user query was directly fed to the code agents (baseline approach), the agents sometimes
focused on the wrong sub-problem or skipped a requirement. Having a clarified spec up front led to
more relevant searches and a more coherent plan. Similarly, the use of Elicit and NotebookLM to
inject external knowledge was validated in scenarios where the code change required understanding
concepts outside the codebase. For instance, in one bug fix, the Planner agent suggested using


10


a debounce mechanism for an API call; the knowledge summary included a brief explanation of
debouncing (from a blog post retrieved by Elicit), which guided the coding agent to implement
it correctly. Without that, the baseline agent attempted a simplistic fix that did not address the
root cause. These observations align with the premise of retrieval-augmented generation: providing
pertinent information at generation time greatly improves correctness.


**Lessons on Multi-Agent Orchestration.** We adopted multiple specialized agents to mirror
the human software development process (design, coding, testing, reviewing). This division of labor
generally worked well. One lesson was the importance of clearly delineating responsibilities to avoid
both gaps and overlaps. Early in development, we occasionally encountered situations where two
agents would both attempt to modify the same file (e.g., both frontend and backend agents editing
a shared config) or conversely, an agent assumed another would handle a step that got missed.
We mitigated this by refining the Planner’s prompt to explicitly assign sub-tasks to agent roles,
and by implementing a simple lock in the orchestrator to prevent concurrent edits to the same file.
Another insight is that the quality assurance step with a dedicated reviewer agent is invaluable.
The reviewer caught subtle issues (like potential null pointer access and minor security concerns)
that the coding agents overlooked while focusing on feature implementation. This reflects how
human code reviews add value even when code ”works”, and suggests that AI coding agents benefit
from a second pair of eyes as well.


**Limitations.** Despite its successes, our approach has limitations. First, the dependency on highquality external knowledge is a double-edged sword. In one experiment, Elicit returned an irrelevant
research paper due to an ambiguous query, and although NotebookLM summarized it faithfully,
that summary added noise to the context and confused the Planner agent. Robust retrieval ranking
and perhaps filtering by a human or a more advanced AI could be needed to ensure only useful
information is fed into the system. Second, the current orchestrator logic is relatively brittle; it
follows a predetermined sequence (plan _→_ code _→_ test _→_ review). If an unexpected situation arises
(e.g., the plan is flawed or a new requirement emerges mid-way), the system is not yet equipped
to dynamically re-plan from scratch. This is an area where more adaptive, possibly reinforcement
learning-based, agent controllers (as explored in MARL settings) could help in the future. Third,
the computational cost, while acceptable for our use, might become problematic on very large
projects or if many agents run in parallel. Techniques like context compression, caching of vector
search results, or using smaller specialized models for certain agents could help reduce overhead.
Another limitation is that we relied heavily on the presence of a comprehensive test suite. If
tests are sparse, the system might incorrectly judge a task as complete. Incorporating static analysis
tools (which we did to some extent via linters) and perhaps a ”spec verification” agent to reason
about requirements could partially address this gap. Moreover, error tracing can be challenging in a
multi-agent context; if a final result is wrong, it takes careful log analysis to pinpoint which agent’s
action or which piece of context led to the mistake. Tooling like SeaView [6] could be integrated to
visualize agent interactions and states, making debugging easier for developers overseeing the AI.


**Generality and Future Work.** While our implementation targeted a specific web application
(Next.js/TypeScript stack), the principles are generalizable. We envision applying the same context
engineering pattern to other domains (e.g., Java microservices, data science notebooks) by swapping
in relevant retrieval sources and agent specializations. The modular design allowed us to add an
additional agent (for example, we introduced a database-migrator agent to handle SQL schema
changes in one case) without altering the core orchestrator logic. This suggests that as long as


11


tasks can be clearly partitioned, the multi-agent approach can scale to very complex projects by
simply growing the team of AI agents.
Looking forward, integrating learning mechanisms is an exciting avenue. Currently, our system
does not learn from its mistakes beyond a single session. One could imagine logging all agent interactions and outcomes to fine-tune the agents or a meta-controller, akin to an RL (reinforcement
learning) paradigm. Another direction is improving the Planner agent with more sophisticated algorithms (e.g., search-based planning or using graph representations of the code as in AllianceCoder’s
analysis). Finally, with the rapid progress in LLM capabilities, we anticipate that some components
(like the Intent Translator) could eventually be subsumed by more powerful code-focused models,
but the need to orchestrate multiple steps and use tools will persist. Our work provides a blueprint
for how such orchestration can be done in a robust, context-rich way.

### **7 Conclusion**


We presented a novel context engineering methodology for multi-agent LLM-based code assistants,
combining intent clarification, semantic retrieval, knowledge synthesis, and coordinated sub-agents.
In a case study on a large codebase, this approach substantially outperformed a conventional singleagent setup, delivering more accurate and complete code solutions with minimal human input. The
results underscore the importance of supplying LLMs with not just more information, but the _right_
information in the right form, as well as structuring the problem-solving process into manageable
subtasks. By drawing on ideas from recent research (planning, modular agents, RAG, etc.) and
unifying them in a practical workflow, we achieved a system that moves closer to autonomous
software development.
There are many avenues for further work. Our ongoing efforts include scaling up evaluation
to diverse projects and benchmarks to quantify gains more rigorously, and enhancing the system’s
adaptability (making the planner and orchestrator more dynamic and error-aware). We are also
interested in exploring how human developers and AI agents can best collaborate; for instance,
allowing a human to intervene in the agent loop in a structured way (perhaps to approve a plan or
provide hints) could combine the strengths of both.
Overall, our findings suggest that the era of **multi-agent, context-rich code assistants** is on
the horizon. By carefully engineering the context and workflow in which advanced LLMs operate,
we can unlock capabilities that single monolithic prompts alone cannot achieve. We hope this work
provides a foundation and inspiration for building the next generation of AI-assisted development
tools.

### **References**


[1] Bui, N. D. Q., Phan, H. N., and Nguyen, P. X. (2024). _HyperAgent: Generalist Software_
_Engineering Agents to Solve Coding Tasks at Scale_ . arXiv:2409.16299.


[2] Arora, D., Sonwane, A., Wadhwa, N., Mehrotra, A., Utpala, S., Bairi, R., Kanade, A.,
and Natarajan, N. (2024). _MASAI: Modular Architecture for Software-engineering AI Agents_ .
arXiv:2406.11638.


[3] Wen, J., Guan, J., Wang, H., Wu, W., and Huang, M. (2025). _CodePlan: Unlocking Reasoning_
_Potential in Large Language Models by Scaling Code-form Planning_ . In _Proceedings of ICLR_
_2025_ .


12


[4] Aggarwal, V., Kamal, O., Japesh, A., Jin, Z., and Sch¨olkopf, B. (2025). _DARS: Dynamic_
_Action Re-Sampling to Enhance Coding Agent Performance by Adaptive Tree Traversal_ .
arXiv:2503.14269.


[5] Gu, W., Chen, J., Wang, Y., Jiang, T., Li, X., Liu, M., Liu, X., Ma, Y., and Zheng, Z. (2025).
_What to Retrieve for Effective Retrieval-Augmented Code Generation? An Empirical Study_
_and Beyond_ . arXiv:2503.20589.


[6] Bula, T., Pujar, S., Buratti, L., Bornea, M., and Sil, A. (2025). _SeaView: Software Engineering_
_Agent Visual Interface for Enhanced Workflow_ . arXiv:2504.08696.


[7] Anthropic. (2025). _How we built our multi-agent research system_ . Engineering Blog, published
June 13, 2025.


13


