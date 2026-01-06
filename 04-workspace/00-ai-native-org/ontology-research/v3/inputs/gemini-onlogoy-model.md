Unified Digital Work Ontology (UDWO): Ein Paradigmenwechsel in der Prozessarchitektur – Validierung der 8-Entitäten-Hypothese und Synthese des MVO-Metamodells
Executive Summary
Der vorliegende Forschungsbericht „Unified Digital Work Ontology (UDWO)“ stellt eine umfassende Analyse des Status quo und der Zukunft der digitalen Prozessautomatisierung dar, basierend auf dem Forschungsstand der Jahre 2024 und 2025. In einer Zeit, in der generative künstliche Intelligenz (GenAI) von der experimentellen Phase in die operative Skalierung übergeht, stoßen traditionelle, rein imperative Prozessmodelle (wie BPMN) an ihre ontologischen Grenzen. Die Komplexität moderner Arbeitssysteme, charakterisiert durch autonome Agenten, unstrukturierte Datenströme und dynamische Entscheidungswege, erfordert eine radikale Neukonzeption der zugrunde liegenden Metamodelle.
Ziel dieser Untersuchung ist die Validierung der 8-Entitäten-Hypothese, die postuliert, dass sich jede Form digitaler Arbeit in die fundamentalen atomaren Einheiten Goal, Task, Rule, Resource, Role, Data, Event und Agent zerlegen lässt. Darauf aufbauend wird das Model-View-Ontology (MVO) Metamodell synthetisiert – ein Architekturansatz, der die starre Kopplung von Prozesslogik und Datenhaltung überwindet. Das MVO-Modell integriert deklarative Logik für flexible KI-Steuerung, KI-Agenten als autonome Akteure und Object-Centric Process Mining (OCPM) als empirische Feedback-Schleife.
Die Analyse stützt sich auf eine breite Basis aktueller Forschung, darunter die Spezifikationen der „Triple Crown“ des Business Process Management (BPMN, CMMN, DMN), die neu etablierte Shared Data Model and Notation (SDMN), den OCEL 2.0-Standard für objektzentrierte Ereignislogs sowie Architekturen moderner Multi-Agenten-Systeme wie AgentPro.
1. Einleitung: Die ontologische Krise des klassischen Prozessmanagements
1.1 Vom imperativen Diktat zur deklarativen Autonomie
Über Jahrzehnte hinweg folgte das Business Process Management (BPM) einem imperativen Paradigma: Der Prozessdesigner wusste im Voraus genau, welche Schritte in welcher Reihenfolge auszuführen waren. Standards wie die Business Process Model and Notation (BPMN) wurden entwickelt, um diese deterministischen Pfade ("Happy Paths") zu visualisieren und zu exekutieren.1 Diese Herangehensweise, die ihre Wurzeln in der industriellen Fließbandfertigung hat, erweist sich jedoch in der modernen Wissensarbeit und insbesondere im Kontext autonomer KI-Systeme zunehmend als insuffizient.
Die Forschung der Jahre 2024 und 2025 verdeutlicht eine fundamentale Verschiebung. Imperative Modelle sind starr; sie scheitern an der Variabilität und Unvorhersehbarkeit komplexer Szenarien ("Knowledge Work"). Hier setzen deklarative Ansätze an, wie sie in der Declarative Process Intermediate Language (DPIL) oder Declare-Modellen zu finden sind.3 Anstatt den Weg vorzuschreiben ("Tue erst A, dann B"), definieren deklarative Modelle den Lösungsraum durch Constraints ("B darf nicht vor A passieren") und Ziele. Dies korrespondiert direkt mit der Arbeitsweise moderner Large Language Models (LLMs), die nicht stur Skripten folgen, sondern auf Basis von Kontext ("Reasoning") und Zielen ("Goals") dynamisch Handlungspläne generieren.5
1.2 Die Fragmentierung der Arbeitsmodelle
Ein weiteres Kernproblem der aktuellen Landschaft ist die Fragmentierung der Ontologien. Ein "Auftrag" in einem BPMN-Diagramm ist semantisch oft nicht deckungsgleich mit dem "Auftrag" in einer DMN-Entscheidungstabelle (Decision Model and Notation) oder einem CMMN-Fall (Case Management Model and Notation). Dies führt zu Datensilos und Inkonsistenzen, die eine durchgängige Automatisierung behindern.
Erst mit der Einführung der Shared Data Model and Notation (SDMN), die 2024 als Beta-Spezifikation an Reife gewann, wurde ein Mechanismus geschaffen, um Datenstrukturen notationübergreifend zu standardisieren.1 SDMN erlaubt es, DataItems und ItemDefinitions zentral zu definieren und in BPMN, CMMN und DMN konsistent wiederzuverwenden.8
1.3 Zielsetzung und Struktur des Berichts
Dieser Bericht zielt darauf ab, diese disparaten Entwicklungen – deklarative KI-Steuerung, SDMN-Datenintegration und objektzentriertes Mining – in der Unified Digital Work Ontology (UDWO) zu vereinen.
Der Bericht gliedert sich wie folgt:
Kapitel 2 analysiert die Synergien der BPM+-Standards (BPMN, CMMN, DMN) unter dem Einflus von SDMN.
Kapitel 3 untersucht den Paradigmenwechsel zum Object-Centric Process Mining (OCPM) und OCEL 2.0 als Datengrundlage.
Kapitel 4 validiert die 8-Entitäten-Hypothese durch Abgleich mit Enterprise-Frameworks (Microsoft Graph, SAP BOR).
Kapitel 5 synthetisiert das MVO-Metamodell und beschreibt die Integration von KI-Agenten.
Kapitel 6 beleuchtet Mechanismen der Selbstreparatur und Evolution von Prozessmodellen.
2. Literaturrecherche und Modellanalyse: Die Evolution der BPM+ Familie
Die sogenannte "Triple Crown" der Modellierungsstandards – BPMN, CMMN und DMN – bildet das theoretische Rückgrat der UDWO. Die Literaturanalyse 2024/2025 zeigt jedoch, dass diese Standards nicht isoliert, sondern als integriertes Ökosystem betrachtet werden müssen, um KI-Fähigkeiten zu unterstützen.
2.1 BPMN 2.0: Die Orchestrierungsschicht
BPMN bleibt der de-facto Standard für vorhersagbare, repetitive Abläufe. Die Forschung hebt jedoch hervor, dass BPMN in einer KI-getriebenen Welt zunehmend zur reinen "View" (Sicht) oder zum Container für Agenten-Interaktionen wird, anstatt die gesamte Logik zu enthalten.
Lanes und Rollen: BPMN definiert Verantwortlichkeiten visuell durch Lanes. In der UDWO wird dies auf die Entität Role abstrahiert, die dynamisch von Menschen oder Agents besetzt werden kann.9
Tasks als Integrationspunkte: BPMN-Tasks (Service Tasks, User Tasks) sind die Schnittstellen, an denen Arbeit verrichtet wird. Die UDWO erweitert dieses Konzept, indem sie Tasks nicht nur als Schritte im Fluss, sondern als instanziierbare Objekte betrachtet, die von Agenten generiert werden können.10
2.2 CMMN 1.1: Das Framework für Agentic Workflows
Case Management Model and Notation (CMMN) erfährt durch den Aufstieg von KI-Agenten eine Renaissance. CMMN ist darauf ausgelegt, unstrukturierte Prozesse zu modellieren, die stark von Wissen und Kontext abhängen – genau das Terrain, auf dem LLM-basierte Agenten operieren.
Discretionary Items (Ermessensaufgaben): Ein Schlüsselelement von CMMN sind Discretionary Items. Dies sind Aufgaben, die im Modell definiert sind, aber nur bei Bedarf zur Laufzeit aktiviert werden.11
Synergie: Dies ist der perfekte Anknüpfungspunkt für KI-Agenten. Ein Agent kann den Kontext (Case File) analysieren und entscheiden, welche Discretionary Items (z.B. "Zusätzliche Bonitätsprüfung") aktiviert werden müssen. CMMN liefert somit die Struktur für die Autonomie der KI ("Human-in-the-loop" oder "Agent-in-the-loop").13
Plan Model und Stages: CMMN strukturiert den Fall in Phasen (Stages), ohne den genauen Weg vorzuschreiben. Dies korrespondiert mit den Planungsalgorithmen (z.B. Chain-of-Thought) von LLMs, die Teilziele (Milestones) definieren.14
2.3 DMN 1.3: Deterministische Logik in einer probabilistischen Welt
Während LLMs ("Soft Logic") hervorragend im Verstehen von Kontext sind, neigen sie zu Halluzinationen bei exakten Berechnungen oder Regelbefolgung. Decision Model and Notation (DMN) bietet hier die notwendige "Hard Logic".
Decision Services: DMN kapselt Geschäftsregeln in wiederverwendbare Services. In der UDWO fungiert DMN als "Guardrail" (Leitplanke) für Agenten. Ein Agent mag den Prozess steuern, aber wenn er entscheiden muss, ob ein Kredit gewährt wird, ruft er einen DMN-Service auf, um eine deterministische, auditierbare Entscheidung zu erhalten.2
Integration: Die Trennung von Entscheidung (DMN) und Prozess (BPMN/CMMN) ist essenziell für die Agilität. Regeln können geändert werden, ohne den Prozessfluss neu zu deployen.
2.4 SDMN: Der ontologische "Klebstoff"
Die Shared Data Model and Notation (SDMN) ist die kritischste Komponente für die UDWO. Sie ermöglicht es, die Datenobjekte, die in BPMN, CMMN und DMN verwendet werden, semantisch eindeutig zu definieren.
DataItem und ItemDefinition: SDMN führt diese Konstrukte ein, um Datenstrukturen zu modellieren. Ein DataItem in SDMN kann von einem BPMN DataObject, einem CMMN CaseFileItem und einem DMN InputData Element referenziert werden.7
Cross-Model Consistency: Wenn sich die Definition eines "Kunden" in SDMN ändert (z.B. neues Attribut "Risikoklasse"), propagiert diese Änderung automatisch in alle verbundenen Modelle. Dies verhindert die klassische Diskrepanz zwischen Prozessmodell und Realität.1
Tabelle 1: Synergien der BPM+ Standards in der UDWO
Standard
Primäre Rolle in UDWO
UDWO Entität Mapping
Beitrag zur Agenten-Integration
BPMN
Orchestrierung deterministischer Teilprozesse
Task, Event, Role
Visualisierung von Agenten-Handlungen ("View"); Definition von festen Routinen.
CMMN
Rahmenwerk für adaptive Fallbearbeitung
Goal (Milestone), Task (Discretionary)
Bietet den "Sandkasten" (Case Plan), in dem Agenten dynamisch Aufgaben (Discretionary Items) wählen können.
DMN
Deterministische Entscheidungslogik
Rule
Fungiert als "Tool" für Agenten zur sicheren Entscheidungsfindung (Vermeidung von Halluzinationen).
SDMN
Semantische Datendefinition
Data (Schema)
Stellt sicher, dass Agenten, Regeln und Prozesse über dieselben Datenobjekte sprechen.

