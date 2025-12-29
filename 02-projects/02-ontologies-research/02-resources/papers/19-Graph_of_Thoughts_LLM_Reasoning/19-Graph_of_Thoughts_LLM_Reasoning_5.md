<!-- Source: 19-Graph_of_Thoughts_LLM_Reasoning.pdf | Chunk 5/7 -->

Table 21: Keyword counting for an example 4-passage split (GoT4): **Step 1 (Prompt/Response)**


**Step 1 – Prompt:**


_<_ Instruction _>_ Split the following input text into 4 paragraphs of approximately same length.


Only output the final 4 paragraphs in the following format without any additional text or thoughts:


_{{_


"Paragraph 1": "Some paragraph text _. . ._ ",


"Paragraph 2": "Some paragraph text _. . ._ ",


"Paragraph 3": "Some paragraph text _. . ._ ",


"Paragraph 4": "Some paragraph text _. . ._ "


_}}_


_<_ /Instruction _>_


_<_ Example _>_ See Table 19 _<_ /Example _>_


Input: **My friend, Alex from Peru**, once recounted his journey to Argentina where he learned about the strong cultural ties
between Argentina and Brazil due to their shared history. He spoke fondly of his time in Argentina and Brazil, marveling at
the similar music, dance, and culinary traditions that seamlessly **bridged the borders of these countries. It reminded me**
**of a** documentary I’d watched about the ancient Silk Road that spanned across Iran and China. It touched upon the shared
historical narratives of Iran and China, highlighting how goods, ideas, and culture flowed between these two countries for
centuries. Intriguingly, the documentary also brought up some parallels between this eastern route and the vibrant exchange
between Italy and France during the Renaissance. The cultural and intellectual bonds between Italy and France were indeed
profound, just as the resilient trade relations that existed **between the United States and Canada. The United States**
**and Canada, apart** from their geographical proximity, shared an economic bond that strongly influenced their policies
and international standing. Similarly, the ties between Australia and New Zealand shed light on their gestalt identity in the
Pacific region. Despite their unique characteristics, Australia and New Zealand were often viewed as a single entity due to
their remarkably similar backgrounds in terms of culture, language, and colonial history. Inspired by these chronicles of
interconnectedness, I decided to delve deeper into history and found a fascinating account of how Ukraine and Poland had
influenced each other **through years of coexistence. Despite their tumultuous past**, Ukraine and Poland shared a cultural
tapestry that was deeply woven into their histories. It was quite similar to the complex relationship between North Korea
and South Korea, which, despite their political differences, shared common heritage and traditions. Thus, from Argentina to
South Korea, the world was an intricate web of countries intertwined with each other through shared histories, cultures, **and**
**sometimes, shared destinies.**


**Step 1 – Response (Fully Correct):**


_{{_


"Paragraph 1": "My friend, Alex from Peru ... (Omitted) ... bridged the borders of these countries.",


"Paragraph 2": "It reminded me of a ... (Omitted) ... between the United States and Canada.",


"Paragraph 3": "The United States and Canada, apart ... (Omitted) ... through years of coexistence.",


"Paragraph 4": "Despite their tumultuous past ... (Omitted) ... and sometimes, shared destinies."


_}}_


33


Table 22: Keyword counting for an example 4-passage split (GoT4): **Step 2a (Prompt/Responses)**


**Step 2a – Prompt:**


_<_ Instruction _>_ Count the frequency of how many times each country is explicitly named in the input text. You can generate
any intermedate lists and states, but the final output should only contain the frequency of each country that appears at least
once in the following json format, prefixed with ”Output: ” (make sure to keep the same spelling for each country in the
output as in the input text):


_{{_


"country1": frequency1,


"country2": frequency2,


_. . ._


_}}_


_<_ /Instruction _>_


_<_ Approach _>_


To count the frequency for each country follow these steps:


1. Split the input passage into four paragraphs of similar length.

2. Count the frequency of each country in each paragraph.

3. Combine the frequencies of each country from each paragraph by adding them together.


_<_ /Approach _>_


