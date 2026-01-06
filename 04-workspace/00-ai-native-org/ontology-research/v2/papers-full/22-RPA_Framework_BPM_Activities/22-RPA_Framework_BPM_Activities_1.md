<!-- Source: 22-RPA_Framework_BPM_Activities.pdf | Chunk 1/1 -->

## A framework to evaluate the viability of robotic process automation for business process activities

Christian Wellmann [1], Matthias Stierle [1], Sebastian Dunzer [1], and Martin
Matzner [1]


Friedrich-Alexander-Universit¨at Erlangen-N¨urnberg, Institute of Information
Systems, N¨urnberg, Germany
{christian.wellmann, matthias.stierle,sebastian.dunzer,
martin.matzner}@fau.de
[http://is.rw.fau.eu](http://is.rw.fau.eu)


Abstract. Robotic process automation (RPA) is a technology for centralized automation of business processes. RPA automates user interaction with graphical user interfaces, whereby it promises efficiency gains
and a reduction of human negligence during process execution. To harness these benefits, organizations face the challenge of classifying process
activities as viable automation candidates for RPA. Therefore, this work
aims to support practitioners in evaluating RPA automation candidates.
We design a framework that consists of thirteen criteria grouped into
five perspectives which offer different evaluation aspects. These criteria
leverage a profound understanding of the process step. We demonstrate
and evaluate the framework by applying it to a real-life data set.


Keywords: RPA support · viability assessment · process activity evaluation · process characteristics.


This is an accepted manuscript for the RPA Forum at the Int. Conference
on Business Process Management (BPM 2020). The final authenticated version
[is available online at https://doi.org/10.1007/978-3-030-58779-6 14.](https://doi.org/10.1007/978-3-030-58779-6_14)


1 Introduction


The state of technology is continuously advancing, resulting in shorter intervals
to scrutinize whether tasks can be automated or rely on human execution [1].
The recent rise of robotic process automation (RPA) challenges this status quo
once more and further blurs the boundaries of human computer interaction [22].
RPA automates repetitive and monotonous tasks by configuring software robots
to mimic the actions of the user on the presentation layer [2]. Organizations are
hoping for RPA to lead to an increase in time for employees to focus on valueadding activities and to cut costs [18] through eliminating time spent interacting
with information systems and data transfer [32]. Furthermore, companies expect


2 C. Wellmann et al.


RPA to improve the quality of their work, eliminate human negligence and increase reaction time around the clock [9]. Primarily driven by changing market
dynamics and global competition, companies are forced to cut costs through the
implementation of new technologies like RPA, especially when they promise a
quick and high return on investment [1].
While the benefits for organizations in applying RPA seem evident, the question remains as to why there are currently only few success stories of RPA adoption. One of the biggest challenges identified for a successful RPA implementation
is the selection of suitable processes or process activities for RPA [13,32,1]. The
methods available to date mostly offer high-level decision-making support with
the focus set on profitability rather than assessing the RPA viability of processes
or tasks [5,22,33].
The objective of this work is to offer practitioners a process characteristic
evaluation framework including a set of criteria and exemplary evaluation metrics. To understand the parameters of RPA, the following research question needs
to be answered:
What are the characteristics of a process activity, or a set of process activities,
that facilitate viable robotic process automation?
By answering the question, this work contributes to broadening the understanding in the selection of process activities for RPA. Furthermore, it serves as
a basis for the creation of a framework that examines the process activity from
different perspectives for its suitability for RPA. In addition, the application of
the framework highlights challenges when assessing the criteria and opens up
new research opportunities.
This study is structured as follows: In Section 2, the term robotic process
automation is defined and the results of a literature review are presented as
a concept matrix. Further, the existing methods for process or process activity
selection are compared to derive the similarities and differences. In Section 3, the
process characteristic evaluation framework is presented. Section 4 outlines the
evaluation approach, the data set and the pre-processing of the process before
the framework is applied and validated. The contributions, limitations and future
research are summarized in Section 5.


2 Background


2.1 Robotic Process Automation (RPA)


While the interest in RPA is still steadily increasing [29], there is no well accepted definition found in literature. Despite the arguable lack of definition, certain characteristics describing the term Robotic Process Automation are found
throughout the literature.
RPA incorporates different tools and methodologies [9,23,27,1] aiming to automate repetitive and structured service tasks that were previously performed
by humans [2,21,1]. This is achieved by the application of software algorithms
known as software robots or bots, which are imitating the execution flow of


A framework for RPA viability assessment 3


humans on the front-end [2,11,16,24,26,1]. Just as a human user, robots can interact with the user interface through mouse clicks, key board interactions and
interpretation of text and graphics [26], as well as log into multiple applications
to extract, process and enter structured or semi-structured data from different
sources [33]. RPA usually does not require defined interfaces as the software sits
on top of information systems and accesses applications only through the presentation layer [2,35], thus the back-end systems remain unchanged [20,1]. As a
result the robots perform activities in a non-invasive manner [16] without the
need of application programming interfaces (API) to transfer and process data

[33].
Depending on the configuration approach for software robots, little to no programming knowledge is required to implement and manage the orchestration and
execution of the robots often referred to as low-code development [13,16,20,26,25].
Although RPA typically favors less complex and cognitive tasks, advances in machine learning can extend the range of RPA application in the future [3,33].
In this work, we define RPA as an automation technology which performs
work on the presentation layer, can be set up by a business user, and is managed
on a centralized platform.


2.2 Process characteristics of automatable activities


In order to develop the framework, the question - What are the characteristics
of a process activity, or a set of process activities, that are suitable for robotic
process automation? - must first be answered. To obtain a comprehensive list of
potential process characteristic evaluation criteria, a literature review following
the guidelines proposed by [34] is conducted. For an exhaustive review, sources
are searched for in the databases Scopus, Google Scholar, and IEEE Xplore Digital library. The identified criteria are then compiled, checked for redundancy
and listed in a concept matrix (Table 1) that relates the criteria with the source
articles and visualizes the acceptance and relevance through the number of mentions. In particular, we used the criteria presented by Wanner et al. [33] as a
starting point and extended the list through several iterations.
Ideal candidate processes for automation must be standardized [2,3,4,5,7,9,10,11,12,13,14,15,16,17,19,21,20,2
Therefore, the process or task needs to be strictly defined and structured [3,15,17,24,33,37].
A high degree of standardization before automation is necessary to result in a low
amount of process variations and outcomes [33]. No or low subjective judgment
or interpretation skills [7,17,32,37] are required for decision making as the process follows a rule-based flow [5,7,13,14,16,19,24,26,29,32,33,37,38]. Well-suited
tasks for standardized processes are also mentioned to be mundane, simple and
monotonous [7,9,31].
In combination with a high degree of standardization, the execution frequency
of a process or task has a big impact on the automation potential. In favor of
RPA suitability, tasks need to be performed repetitively and in high transaction
volumes [7,9,10,13,14,15,16,17,19,22,24,25,26,29,31,32,33,37]. Besides the volume
of transactions it is mentioned that the transaction of a substantial amount of
data implies an aptitude for RPA [37].


4 C. Wellmann et al.


Furthermore, the maturity of a process is an indicator as to whether it fulfills
fundamental requirements for an automation effort. Maturity describes the frequency of changes to the logical execution flow of the process [5,32] and further,
that the process and its tasks are specified, predictable, stable and measurable [13,15,22,29,32]. Contrary to standardization, the failure rate describes the
amount of deviations from the defined process flow. Candidate processes suited
for RPA show little or no amount of exceptions when tasks are being executed

[5,10,17,32,33] and do not require human intervention. Additionally, the ratio
of process tasks that undergo an unusual process flow or inhibit the structured
flow to completion is limited or zero [5,33].


Characteristics


Articles


[10] - - - - 
[3]  -  
[9]  -  -  -  
[22] - - 
[24] - - - 
[26] - - - - 
[5]  -  -  -  
[7]  -  -  -  
[14] - - 
[15] - - - - 
[16] - - - 
[17] - - - - 
[19] - - - - 
[25] - - - 
[29] - - - - - - 
[31] - - 
[33] - - - - - - - - - 
[37] - - - - 
[38] - 
[13] - - - 
[32] - - - - - Total 20 18 17 9 8 7 5 4 3 2 1


Table 1. Concept matrix with dimensions [34]


With the objective to further minimize the exceptions, stability of the systems in use and the process outcome is crucial. For an execution following the


A framework for RPA viability assessment 5


predefined rules, the stability of user interfaces and the interaction between different systems is essential [26]. Ideal candidate tasks for RPA have as a result a
limited number of exceptions and high predictability of their outcomes to avoid
uncertainties and disruptions [10,33].
The speed of tasks that require access and interaction with multiple systems
can be increased immensely (e.g. data entry between systems). In 17 out of 21
examined papers, tasks including the access to different systems are mentioned to
be suitable for RPA (see Table 1). Whenever multiple systems need to be accessed
by a user, the manual effort is high and also reflected by the time consumption for
this task. A software robot can work within the different systems flawlessly and
execute the tasks more rapidly, enabling not only the extraction of information
but also the triggering of events, when a task is completed [3,9,16,17,25].
In order for process activities to be performed between multiple systems,
the data needs to be in a structured and digital form. When data is structured

[5,7,15,19,24,25,29,32,33,38], the software robot can then successfully interpret
the given input and follow the execution flow of the process activities.
Apart from process and process activity characteristics, literature mentions
that proneness to human errors is also an indicator for RPA potential. This
assumption is based on the fact, that with increasing volume of tasks, humans
will more likely cause exceptions by false entry or incorrect data manipulation
than a program would [9,13,16,17,29,37].
Moreover, a process or task can be judged by its impact or value to the
business. This is where literature does not provide a clear outline due to the
small amount of mentions. While some argue that automation potential exists
for processes with a low degree of business value [9], others state that processes
with a low execution frequency but a high business value are suitable candidates
for automation [10,37].
Focusing on the voluminous and repetitive processes, the number of users
involved in the execution reflect another perspective on RPA suitability. Kokina
and Blanchet [19] indicate potential benefits where several people are performing
the same processes, when these are repetitive and require no or low subjective
judgment. A different perspective highlights the handovers of work between different stakeholder across departments as a factor to consider [33].
Last, the execution time of a process is a criteria to assess the suitability
of processes for RPA [33]. Decreasing the time spent with repetitive and highly
transactional jobs, increases time for employees to focus on more value-adding
tasks [3].


3 Process characteristics evaluation framework


To support practitioners in evaluating the viability of RPA for process activities,
we summarized the findings of our literature review in a framework.
Table 2 visualizes the process characteristics evaluation framework (PCEF).
We present five perspectives – task, time, data, system, and human – that contain
several characteristics that analysts can use to evaluate a process accordingly.


6 C. Wellmann et al.


We present examples for evaluation of the criteria but the list is certainly not
exhaustive. We decided to exclude value as a criteria from the framework as it
is implicitly covered by other criteria such as frequency and urgency.


Perspective Criteria Exemplary Evaluation


Standardization Number of different activities
Number of variations to execution flow in business


Maturity Number of deviation cases over time
Ratio of deviation cases over time



Task


Time



Number of deviation cases over time
Ratio of deviation cases over time


Determinism Number of manual interactions
Time to solve manual interaction


Failure rate Number of unsuccessful terminations
Number of manual interactions
Number of rework loops


Frequency Number of executions


Duration Average time to task completion


Urgency Average reaction time



Data Structuredness Consistent use of data objects


Interfaces Number of execution steps
Time spent on application interface



System


Human



Stability Number of exceptions


Number of systems Number of systems involved
(e.g. CRM, ERP)


Resources Number of users performing same task
Number of users involved in process


Proneness to human Number of exceptions
error Time to solve exception


Table 2. Process characteristics evaluation framework


A framework for RPA viability assessment 7


Task perspective The task perspective refers to the execution of process activities. Its criteria are standardization, maturity, determinism, and failure rate.
First, standardization refers to a process’s degree of structure. In standardized processes, every process element is unambiguous, and the execution order
remains the same in each process instance. As a result, stakeholders receive
the same outcome from a standardized process [20,22]. Thus, we examine the
execution order and the number of process variants to measure a process’s standardization. We can, for instance, analyze predecessors and successors of the
process of interest. Ideally, the order of execution remains the same and equals
to the desired process flow.
Maturity indicates that no frequent changes to the process flow are observable. Therefore, processes need to be specified and predictable over a period in
time [5,22]. Mature processes usually terminate successfully and show a comparably low number of variants [32,15]. The evaluation focuses on the number of
process variants and the difference between the ideal and variant process paths.
Determinism is one of the most distinctive criteria to assess the viability
of RPA. Deterministic activities consist of logical execution steps without any
form of cognitive assessment [7,17,32,37]. This is a fundamental requirement
for software robots since human judgment aggravates automation. To fulfill the
criterion, logical and rule-based steps suffice to describe a process. Hence, the
evaluation examines manual interactions and execution time.
Last, the failure rate relates to self loops to repair previous executions and a
non-recoverable unsuccessful termination. A low failure rate leverages automation. The failure rate subsequently focuses on the amount of deviations from the
ideal process flow caused by failures, and their respective causes [5,10,17,32,33].
A high failure rate might correspond to poor standardization, maturity or determinism as the causes for exceptions.


Time perspective The criteria listed under the time perspective focus on the
duration and frequency of processes and process steps.
First of all, the frequency describes the absolute number a process step occurs over time. The execution frequency is high when tasks are repeated daily
and in high transaction volumes [7,9]. The criterion measures the number of an
activity’s occurrences in a certain period.
Additionally, the framework includes the duration which expresses the time
required to execute a process or an activity. The duration needed to execute a
process or an activity is a quantifiable indicator of the time-saving potential.
The final time-based criterion of the framework is urgency which describes
how critical the immediate execution of a process step is. The delayed execution may cause an increasing overall duration, or may hinder progress. Software
robots are working 24/7, unlike users with relatively short time frames. For this
reason, the evaluation focuses on the time needed to react to execute such urgent
tasks.


8 C. Wellmann et al.


Data perspective In many processes, information is processed in multiple
systems. Therefore, the data perspective resembles the structuredness of data.
If a robot shall process data, the data source must be digital [25]. Moreover,
the data must at least be semi-structured to enable automation [5]. When a
process involves handling data, users may perform simple operations to extract
it from the source and enter it into a system [15,19,24,33,38]. This is a crucial
requirement for the successful interpretation and execution of process steps. To
evaluate this criterion the data source is analyzed. Typically structured data
is in semi-structured forms like spreadsheets, websites, or emails. Unstructured
and hardly accessible data impedes RPA.


System perspective The fourth perspective in the framework is related to the
underlying systems. The perspective poses the interaction with interfaces, and
the stability of information systems.
Due to our preceding research we added the criterion interface to our framework. The criterion interface is evaluated by identifying whether the task could
be solved using software robots. Here, the time spent in an application’s interface
and the number of required execution steps serve as indicators.
Another system-related criterion is the stability. Ideally, systems and applications involved in process automation are stable. During process execution,
all operations on the user interface perform accordingly, and users only seldom
experience interruptions [10,26,33]. A stable operating system also relates to
this criterion. It guarantees the absence of system related exceptions during automation. For analyzing system stability, we propose the number of soft- and
hardware exceptions. Important in practice is to distinguish between exceptions
caused by the systems or applications themselves and external factors such as
capacity errors or connection.
The last system-related criterion in the framework is the number of systems.
It deals with process parts or activities that interact with multiple information systems. Consequently, the interaction between systems is necessary, but
no value is added when performed by a person [16,17,25]. In fact, robots outperform humans in atomic operations, like copy and paste [3,9]. Thus, automation
candidate tasks transfer information from one to other systems. The potential
of more involved systems is higher, if these are running stably.


Human perspective The last perspective deals with humans computer interaction focusing on the human. The perspective comes with two peculiarities,
resources and proneness to human error.
The framework includes resources as criterion to highlight the number of
users involved in the process. Especially frequent activities require resources to
deal with the volume of work. This criteria can be assessed from two view points.
First, based on the number of users performing the same task. Second, multiple
users contribute to an activity’s instance. [19,33]. To assess the resource savings,
we utilize the count of users performing the same task, and the number of users
involved in one task instance.


A framework for RPA viability assessment 9


The last aspect in the PCEF is the proneness to human errors as a criterion. Humans tend to erroneous behavior when executing monotonous and
voluminous tasks which results in such errors that solely relate to human nature

[9,13,16,17,29,37]. Eliminating such mistakes with business rules or robots yields
to additional savings regarding costs and time. Measuring the error proneness
relies on the number of human mistakes and the required time to fix those.


4 Evaluation


The evaluation focuses on event logs generated through PAIS. Event logs reveal
insights about the business process and its execution. We aim at an objective
evaluation by using a publicly available data-set to show the applicability of the
PCEF [8]. We determine process characteristics with Process Mining Software [1] .
Hence, we test the framework for its applicability in a practical environment.
The candidate process describes a P2P process of a multinational coatings
and paints enterprise. Due to its administrative character, it is a suitable candidate for automation. In this case, RPA minimizes manual work and increases
efficiency at the enterprise’s bottom line. The candidate process covers the steps
from creating a purchase order to the clearance of the invoice. A purchase order
contains at least one purchase order item. An item stores attributes describing
the resources involved, value of events and anonymized company information.
In total, the data set includes more than 1.5 million events, and 251,734
purchase order items (cases) in 76,349 purchase orders. To illustrate the structure
of the event log, Table 3 visualizes an event log from the data set.
To analyse the framework, we focus on the paths related to Item Category: 3way match, invoice before GR. We further drill down selecting the most common
variants ( [˜] 90%) in 2018. These filters result in 197,010 cases with 136 process
variants.
Examining the event log reveals that traces including the manual activity
’Change Quantity’ take a month longer on average.
Thus, we select ’Change Quantity’ as our process step of interest, and apply
our framework to evaluate the activity. Note that we consider the deletion of a
purchase order item and the reoccurrence of ‘Change Quantity’ as incompliant.
Standardization. The criterion examines a process’s degree of structure, and it
relates to a low number of overall variants.
Our analysis of ‘Change Quantity’ reveals that it has five valid predecessors covering 95% of all incoming process paths, and two valid successors that
cover 94% of all outgoing traces. Additionally, we examine the activity’s process
segment in different business units.
Every business unit conducts the activity in the same context. Consequently,
we identify a logical and structured process flow. The assessment shows that
the process is rather standardized, since 95% of all preceding and 93% of all
following activities are compliant and follow a certain pattern.


1 https://www.celonis.com


10 C. Wellmann et al.


Table 3. Exemplary event with contextual attributes from the event log


Attribute Value


Case ID 2000000000 00001
Activity Record Goods Receipt
Resource user 000
Complete Timestamp 2018/03/06 07:44:00.000
Variant Variant 65
Variant index 65
(case) Company companyID 0000
(case) Document Type EC Purchase order
(case) GR-Based Inv. Verif. false
(case) Goods Receipt true
(case) Item 1
(case) Item Category 3-way match, invoice before GR
(case) Item Type Standard
(case) Name vendor 0000
(case) Purch. Doc. Category name Purchase order
(case) Purchasing Document 2000000000
(case) Source sourceSystemID 0000
(case) Spend area text CAPEX & SOCS
(case) Spend classification text NPR
(case) Sub spend area text Facility Management
(case) Vendor vendorID 0000
Cumulative net worth (EUR) 298.0
User user 000


Maturity. The maturity expresses the number of compliant process variants
which establish over time. In total there are 25 variants containing the activity. Out of these 25 variants, 22 are following compliant pre- and sucessors while
three are incompliant. There are 2 variants reworking the activity and one which
causes the deletion of purchase order items.
Determinism. To assess the criterion, we must know the steps done on the user
interface and the respective throughput time of steps need to be evaluated. The
event log does not include information about the performance of the activity
’Change Quantity’ on the presentation layer. Therefore, the criterion can not be
evaluated for this data set.
Failure Rate. In this process, the execution fails when a self-loop occurs or the
process ends with the activity ‘Delete Purchase Order Item’. Reworking ‘Change
Quantity’ occurs in 3,91%, and the process determination with order item deletion happens in 1,42%. Since we only consider the outcome of one activity, we
ignore the full process context, since we cannot determine which cases actually
terminated and which are still running.
The resulting failure rate of the process is 5,33%.
Frequency. The average number of ’Change Quantity’ occurrences is 31 times
a day. Although the execution of ’Change Quantity’ varies month by month, it


A framework for RPA viability assessment 11


occurs at least 379 times a month. Regarding frequency, the activity is a valid
automation candidate.
Duration. The duration expresses an activity’s impact on the overall process
throughput time and its own required time. Information about its own execution
time to execute is missing. However, while processes without have an average
throughput time of 64 days, processes including the activity take 93 days on
average.
Urgency. The majority of the tasks are executed during the main business hours.
But, ‘Change Quantity’ quite often occurs outside of these hours. This incidence
might indicate, that certain purchase orders need fast reaction. Automation runs
all the time and minimizes the delay caused by the working hours of a user.
Structuredness of data. To perform the activity ’Change Quantity’, workers modify the purchase order document. If the source data containing the new quantity
and the purchase order document are structured data objects, a software robot
could perform the transaction. However, as the event log does not contain related
information, we cannot evaluate the criterion.
Interfaces. This aspect analyses the number of interfaces and the interactions
with these interfaces. The event log does not contain such information. Thus, we
cannot evaluate the criterion.
Stability. The stability corresponds to a low number of deviating paths and
software exceptions. The event log does not include information about exceptions
and their cause. Thus, the criterion can not be evaluated for the data set.
Number of systems. Since the event log originates from an SAP ECC system,
which is a roofing system, we cannot determine whether there are more systems
involved in the process. Therefore, our evaluation of the number of systems is
incomplete.
Resources Analyzing the number of users that execute the ’Change Quantity’
unveils that 138 different users execute the task. With the successful implementation of a robot, we can spare working time of these users.
Proneness to human error. Since the process step is exclusively executed by
users, we assume that all related errors are of human origin. Since only about
every twentieth case fails, we assume the process is rather stable, and software
robots could not leverage better performance.
As we demonstrate, the RCEF aids in determining characteristics of processes
or process steps which are automation candidates. Although we could not assess
all criteria in our case, the evaluation provides important insights.
The process flow is quite standardized. On one hand the activity is in 22
different compliant process variants, on the other hand only three infrequent
variants lead to non-compliance. In total, the overall failure rate is 5,33%, highlighting that 94,67% of all executions are fully compliant. The activity constantly
occurs during the observation, 31 times per day on average. Since ’Change Quantity’ occurs outside usual business hours, we assume the execution is urgent to
a certain extent and is restrained by manual execution. Moreover, we can spare
working hours of 138 users, if we can automate the activity successfully. Without
being able to assess the determinism, we cannot assess the viability of RPA im

12 C. Wellmann et al.


plementation for the activity. Still, without knowing anything about the process
context, the framework enables wide assessment.
However, the application of the framework also revealed some deficits when
validating the efficacy and validity through process mining software. First, missing attributes such as starting timestamps in the event log impede the possibility
to assess typically easy to evaluate criteria like the execution time or execution
urgency. Second, the possible lack of information about exceptions in the event
log inhibits the ability to distinguish between a system-related stability or human
error caused issue. Third, crucial information about the interaction on the user
interface is missing and prevents the examination of the criteria determinism,
structuredness of data, interfaces and number of systems. The missing information prevents the extraction of information such as the degree of deterministic
behavior when executing a sequence of steps, the throughput time for individual
steps or the number of applications and web-based systems used. To extend the
detail of information, the use of an user interaction logger [6] can bridge the gap
between front-end and back-end information gathering.


5 Conclusion


By conducting a literature review, this study identified process activity characteristics for RPA. These insights were used to develop a process characteristic
evaluation framework that assesses the suitability of process activities for RPA.
The framework includes a set of thirteen criteria grouped into five evaluation perspectives, enabling the examination of a process activity on different reference
levels. This abstraction of a process step emphasizes its connections to preceding
and succeeding steps and provides a concrete decision support considering the
most important factors involved.
Therefore, this study offers practitioners a guideline to evaluate a process
activity for an RPA implementation effort through the application of process
mining. The analysis reveals the standardization of the activity, its maturity
over time, the determinism of execution steps, the failure rate, the volume of
executions with respect to completion and reaction times, the structuredness of
data used, the interaction on the user interface, stability and number of systems,
users involved and the cause of exceptions related to human error. This study
proved the efficacy and validity of the framework by evaluating a process activity
through event logs out of a real-life data set. Based on the universal perspectives
within the framework, the applicability in different organizations and industries
is seen as given.
Despite the demonstration and application of the framework, it is tested only
with one data set and process. The evaluation has shown that not all criteria can
be tested against this data set and to guarantee generalization, the framework
must be validated through application to multiple and different kinds of processes. In particular, the framework contains qualitative criteria that could not
be tested with the data set. Further evaluation of these criteria – e.g. through
case studies – is necessary. Another important aspect is that the data set was


A framework for RPA viability assessment 13


anonymized and modified before publishing, limiting the accessible information
stored in the event logs. Further, the assumptions made about the data set, including filters set for the focus on one execution flow, limit the significance of
the evaluation results. Additionally, the criteria must be tested for redundancy
and their respective evaluation examples need further validation and extension.
Although these factors impair the evaluation of the framework, they offer
various opportunities for future research. First, the framework should be evaluated in different ways to ensure comprehensive validation. These can include
the application of the framework to new data sets as well as the assessment
of a process with a process owner. Conducting expert interviews to assess the
usefulness of the framework is another option to account for the solution objective. Changing the evaluation approach and substituting process mining through
robotic process mining [6] can also widen the scope of information extraction.
Second, the increasing number of articles on this topic generates new insights
that can derive additional perspectives and criteria. By conducting a case study
research further evaluation examples could surface and help practitioners to examine their processes. Finally, possible advances also include the quantification

[33] or the weighting of criteria to signal if the process activity is suitable for
RPA or not.


Acknowledgments This project is funded by the German Federal Ministry
of Education and Research (BMBF) within the framework programme Software
Campus (https://softwarecampus.de) under the number 01IS17045.


References


1. van der Aalst, W.M., Bichler, M., Heinzl, A.: Robotic process automation. Business
& Information Systems Engineering 60, 269–272 (2018)
2. Aguirre, S., Rodriguez, A.: Automation of a business process using robotic process
automation (rpa): A case study. In: Workshop on Engineering Applications. pp.
65–71. Springer (2017)
3. Anagnoste, S.: Robotic automation process - the next major revolution in terms of
back office operations improvement. Proceedings of the International Conference
on Business Excellence 11(1), 676 – 686 (2017)
4. Asatiani, A., Penttinen, E.: Turning robotic process automation into commercial
success–case opuscapita. Journal of Information Technology Teaching Cases 6(2),
67–74 (2016)
5. Beetz, R., Riedl, Y.: Robotic process automation: Developing a multi-criteria evaluation model for the selection of automatable business processes. In: AMCIS2019.
AIS Electronic Library (2019)
6. Bosco, A., Augusto, A., Dumas, M., La Rosa, M., Fortino, G.: Discovering automatable routines from user interaction logs. In: International Conference on Business
Process Management. pp. 144–162. Springer (2019)
7. Cooper, L.A., Holderness Jr, D.K., Sorensen, T.L., Wood, D.A.: Robotic process
automation in public accounting. Accounting Horizons 33(4), 15–35 (2019)


14 C. Wellmann et al.


8. van Dongen, B.: Bpi challenge 2019 (2019),
[https://doi.org/10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1, 4TU.Centre](https://doi.org/10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1)
for Research Data. Dataset
9. Fernandez, D., Aman, A.: Impacts of robotic process automation on global accounting services. Asian Journal of Accounting and Governance 9, 123–132 (2018)
10. Fung, H.P.: Criteria, use cases and effects of information technology process automation (itpa). Advances in Robotics & Automation 3 (2014)
11. Geyer-Klingeberg, J., Nakladal, J., Baldauf, F., Veit, F., van der Aalst, W., Casati,
F., Conforti, R., de Leoni, M., Dumas, M.: Process mining and robotic process
automation: A perfect match. In: BPM (Dissertation/Demos/Industry). pp. 124–
131 (2018)
12. Hallikainen, P., Bekkhus, R., Pan, S.L.: How opuscapita used internal rpa capabilities to offer services to clients. MIS Quarterly Executive 17, 41–52 (01 2018)
13. Hindel, J., Cabrera Prez, L., Stierle, M.: Robotic Process Automation: Hype or
Hope? In: Proceedings of the 15th International Conference on Wirtschaftsinfor[matik (2020). https://doi.org/10.30844/wi 2020 r6-hindel](https://doi.org/10.30844/wi{_}2020{_}r6-hindel)
14. Hofmann, P., Samp, C., Urbach, N.: Robotic process automation. Electronic Mar[kets 30, 99106 (08 2019). https://doi.org/10.1007/s12525-019-00365-8](https://doi.org/10.1007/s12525-019-00365-8)
15. Huang, F., Vasarhelyi, M.A.: Applying robotic process automation (rpa) in auditing: A framework. International Journal of Accounting Information Systems 35,
100433 (2019)
16. Ivanˇci´c, L., Vugec, D.S., Vukˇsi´c, V.B.: Robotic process automation: Systematic
literature review. In: International Conference on Business Process Management.
pp. 280–295. Springer (2019)
17. Jimenez-Ramirez, A., Reijers, H.A., Barba, I., Del Valle, C.: A method to improve the early stages of the robotic process automation lifecycle. In: International
Conference on Advanced Information Systems Engineering. pp. 446–461. Springer
(2019)
18. Kaya, C.T., Turkyilmaz, M., Birol, B.: Impact of rpa technologies on accounting
systems. Journal of Accounting & Finance 82, 235–250 (2019)
19. Kokina, J., Blanchette, S.: Early evidence of digital labor in accounting: Innovation
with robotic process automation. International Journal of Accounting Information
Systems 35, 100431 (2019)
20. Lacity, M.C., Willcocks, L.P.: Robotic process automation at telefnica o2. MIS
Quarterly Executive 15(1), 21–35 (2016)
21. Lacity, M.C., Willcocks, L.P.: A new approach to automating services. MIT Sloan
Management Review (2017)
22. Leshob, A., Bourgouin, A., Renard, L.: Towards a process analysis approach to
adopt robotic process automation. In: 2018 IEEE 15th International Conference
on e-Business Engineering (ICEBE). pp. 46–53. IEEE (2018)
23. Mendling, J., Decker, G., Hull, R., Reijers, H.A., Weber, I.: How do machine learning, robotic process automation, and blockchains affect the human factor in business process management? Communications of the Association for Information
Systems 43(1), 19 (2018)
24. Moffitt, K.C., Rozario, A.M., Vasarhelyi, M.A.: Robotic process automation for
auditing. Journal of Emerging Technologies in Accounting 15(1), 1–10 (2018)
25. Osmundsen, K., Iden, J., Bygstad, B.: Organizing robotic process automation: Balancing loose and tight coupling. In: Proceedings of the 52nd Hawaii International
Conference on System Sciences (2019)


A framework for RPA viability assessment 15


26. Penttinen, E., Kasslin, H., Asatiani, A.: How to choose between robotic process
automation and back-end system automation? In: European Conference on Information Systems 2018 (2018)
27. Ratia, M., Myll¨arniemi, J., Helander, N.: Robotic process automation-creating
value by digitalizing work in the private healthcare? In: Proceedings of the 22nd
International Academic Mindtrek Conference. pp. 222–227 (2018)
28. Romao, M., Costa, J., Costa, C.J.: Robotic process automation: A case study in
the banking industry. In: 2019 14th Iberian Conference on Information Systems
and Technologies (CISTI). pp. 1–6. IEEE (2019)
29. Santos, F., Pereira, R., Vasconcelos, J.B.: Toward robotic process automation implementation: an end-to-end perspective. Business Process Management Journal
26(2), 405–420 (2019)
30. Seasongood, S.: Not just for the assembly line: A case for robotics in accounting
and finance. Financial Executive 32(1), 31–32 (2016)
31. S¨onmez, O.E., B¨orek¸ci, D.Y.: A conceptual study on rpas as of intelligent automation. In: International Conference on Intelligent and Fuzzy Systems. pp. 65–72.
Springer (2019)
32. Syed, R., Suriadi, S., Adams, M., Bandara, W., Leemans, S.J., Ouyang, C., ter
Hofstede, A.H., van de Weerd, I., Wynn, M.T., Reijers, H.A.: Robotic process
automation: Contemporary themes and challenges. Computers in Industry 115,
103162 (2020)
33. Wanner, J., Hofmann, A., Fischer, M., Imgrund, F., Janiesch, C., GeyerKlingeberg, J.: Process selection in rpa projects–towards a quantifiable method
of decision making. In: ICIS 2019 Proceedings (2019)
34. Webster, J., Watson, R.T.: Analyzing the past to prepare for the future: Writing
a literature review. MIS Quarterly 26(2), xiii–xxiii (2002)
35. Willcocks, L.P., Lacity, M.: Service automation robots and the future of work. SB
Publishing (2016)
36. Willcocks, L.P., Lacity, M., Craig, A.: Robotic process automation at xchanging.
The Outsourcing Unit Working Research Paper Series 15(03) (2015)
37. Yatskiv, S., Voytyuk, I., Yatskiv, N., Kushnir, O., Trufanova, Y., Panasyuk, V.:
Improved method of software automation testing based on the robotic process automation technology. In: 2019 9th International Conference on Advanced Computer
Information Technologies (ACIT). pp. 293–296. IEEE (2019)
38. Zhang, C.: Intelligent process automation in audit. Journal of Emerging Technologies in Accounting 16(2), 69–88 (2019)


