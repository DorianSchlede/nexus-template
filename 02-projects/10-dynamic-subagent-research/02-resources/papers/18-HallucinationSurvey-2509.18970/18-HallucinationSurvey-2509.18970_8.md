<!-- Source: 18-HallucinationSurvey-2509.18970.pdf | Chunk 8/8 -->

APPENDIX A
LOOP OF LLM-BASED MULTI-AGENT SYSTEM


Different from the single-agent setting, each LLM-based
agent in the MAS must communicate with other agents to
accomplish goals. To model these processes, a communication
structure _Gt_ is introduced among _N_ agents. Furthermore, _Gt_
would evolve with time to align with the dynamic adjustments
of MAS. Therefore, compared with Section II-B, the loop of
LLM-based MAS includes two additional procedures: **Broad-**
**casting** and **Structure Evolution** .

_•_ **Reasoning** : Each agent _i_ first generates its own plan _p_ _[i]_ _t_
for the next action conditioned on _b_ _[i]_ _t_ [and] _[ g]_ [:]


_p_ _[i]_ _t_ [= Φ] _[i]_ [(] _[b]_ _t_ _[i][, g]_ [)] _[.]_ (15)


_•_ **Execution** : Each agent _i_ then translates _p_ _[i]_ _t_ [into an exe-]
cutable action _a_ _[i]_ _t_ [:]


_a_ _[i]_ _t_ [=] _[ E][i]_ [(] _[b]_ _t_ _[i][, p][i]_ _t_ [)] _[.]_ (16)


_•_ **Broadcasting** : The agent _i_ broadcasts its message to its
neighbors in _Gt_ according to its plan _p_ _[i]_ _t_ [:]

      - _qt_ _[i][→][j]_ �� _j ∈_ _N_ ( _i_ )� = _B_ ( _b_ _[i]_ _t_ _[, p]_ _t_ _[i][, G][t]_ [)] _[.]_ (17)


Here   - _qt_ _[i][→][j]_ �� _j ∈_ _N_ ( _i_ )� denotes the messages sent by
the agent _i_ to its neighbors (i.e., _N_ ( _i_ )) at the time step _t_ .

_•_ **Feedback** : The learning environment would also provide
a reward _rt_ based on _st_ and _{a_ _[i]_ _t_ _[}][N]_ _i_ =1 [:]


_rt_ = _R_             - _st, {a_ _[i]_ _t_ _[}]_ _i_ _[N]_ =1� _._ (18)


_•_ **Environment** **Transition** : The learning environment
transitions to _st_ +1 based on _st_ and _{a_ _[i]_ _t_ _[}][N]_ _i_ =1 [:]


Pr     - _st_ +1�� _st, {ait_ _[}]_ _i_ _[N]_ =1� = _T_     - _st, {a_ _[i]_ _t_ _[}]_ _i_ _[N]_ =1� _._ (19)


_•_ **Perception** : Each agent _i_ perceives _st_ +1 to generate the
observation _o_ _[i]_ _t_ +1 [:]


_o_ _[i]_ _t_ +1 [=] _[ Z]_ _[i]_ [�] _st_ +1 _, b_ _[i]_ _t_ _[, a]_ _t_ _[i][,]_     - _qt_ _[j][→][i]_ �� _j ∈_ _N_ ( _i_ )�� _,_ (20)


where   - _qt_ _[j][→][i]_ �� _j ∈_ _N_ ( _i_ )� denotes the messages received
by the agent _i_ from its neighbors at the time step _t_ .

_•_ **Memorization** : The external memory module of the
agent _i_ is updated as follows,


_m_ _[i]_ _t_ +1 [=] _[ L]_ _M_ _[i]_  - _m_ _[i]_ _t_ _[, a][i]_ _t_ _[,]_  - _qt_ _[j][→][i]_ �� _j ∈_ _N_ ( _i_ )� _, o_ _[i]_ _t_ +1� _._ (21)


_•_ **Belief Update** : Then the agent _i_ refines its belief state as
follows,


_b_ _[i]_ _t_ +1 [=] _[ L]_ _B_ _[i]_   - _b_ _[i]_ _t_ _[, m][i]_ _t_ +1 _[, a][i]_ _t_ _[,]_   - _qt_ _[j][→][i]_ �� _j ∈_ _N_ ( _i_ )� _, rt_ _[i][, o][i]_ _t_ +1 _[, g]_   - _._
(22)

_•_ **Structure Evolution** : Based on _{b_ _[i]_ _t_ +1 _[}][N]_ _i_ =1 [and] _[ G][t]_ [, the]
communication structure can be updated as follows,