_<_ Examples _>_ See Table 18 _<_ /Examples _>_


Input: My friend, Alex from Peru, once recounted his journey to Argentina where he learned about the strong cultural ties
between Argentina and Brazil due to their shared history. He spoke fondly of his time in Argentina and Brazil, marveling at
the similar music, dance, and culinary traditions that seamlessly bridged the borders of these countries.


**Step 2a – 10 Responses:**


1. _{{_ "Peru": 1, "Argentina": 1, "Brazil": 1 _}}_ (3 Errors - Missing two ”Argentina” and one ”Brazil”)
2. _**{{**_ **"Peru": 1, "Argentina": 2, "Brazil": 2** _**}}**_ **(1 Error - Missing one ”Argentina”)**
3. _{{_ "Peru": 1, "Argentina": 2, "Brazil": 2 _}}_ (1 Error - Missing one ”Argentina”)
4. _{{_ "Peru": 1, "Argentina": 1, "Brazil": 1 _}}_ (3 Errors - Missing two ”Argentina” and one ”Brazil”)
5. _{{_ "Peru": 1, "Argentina": 2, "Brazil": 2 _}}_ (1 Error - Missing one ”Argentina”)
6. _{{_ "Peru": 1, "Argentina": 2, "Brazil": 2 _}}_ (1 Error - Missing one ”Argentina”)
7. _{{_ "Peru": 1, "Argentina": 1, "Brazil": 1 _}}_ (3 Errors - Missing two ”Argentina” and one ”Brazil”)
8. _{{_ "Peru": 1, "Argentina": 1, "Brazil": 1 _}}_ (3 Errors - Missing two ”Argentina” and one ”Brazil”)
9. _{{_ "Peru": 1, "Argentina": 1, "Brazil": 1 _}}_ (3 Errors - Missing two ”Argentina” and one ”Brazil”)
10. _{{_ "Peru": 1, "Argentina": 1, "Brazil": 1 _}}_ (3 Errors - Missing two ”Argentina” and one ”Brazil”)


34


Table 23: Keyword counting for an example 4-passage split (GoT4): **Step 2b (Prompt/Responses)**


**Step 2b – Prompt:**


_<_ Instruction _>_ Count the frequency of how many times each country is explicitly named in the input text. You can generate
any intermedate lists and states, but the final output should only contain the frequency of each country that appears at least
once in the following json format, prefixed with ”Output: ” (make sure to keep the same spelling for each country in the
output as in the input text):


_{{_


"country1": frequency1,


"country2": frequency2,


_. . ._


_}}_


_<_ /Instruction _>_


_<_ Approach _>_


To count the frequency for each country follow these steps:


1. Split the input passage into four paragraphs of similar length.

2. Count the frequency of each country in each paragraph.

3. Combine the frequencies of each country from each paragraph by adding them together.


_<_ /Approach _>_


_<_ Examples _>_ See Table 18 _<_ /Examples _>_


Input: It reminded me of a documentary I’d watched about the ancient Silk Road that spanned across Iran and China. It
touched upon the shared historical narratives of Iran and China, highlighting how goods, ideas, and culture flowed between
these two countries for centuries. Intriguingly, the documentary also brought up some parallels between this eastern route
and the vibrant exchange between Italy and France during the Renaissance. The cultural and intellectual bonds between Italy
and France were indeed profound, just as the resilient trade relations that existed between the United States and Canada.


**Step 2b – 10 Responses:**


1. _{{_ "Iran": 1, "China": 1, "Italy": 1, "France": 1, "United States": 1, "Canada": 1 _}}_

(4 Errors - Missing one ”Iran”, one ”China”, one ”Italy” and one ”France”)
2. _{{_ "Iran": 1, "China": 1, "Italy": 1, "France": 1, "United States": 1, "Canada": 1 _}}_

(4 Errors - Missing one ”Iran”, one ”China”, one ”Italy” and one ”France”)
3. _{{_ "Iran": 3, "China": 2, "Italy": 1, "France": 1, "United States": 1, "Canada": 1 _}}_

