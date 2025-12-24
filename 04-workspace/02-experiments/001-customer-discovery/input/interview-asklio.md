Meeting Title: Bene und Timo 
Date: Nov 27
Meeting participants: Timo Bunk

Transcript:
 
Them: Us the first.  
Me: Ähm okay, also es sind fünf Teile, die letzten zwei lassen wir jetzt einfach weg. Der erste Teil ist quasi einfach welchen Toolstack benutzt ihr und auf welchem Frameworks baut ihr die Agent und so weiter? Also langchain, lang lang et cetera. Also wie sieht euer Engineering Stack dazu aus?  
Them: Leng chain. OpenAI über Azure.  
Me: Okay. Observability? Macht ihr langfuse oder habt ihr da Tracing  
Them: Wir haben Lenk Smith für Observability.  
Me: Okay.  
Them: Genau.  
Me: Benutzte Evaluations? Und in was für Evaluations benutzt ihr? Ja.  
Them: Wir wir haben angefangen, so die erste jetzt mal rein zu basteln.  
Me: Okay.  
Them: Für son paar Key Prozesse.  
Me: Okay.  
Them: Aber da bin ich leider nicht tief genug drin. Also das kann ich dir nicht richtig beantworten. Und ich weiß auch nicht, ob ob das grade schon gut funktioniert, aber werden halt irgendwann genau diese diese Punkte so, wenn irgendwas angepasst. Und dann bricht's an irgend 'ner anderen Stelle und jeder ist so, hä, okay, warum?  
Me: Welcome to my life Genaues Problem hatten wir auch zweieinhalb Jahre.  
Them: Dann kommt's zu dem Punkt, wo Du dann sagst, ah, lass es lieber nicht anfassen. Das funktioniert eigentlich schon ganz gut.  
Me: Ok. Eu tenho os sprints mir meine ganzen Fragen. Das ist das beste Interview, was ich bisher hatte. Mit meinen ersten sieben Hypothesen hast Du mit drei Sätzen validiert. Wie guckt ihr eure Production Data an oder wie schaut ihr da rein in eure Production Data?  
Them: Was genau meinst Du damit?  
Me: Genau, also ich hab ja Kunden und die erzeugen ja quasi Traces, die chatten. Dann ihr habt ja nicht nur Chatbots, hab gesehen, sondern ihr habt ja auch quasi einfach Backgroundjobs mit LLMs und Agents.  
Them: Yeah.  
Me: Guckt ihr da rein in die Production Data? Wie geht ihr damit Macht ihr da so Post Use it Analysis quasi und so?  
Them: Yeah. We need some post talk. Und haben quasi Post hoc Events auf den Feldern.  
Me: Mhmm.  
Them: Und tracken, wenn Also das ist bei uns ganz praktisch, weil viele von den Also wir haben oft human in the loop,  
Me: Mhmm.  
Them: und wir tracken wenn die Menschen quasi Felder  
Me: Okay.  
Them: anders machen, als die KI das gemacht hat. Und das ist relativ praktisch für uns. Also am Anfang haben wir da super, super viel gelernt, weil da wir dann einfach all diese Cases angeschaut haben. Also wir haben die dann manuell angeschaut, wenn das  
Me: Yep. Yeah.  
Them: deine nächste Frage beantwortet. Und dann haben wir uns angeschaut, hey, okay, warum ist das so? Und manchmal ehrlich gesagt haben wir's auch nicht gecheckt. Das ist halt auch  
Me: Yeah.  
Them: Problem, weil wir dann auch so waren so, hey, hätten's genauso entschieden wie die KI.  
Me: Yeah.  
Them: Warum hat der Mensch das anders entschieden? Ja, dann sind wir irgendwann zu Punkt gekommen, wo das wahrscheinlich irgendwie so siebzig, achtzig Prozent der Fälle waren so, wo wir gesagt haben so, hä, nee, ich werd's auch so gemacht wie die KI, wir checken nicht, warum's anders ist oder selbst wenn wir's checken, dann würden wir's nicht checken, warum. Und dann haben wir's meistens so gelassen und nicht mehr angefasst, kurz.  
Me: Okay, verstehe. Dann warte mal kurz, was fehlt denn jetzt hier noch? Genau, wie sieht euer Optimization Flow aus? Das ist jetzt quasi Teil zwei, Du bist fast bisschen vorweggenommen. Wenn ihr Änderungen macht, habt ihr so Art ich hab jetzt rausgehört, ihr macht manual tuning son bisschen, ihr guckt euch das an und dann tankert ihr so, machen übrigens alle so, mit allen, denen ich bisher gesprochen hab.  
Them: Got it.  
Me: Enkel so wie wir selbst, ja. Wir haben jetzt erst angefangen, dass quasi mit Testdaten  
Them: Yeah.  
Me: setzen und so zu füttern. Wie geht ihr da vor? Macht ihr dann habt ihr eine Testdaten Test Data Bench, Test ihr die Prompts dann quasi auf eine Test Data oder sag einfach, wie ihr vorgeht, bei Optimisierung. Also ihr findet jetzt die root causes, oder denkt, ihr habt einen oder so. Wie geht ihr vor?  
Them: Nomara was a as a jetzt kommt quasi, mir meinen wir ja so,  
Me: Yep.  
Them: Ding. Ich sammel die einfach normalerweise. Wir sammeln die  
Me: Yeah. Mhmm.  
Them: also viel, also entweder wir machen sie über Post Talk, aber wir dann kommen wir irgendwann zu 'nem Punkt, wo uns Post Talk halt nicht mehr nicht mehr hilft und dann bekommen wir halt User Feedback. Und wir sammeln einfach alles User Feedback in in irgendwelchen Channels und dann  
Me: Mhmm.  
Them: wenn wir merken so, okay, dieses Feature hat grade viel User Feedback, dann schaut sich das irgendjemand an an und baut eine neue Version, entweder halt wirklich so inkrementell dann probieren wir's wirklich einfach aus. Also da haben wir irgendwie so hundert gesammelt, schmeißen die hundert dagegen, wenn's dann davon dann neunzig passen, dann passt. Und dann schauen wir's uns erst mal nicht mehr an. Wenn wir merken, dass wir halt irgendwie halt wirklich die verändern müssen,  
Me: Yep.  
Them: Dann bauen wir meistens eine neue Version mit 'nem Feature Flag. Und testen das dann quasi halt, testen das dann einfach a b Also und a b ist da auch wirklich sehr viel manual a b. Wir stellen das einfach live bei irgendwelchen Konten und schauen uns an, wie's  
Me: Okay. Crazy.  
Them: performt im Vergleich zu ändern kommt.  
Me: Okay, crazy. Also ihr macht das wirklich so sehr old school. Wie man früher quasi im Web Design das so gemacht hat. Okay. Also man spricht ja dafür, dass ihr eine gute Kundenbasis habt, dass ihr euch das traut.  
Them: Oder dass die Kunden viel geboren sind.  
Me: Ja. Okay. Kannst Du ungefähr sagen, wie viel Zeit er drauf verwendet? So verhältnismäßig fünfzig Prozent oder Stunden die Woche vom vom Team, wie viel geht da, wie viel Zeit geht da rein in dieses ganze Debugging, root cause analysis? Und so weiter und so fort. Von dir, vom Engineering Team, ist es die Hauptteil der Aufgabe eigentlich,  
Them: Name. Ich überleg grade quasi so für unsere so für unsere wichtigste Chain vielleicht so drei, vier Entwicklertage Monat. Genau und dann haben wir halt noch die ganzen anderen, aber da hab ich ehrlich gesagt keinen Plan. Weil passieren halt viel so nebenbei und grade bei neuen Features macht halt irgend Engineer, der es grade baut, macht halt irgendwann irgendwas. Also kann ich superschwer abschätzen.  
Me: Okay. Okay. Ja, müsst ich vielleicht noch mal mit den Engineering Team oder irgendjemand ausm Team dann da sprechen, aber ist okay. Der Der Ihr habt da so quasi ihr benutzt noch keine irgendwelche oder irgendwelche Tools, wo automatische Auswertungen fahrt und so weiter, wo ihr Reports bekommt. Okay.  
Them: Halt außer außer Length Smith, bei dem wir halt irgendwie mit dem halt irgendwie die Sachen Sachen relativ gut testen können. Das heißt, wenn wir halt irgendwie Testcases gesammelt haben, dann sehen wir zumindest, die jetzt passend zusammen mit irgendwie sonem alten random Dataset.  
Me: Okay.  
Them: Genau.  
Me: Okay. Das heißt, ihr erweitert euer eigentlich aus Production Data kontinuierlich.  
Them: Natürlich natürlich machen wir das nicht. Wer würde denn mit Production Data Test  
Me: Dann auch. Nein, also jetzt nicht auf Production System quasi, also nehmt quasi echte  
Them: Ja, ja. Jetzt  
Me: Also  
Them: Ja, ja. Genau, wir nehmen wir nehmen einfach die wir nehmen also das  
Me: anonymisiert und  
Them: genau, deswegen das muss auf jeden  
Me: Anonymisiert und quasi, genau.  
Them: Fall, Ja, ja. Genau, also wir arbeiten natürlich, wir arbeiten natürlich nie mit  
Me: So wie es gehört.  
Them: Produkte, Tiefdaten und würden damit auch nichts essen.  
Me: Yeah. Correct. As a ja, ist notiert. Ihr wenn produktiven Fälle auf der Produktion, die ihr gesehen habt und fügt  
Them: Anonymisiert, ne, voll  
Me: sie als Testcases hinzu.  
Them: Anonymisiert, ne, vollständig anonymisiert natürlich, DSGVO konform und so weiter.  
Me: Perfect. Okay. It's recorded. Cool. Habt ihr mal den Framework Switch gemacht in dieser ganzen Zeit? Ihr mal euch von 'nem Tooling verabschiedet oder weißt Du, das das  
Them: Ich glaub nicht, seitdem ich da bin, weiß ich aber nicht.  
Me: Okay, also ihr habt quasi, seitdem Du da bist, wart ihr auf Langchain, Lang Smith, Post  
Them: Ja, genau, also Ja, genau. Also wir sind jetzt mit diesem mit der offiziellen v eins  
Me: chain,  
Them: von Langchain auch auf die offizielle Langchain v eins und ich glaub, seitdem haben wir Langchain.  
Me: Okay, passt. Du hast vorher was gesagt, Du weißt nicht, nicht, ob's da noch geht oder degradatet und so. Wie viel wie läuft es bei euch mit dem Releaseprozess jetzt speziell von AI Agents und diesen Prompts? Also wenn ihr Prompts verändert, wie läuft das ab? Wie fühlt sich das an? Was ist und Du hast son bisschen angedeutet, kannst Du dazu noch paar Wörter verlieren, einerseits wie er's macht und zweitens, so subjektiv wie das Gefühl ist, finde ich, wie du dich dabei fühlst.  
Them: Ich glaub, am Anfang fühlt sich's fühlt sich's eigentlich immer gut an, weil am Anfang wird halt alles immer besser. Also es ist so  
Me: Inhit  
Them: ja, ich glaub, wenn Du irgendwas an der oder irgendwas an wird's halt immer besser. So lange, bis Du halt an Punkt kommst, wo es relativ gut ist. Und ich glaub, wir sind nicht bei gar nicht bei so vielen Punkten an sonem Punkt, wo ich wo ich denk so, boah, okay, das ist jetzt wirklich so gut, dass ich Angst hab, dass wir dass wenn wir da jetzt was ändern, dass das es dann dadurch schlechter wird. Hat außer bei außer vielleicht bei so zwei so Chains,  
Me: Is this  
Them: und da machen wir das so wie wie vorher gesagt, also wir bauen das als Feature Flag.  
Me: Mhmm.  
Them: Und dann kennen wir ja die Kunden die vielleicht also meistens entweder die Kunden, die halt Netze gutes Feedback geben oder die Kunden, die halt mit der alten Chain die größten Probleme hatten.  
Me: Yeah. Okay.  
Them: Stellen wir das einfach manchmal sagen wir denen so, hey, wir haben das bei euch umgestellt, könnt ihr könnt ihr drauf achten, wie wie es läuft. Manchmal  
Me: Okay.  
Them: sagen wir auch einfach so 'n neues  
Me: Okay.  
Them: Modell ist jetzt bisschen anders.  
Me: Also er geht auch aktiv mit Kommunikation gegen dieses undeterministische Verhalten vor, weil er nicht zu hundert Prozent wisst, wie sich das LLM mir ein neues LLM dann da verhält oder wenn sich das prompt anpasst, Also ihr ihr fangt viel auch über Kommunikation ab, wenn ich das jetzt richtig verstanden hab.  
Them: Genau, wir lassen manchmal manchmal lassen wir auch einfach die, das machen wir inzwischen nicht mehr so viel, weil wir zu viele Kunden haben. Am Anfang haben wir die Kunden auch einfach also mal die neue das neue Feature Flag an deren Testsystem enabled.  
Me: Mhmm.  
Them: Also dadurch, dass wir für so Enterprise Software machen, hat ja halt jeder bei uns auch Testsystem.  
Me: Okay.  
Them: Das heißt, wir können die auch immer im Test, also wir können im Testsystem testen, und die auch, das heißt quasi, also wir haben devstaging prod,  
Me: Yep.  
Them: und steht den beiden zur Verfügung.  
Me: Das heißt, ihr rollt auf denjenigen, ihr ihr deployt auch auf den hier Azure, das hab ich, glaub ich, gesehen, ja. Das heißt,  
Them: Nee, wir deployen auf unserem auf unserem Azure.  
Me: okay. Okay.  
Them: Genau, aber wir wir schippen die Sachen natürlich alle immer erst ins und durch die Feature Flex  
Me: Okay.  
Them: bei bei manchen Kunden aktivieren das halt ins Staging und sagen testet findet's selbst raus. Also viele wirklich viel Arbeit machen auch unsere Kunden. Im Testen.  
Me: Das ist super, dass ihr das Auto jetzt was habt. Okay. Dann habe ich eine Frage noch, was wär jetzt quasi dein größter Pain Point? This r, b, get agents go live faster. Also Oder maintain agents in production. Oder wie auch immer die Features, also quasi wie auch immer. Also AB oder C.  
Them: Das ist noch mal a, b und c Kannst Du noch mal a, b und c vorlesen?  
Me: Ja. Push to production with confidence. Get go live faster, also for neuen features, or maintain features in production or agents in production.  
Them: Ich hab c also und vor allem improve.  
Me: Okay. Yeah. Und wenn Du jetzt dir Tool wünschen könntest, was diesen Paint Point quasi Maintainen und Improven lösen würde, welche Features würdest Du dir wünschen aus PM Sicht und vielleicht dann 'n zweite Antwort aus, wenn Du dich in Engineer versetzt.  
Them: Ich glaub, das ich le les regelmäßig diese Post und denk mir so so, alter, dann macht das  
Me: Yep.  
Them: das grade jeder, sollten wir das nicht auch machen? Und hab aber, glaub ich, keinen so ich glaub, Du bekommst nur die PM Antwort. Ich hab, glaub ich, keinen so konkreten Plan, wie wie wir das wie wir das umsetzen, ne? Was vielleicht daran liegt, es bis jetzt noch nicht wichtig genug war. Also ich hab mich son paar Mal da reingelesen und dann war ich so, okay, okay. Wie wie setzen wir das auf? Aber ohne dass ich so war, so so setzt man, hier ist dein Tool, so setzt man das auf, so funktioniert das. Son bisschen so wie diese Post hoc Experience, wo Du dich so sagst, so, ich also  
Me: Yep.  
Them: aus Productsicht ist Post hoc so mein Tool.  
Me: Yeah.  
Them: Aber im Zweifelsfall bau ich einfach all die Postdoc Events selbst rein, wenn meine Engineers mich mich ignorieren und dann funktioniert das auch. Und das das finde ich halt zum Beispiel  
Me: Mhmm.  
Them: das find ich extrem geil an, geil an Post Talk. Und so stell ich mir das halt also so stell ich mir halt Tools vor. Ich denk mir so so ich als Product Manager irgendwie son bisschen Coding Experience,  
Me: Mhmm.  
Them: sollte dem Engineer erklären können, warum das sinnvoll ist und wie er das machen kann. Und ich versteh's selbst noch.  
Me: Okay.  
Them: Das wär, glaub ich, mein Anspruch.  
Me: Ich hab noch eine abschließende Sag, Entschuldigung, ich wollte ihn bitte überreichen.  
Them: Ja, Nee, für eine Frage, ich bin bin hab da nachher noch Zeit.  
Me: Die Habt ihr einen Nutzt ihr Cloud Code als Engineering Setup? Habt ihr quasi so Agente ausgerollt in der Org?  
Them: Wir nutzen Cursor und  
Me: Ja. Okay.  
Them: und Codecs, aber kein Cloud Code.  
Me: Ja, es ist ja egal, es ist selber. Aber okay. Meine Fragen wären damit durch. Das heißt, ich kann dir jetzt noch paar Antworten geben zu den Sachen, denen Du gesagt hast, weil ich hier auch in dem Das heißt, damit Du auch was hast von Termin,  
Them: Got you. Go.  
Me: ich stoppe Recording, weil ich möchte nicht quasi die Analyse jetzt mit meinen Themen dann quasi 