3. Datenbasis der Ontologie: Object-Centricity und OCEL 2.0
Um eine Unified Digital Work Ontology zu schaffen, müssen wir uns von der "Case-Centric"-Sichtweise (ein Prozess = ein Fall ID) lösen, die das traditionelle Process Mining dominierte. Die Realität ist ein Netzwerk interagierender Objekte.
3.1 Object-Centric Process Mining (OCPM)
OCPM repräsentiert einen Paradigmenwechsel. Anstatt Ereignisse einem einzigen Fall zuzuordnen (z.B. einer Bestellnummer), erlaubt OCPM die Zuordnung von Ereignissen zu mehreren Objekten unterschiedlicher Typen (z.B. Bestellung, Kunde, Artikel, Lieferung).16
Konvergenz und Divergenz: OCPM löst das Problem, dass Prozesse oft zusammenlaufen (mehrere Bestellungen in einer Lieferung) oder sich aufspalten. Dies spiegelt die reale Komplexität von Wertschöpfungsketten wider, die durch die UDWO abgebildet werden soll.
3.2 OCEL 2.0: Der Standard für dynamische Objektzustände
Der 2024 finalisierte OCEL 2.0 Standard (Object-Centric Event Log) liefert das technische Fundament für die Datenspeicherung der UDWO.
E2O und O2O Beziehungen: OCEL 2.0 definiert explizit Event-to-Object (E2O) und Object-to-Object (O2O) Beziehungen. Dies ermöglicht es, den Kontext eines Events vollständig zu erfassen.17
Beispiel: Ein Event "Paket verpackt" hat E2O-Beziehungen zu den Objekten "Paket" und "Artikel". Gleichzeitig existiert eine O2O-Beziehung zwischen "Paket" und "Lieferauftrag".
Dynamische Attribute: Ein entscheidendes Feature von OCEL 2.0 ist die Fähigkeit, Änderungen von Objektattributen über die Zeit zu tracken.17 Ein Objekt ist nicht statisch; sein Zustand (z.B. "Rechnungsstatus") ändert sich durch Events. Dies ermöglicht es der UDWO, den State (Zustand) des Systems zu jedem Zeitpunkt exakt zu rekonstruieren.
Technische Implementierung: OCEL 2.0 bietet Implementierungen in XML, JSON und SQLite. Insbesondere die relationale SQLite-Implementierung mit typunabhängigen Tabellen (event_object, object_object) bietet eine performante Basis für die Instanziierung der UDWO in realen Systemen.17
4. Validierung der 8-Entitäten-Hypothese
Die Kernhypothese der UDWO besagt, dass sich digitale Arbeit vollständig durch acht atomare Entitäten beschreiben lässt. Diese Hypothese wird nun durch Abgleich mit etablierten Enterprise-Architecture-Frameworks (wie Zachman, TOGAF), modernen APIs (Microsoft Graph) und den BPM+-Standards validiert.
4.1 Entity 1: Goal (Ziel)
Definition: Der angestrebte Endzustand oder das Ergebnis ("Why").
Validierung:
Agentic AI: In Frameworks wie AgentPro ist das Goal der initiale Input für den Agenten. Das System nutzt Techniken wie Monte Carlo Tree Search (MCTS), um Pfade zu simulieren, die zum Ziel führen.18 Ohne explizites Goal ist autonomes Handeln unmöglich.
CMMN: Repräsentiert durch Milestones und ExitCriteria.11
Zachman: Korrespondiert mit der "Motivation"-Spalte (Ends/Means).
4.2 Entity 2: Task (Aufgabe)
Definition: Eine atomare Handlungseinheit ("What").
Validierung:
Microsoft Graph: Die API definiert explizit TaskDefinition und PrintTaskDefinition als zentrale Ressourcen für Arbeitsmanagement.19
BPMN/CMMN: Task (BPMN) und PlanItem (CMMN) sind die zentralen Ausführungselemente.
Jira: Issue Types (Task, Sub-task) bilden die operative Ebene ab.21
Insight: In der UDWO ist ein Task eine Instanz einer Handlungsanweisung, die dynamisch generiert werden kann.
4.3 Entity 3: Rule (Regel)
Definition: Logik, die Ausführung und Entscheidungen steuert ("How/Control").
Validierung:
SQL/Datenbanken: Constraints (Unique, Check) sind fundamentale Regeln zur Datenintegrität.22
DMN: Decision Tables formalisieren Geschäftsregeln.15
Declarative Mining: Constraints wie response oder co-existence in Declare/DPIL definieren temporale Regeln.24
4.4 Entity 4: Resource (Ressource)
Definition: Das Mittel zur Ausführung ("With What").
Validierung:
SAP BOR: Das Business Object Repository unterscheidet technische Objekte und Ressourcen.25
BPMN: Ressourcendefinitionen für Simulationen.
Unterscheidung: Eine Ressource ist passiv (Werkzeug, Server, Geld).
4.5 Entity 5: Role (Rolle)
Definition: Die Berechtigung und Verantwortlichkeit ("Who").
Validierung:
Microsoft Graph: AppRole und Delegated Permissions trennen die Identität (User) von der Rolle (Admin, Reader).26
BPMN: Swimlanes repräsentieren Rollen, nicht spezifische Personen.9
4.6 Entity 6: Data (Daten/Artefakt)
Definition: Das Objekt, das bearbeitet wird ("What").
Validierung:
SDMN: ItemDefinition ist der Beweis für die Notwendigkeit einer eigenen Daten-Entität.7
OCEL 2.0: Object als zentraler Ankerpunkt für Events.16
4.7 Entity 7: Event (Ereignis)
Definition: Ein Zustandswechsel in der Zeit ("When").
Validierung:
OCPM: Events sind die atomaren Beobachtungen der Realität.
EDA (Event-Driven Architecture): Events triggern Agenten und Prozesse.
4.8 Entity 8: Agent (Agent/Akteur)
Definition: Ein autonomer Akteur, der Goals verfolgt ("Who - Active").
Validierung (Neu): Dies ist die Erweiterung der klassischen Modelle.
Abgrenzung: Ein Agent ist mehr als eine Resource (da er autonom entscheidet) und mehr als eine Role (da er eine konkrete Instanz ist, z.B. "GPT-4-Turbo Instance #3").
Forschung: "Agentic Workflow Patterns" 27 und Frameworks wie "AgentPro" 18 zeigen, dass Agenten eine eigene ontologische Klasse benötigen, die Attribute wie "Memory", "Tools" und "Planning Strategy" besitzt.
5. Synthese des Neuen Metamodells: MVO (Model-View-Ontology)
Das MVO-Metamodell (Model-View-Ontology) ist die architektonische Antwort auf die Anforderungen der UDWO. Es entkoppelt die Datenhaltung (Ontology) von der Steuerungslogik (Model) und der Benutzerinteraktion (View), inspiriert durch das MVC-Pattern der Softwareentwicklung, jedoch adaptiert für autonome Prozesslandschaften.
5.1 Ontology (O): The Semantic Ground Truth
Die Ontologie-Schicht ist das persistente Gedächtnis des Unternehmens. Sie ist ein Knowledge Graph, der auf den Standards OCEL 2.0 (für Instanzdaten) und SDMN (für Schemata) basiert.
Inhalt: Hier leben die Instanzen aller 8 Entitäten. Ein konkreter "Kundenauftrag #123" (Data) ist verknüpft mit den Events seiner Bearbeitung, den ausgeführten Tasks und den beteiligten Agenten.
Technologie: Graph-Datenbanken (z.B. Neo4j) oder RDF-Stores, die OCEL-Daten importieren können.
Funktion: Sie liefert den Kontext für KI-Agenten. Wenn ein Agent fragt "Wie ist der Status von Auftrag #123?", queryt er die Ontologie (RAG - Retrieval Augmented Generation).28
5.2 Model (M): The Agentic Execution Engine
Das "Modell" ist in der UDWO nicht mehr ein statisches Diagramm, sondern eine dynamische Execution Engine, die deklarativ gesteuert wird.
Deklarativer Kern: Anstatt imperativer Pfade definiert das Modell Goals (Ziele) und Rules (Constraints).
Agentic Planning: Ein Orchestrator-Agent (basierend auf LLMs) empfängt ein Goal und den aktuellen State aus der Ontologie. Er nutzt Planungsmethoden (z.B. ReAct - Reason & Act), um zur Laufzeit die notwendigen Tasks zu generieren.27
Synergie mit CMMN: Der Agent agiert innerhalb eines virtuellen CMMN-Plans, wobei er Discretionary Items auswählt.
Validierung durch DMN: Bevor der Agent einen kritischen Task ausführt, konsultiert er DMN-Services (Rules), um die Compliance sicherzustellen.
5.3 View (V): Context-Specific Projections
Da die zugrunde liegende Ontologie und die dynamischen Agenten-Pfade hochkomplex sind, benötigen menschliche Nutzer vereinfachte Sichten.
Generative Views: Die Views werden generiert, nicht fest modelliert.
Management View (BPMN): Ein Algorithmus projiziert die geplanten oder ausgeführten Tasks in ein BPMN-Diagramm, um den Ablauf verständlich zu machen ("On-the-fly Process Mining").
Case Worker View (CMMN): Ein Sachbearbeiter sieht eine klassische Fallakte mit Aufgabenlisten.
Conversational View: Ein Endanwender chattet mit dem System ("Wo ist mein Paket?"), und das System generiert eine natürlichsprachliche Antwort aus den Events der Ontologie.24
Abbildung: Architektur des MVO-Metamodells
User Input (Event/Goal) -> Triggert Model (Agent).
Agent -> Liest State aus Ontology (Data/Rule).
Agent -> Plant & Führt aus (Task via Resource).
Ontology -> Speichert Resultat als Event (OCEL).
View Generator -> Aktualisiert BPMN/UI für den User.
6. Integration von KI-Agenten, Deklarativer Logik und Selbstreparatur
Das MVO-Modell entfaltet sein volles Potenzial erst durch die tiefe Integration von KI-Mechanismen, die über einfache Textgenerierung hinausgehen.
6.1 Das "AgentPro" Pattern und Process Supervision
Wie integriert man unzuverlässige LLMs in kritische Geschäftsprozesse? Die Forschung zu AgentPro 18 liefert die Blaupause für die UDWO.
Architektur: AgentPro nutzt einen LLM-Agenten für die Generierung von Schritten und ein separates Process Reward Model (PRM) zur Überwachung.
Anwendung in UDWO: Der Agent schlägt einen Task vor (z.B. "Sende E-Mail an Kunden"). Das PRM (welches Zugriff auf die Rules der Ontologie hat, z.B. DMN-Regeln oder Declare-Constraints) bewertet diesen Schritt. Verletzt der Schritt eine Regel (z.B. "Keine E-Mail ohne vorheriges Approval"), wird er abgelehnt (Rejection Sampling). Dies implementiert eine "Process Supervision", die Fehler frühzeitig in der Reasoning-Kette abfängt.
6.2 Deklarative Logik als Sprache der Agenten
Damit Agenten und PRMs effektiv kommunizieren können, bedarf es einer formalen Sprache. Hier kommen deklarative Modelle wie Declare oder DPIL ins Spiel.
Übersetzung: LLMs sind in der Lage, natürlichsprachliche Anforderungen ("Vier-Augen-Prinzip bei Auszahlungen") in formale Declare-Constraints (co-existence(approval, payout)) zu übersetzen.24
Nutzung: Diese generierten Constraints werden als Rules in der Ontologie gespeichert und vom PRM zur Laufzeit gegen den Plan des Agenten geprüft.
6.3 Self-Evolving Ontologies und Repair
Ein revolutionärer Aspekt der UDWO ist die Fähigkeit zur Selbstreparatur (Self-Repair).
Problem: Geschäftsprozesse driften oft von der Realität ab (Concept Drift), z.B. wenn sich externe APIs ändern oder neue Kundenanforderungen entstehen.30
Lösung:
Detection: OCPM-Algorithmen überwachen den Strom der OCEL-Events in der Ontologie. Sie erkennen Abweichungen zwischen dem erwarteten Verhalten (Model) und dem tatsächlichen Verhalten (Events).
Diagnosis & Repair: Ein spezialisierter "Ontology Engineer Agent" (wie im Ontogenix-Ansatz beschrieben 32) analysiert die Abweichung. Er nutzt RAG (Retrieval Augmented Generation), um externe Dokumentation (z.B. API-Updates) zu konsultieren.
Evolution: Der Agent schlägt eine Anpassung der Tasks (z.B. neues Mapping) oder der Rules vor. Nach Bestätigung durch einen Menschen ("Human-in-the-Loop") wird die Ontologie aktualisiert.
7. Fazit und Ausblick
Die Validierung der 8-Entitäten-Hypothese und die Synthese des MVO-Metamodells markieren einen Wendepunkt im Verständnis digitaler Arbeit. Die Konvergenz von SDMN (Datenstruktur), OCPM/OCEL 2.0 (Dateninstanz/Events) und Agentic AI (Steuerung) ermöglicht Systeme, die nicht mehr nur automatisiert, sondern autonom und adaptiv sind.
BPMN, CMMN und DMN sterben nicht aus; sie transformieren sich. BPMN wird zur Visualisierungssprache (View), CMMN zum Strukturgeber für Agentenräume und DMN zum Sicherheitsanker (Rule). Die UDWO liefert den gemeinsamen semantischen Boden, auf dem diese Standards synergetisch zusammenwirken können.
Für Unternehmen bedeutet die Implementierung einer UDWO-basierten Architektur (z.B. durch Nutzung von Microsoft Graph als rudimentäre Ontologie und darauf aufsetzenden Agenten-Frameworks), dass sie die "technischen Schulden" starrer Prozessmodelle abbauen und eine Organisation schaffen können, die sich organisch an neue Marktanforderungen anpasst – getrieben durch die Symbiose von menschlicher Intention (Goal) und maschineller Ausführung (Agent).
Tabellenanhang
Tabelle 2: Mapping der 8 Entitäten auf Technologien und Standards
UDWO Entität
Definition (Semantik)
BPM+ Standard (OMG)
Implementierung (Tech)
Agentic Rolle
Goal
Angestrebter Endzustand
CMMN Milestone / ExitCrit
Prompt / Objective Function
Initiiert Planning (ReAct)
Task
Atomare Handlung
BPMN Task / CMMN PlanItem
MS Graph TaskDefinition
Output des Planning-Steps
Rule
Einschränkung/Logik
DMN Decision / Declare
SQL Constraints / DMN Engine
Guardrail / Reward Model
Resource
Passives Werkzeug
BPMN Resource
SAP BOR / APIs
Tool (via Function Calling)
Role
Berechtigung/Funktion
BPMN Lane / CMMN Role
MS Graph AppRole
Identität des Agenten
Data
Informationsobjekt
SDMN ItemDefinition
OCEL 2.0 Object
Input für Reasoning (RAG)
Event
Zustandswechsel
BPMN Event
OCEL 2.0 Event
Trigger / Memory
Agent
Autonomer Akteur
(neu) / CMMN Worker
LLM (GPT/Llama)
Orchestrator / Entscheider