(3 Errors - Surplus of one ”Iran”, missing one ”Italy” and one ”France”)
4. _{{_ "Iran": 1, "China": 1, "Italy": 1, "France": 1, "United States": 1, "Canada": 1 _}}_

(4 Errors - Missing one ”Iran”, one ”China”, one ”Italy” and one ”France”)
5. _{{_ "Iran": 2, "China": 2, "Italy": 1, "France": 1, "United States": 1, "Canada": 1 _}}_

(2 Errors - Missing one ”Italy” and one ”France”)
6. _{{_ "Iran": 1, "China": 1, "Italy": 1, "France": 1, "United States": 1, "Canada": 1 _}}_

(4 Errors - Missing one ”Iran”, one ”China”, one ”Italy” and one ”France”)
7. _{{_ "Iran": 1, "China": 1, "Italy": 1, "France": 1, "United States": 1, "Canada": 1 _}}_

(4 Errors - Missing one ”Iran”, one ”China”, one ”Italy” and one ”France”)
8. _{{_ "Iran": 1, "China": 1, "Italy": 1, "France": 1, "United States": 1, "Canada": 1 _}}_

(4 Errors - Missing one ”Iran”, one ”China”, one ”Italy” and one ”France”)
9. _{{_ "Iran": 1, "China": 1, "Italy": 1, "France": 1, "United States": 1, "Canada": 1 _}}_

(4 Errors - Missing one ”Iran”, one ”China”, one ”Italy” and one ”France”)
10. _**{{**_ **"Iran": 2, "China": 2, "Italy": 1, "France": 2, "United States": 1, "Canada": 1** _**}}**_

**(1 Error - Missing one ”Italy”)**


35


Table 24: Keyword counting for an example 4-passage split (GoT4): **Step 2c (Prompt/Responses)**


**Step 2c – Prompt:**


_<_ Instruction _>_ Count the frequency of how many times each country is explicitly named in the input text. You can generate
any intermedate lists and states, but the final output should only contain the frequency of each country that appears at least
once in the following json format, prefixed with ”Output: ” (make sure to keep the same spelling for each country in the
output as in the input text):


_{{_


"country1": frequency1,


"country2": frequency2,


_. . ._


_}}_


_<_ /Instruction _>_


_<_ Approach _>_


To count the frequency for each country follow these steps:


1. Split the input passage into four paragraphs of similar length.

2. Count the frequency of each country in each paragraph.

3. Combine the frequencies of each country from each paragraph by adding them together.


_<_ /Approach _>_


_<_ Examples _>_ See Table 18 _<_ /Examples _>_


Input: The United States and Canada, apart from their geographical proximity, shared an economic bond that strongly
influenced their policies and international standing. Similarly, the ties between Australia and New Zealand shed light on
their gestalt identity in the Pacific region. Despite their unique characteristics, Australia and New Zealand were often viewed
as a single entity due to their remarkably similar backgrounds in terms of culture, language, and colonial history. Inspired
by these chronicles of interconnectedness, I decided to delve deeper into history and found a fascinating account of how
Ukraine and Poland had influenced each other through years of coexistence.


**Step 2c – 10 Responses:**