_Gt_ +1 = _U_        - _Gt, {b_ _[i]_ _t_ +1 _[}][N]_ _i_ =1� _._ (23)



APPENDIX B
HALLUCINATION EXAMPLE EXPLANATION


As shown in Fig. 5, we present the representative examples
of each type of agent hallucinations as follows,


_•_ **Goal Understanding Hallucinations.** In this example,
the user asks the agent to “recommend a restaurant
suitable for dining with elders”. The underlying goal is
clearly to find a restaurant whose cuisine is light and
easy to digest and whose environment is appropriate
for family gatherings. However, the agent recommends
“Spicy World”, a restaurant specializing in very spicy
crayfish and boiled fish, thereby completely ignoring the
prerequisite “suitable for elders”.

_•_ **Intention Decomposition Hallucinations.** In this example, the user asks the agent to plan a “family picnic for 10
people” and explicitly requires that the total budget for
“purchasing food” must not exceed 500 yuan. Clearly,
this plan must include a sub-intentions for “cost calculation” to verify whether the total expenditure satisfies the
budget constraint. However, when decomposing the task,
the agent only considers two steps: “choose a venue” and
“buy food”, thereby omitting a crucial component in the
decomposition of the user’s intention.

_•_ **Planning Generation Hallucinations.** This example illustrates hallucinations arising in the process of generating a concrete plan for a sub-intention derived from intention decomposition, namely “screen venues”. Given the
user’s requirements, the chosen venue should explicitly
allow picnicking. Nevertheless, the agent selects merely
“a lawn that is open all day”, conflating “opening hours”
with “time during which picnics are permitted”. In other
words, the model hallucinates at the planning stage for
the sub-intentions, failing to align the generated plan with
the constraints specified in the user’s intent.

_•_ **Perception Hallucinations.** In this example, the user asks
the agent to describe the content of an image. In the
image, a chair is located to the right of a bookshelf,
yet the agent responds that “the chair is to the left of
the bookshelf”. This error is a prototypical perceptual
hallucination, in which the agent’s visual understanding
or spatial localization is systematically biased.

_•_ **Memory Retrieval Hallucinations.** Here, the user asks
the agent to “tell me about tomorrow’s meeting schedule”.
The memory store contains two relevant events: a project
discussion meeting at 10:00 a.m. today and a customer
meeting at 1:00 p.m. tomorrow. However, the agent fails
to correctly anchor the events to their respective dates and
instead treats both meetings as if they were scheduled for
tomorrow. This illustrates that hallucinations can arise at
the memory retrieval stage, where agents mis-retrieve or
mis-align temporally indexed information.

_•_ **Memory Update Hallucinations.** In this example, the
user instructs the agent to “cancel all meetings tomorrow
morning”. During the memory update process, however,
the agent erroneously clears the entire schedule for the
following day, including the afternoon meeting. This reflects a hallucination in self-managed memory editing: the


JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 22



















Fig. 5. The depiction of different types of agent hallucinations, each illustrated with a representative example. The detailed explanation is given in Appendix B.



agent performs an overgeneralized or incorrect update,
leading to a memory update hallucination.

_•_ **Tool Selection Hallucinations.** The user plans to travel to
Kyoto in autumn and asks the agent to recommend tourist
attractions. The agent incorrectly calls a non-existent
tool named “get kyoto travel info”, whereas the correct
tool in the system should be “recommend tourist spots”.
This indicates that, when selecting external tools, the
agent may “invent” plausible-sounding but non-existent
APIs or function names, thereby exhibiting tool selection
hallucinations.

_•_ **Tool Calling Hallucinations.** Similar to the previous
case, this time the agent selects the correct tool, “recommend tourist spots”, but arbitrarily appends an extra
parameter language=“English”, which is not part of the
tool’s actual specification. This demonstrates that even
when the tool name is correct, the agent may hallucinate
at the parameter level—engaging in hallucinatory argument extension—which can cause the call to fail or yield
unintended behavior.

_•_ **Communication Hallucinations.** This example illustrates an “echo chamber effect” in multi-agent communication, a particularly typical form of communication



hallucination. Initially, the client states that they require
a “code review”. As the message passes along a chain
of agents, the first agent mishears it as “cold review”,
the second relays it as “gold review”, and the third
finally interprets it as “old review”. Through multiple
rounds of transmission, the information is progressively
distorted until it becomes completely detached from the
original meaning. This hallucination shows that, when
multiple agents collaborate, minor mis-hearings or misinterpretations can be amplified, producing a “telephone
game” style accumulation of deviations.