Tabelle 3: Imperative vs. Deklarative/Agentische Modellierung (MVO)
Merkmal
Imperativ (BPMN "Old School")
MVO (UDWO & Agentic)
Kontrollfluss
Fest verdrahtet (Pfeile)
Emergent (durch Goals & Rules)
Datenhaltung
Prozessvariablen (flüchtig)
Objektzentriert (Ontologie/OCEL)
Flexibilität
Design-Time (Deployment nötig)
Run-Time (sofortige Adaption)
Fehlerbehandlung
Ausnahmebehandlung (Exception)
Re-Planning / Self-Repair
Rolle der KI
Task-Abarbeitung (Service)
Prozesssteuerung (Agent)

Referenzen
Exploring Shared Data Model and Notation (SDMN) and Its Role in BPM+ | BPMInstitute.org, Zugriff am Dezember 27, 2025, https://www.bpminstitute.org/resources/articles/exploring-shared-data-model-and-notation-sdmn-and-its-role-in-bpm/
Understanding the “Why”, not just the “How”, of the BPMN-CMMN-DMN Triple Crown, Zugriff am Dezember 27, 2025, https://www.trisotech.com/understanding-the-why-not-just-the-how-of-the-bpmn-cmmn-dmn-triple-crown/
PADL 2024 - : The 26th International Symposium on Practical Aspects of Declarative Languages, Zugriff am Dezember 27, 2025, https://popl24.sigplan.org/home/PADL-2024
The Declarative Process Intermediate Language (DPIL) - Chair for Databases and Information Systems, Zugriff am Dezember 27, 2025, https://www.ai4.uni-bayreuth.de/en/research/Former-Projects/akkordeon2/akkordeon.html
LLM Agents Explained: Complete Guide in 2025 - Dynamiq, Zugriff am Dezember 27, 2025, https://www.getdynamiq.ai/post/llm-agents-explained-complete-guide-in-2025
How LLM Reasoning and Planning Stop Pattern Matching Failures - Galileo AI, Zugriff am Dezember 27, 2025, https://galileo.ai/blog/llm-reasoning-planning
Shared Data Model and Notation (SDMN) - Object Management Group (OMG), Zugriff am Dezember 27, 2025, https://www.omg.org/spec/SDMN/1.0/Beta2/PDF
About the Shared Data Model and Notation Specification Version 1.0 beta 2, Zugriff am Dezember 27, 2025, https://www.omg.org/spec/SDMN/1.0/Beta2/About-SDMN
Ultimate guide to BPMN in Jira - Flower BPM, Zugriff am Dezember 27, 2025, https://flower-bpm.com/blog/ultimate-guide-to-bpmn-in-jira
CMMN Patterns Made Easily with BPMN - Camunda, Zugriff am Dezember 27, 2025, https://camunda.com/blog/2023/07/cmmn-patterns-bpmn/
CMMN 1.1 · Flowable Open Source Documentation, Zugriff am Dezember 27, 2025, https://www.flowable.com/open-source/docs/cmmn/ch06-cmmn
Case Management Model and Notation (CMMN) - Sparx Systems, Zugriff am Dezember 27, 2025, https://sparxsystems.com/resources/user-guides/15.2/model-domains/cmmn-models.pdf
CMMN as an Agentic Framework : A New Paradigm for Adaptive Case Management | by Pratik Pandya | Medium, Zugriff am Dezember 27, 2025, https://medium.com/@pratikhp82/cmmn-as-an-agentic-framework-a-new-paradigm-for-adaptive-case-management-79ad0ee875e8
CMMN Example - Claims File Case - Visual Paradigm, Zugriff am Dezember 27, 2025, https://www.visual-paradigm.com/guide/cmmn/cmmn-example/
Program - Decision Intelligence Technologies – DecisionCamp.org - WordPress.com, Zugriff am Dezember 27, 2025, https://decisioncamp2025.wordpress.com/program/
Object-Centric Process Mining - Emergent Mind, Zugriff am Dezember 27, 2025, https://www.emergentmind.com/topics/object-centric-process-mining
OCEL (Object-Centric Event Log) 2.0 Specification, Zugriff am Dezember 27, 2025, https://arxiv.org/abs/2403.01975
AgentPro: Enhancing LLM Agents with Automated ... - ACL Anthology, Zugriff am Dezember 27, 2025, https://aclanthology.org/2025.emnlp-main.506.pdf
Get taskDefinition - Microsoft Graph v1.0, Zugriff am Dezember 27, 2025, https://learn.microsoft.com/en-us/graph/api/printtaskdefinition-get?view=graph-rest-1.0
Get taskDefinition - Microsoft Graph v1.0, Zugriff am Dezember 27, 2025, https://learn.microsoft.com/en-us/graph/api/identitygovernance-taskdefinition-get?view=graph-rest-1.0
Configure the work type hierarchy - Atlassian Support, Zugriff am Dezember 27, 2025, https://support.atlassian.com/jira-cloud-administration/docs/configure-the-issue-type-hierarchy/
Unique constraints and check constraints - SQL Server - Microsoft Learn, Zugriff am Dezember 27, 2025, https://learn.microsoft.com/en-us/sql/relational-databases/tables/unique-constraints-and-check-constraints?view=sql-server-ver17
constraints | dbt Developer Hub, Zugriff am Dezember 27, 2025, https://docs.getdbt.com/reference/resource-properties/constraints
Are Large Language Models Fluent in Declarative Process ... - IJCAI, Zugriff am Dezember 27, 2025, https://www.ijcai.org/proceedings/2025/0501.pdf
The Business Object Repository - SAP Help Portal, Zugriff am Dezember 27, 2025, https://help.sap.com/docs/SAP_NETWEAVER_700/1096de9d6c53101485e28e694337daa3/4d5b2781e5e91c86e10000000a42189b.html
Microsoft Graph permissions reference, Zugriff am Dezember 27, 2025, https://learn.microsoft.com/en-us/graph/permissions-reference
7 Patterns for Building Better AI Agents Using BPMN in Camunda - YouTube, Zugriff am Dezember 27, 2025, https://www.youtube.com/watch?v=-TU2v6CooQ0
Patterns for Building LLM-based Systems & Products - Eugene Yan, Zugriff am Dezember 27, 2025, https://eugeneyan.com/writing/llm-patterns/
Architectural Pattern for LLM integration and adoption | by Supriya Vasudevan | Medium, Zugriff am Dezember 27, 2025, https://medium.com/@supriyadevan54/architectural-pattern-for-llm-integration-and-adoption-79642e12bbbe
A Comprehensive Drift-Adaptive Framework for Sustaining Model Performance in COVID-19 Detection From Dynamic Cough Audio Data - NIH, Zugriff am Dezember 27, 2025, https://pmc.ncbi.nlm.nih.gov/articles/PMC12174887/
A Comprehensive Drift-Adaptive Framework for Sustaining Model Performance in COVID-19 Detection From Dynamic Cough Audio Data: Model Development and Validation - Journal of Medical Internet Research, Zugriff am Dezember 27, 2025, https://www.jmir.org/2025/1/e66919
OntoGenix: LLM-Powered Ontology Engineering with Self-Repairing Multi-Agent Systems, Zugriff am Dezember 27, 2025, https://medium.com/@mikel1982mail/ontogenix-llm-powered-ontology-engineering-with-self-repairing-multi-agent-systems-c8c0e8d9a254