1. _**{{**_ **"United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 1, "Poland": 1** _**}}**_

**(Fully Correct)**
2. _{{_ "United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 1, "Poland": 1 _}}_

(Fully Correct)
3. _{{_ "United States": 1, "Canada": 1, "Australia": 1, "New Zealand": 1, "Australia and New Zealand":
1, "Ukraine": 1, "Poland": 1 _}}_
(3 Errors - Missing one ”Australia, one ”New Zealand” and surplus of one ”Australia and New Zealand”)
4. _{{_ "United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 1, "Poland": 1 _}}_

(Fully Correct)
5. _{{_ "United States": 1, "Canada": 1, "Australia": 1, "New Zealand": 1, "Australia and New Zealand":
1, "Ukraine": 1, "Poland": 1 _}}_
(3 Errors - Missing one ”Australia, one ”New Zealand” and surplus of one ”Australia and New Zealand”)
6. _{{_ "United States": 1, "Canada": 1, "Australia": 1, "New Zealand": 1, "Ukraine": 1, "Poland": 1 _}}_

(2 Errors - Missing one ”Australia” and one ”New Zealand”)
7. _{{_ "United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 1, "Poland": 1 _}}_

(Fully Correct)
8. _{{_ "United States": 1, "Canada": 1, "Australia": 1, "New Zealand": 1, "Ukraine": 1, "Poland": 1 _}}_

(2 Errors - Missing one ”Australia” and one ”New Zealand”)
9. _{{_ "United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 1, "Poland": 1 _}}_

(Fully Correct)
10. _{{_ "United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 1, "Poland": 1 _}}_

(Fully Correct)


36


Table 25: Keyword counting for an example 4-passage split (GoT4): **Step 2d (Prompt/Responses)**


**Step 2d – Prompt:**


_<_ Instruction _>_ Count the frequency of how many times each country is explicitly named in the input text. You can generate
any intermedate lists and states, but the final output should only contain the frequency of each country that appears at least
once in the following json format, prefixed with ”Output: ” (make sure to keep the same spelling for each country in the
output as in the input text):


_{{_


"country1": frequency1,


"country2": frequency2,


_. . ._


_}}_


_<_ /Instruction _>_


_<_ Approach _>_


To count the frequency for each country follow these steps:


1. Split the input passage into four paragraphs of similar length.

2. Count the frequency of each country in each paragraph.

3. Combine the frequencies of each country from each paragraph by adding them together.

_<_ /Approach _>_


_<_ Examples _>_ See Table 18 _<_ /Examples _>_


Input: Despite their tumultuous past, Ukraine and Poland shared a cultural tapestry that was deeply woven into their histories. It was quite similar to the complex relationship between North Korea and South Korea, which, despite their political
differences, shared common heritage and traditions. Thus, from Argentina to South Korea, the world was an intricate web of
countries intertwined with each other through shared histories, cultures, and sometimes, shared destinies.


**Step 2d – 10 Responses:**


1. _**{{**_ **"Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1** _**}}**_ **(Fully Correct)**
2. _{{_ "Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Fully Correct)
3. _{{_ "Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Fully Correct)
4. _{{_ "Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Fully Correct)
5. _{{_ "Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Fully Correct)
6. _{{_ "Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Fully Correct)
7. _{{_ "Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Fully Correct)
8. _{{_ "Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Fully Correct)
9. _{{_ "Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Fully Correct)
10. _{{_ "Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Fully Correct)


37


Table 26: Keyword counting for an example 4-passage split (GoT4): **Step 3a (Prompt/Responses)**


**Step 3a – Prompt:**


_<_ Instruction _>_ Combine the following 2 dictionaries, each containing the frequency of countries in a text, into a single
dictionary. Simply add the frequencies together for each country and if a country is not present in one of the dictionaries,
add it to the final dictionary with the frequency from the other dictionary.


Only output the final merged dictionary without any additional text or thoughts! _<_ /Instruction _>_


_<_ Approach _>_


To combine the 2 dictionaries into single one, follow these steps:


1. Create a new dictionary to store the combined frequencies.

2. Iterate through the keys of the first dictionary and add the frequency of each country to the new dictionary.

3. Iterate through the keys of the second dictionary and add the frequency of each country to the new dictionary and if it is
already present, add the frequency to the existing value.


_<_ /Approach _>_


Combine the following 2 dictionaries into a single dictionary:


_{{_ "Peru": 1, "Argentina": 2, "Brazil": 2 _}}_


_{{_ "Iran": 2, "China": 2, "Italy": 1, "France": 2, "United States": 1, "Canada": 1 _}}_


Combined Output:


**Step 3a – 3 Responses:**

1. _**{{**_ **"Peru": 1, "Argentina": 2, "Brazil": 2, "Iran": 2, "China": 2, "Italy": 1, "France": 2, "United**
**States": 1, "Canada": 1** _**}}**_ **(Valid - No Improvement) (2 Errors - from counting)**
2. _{{_ "Peru": 1, "Argentina": 2, "Brazil": 2, "Iran": 2, "China": 2, "Italy": 1, "France": 2, "United
States": 1, "Canada": 1 _}}_ (Valid - No Improvement) (2 Errors - from counting)
3. _{{_ "Peru": 1, "Argentina": 2, "Brazil": 2, "Iran": 2, "China": 2, "Italy": 1, "France": 2, "United
States": 1, "Canada": 1 _}}_ (Valid - No Improvement) (2 Errors - from counting)


38


Table 27: Keyword counting for an example 4-passage split (GoT4): **Step 3b (Prompt/Responses)**


**Step 3b – Prompt:**


_<_ Instruction _>_ Combine the following 2 dictionaries, each containing the frequency of countries in a text, into a single
dictionary. Simply add the frequencies together for each country and if a country is not present in one of the dictionaries,
add it to the final dictionary with the frequency from the other dictionary.


Only output the final merged dictionary without any additional text or thoughts! _<_ /Instruction _>_


_<_ Approach _>_


To combine the 2 dictionaries into single one, follow these steps:


1. Create a new dictionary to store the combined frequencies.

2. Iterate through the keys of the first dictionary and add the frequency of each country to the new dictionary.

3. Iterate through the keys of the second dictionary and add the frequency of each country to the new dictionary and if it is
already present, add the frequency to the existing value.


_<_ /Approach _>_


Combine the following 2 dictionaries into a single dictionary:


_{{_ "United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 1, "Poland": 1 _}}_


_{{_ "Ukraine": 1, "Poland": 1, "North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_


Combined Output:


**Step 3b – 3 Responses:**

1. _**{{**_ **"United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 2, "Poland": 2,**
**"North Korea": 1, "South Korea": 2, "Argentina": 1** _**}}**_ **(Valid - No Improvement) (Fully Correct)**
2. _{{_ "United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 2, "Poland": 2,
"North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Valid - No Improvement) (Fully Correct)
3. _{{_ "United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 2, "Poland": 2,
"North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_ (Valid - No Improvement) (Fully Correct)


39


Table 28: Keyword counting for an example 4-passage split (GoT4): **Step 3c (Prompt/Responses)**


**Step 3c – Prompt:**


_<_ Instruction _>_ Combine the following 2 dictionaries, each containing the frequency of countries in a text, into a single
dictionary. Simply add the frequencies together for each country and if a country is not present in one of the dictionaries,
add it to the final dictionary with the frequency from the other dictionary.


Only output the final merged dictionary without any additional text or thoughts! _<_ /Instruction _>_


_<_ Approach _>_


To combine the 2 dictionaries into single one, follow these steps:


1. Create a new dictionary to store the combined frequencies.

2. Iterate through the keys of the first dictionary and add the frequency of each country to the new dictionary.

3. Iterate through the keys of the second dictionary and add the frequency of each country to the new dictionary and if it is
already present, add the frequency to the existing value.


_<_ /Approach _>_


Combine the following 2 dictionaries into a single dictionary:


_{{_ "Peru": 1, "Argentina": 2, "Brazil": 2, "Iran": 2, "China": 2, "Italy": 1, "France": 2, "United
States": 1, "Canada": 1 _}}_


_{{_ "United States": 1, "Canada": 1, "Australia": 2, "New Zealand": 2, "Ukraine": 2, "Poland": 2,
"North Korea": 1, "South Korea": 2, "Argentina": 1 _}}_


Combined Output:


**Step 3c – 3 Responses:**

1. _**{{**_ **"Peru": 1, "Argentina": 3, "Brazil": 2, "Iran": 2, "China": 2, "Italy": 1, "France": 2, "United**
**States": 2, "Canada": 2, "Australia": 2, "New Zealand": 2, "Ukraine": 2, "Poland": 2, "North**
**Korea": 1, "South Korea": 2** _**}}**_ **(Valid - No Improvement) (2 Errors - from counting)**
2. _{{_ "Peru": 1, "Argentina": 3, "Brazil": 2, "Iran": 2, "China": 2, "Italy": 1, "France": 2, "United
States": 2, "Canada": 2, "Australia": 2, "New Zealand": 2, "Ukraine": 2, "Poland": 2, "North
Korea": 1, "South Korea": 2 _}}_ (Valid - No Improvement) (2 Errors - from counting)
3. _{{_ "Peru": 1, "Argentina": 3, "Brazil": 2, "Iran": 2, "China": 2, "Italy": 1, "France": 2, "United
States": 2, "Canada": 2, "Australia": 2, "New Zealand": 2, "Ukraine": 2, "Poland": 2, "North
Korea": 1, "South Korea": 2 _}}_ (Valid - No Improvement) (2 Errors - from counting)


**Final Result (2 Errors):**


_{{_ "Peru": 1, "Argentina": 3, "Brazil": 2, "Iran": 2, "China": 2, "Italy": 1, "France": 2, "United
States": 2, "Canada": 2, "Australia": 2, "New Zealand": 2, "Ukraine": 2, "Poland": 2, "North Korea":
1, "South Korea": 2 _}}_


40


**E** **Example Prompts - Document Merging**

We present the prompts only for GoT of the document merging task, as GoT2 only differs in the fact that it merges the
4 NDAs in 2 steps rather than 1. For document merging, we
employ four distinct types of operations that interact with the
LLM, each with its corresponding prompts. First, there is the
**Generate** operation, utilizing the _merge_ ~~_p_~~ _rompt_ to instruct
the LLM to merge the 4 NDAs into 1. Second, the **Score**
operations instructs the LLM to score a given merged NDA
using the _score_ _prompt_ . Next, the **Aggregate** operation employs the _aggregate_ ~~_p_~~ _rompt_ to instruct the LLM to aggregate
multiple merge attempts into a single, better one. Finally, the
**Improve** operation leverages the _improve_ _prompt_ to instruct
the LLM to improve a merged NDA.
First, we present the prompt stubs (Table 29 - Table 30),
serving as templates to dynamically generate appropriate
prompts at runtime. Following this, we outline the LLM interactions throughout a complete merging process (Table 31

- Table 49). However, instead of displaying each input/generated NDA in every prompt/response, we present the 4 input NDAs in Table 31 - Table 33 and the final merged NDA
in Table 49. Furthermore, as scoring is done using the LLM
as well, we will present these interactions for the best performing merged NDAs (Tables 39 - 40 and Tables 47 - 48).
Lastly, most responses are limited to a few lines only, as
they don’t offer any further insights and would otherwise
span multiple pages. However, we refer the interested reader
to the results in the corresponding code repository [2] for full
logs and further examples.


2https://github.com/spcl/graph-of-thoughts



41


Table 29: Prompt stubs for the document merging task; parameters in single curly brackets will be substituted at runtime.


**merge** ~~**p**~~ **rompt:** Merge the following 4 NDA documents _<_ Doc1 _>_ - _<_ Doc4 _>_ into a single NDA, maximizing retained
information and minimizing redundancy. Output only the created NDA between the tags _<_ Merged _>_ and _<_ /Merged _>_,
without any additional text.


Here are NDAs _<_ Doc1 _>_ - _<_ Doc4 _>_ :


_<_ Doc1 _> {_ doc1 _} <_ /Doc1 _>_


_<_ Doc2 _> {_ doc2 _} <_ /Doc2 _>_


_<_ Doc3 _> {_ doc3 _} <_ /Doc3 _>_


_<_ Doc4 _> {_ doc4 _} <_ /Doc4 _>_


**score** ~~**p**~~ **rompt:** The following NDA _<_ S _>_ merges NDAs _<_ Doc1 _>_ - _<_ Doc4 _>_ .


Please score the merged NDA _<_ S _>_ in terms of how much redundant information is contained, independent of the original
NDAs, as well as how much information is retained from the original NDAs.


A score of 10 for redundancy implies that absolutely no information is redundant, while a score of 0 implies that at least half
of the information is redundant (so everything is at least mentioned twice).


A score of 10 for retained information implies that all information from the original NDAs is retained, while a score of 0
implies that no information is retained.


You may provide reasoning for your scoring, but the final score for redundancy should be between the tags _<_ Redundancy _>_
and _<_ /Redundancy _>_, and the final score for retained information should be between the tags _<_ Retained _>_ and _<_ /Retained _>_,
without any additional text within any of those tags.


Here are NDAs _<_ Doc1 _>_ - _<_ Doc4 _>_ :


_<_ Doc1 _> {_ doc1 _} <_ /Doc1 _>_


_<_ Doc2 _> {_ doc2 _} <_ /Doc2 _>_


_<_ Doc3 _> {_ doc3 _} <_ /Doc3 _>_


_<_ Doc4 _> {_ doc4 _} <_ /Doc4 _>_


Here is the merged NDA _<_ S _>_ :


_<_ S _> {_ s _} <_ /S _>_


**aggregate** ~~**p**~~ **rompt:** The following NDAs _<_ S1 _>_ - _<_ S _{_ num ~~n~~ das ~~s~~ ummaries _}>_ each merge the initial NDAs _<_ Doc1 _>_ _<_ Doc4 _>_ .


Combine the merged NDAs _<_ S1 _>_ - _<_ S _{_ num ~~n~~ das ~~s~~ ummaries _}>_ into a new one, maximizing their advantages and overall
information retention, while minimizing redundancy.


Output only the new NDA between the tags _<_ Merged _>_ and _<_ /Merged _>_, without any additional text.


Here are the original NDAs _<_ Doc1 _>_ - _<_ Doc4 _>_ :


_<_ Doc1 _> {_ doc1 _} <_ /Doc1 _>_


_<_ Doc2 _> {_ doc2 _} <_ /Doc2 _>_


_<_ Doc3 _> {_ doc3 _} <_ /Doc3 _>_


_<_ Doc4 _> {_ doc4 _} <_ /Doc4 _>_


Here are the merged NDAs _<_ S1 _>_ - _<_ S _{_ num ~~n~~ das ~~s~~ ummaries _}>_ :


_<_ S1 _> {_ s1 _} <_ /S1 _>_


_. . ._


_<_ S _{_ num ~~n~~ das ~~s~~ ummaries _}> {_ s _{_ num ~~n~~ das ~~s~~ ummaries _}} <_ /S _{_ num ~~n~~ das ~~s~~ ummaries _}>_


42


Table 30: Prompt stubs for the document merging task _continued_ ; parameters in single curly brackets will be substituted at
runtime.


**improve** ~~**p**~~ **rompt:** The following NDA _<_ S _>_ merges initial NDAs _<_ Doc1 _>_ - _<_ Doc4 _>_ .


Please improve the merged NDA _<_ S _>_ by adding more information and removing redundancy. Output only the improved
NDA, placed between the tags _<_ Merged _>_ and _<_ /Merged _>_, without any additional text.


Here are NDAs _<_ Doc1 _>_ - _<_ Doc4 _>_ :


_<_ Doc1 _> {_ doc1 _} <_ /Doc1 _>_


_<_ Doc2 _> {_ doc2 _} <_ /Doc2 _>_


_<_ Doc3 _> {_ doc3 _} <_ /Doc3 _>_


_<_ Doc4 _> {_ doc4 _} <_ /Doc4 _>_


Here is the merged NDA _<_ S _>_ :


_<_ S _> {_ s _} <_ /S _>_


43


Table 31: Input NDA 1 and 2


_<_ Doc1 _>_


NON-DISCLOSURE AGREEMENT (NDA)


1. Agreement between [Your Company Name] and [Recipient Name] on [Date].

2. Information sharing for the purpose of [specific project or purpose].

3. ”Confidential Information” includes all potentially commercially valuable information, specifically software development
tactics, processes, and in-house research results.

4. Receiving party is obligated to protect the Confidential Information, use it solely for the disclosed purpose, and not
disclose it without consent.

5. Breach penalties include injunctive relief, other remedies, and a $200,000 fee per breach.

6. The Agreement applies to the Parties and their successors and assigns. It contains all related agreements and lack of
enforcement doesn’t imply waiver.

7. The Agreement is under the laws of [State].

8. Signed by [Your Company Name] and [Recipient Name] at the above date.


_<_ /Doc1 _>_


_<_ Doc2 _>_


NON-DISCLOSURE AGREEMENT (NDA)


Effective from [Effective Date], this NDA involves [Your Company Name] (”Disclosing Party”), and [Recipient Name]
(”Receiving Party”).


1. Purpose: The Disclosing Party will disclose confidential information related to [Topic of Research] to the Receiving Party
for [Purpose].

2. Confidential Information: Defined as all non-public reports, data, designs, and other materials provided by the Disclosing
Party to the Receiving Party.

3. Receiving Party’s Obligations:


a. Use, reproduce, or distribute the confidential information only for the agreed purpose.
b. Restrict access to the information to necessary parties, ensuring they abide by strict confidentiality.
c. Return or destroy all confidential information upon request or at the end of the agreement.


4. Exclusions: Information will not be classified as confidential if it is already known to the Receiving Party, publicly known,
or independently developed by the Receiving Party.

5. Non-Competition: The Receiving Party will not engage in any competing business against the Disclosing Party during
the agreement and one year after its termination.

6. Term and Termination: The agreement is valid for [e.g., ”two years”], unless terminated earlier with [e.g., ”30 days”]
written notice. The Receiving Party’s non-disclosure and non-competition obligations persist post-termination.

7. General Provisions:


a. Governing Law: [Your State]’s laws apply.
b. Amendments: Only valid if written and signed by both parties.
c. Entire Agreement: This contract overrules previous related agreements.


Signed as of the Effective Date by [Your Company Name] - Disclosing Party [Recipient Name] - Receiving Party.


_<_ /Doc2 _>_


44


Table 32: Input NDA 3


_<_ Doc3 _>_


CONFIDENTIALITY & NON-DISCLOSURE AGREEMENT


Entities Involved:


Effective [Date], between [AquaBlue Innovations], established in [State], and [PineTree Solutions], a registered entity.


Objective:


To safeguard classified data during talks of a potential technological alliance.


Specification of Protected Information:


Particularly:


a. System designs and architectural schematics.

b. Proprietary computational algorithms.


Receiver’s Obligations:


a. Maintain strict non-disclosure using best practices.

b. Employ solely for the aforementioned aim.

c. No unveiling without explicit authorization.


Violation Ramifications:


A charge of $280,000 for every infringement, plus possible legal proceedings.


General Terms:


Binding for both parties and any successors. This encapsulates the entire accord.


Legal Reference:


Governed as per [State]’s legal framework.


Attestation:


Duly signed on [Date].

[AquaBlue Innovations] [PineTree Solutions]


_<_ /Doc3 _>_


45


Table 33: Input NDA 4


_<_ Doc4 _>_


SECRECY & DISCLOSURE AGREEMENT


Contracting Parties:


Dated [Date], drawn between [AquaBlue Innovations], a [State]-based corporation, and [PineTree Solutions], a licensed
organization.


Aim:


To protect exclusive insights amidst dialogues for a technological partnership.


Categorization of Sensitive Data:


Includes:


a. Internal software blueprints.

b. Intellectual property awaiting patents.


Commitments of Recipient:


a. Uphold confidentiality, ensuring data integrity.

b. Utilize strictly for collaborative ventures.

c. No exposure without prior consensus.


Repercussions for Non-Compliance:


$295,000 fine for each transgression, and the option for legal recourse.


Overall Provisions:


Legally enforceable for signatories and successors. Complete and sole agreement.


Juridical Standpoint:


Under the auspices of [State] laws.


Ratification:


Confirmed and endorsed on [Date].

[AquaBlue Innovations] [PineTree Solutions]


_<_ /Doc4 _>_


Table 34: Merging 4 example NDAs: Execution plan ( **GoO** )


**GoO:**

