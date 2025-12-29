<!-- Source: 07-Classifying_Processes_Barry_Smith.pdf | Chunk 2/2 -->

_constant speed running process_
_cardiovascular exercise process_
_air-displacement process_
_compression sock testing process_


as well as of multiple determinate universals such as


_running process of 30 minute duration_
_3.12 m/s motion process_
_9.2 calories per minute energy burning process_
_30.12 liters per kilometer oxygen utilizing process_


and so on.
How, given the complexity of this list and of the many similar
lists which could be created for many other types of process, are
we to create classifications of the process universals instantiated
in different domains in the sort of principled way that will be


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 483


necessary to ensure consistency and interoperability when classifications are needed for the annotation of data in domains such as
physiology or pathology?
To see the lines of our answer to this question, consider Figure 4,
which illustrates the cardiac events occurring in the left ventricle of
a human heart. This figure tells us that each successive beating of
the heart is such as to involve multiple different sorts of physiological processes, corresponding to measurements along the six distinct dimensions of _aortic pressure_, _atrial pressure_, _ventricular pressure_,
_ventricular volume_, _electrical activity_, and _voltage_ [40], respectively. [41]


**Figure 4 A Wiggers diagram, showing the cardiac processes occurring in**
**the left ventricle** [42]



120


100


80


60


40


20


0


130


90


50











Aortic pressure


Atrial pressure


Ventricular pressure


Ventricular volume


Electrocardiogram



Phonocardiogram


40 Here voltage is used as a proxy for the intensity of sound.
41 As de Bono, et al., point out, these measurements reflect the variables encoded in
models of human physiology created by scientists using ordinary differential equations
(Bernard de Bono, Robert Hoehndorf, et al., ‘The RICORDO Approach to Semantic
Interoperability for Biomedical Data and Models: Strategy, Standards and Solutions’, _BMC_
_Research Notes_ 4 (2011), 31).
42 Cardiac Cycle, Left Ventricle, http://commons.wikipedia.org/wiki/File:Wiggers_
Diagram.svg.


© 2012 Blackwell Publishing Ltd


484 BARRY SMITH


These structural dimensions are, equivalently, different dimensions along which processes can be compared. When comparing
two heart beating processes as being for example of the _same rate_,
or when comparing two games of chess as consisting of the _same_
_series of moves_, then there is something in each of the two processes
which is – not numerically but qualitatively – ‘the same’. This
something which the two processes share in common we shall
refer to in what follows to as a _process profile_ .
What they share in common more precisely is that each contains an instantiation of the same _process profile universal_ . The
figure illustrates multiple instantiations of multiple process
profile universals reflecting the fact that we can measure and
compare cardiac processes along multiple different axes, each of
which corresponds, in our proposed terminology, to a different
determinable process profile universal.
In the _running_ case, similarly, we can measure and compare
along different structural dimensions pertaining to _speed of motion_,
_energy consumed_, _oxygen utilized_, and so forth. In each case we focus
on some one structural dimension and thereby ignore, through a
process of selective abstraction, all other dimensions within the
whole process.
Not every dimension of comparison between processes corresponds to a determinable process profile universal in the sense
here intended. When we compare processes as to their duration,
for example, or as to the time at which they occur or their trajectory in space and time, then we can advert simply to the temporal
or spatiotemporal regions which the processes occupy (see again
Table 2 above). We can compare processes also for example in
terms of whether they involve the same participants, or take place
in the same spatial regions. Process profiles enter into the picture
only where it is something (thus some occurrent entity) _in the_
_processes themselves_ that serves as _fundamentum comparationis_ .


_4.1 Quality Process Profiles_


The simplest example of a process profile is that part of a process
which serves as the target of selective abstraction focused on a
sequence of instances of determinate qualities such as temperature or height. When we measure, for example, the _process of_
_temperature increase_ in patient John, then there is a sequence of
determinate temperature qualities whose values when measured
on some scale are recorded on John’s temperature chart. Process


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 485


profiles of this simple sort can very often be represented by means
of a graph in which measures of a certain quality are plotted
against time.


_4.2 Rate Process Profiles_


On a somewhat higher level of complexity are what we shall call
rate process profiles, which are the targets of selective abstraction
focused not on determinate quality magnitudes plotted over successive instants of time, but rather on certain ratios between these
magnitudes and associated intervals of elapsed time. A speed
process profile, for example, is represented by a graph plotting
against time the ratio of distance covered per unit of time. Since
rates may change, and since such changes, too, may have rates of
change, we have to deal here with a hierarchy of process profile
universals at successive levels, including:


_speed profile_
_constant speed profile_
_2 mph constant speed profile_
_3 mph constant speed profile_
_acceleration profile (increasing speed profile)_
_constant acceleration profile_
_32 ft/s_ _[2]_ _acceleration profile_
_33 ft/s_ _[2]_ _acceleration profile_
_variable acceleration profile_
_increasing acceleration profile_


