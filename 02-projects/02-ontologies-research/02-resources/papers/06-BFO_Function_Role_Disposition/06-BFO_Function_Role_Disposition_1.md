<!-- Source: 06-BFO_Function_Role_Disposition.pdf | Chunk 1/1 -->

# **_Function, role and disposition in Basic_**

1 2*
# _Formal Ontology Robert Arp and Barry Smith_



Revised version: November 2011; original appeared in _Proceedings of Bio-Ontologies_

_[Workshop](https://pdfs.semanticscholar.org/acb2/8e3f4fca09a05aa544baa3cdee5ed7282a1b.pdf)_, Intelligent Systems for Molecular Biology (ISMB), Toronto, 2008, 45-48



; original appeared in



Revised version: November 2011



1 _The Analysis Group, LLC, rarp@tag-llc.com_
2 _National Center for Biomedical Ontology (NCBO), Department of Philosophy, University at Buffalo,_ _phi-_
_smith@buffalo.edu_

- To whom correspondence should be addressed.

### **ABSTRACT**


Numerous research groups are now utilizing Basic Formal Ontology (BFO) as an upper-level framework to assist in the organization and integration of biomedical and other types of information. In this
paper, we attempt to elucidate the categories of _role_, _disposition_, _function_, and _capability_ in BFO by
means of definitions and examples. We also discuss _tendency_ as one variety of disposition, and introduce the defined classes _artifactual function_ and _biological function_, providing definitions for each. Our
motivation is to help advance the coherent ontological treatment of these categories and to shed light on
BFO’s general structure and use.


**1** **Introduction**

The ontologies which together form the Open Biomedical Ontologies (OBO) Foundry [1] —including the
Gene Ontology, the Foundational Model of Anatomy, the Protein Ontology, and the Ontology for Biomedical Investigations—utilize Basic Formal Ontology (BFO) to assist in the categorization of entities
and relationships in their respective domains of research. Individuals and groups in organizations such
as BioPAX, [2] Science Commons, [3] Ontology Works, [4] the National Cancer Institute, [5] and Computer Task
Group, [6] also utilize BFO in their work.

BFO is an upper-level ontology developed to support integration of data obtained through scientific
research. It is deliberately designed to be very small, so that it may represent in a consistent fashion
those upper-level categories common to domain ontologies developed by scientists in different fields. It
is also kept small in order to exercise the principles of modularity and to allow the division of expertise;
a top-level ontology should not contain terms like ‘cell’, ‘death’, or ‘plant’ that properly belong in domain-specific ontology modules of narrower scope.

BFO adopts a view of reality as comprising (1) continuants, entities that continue or persist through
time, such as objects, qualities, and functions, and (2) occurrents, the events or happenings in which
continuants participate. [7,8] The subtypes of continuant and occurrent represented in BFO are presented in
Figures 1 and 2, respectively. [9]


**1**


_**Realizable Entities in Basic Formal Ontology**_


_continuant_
_independent continuant_
_material entity_
_object_
_fiat object part_
_object aggregate_
_object boundary_
_site_
_dependent continuant_
_generically dependent continuant_
_specifically dependent continuant_
_quality_
_realizable entity_
_role_
_disposition_
_capability_
_function_
_spatial region_
_zero-dimensional region_
_one-dimensional region_
_two-dimensional region_
_three-dimensional region_

Figure 1: Continuants in BFO 1.1


_occurrent_
_processual entity_
_process_
_process boundary_
_process aggregate_
_fiat process part_
_processual context, deprecated_
_spatiotemporal region_
_scattered spatiotemporal region_
_connected spatiotemporal region_
_spatiotemporal instant_
_spatiotemporal interval_
_temporal region_
_scattered temporal region_
_connected temporal region_
_temporal instant_
_temporal interval_


Figure 2: Occurrents in BFO 1.1


**2**


_**Realizable Entities in Basic Formal Ontology**_

### **2 Function, Role, and Other Terminological Confusions**

The term ‘function’ is used to describe both biological entities [10] and human-designed artifacts. [11, 12] Consider, for example, assertions such as:

  - the function of the kidney is to filter out waste and water which become urine,

  - the function of the protein tyrosine phosphatase SHP-1 is to control intracellular phosphotyrosine
levels in lymphocytes,

  - a three-gene operon (CmeABC) functions as a multidrug efflux system in Campylobacter jejuni,

  - the function of a potometer is to measure water uptake in a tube, such as a leafy shoot, and

  - a retort functions to distill substances in the lab.


Functions play a central role in virtually all of the biomedical disciplines, even if some thinkers deny
their existence. [13] One of the three constituent ontologies of the Gene Ontology (GO) is devoted to the
representation of molecular functions associated with genes and gene products. [14] Functions are invoked
in standard definitions of health and disease—for example, the work of Boorse [15] —as well as classifications of disabilities. An example is the World Health Organization’s International Classification of
Functions, Disabilities and Health (ICF). [16]


The term ‘function’ is sometimes used interchangeably with the term ‘role’ as, for example, when
Zhou and Ouyang tell us that “GATA-3 plays a central role in regulating Th1 and Th2 cell differentiation”; but then a few lines later note that they will “review the function of GATA-3 in Th1 and Th2 cell
differentiation.” [17] In the glossary of his recent book on molecular biology, Hunter defines function as:
“the role that a structure plays in the processes of a living thing”. [18]


Analogous issues arise with regard to the terms ‘disposition’, ‘tendency’, and ‘capability’, as in:


blood has the tendency or disposition to coagulate,


the uranium pile has the disposition or tendency to chain react,


that patient has suicidal dispositions or tendencies,


after myocardial infarction, human bone marrow cells have regenerative tendencies or capabilities,


and


nitridergic peptides are encoded by the gene disposition or capability in Drosophila melanogaster.


Such confusion is important, since it highlights inconsistent thinking about biological and clinical
phenomena. It stands in the way of coherent computer representations of data, and serves as an obstacle
to understanding influential ontologies such as the GO.

### **3 Basic Formal Ontology (BFO)**

In BFO, all entities are divided into continuants and occurrents. Continuants can be either independent
or dependent. The principle examples of independent continuants are the objects we see around us every


**3**


_**Realizable Entities in Basic Formal Ontology**_


day. These serve as the bearers or carriers of dependent continuants such as qualities and realizable entities.

Dependent continuants are related to their bearers by inherence. Inherence is defined as a one-sided,
existential dependence relation. This means that, in order for a dependent continuant to exist, some other
independent continuant must exist to serve as its bearer. When inherence is specific, dependent continuants are termed specific dependent continuants. For example, an instance of a quality such as round or
red is termed a specific dependent continuant since it cannot exist except as a quality of a specific independent continuant such as this ball or that rash. The redness of this ball cannot become (and could not
have been) the redness of that ball. Thus, specifically dependent continuants, such as qualities, functions, roles, and dispositions can exist only insofar as they are the qualities, functions, roles, and dispositions of specific independent continuants. For example:

  - negative charge is a quality of this phosphate,

  - adhesion is the quality of the water in this flask,

  - detoxification is a function of the liver,

  - production of glycogen is a function of the endoplasmic reticulum,

  - pathogen is the role of this bacterium in cholera,

  - human subject is the role of this person in the clinical trial,

  - a threatened rattlesnake is disposed to strike, and

  - mature bamboo scaffolding has the disposition to be cyclone-resistant.

Specifically dependent continuants, such as headaches or talents, cannot migrate from one bearer to
another, as contrasted with generically dependent continuants, such as the pdf file on your laptop, which
can exist in a multiplicity of bearers.

Cross-cutting the division between dependent and independent entities is the division between types
and instances. The terms used in biological ontologies such as the Gene Ontology refer to types; experiments carried out by biologists in their labs refer to corresponding instances. Scientific theories are concerned, not with particular instances of things, but rather with universals or types. Data is gathered to
reflect the shared universal features of instances. Cells, cell nuclei, cell membranes and so on form types
that scientists refer to, not by virtue of this or that cell, but rather by virtue of the universal features
shared by cells observed in many different contexts.

### **4 Realizable Entity**


Functions, roles, dispositions and capabilities are associated with certain kinds of processes or activities in which they can be realized. For example:

  - a screwdriver’s function is realized in the actual process of turning a screw,

  - the function of the camera eye is realized when a picture is taken,

  - a person’s role as a stenographer is realized during the trial proceedings in a court room,

  - the Waterford crystal’s fragile disposition is realized as it smashes on the floor, and

  - the wooden door’s capability to expand is realized in the hot and humid months of summer.


**4**


_**Realizable Entities in Basic Formal Ontology**_


Functions, roles, dispositions and capabilities are _realizable entities_ in BFO. A _realizable entity_ is defined as a specifically dependent continuant that has an independent continuant entity as its bearer, and
whose instances can be realized (manifested, actualized, executed) in associated processes in which the
bearer participates.

Typically an instance of a realizable entity is realized throughout the course of its existence. However
it may exhibit periods of dormancy, when it exists by inhering in its bearer but is not manifested—as,
for example, in the case of diseases which are marked by periods of dormancy, or by many occupational
roles, which are not realized when the bearer is asleep. Some realizables, such as the function of a sperm
to penetrate an ovum, may be such that they can be manifested only once in their lifetime; or, as again in
the case of sperm, they may be such that they are realized only in very rare cases. Others, such as the
function of the heart to pump blood, are realized continuously.

The above implies an absolute distinction between being the bearer of a realizable entity, and exercising or realizing this entity in some activity or process, as in:

  - the person has the role of nurse, and exercises this role when administering a prescribed drug to a
patient in the hospital,

  - each atom of element A has the disposition to become an atom of element B in radioactive decay, and this disposition is realized when element B comes into existence from A, and

  - the ladle has the function of holding liquids, but may never exercise this function because it sits
packaged on the shelf of a stock room.

We are now in a position where we can define the three sub-types of realizable entities recognized by
BFO—role, disposition, function, and capability.

### **5 Role (Externally-Grounded Realizable Entity)**


A role is a realizable entity which exists because the bearer is in some special physical, social, or institutional set of circumstances in which the bearer does not have to be, and is not such that, if it ceases
to exist, then the physical make-up of the bearer is thereby changed. [19]


‘Role’ is another name for what we might call an _extrinsic_ or _externally-grounded_ realizable entity.
An entity is a role not because of the way it itself is, but because of something that happens or obtains
externally. Examples include:


    - the role of an instance of a chemical compound to serve as analyte in an experiment,

    - the role of a portion of penicillin to act as a drug,


    - the role of bacteria in causing infection, and

    - the role of a stone in marking a boundary.


Roles are optional. A person can lose the role of student without being physically changed. Because a
role is not a reflection of the in-built physical make-up of its bearer, there are therapeutic and prophylactic roles, and input and output roles. For example, the primary function—or input role—of mitochondria
is to produce adenosine triphosphate (ATP). [20] However, given that they produce high levels of oxidative
stress, these same mitochondria play an output role in Alzheimer’s disease. A heart has the function of


**5**


_**Realizable Entities in Basic Formal Ontology**_


pumping blood, but in certain circumstances that same heart can play the role of dinner for a lion or of
plasticized prop in a museum display. Water does not have any function _per se_, but it does play many
different roles, for example in helping to initiate the growth process of a seed, or in a hydroelectric experiment, or in washing clothes.


Many prominent types of role involve social ascription. A person can play the role of lawyer or of
surrogate to a patient, but it is not necessary that they be lawyers or surrogates.


There is also a distinction between _having_ a role and _playing_ a role. An entity can play a role, as
when a passenger plays the role of a pilot on a commercial plane in an emergency, or a pyramidal neuron plays the role occupied by a damaged stellar neuron in the brain; but neither the person nor the pyramidal neuron _have_ those roles. In contrast to ‘function’ (which we define shortly) the term ‘role’ designates a realizable entity whose manifestation brings about some result or end that is not typical of its
bearer in virtue of the latter’s physical make-up.


In the narrow sense that concerns us here, roles are specifically dependent instances. A role exists only when some independent continuant serves as its bearer. For example: Jane Doe’s present role as director of this institute, or Joe Brown’s role in that play being performed tonight on Broadway. The term
‘role’ can be used in a broader sense in contexts such as Jane is the seventh person to fill the role of director of our institute.

### **6 Disposition (Internally-Grounded Realizable Entity)**


It is common to find researchers making claims like:


  - an atom of element X has the disposition to decay to an atom of element Y,

  - the cell wall is disposed to filter chemicals in endocitosis and exocitosis,


  - certain people have a disposition to develop colon cancer, and

  - children are innately disposed to categorize objects in certain ways.


(1) A _disposition_ is a realizable entity which is such that, if it ceases to exist, then its bearer is physically changed, and whose realization occurs in virtue of the bearer’s physical make-up when this
bearer is in some special physical circumstances. [21]


Unlike roles, dispositions are not optional. If an entity is a certain way, then it has a certain disposition, and if it ceases to be that way, then it loses that disposition. A disposition is also known as an _in-_
_ternally-grounded_ realizable entity. That is, it is a realizable entity that is a reflection of the in-built or
acquired physical make-up of the independent continuant.


Dispositions exist along a strength continuum. Weaker forms of disposition are realized in only a
fraction of triggering cases. These forms occur in a significant number of entities of a similar type such
that there exists a statistical, concomitant correlation present between two entities, if they are in certain
circumstances. Examples of weaker forms of disposition include:


  - a hemophiliac’s disposition to bleed an abnormally large amount of blood,


**6**


_**Realizable Entities in Basic Formal Ontology**_


  - a person who smokes two packs of cigarettes a day throughout adulthood has the disposition to
die of a disease earlier than average, and


  - crime has the disposition to rise in heavily populated cities during the summer months.


Further, we are referring to weaker forms of disposition when we consider genetic and other risk factors for specific diseases.


By contrast, we can distinguish a stronger form of disposition, known as a sure-fire disposition,
which is generally executed as a rule. Examples of sure-fire disposition include:


  - the skin has the sure-fire disposition to be penetrated by a needle when a phlebotomist takes
blood,


  - a car windshield has a sure-fire disposition to break if it is struck with a sledgehammer moving at
100 feet per second, and


  - a cell has the sure-fire disposition to become diploid following mitosis,

  - a magnet has a sure-fire disposition to produce an electrical field.

### **7 Function**

A function is a disposition that exists in virtue of the bearer’s physical make-up, [22, 23 ] and this physical
make-up is something the bearer possesses because it came into being, either through evolution (in the
case of natural biological entities) or through intentional design (in the case of artifacts), in order to realize processes of a certain sort. Examples include:


  - the function of amylase in saliva to break down starch into sugar,


  - the function of a hammer to drive in nails, and

  - the function of a heart pacemaker to regulate the beating of a heart through electricity.


Functions are realized in processes called functionings. Each function has a bearer with a specific
type of physical make-up. This is something which, in the biological case, the bearer has naturally
evolved to have (as in a hypothalamus secreting hormones) and, in the artifact case, something which
the bearer has been constructed to have (as in an Erlenmeyer flask designed to hold liquid).


It is not accidental or arbitrary that a given eye has the function to see or that a given screwdriver has
been designed and constructed with the function of fastening screws. Rather, these functions are integral
to these entities in virtue of the fact that the latter have evolved, or been constructed, to have a corresponding physical make-up. Thus, for example, because of its physical make-up the heart’s function is
to pump blood and not merely to thump or produce sounds, which are by-products of the heart’s proper
functioning. [24]


Like disposition, a function is an internally-grounded realizable entity: it is such that if it ceases to exist, then its bearer is physically changed. A non-functioning lung or attic fan would indicate that the
physical make-up of these things had changed—in the case of the lung, possibly a cancerous lesion; in
the case of the attic fan, possibly a screw missing. These entities would still have their function, but they


**7**


_**Realizable Entities in Basic Formal Ontology**_


would not be capable of functioning until the physical change is rectified. The entities would lose their
function if they were changed drastically, for example by being permanentaly removed from the body,
in the case of the lung, or by being irreparably crushed in the case of the attic fan Thus, if a continuant
has a function, then it is built to exercise this function reliably on the basis of its physical make-up. But
again, a function need not in every case be exercised or manifested: its bearer may be broken, or it may
never be in the right kind of context, or provided with the right kind of input.

We can distinguish two varieties of function, artifactual function and biological function.

### **_8.1 Artifactual Function_**


An artifactual function is a function whose bearer’s physical make-up has been designed and made intentionally (typically by one or more human beings) to function in a certain way, and whose instances
are similarly designed and made intentionally, and do indeed reliably function in this way. [25] (Dipert,
1993; McLaughlin, 2001). Examples include:


  - the function of a pycnometer to hold liquid,

  - the function of a fan to circulate air, and


  - the function of a Bunsen burner to produce a flame.

### **_8.2 Biological Function_**


A biological function is a function whose bearer is part of an organism, and exists and has the physical
make-up it has because it has evolved that way and contributes to the organism’s realization of a life
plan appropriate to an organism of its type.


A biological function is a function whose bearer is part of an organism, and that bearer’s existence
and physical make-up is due to having evolved in a way that contributes to the organism’s fulfillment of
an appropriate life-plan. Examples include:


  - the function of a mitochondrion in the production of ATP, and

  - the function of the wax-producing mirror gland of the worker honey bee to produce beeswax.


Note that we do not define biological function in terms of giving rise to processes conducive to an organism’s survival. This is because the manifestations of biological functions are not in every case beneficial to the survival of the corresponding organism, as in organisms that die when they reproduce, such
as Arabis laevigata and Octopus lutens. Rather, functions are such that their realizations contribute to the
corresponding organism’s fulfillment of a life that is typical or characteristic for an organism of its kind.


Biological functions are, according to the proposed definition, attributed to parts of organisms and not
to whole organisms themselves; thus, your heart, liver, and other bodily organs have functions, but you
yourself do not. It is not appropriate to say that the queen bee and the worker bee have functions they
perform in the hive, despite that fact that they are genetically programmed to perform their specific
tasks. Rather, the queen and worker bees have roles they fulfill, and parts of their bodies have functions
which are performed in the maintenance of the hive. Support for this view is provided by the fact that


**8**


_**Realizable Entities in Basic Formal Ontology**_


the queen and worker bees can lose their roles when the hive is attacked, and can take on soldier bee
roles in defense of the hive, if necessary. [26]

The dichotomy between biological and artifactual function is reflected in the construction of two domain ontologies. Thus, the ontologies of artifactual and biological functions have already been proposed
as a complement to the Gene Ontology’s molecular function and biological process ontologies.

Taking account of what has been communicated thus far, from the point of view defended by BFO, we
should correctly state:

  - the (or a) function of the heart is to pump blood,

  - the role of the surrogate is to stand in for the patient,

  - blood has the disposition to coagulate, and

  - that patient has suicidal tendencies.\

### **8 Conclusion**


Given that numerous research groups are now utilizing BFO as an upper-level framework to assist in
the organization and integration of biomedical information, it is important to distinguish clearly between
the types of realizable entities that significantly feature in domain ontologies for the sciences. We hope
to have provided more detailed classification of terms that will assist scientific researchers as they develop high-quality domain ontologies.


**ACKNOWLEDGEMENTS**


We wish to thank Sivaram Arabandi, Werner Ceusters, Lindsay Cowell, Jennifer Fostel, Frank Gibson, Albert Goldfain, Pierre Grenon, Yongqun He, Leonard Jacuzzo, Ingvar Johansson, Philip Lord,
Chris Mungall, Alan Ruttenberg, Patrice Seyed, Andrew Spear, Chris Stoeckert, Neil Williams, and
Lowell Vizenor for helpful comments. This work is funded by the United States National Institutes of
Health (NIH) through the NIH Roadmap for Medical Research, National Center for Biomedical Ontologies (NCBO), Grant 1 U54 HG004028. Information on the National Centers for Biomedical Computing can be found at http://nihroadmap.nih. gov/bioinformatics.


**REFERENCES**


1 http://www.obofoundry.org/.

2 BioPAX, http://www.biopax.org/; also see BioPAX-OBO at http://neurocommons.org/page/BiopAX-OBO.

3 Science Commons, http://sciencecommons.org/.

4 Ontology Works, http://www.ontologyworks.com/.

5 National Cancer Institute, http://www.cancer.gov/.

6 Computer Task Group, http://www.ctg.com/.

7 Grenon, P. and Smith, B. (2004) SNAP and SPAN: Towards dynamic spatial ontology. _Spatial Cognition and_
_Computation_, **4**, 99–104.

8 Smith, B. and Grenon, P. (2004) The cornucopia of formal-ontological relations. Dialectica, 58, 279–296.

9 See Holger Stenzhorn (http://www.ifo mis.org/bfo).


**9**


_**Realizable Entities in Basic Formal Ontology**_


10 Ariew, A. and Perlman, M. (2002) Introduction. In A. Ariew, R. Cummins, and M. Perlman, eds., _Functions:_
_New Essays in the Philosophy of Psychology and Biology_, Oxford University Press, New York, 1–7.

11 Dipert, R. (1993) Artifacts, Art Works, and Agency. Temple University Press, Philadelphia.

12 Perlman, M. (2004) The modern philosophical resurrection of teleology. The Monist, 87, 3–51.

13 Shrager, J. (2003) The fiction of function. _Bioinformatics_, **19**, 1934- 1936; Churchland, P. (1995) _The Engine of_
_Reason, the Seat of the Soul: A Philosophical Journey into the Brain_ . MIT Press, Cambridge, MA.

14 http://www.geneontology.org/.

15 See Hamann, B. (2006) _Disease: Identification, Prevention, and Control_ . McGraw-Hill, New York; Boorse, C.
(1975) On the distinction between disease and illness. _Philosophy and Public Affairs_, **5**, 49–68.

16 WHO (N.D.) International Classification of Functions, Disabilities and Health (ICF) at:
http://www.who.int/classi-fications/icf/en/.

17 Zhou, M. and Ouyang, W. (2003) The function role of GATA-3 in Th1 and Th2 differentiation. Immunological
Research, 28, 25.

18 Hunter, L. (2009) The Processes of Life: An Introduction to Molecular Biology. MIT Press, Cambridge, MA.

19 http://www.ifomis.org/bfo.

20 Evans, T., Zhu, X., Lee, H., Previll, L., Webber, K., Casadesus, G., Perry, G., and Smith, M. (2006) Alzheimer’s disease: A deregulated cell cycle disease. In M. Sun, ed., Research Progress in Alzheimer’s Disease and
Dementia (pp. 109–122). Nova Publishers, New York.

21 Jansen, L. (2007) Tendencies and other realizables in medical information sciences. Available at:
http://ontology. buffalo.edu/ bfo/Tendencies.pdf.

22 Johansson, I., Smith, B., Munn, K., Tsikolia, N., Elsner, K., Ernst, D., and Siebert, D. (2005) Functional anatomy: A taxonomic proposal. Acta Biotheoretica, 53, 53–66.

23 Mizoguchi, R. and Kitamura, Y. (Forthcoming) A functional ontology of artifacts. _The Monist_ .

24 Millikan, R. (1984) Language, Thought, and Other Biological Categories. MIT Press, Cambridge, MA. Chapters 1 and 2.

25 McLaughlin, P. (2001) What Functions Explain: Functional Explanation and Self-Reproducing Systems. Cambridge University Press, Cambridge, UK. Chapter 3, 42–62.

26 Breed, M., Robinson, G., and Page, R. (2003) Division of labor during honey bee colony defense. Behavioral
Ecology and Sociobiology, 27, 395–401.


**10**