and so on.
The types and subtypes listed here are in some respects analogous to the determinable and determinable types and subtypes of
qualities recognized by BFO-conformant ontologies on the continuant side discussed already in our discussion of Figure 3 above.
And here, too, the reader must bear in mind that the determinate
process profile universals in question – while they need to be
referred to in reporting results of measurement acts using specific
units of measure – are in and of themselves unit-specification
independent.
Measurement data representing rates are often expressed in
terms not of the process profile instantiated across a temporal
interval, but rather of what holds at some specific temporal
instant. The latter is then defined in terms of the former in the
following way:


© 2012 Blackwell Publishing Ltd


486 BARRY SMITH


(1) John is moving with speed _v_ at time instant _t_


asserts, roughly, that there is some temporal interval ( _t_ 1, _t_ 2),
including _t_ in its interior, in which the speed _v_ process profile
universal is instantiated. More precisely (in order to take account
of the fact that John may be moving with a continuously changing
speed in the neighborhood of _t_ ), (1) must be formulated in
something like the following terms:


(2) Given any e, however small, we can find some interval ( _t_ 1,
_t_ 2), including _t_ in its interior, during which the speed _w_ at
which John is moving is such that the difference between _w_
and _v_ is less than e. [43]


_4.3 Cyclical Process Profiles_


One important sub-family of rate process profiles is illustrated by
cyclical processes, for example the 60 beats per minute beating
process of John’s heart, or the 120 beats per minute of his drumming process, and so on.
Cyclical process profiles are a subtype of rate process profiles in
which the salient ratio is not distance covered but rather number of
cycles per unit of time. Here again we find a variety of more specialized universals at lower levels of generality, including for example:


_rate process profile_
_cyclical process profile_
_regular cyclical process profile_
_3 bpm cyclical process profile_
_4 bpm cyclical process profile_
_irregular cyclical process profile_
_increasing cyclical process profile_


and so on.
In the case of a regular cyclical process profile, a rate can be
assigned in the simplest possible fashion by dividing the number of
cycles by the duration of the temporal region occupied by the
process profile as a whole. Irregular cyclical process profiles, for
example as identified in the clinic, or in a morse code transmission,


43 e, _v_ and _w_ are assumed to be measured in some common unit of velocity.


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 487


or in readings on an aircraft instrument panel, may be of specific
interest because they are of diagnostic or forensic significance.


**5. Conclusion: Towards an Ontology of Time Series Graphs**


We have dealt in the foregoing with only a small selection of the
ways in which processes can be classified through division into
types and subtypes. One important next step will deal with the
ways in which such classification is complicated by the fact that
processes are embedded within a series of larger process wholes,
each nested within yet larger process wholes. Thus when a billiard
ball is moving across a table, we can focus on the ball’s motion
relative to the table, but we can also focus on the larger process
which is the motion of the body-table system relative to the motion
of the earth; or we can focus on the motion of the body-table-earth
system relative to the movement of the sun; and so forth.
Human physiological processes, too, are embedded within series
of larger wholes in this way. When studying the heart, for example,
physiologists may investigate processes within the interior of the
left ventricle, interactions between the left ventricle and other parts
of the cardiovascular system, interactions between this system and
other bodily systems, and so on. Physiologists may be interested in
the processes involving multiple organisms; for example they may
be interested in some given organism as part of one or other larger
whole which includes some population of organisms of a relevant
similar type (all humans, all human babies of a given birth weight,
all athletes, and so on). _Normal processes_ are defined for this larger
population (as _normal qualities_ were defined above), and deviations
from this norm are defined for the single organism relative thereto.
A further application of the theory of process profiles will
include the development of an ontology of time series graphs in
terms of a view of process profiles as the truthmakers for such
graphs. On this basis we will then explore how the ontology of
process profiles might throw light on the semantics of differential
equations and of the various mathematical models of dynamic
systems in physics, biology and other disciplines constructed on
their basis. [44]


44 Exploratory work along these lines is described in Daniel L. Cook, et al. ‘Physical
Properties of Biological Entities: An Introduction to the Ontology of Physics for Biology,’
_PLoS ONE_, 2011, 6(12): e28708.


© 2012 Blackwell Publishing Ltd


488 BARRY SMITH


We will investigate also how the theory can be applied not
merely to quantitative information artifacts but also to other sorts
of symbolic representations of processes, as for instance when a
chess game is represented in one or other of the standard chess
notations, or when a symphony performance is represented in a
score. Interestingly, this score itself serves also to provide the set of
instructions for the unfolding performance, and we shall explore
also ways in which the idea of process profiles may help to throw
light on how such planned processes depend on, and are at the
same represented by, the plans or protocols which define them.


_University at Buffalo_
_phismith@buffalo.edu_


© 2012 Blackwell Publishing Ltd


