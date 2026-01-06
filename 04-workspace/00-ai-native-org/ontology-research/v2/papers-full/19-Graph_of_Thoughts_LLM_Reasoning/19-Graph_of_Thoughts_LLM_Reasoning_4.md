<!-- Source: 19-Graph_of_Thoughts_LLM_Reasoning.pdf | Chunk 4/7 -->


_<_ Instruction _>_ Sort the following list of numbers in ascending order. Output only the sorted list of numbers, no additional
text. _<_ /Instruction _>_


_<_ Examples _>_ See Table 4 _<_ /Examples _>_


Input: [0, 5, 6, 7, 1, 4, 5, 9, 4, 6, 2, 5, 8, 6, 2, 6]


**Step 2b – 5 Responses:**


1. [0, 1, 2, 2, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9] (1 Error - Missing one 6)

2. [0, 1, 2, 2, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9] (1 Error - Missing one 6)

3. [0, 1, 2, 2, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9] (1 Error - Missing one 6)
4. **[0, 1, 2, 2, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 8, 9] (Fully Correct)**

5. [0, 1, 2, 2, 4, 4, 5, 5, 5, 6, 6, 6, 7, 8, 9] (1 Error - Missing one 6)


19


Table 8: Sorting of a 32 element list: **Step 3 (Prompt/Responses)**


**Step 3 – Prompt:**


_<_ Instruction _>_ Merge the following 2 sorted lists of length 16 each, into one sorted list of length 32 using a merge sort style
approach. Only output the final merged list without any additional text or thoughts!: _<_ /Instruction _>_


_<_ Approach _>_


To merge the two lists in a merge-sort style approach, follow these steps:


1. Compare the first element of both lists.

2. Append the smaller element to the merged list and move to the next element in the list from which the smaller element
came.

3. Repeat steps 1 and 2 until one of the lists is empty.

4. Append the remaining elements of the non-empty list to the merged list.


_<_ /Approach _>_


Merge the following two lists into one sorted list:


1. [0, 0, 1, 1, 1, 1, 1, 1, 2, 3, 3, 4, 5, 7, 8, 9]

2. [0, 1, 2, 2, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 8, 9]


Merged list:


**Step 3 – 10 Responses:**


1. [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 9, 9]

(2 Errors - Missing one 1 and one 5)

2. [0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 9, 9]

(2 Errors - Missing two 1s)

3. [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 8, 8, 9, 9]

(2 Errors - Missing one 1 and got one extra 6)

4. [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 8, 8, 9]

(3 Errors - Missing one 1, one 9 and got one extra 6)

5. [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 8, 8, 9, 9]

(2 Errors - Missing one 1 and got one extra 6)

6. [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 9, 9]

(2 Errors - Missing one 1 and one 5)

7. [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 8, 8, 9, 9]

(2 Errors - Missing one 1 and got one extra 6)

8. **[0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 9, 9]**

**(1 Error - Missing one 1)**

9. [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 9, 9]

(1 Error - Missing one 1)

10. [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 9, 9]

(2 Errors - Missing one 1 and one 5)


20


Table 9: Sorting of a 32 element list: **Step 4 (Prompt/Responses)**


**Step 4 – Prompt:**


_<_ Instruction _>_ The following two lists represent an unsorted list of numbers and a sorted variant of that list. The sorted
variant is not correct. Fix the sorted variant so that it is correct. Make sure that the output list is sorted in ascending order,
has the same number of elements as the input list (32), and contains the same elements as the input list. _<_ /Instruction _>_


_<_ Approach _>_


To fix the incorrectly sorted list follow these steps:


1. For each number from 0 to 9, compare the frequency of that number in the incorrectly sorted list to the frequency of that
number in the input list.

2. Iterate through the incorrectly sorted list and add or remove numbers as needed to make the frequency of each number in
the incorrectly sorted list match the frequency of that number in the input list.


_<_ /Approach _>_


_<_ Examples _>_ See Table 4 _<_ /Examples _>_


Input: [8, 7, 1, 1, 1, 1, 3, 3, 0, 9, 4, 1, 0, 2, 5, 1, 0, 5, 6, 7, 1, 4, 5, 9, 4, 6, 2, 5, 8, 6, 2, 6]


Incorrectly Sorted: [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 8,
8, 9, 9]


**Step 4 – 10 Responses:**


1. Reason: The incorrectly sorted list is missing two 0s, one 3, one 4, one 6 and one
9. The incorrectly sorted list also contains one extra 1, one extra 2, and one extra 5.
Output: [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 5, 5,
6, 6, 6, 6, 7, 7, 8, 8, 9, 9] 4 Errors   - Missing one 1, two 4s and one 5
Note: The output list has the same number of elements as the input list, is sorted in ascending order, and contains the same elements as the input list.

2. Output: [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7,
8, 8, 9, 9] 1 Error - One extra 6

3. Output: [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6,
7, 7, 7, 8, 8, 8, 9, 9, 9] 6 Errors - One extra 2, 5, 6, 7, 8 and 9

4. Reason: The incorrectly sorted list is missing two 9s and one 0.
Output: [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7,
7, 8, 8, 9, 9, 9, 9] 3 Errors - Missing one 1 and has two extra 9s

5. Reason: The incorrectly sorted list is missing one 0, one 3, one 4, four 6s, and one 9.
Output: [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6,
6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9] 10 Errors - Missing one 1, 2, has four extra 6s, one extra 7, 8 and two extra 9s

6. Output: [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6,
7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9] 8 Errors - Has one extra 2, 3, 6, two extra 7s, one extra 8 and two extra 9s

7. Output: [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 8,
8, 9, 9] 2 Errors - Missing one 1 and has one extra 4

8. Reason: The incorrectly sorted list is missing three 0s, two 3s, two 4s, one 5, two 6s, and one 9.
Output: [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 6,
6, 7, 7, 8, 8, 9] 5 Errors - Missing one 1, 9, has one extra 3 and two extra 6s

9. Reason: The incorrectly sorted list is missing one 0, three 2s, two 3s, two 4s, three 5s, two 6s, one 7, and one 9.
Output: [0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 6,
6, 6, 6, 6, 7, 8, 8, 9, 9] 8 Errors - Missing one 1, one 7, has two extra 2s, two extra 3s, one extra 5 and 6
10. **Reason: The incorrectly sorted list is missing three 1s, one 3, one 4, two 5s, one 6, one 7, one 8, and one 9.**
**Output: [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7,**
**7, 8, 8, 9, 9] (Fully Correct)**


**Final Result (Correctly Sorted):**


[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 9, 9]


21


**C** **Example Prompts - Set Intersection**

We present the prompts only for the intersection of two 32element sets, as those for 64-element and 128-element sets
are identical, except for the _split_ ~~_p_~~ _rompt_ where the size of
the split is adjusted proportionally.
For set intersection, we employ two distinct types of operations that interact with the LLM, each with its corresponding prompts. First, there is the **Generate** operation,
utilizing the _intersect_ ~~_p_~~ _rompt_ to guide the LLM in intersecting two input sets, and the _split_ ~~_p_~~ _rompt_ to direct the
LLM to split a specified set into a designated number of distinct subsets. Second, the **Aggregate** operation leverages the
_merge_ ~~_p_~~ _rompt_ to guide the LLM in combining two sets into
one.
First, we present the prompt stubs (Table 10), serving as
templates to dynamically generate appropriate prompts at
runtime. For clarity, we display their corresponding few-shot
examples separately in Table 11. Following this, we outline
the LLM interactions throughout a complete set intersection
process (Table 12 - Table 15).



22


Table 10: Prompt stubs for the set intersection tasks; parameters in single curly brackets will be substituted at runtime.


**intersect** **prompt:** _<_ Instruction _>_ Find the intersection of two sets of numbers. Output only the set of numbers that are
present in both sets, no additional text. _<_ /Instruction _>_


_<_ Examples _>_ See Table 11 _<_ /Examples _>_


Input Set 1: _{_ set1 _}_


Input Set 2: _{_ set2 _}_


**split** ~~**p**~~ **rompt (32 elements):** _<_ Instruction _>_ Split the following list of 32 numbers into 2 lists of 16 numbers each, the first
list should contain the first 16 numbers and the second list the second 16 numbers.


Only output the 2 lists in the following format without any additional text or thoughts!


_{{_


"List 1": [13, 16, 30, 6, 21, 7, 31, ...],


"List 2": [25, 24, 10, 4, 27, 0, 14, ...]


_}}_


_<_ /Instruction _>_


_<_ Examples _>_ See Table 11 _<_ /Examples _>_


Input: _{_ input _}_


**merge** ~~**p**~~ **rompt:** _<_ Instruction _>_ Merge the following 2 lists into one list by appending the second list to the first list.


Only output the final list without any additional text or thoughts! _<_ /Instruction _>_


List 1: _{_ input1 _}_


List 2: _{_ input2 _}_


23


Table 11: Few-shot examples for each prompt used for the set intersection tasks; some lists are truncated for brevity.


**intersect** **prompt:**


_<_ Examples _>_


Input Set 1: [13, 16, 30, 6, 21, 7, 31, 15, 11, 1, 24, 10, 9, 3, 20, 8]


Input Set 2: [25, 24, 10, 4, 27, 0, 14, 12, 8, 2, 29, 20, 17, 19, 26, 23]


Output: [24, 10, 20, 8]


Input Set 1: [26, 40, 42, 57, 15, 31, 5, 32, 11, 4, 24, 28, 51, 54, _. . ._ (Omitted 18/32 numbers)]


Input Set 2: [16, 60, 36, 48, 0, 15, 5, 19, 46, 24, 1, 6, 61, 10, _. . ._ (Omitted 18/32 numbers)]


Output: [40, 15, 5, 24, 35, 59, 16, 63]


Input Set 1: [115, 61, 35, 103, 90, 117, 86, 44, 63, 45, 40, 30, 74, 33, _. . ._ (Omitted 50/64 numbers)]


Input Set 2: [13, 35, 20, 96, 34, 18, 47, 127, 126, 9, 21, 16, 77, 22, _. . ._ (Omitted 50/64 numbers)]


Output: [115, 35, 90, 117, 63, 40, 30, 33, 15, 89, 50, 12, 2, 84, 7, 57, 96]


_<_ /Examples _>_


**split** ~~**p**~~ **rompt (32 elements):**


_<_ Examples _>_


Input: [26, 40, 42, 57, 15, 31, 5, 32, 11, 4, 24, 28, 51, 54, _. . ._ (Omitted 18/32 numbers)]


Output:


_{{_


"List 1": [26, 40, 42, 57, 15, 31, 5, 32, 11, 4, 24, 28, 51, 54, 12, 22],


"List 2": [33, 35, 7, 13, 2, 59, 8, 23, 43, 16, 29, 55, 25, 63, 21, 18]


_}}_


_<_ /Examples _>_


**merge** ~~**p**~~ **rompt:** 

Table 12: Intersection of two 32-element sets: Execution plan ( **GoO** )


**GoO:**


1. Split the second input set into two sub-sets of equal size (split ~~p~~ rompt)

2. For each sub-set: Intersect the sub-set with the first input set (intersect ~~p~~ rompt) five times; score each sort attempt; keep
the best

3. Merge the resulting intersections into one full intersection set (merge ~~p~~ rompt) 10 times; score each merge attempt; keep
the best


24


Table 13: Intersection of two 32-element sets: **Step 1 (Prompt/Response)**


**Step 1 – Prompt:**


_<_ Instruction _>_ Split the following list of 32 numbers into 2 lists of 16 numbers each, the first list should contain the first 16
numbers and the second list the second 16 numbers.


Only output the 2 lists in the following format without any additional text or thoughts!


_{{_


"List 1": [13, 16, 30, 6, 21, 7, 31, ...],


"List 2": [25, 24, 10, 4, 27, 0, 14, ...]


_}}_


_<_ /Instruction _>_


_<_ Examples _>_ See Table 11 _<_ /Examples _>_


Input: [31, 11, 4, 63, 38, 58, 59, 24, 61, 14, 32, 39, 27, 46, 48, 19, 52, 57, 50, 56, 3, 2, 53, 29,
5, 37, 62, 41, 36, 12, 49, 16]


**Step 1 – Response (Fully Correct):**


_{{_


"List 1": [31, 11, 4, 63, 38, 58, 59, 24, 61, 14, 32, 39, 27, 46, 48, 19],


"List 1": [52, 57, 50, 56, 3, 2, 53, 29, 5, 37, 62, 41, 36, 12, 49, 16]


_}}_


25


Table 14: Intersection of two 32-element sets: **Step 2 (Prompts/Responses)**


**Step 2a – Prompt:**


_<_ Instruction _>_ Find the intersection of two sets of numbers. Output only the set of numbers that are present in both sets, no
additional text. _<_ /Instruction _>_


_<_ Examples _>_ See Table 11 _<_ /Examples _>_


Input Set 1: [11, 60, 1, 49, 21, 33, 14, 56, 54, 15, 23, 40, 45, 22, 7, 28, 20, 46, 51, 6, 34, 37, 3,
50, 17, 8, 25, 0, 35, 47, 18, 19]


Input Set 2: [31, 11, 4, 63, 38, 58, 59, 24, 61, 14, 32, 39, 27, 46, 48, 19]


**Step 2a – 5 Responses:**


1. [11, 14, 46, 14, 19] (1 Error - Duplicated 14)
2. **Output: [11, 14, 46, 19] (Fully Correct)**

3. [11, 14, 46, 14, 19] (1 Error - Duplicated 14)

4. [11, 14, 46, 19] (Fully Correct)

5. [11, 14, 46, 14, 19] (1 Error - Duplicated 14)


**Step 2b – Prompt:**


_<_ Instruction _>_ Find the intersection of two sets of numbers. Output only the set of numbers that are present in both sets, no
additional text. _<_ /Instruction _>_


_<_ Examples _>_ See Table 11 _<_ /Examples _>_


Input Set 1: [11, 60, 1, 49, 21, 33, 14, 56, 54, 15, 23, 40, 45, 22, 7, 28, 20, 46, 51, 6, 34, 37, 3,
50, 17, 8, 25, 0, 35, 47, 18, 19]


Input Set 2: [52, 57, 50, 56, 3, 2, 53, 29, 5, 37, 62, 41, 36, 12, 49, 16]


**Step 2b – 5 Responses:**


1. [50, 56, 49] (2 Errors - Missing 3 and 37)

2. [50, 56, 37, 49] (1 Error - Missing 3)
3. **[56, 49, 37, 3, 50] (Fully Correct)**

4. [50, 56, 37, 49] (1 Error - Missing 3)

5. [50, 56, 37, 49] (1 Error - Missing 3)


26


Table 15: Intersection of two 32-element sets: **Step 3 (Prompt/Responses)**


**Step 3 – Prompt:**


_<_ Instruction _>_ Merge the following 2 lists into one list by appending the second list to the first list.


Only output the final list without any additional text or thoughts! _<_ /Instruction _>_


List 1: [11, 14, 46, 19]


List 2: [56, 49, 37, 3, 50]


**Step 3 – 10 Responses:**


1. **[11, 14, 46, 19, 56, 49, 37, 3, 50] (Fully Correct)**

2. [11, 14, 46, 19, 56, 49, 37, 3, 50] (Fully Correct)

3. [11, 14, 46, 19, 56, 49, 37, 3, 50] (Fully Correct)

4. [11, 14, 46, 19, 56, 49, 37, 3, 50] (Fully Correct)

5. [11, 14, 46, 19, 56, 49, 37, 3, 50] (Fully Correct)

6. [11, 14, 46, 19, 56, 49, 37, 3, 50] (Fully Correct)

7. [11, 14, 46, 19, 56, 49, 37, 3, 50] (Fully Correct)

8. [11, 14, 46, 19, 56, 49, 37, 3, 50] (Fully Correct)

9. [11, 14, 46, 19, 56, 49, 37, 3, 50] (Fully Correct)

10. [11, 14, 46, 19, 56, 49, 37, 3, 50] (Fully Correct)


**Final Result (Correct Intersection):**


[11, 14, 46, 19, 56, 49, 37, 3, 50]


27


**D** **Example Prompts - Keyword Counting**

We present the prompts only for GoT4 of the keyword counting task, as those used for GoT8 and GoTx are identical, except for minor differences in the _split_ ~~_p_~~ _rompt_ where the size
of the split is adjusted.
For keyword counting, we employ three distinct types of
operations that interact with the LLM, each with its corresponding prompts. First, there is the **Generate** operation,
utilizing the _count_ ~~_p_~~ _rompt_ to guide the LLM in counting the
keywords in a text, and the _split_ ~~_p_~~ _rompt_ to direct the LLM
to split a given text into a number of passages. Next, the **Ag-**
**gregate** operation leverages the _merge_ ~~_p_~~ _rompt_ to guide the
LLM in merging two dictionaries of counted keywords into
one. Finally, the **ValidateAndImprove** operation employs
the _improve_ _merge_ ~~_p_~~ _rompt_ to instruct the LLM to correct
mistakes that were made in a previous Aggregate operation.
We present the prompt stubs (Table 16 - Table 17), serving
as templates to dynamically generate appropriate prompts at
runtime. For clarity, we display their corresponding few-shot
examples separately in Table 18 and Table 19. Following
this, we outline the LLM interactions throughout a complete
keyword counting process (Table 20 - Table 28).



28


Table 16: Prompt stubs for the keyword counting task; parameters in single curly brackets will be substituted at runtime.


**count** ~~**p**~~ **rompt:** _<_ Instruction _>_ Count the frequency of how many times each country is explicitly named in the input text.
You can generate any intermedate lists and states, but the final output should only contain the frequency of each country that
appears at least once in the following json format, prefixed with ”Output: ” (make sure to keep the same spelling for each
country in the output as in the input text):


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


Input: _{_ input ~~t~~ ext _}_


**split** ~~**p**~~ **rompt:** _<_ Instruction _>_ Split the following input text into 4 paragraphs of approximately same length.


Only output the final 4 paragraphs in the following format without any additional text or thoughts:


_{{_


"Paragraph 1": "Some paragraph text _. . ._ ",


"Paragraph 2": "Some paragraph text _. . ._ ",


"Paragraph 3": "Some paragraph text _. . ._ ",


"Paragraph 4": "Some paragraph text _. . ._ "


_}}_


_<_ /Instruction _>_


_<_ Example _>_ See Table 19 _<_ /Example _>_


Input: _{_ input ~~t~~ ext _}_


29


Table 17: Prompt stubs for the keyword counting task _continued_ ; parameters in single curly brackets will be substituted at
runtime.


**merge** ~~**p**~~ **rompt:** _<_ Instruction _>_ Combine the following 2 dictionaries, each containing the frequency of countries in a text,
into a single dictionary. Simply add the frequencies together for each country and if a country is not present in one of the
dictionaries, add it to the final dictionary with the frequency from the other dictionary.


Only output the final merged dictionary without any additional text or thoughts! _<_ /Instruction _>_


_<_ Approach _>_


To combine the 2 dictionaries into single one, follow these steps:


1. Create a new dictionary to store the combined frequencies.

2. Iterate through the keys of the first dictionary and add the frequency of each country to the new dictionary.

3. Iterate through the keys of the second dictionary and add the frequency of each country to the new dictionary and if it is
already present, add the frequency to the existing value.


_<_ /Approach _>_


Combine the following 2 dictionaries into a single dictionary:


_{_ dictionary ~~1~~ _}_


_{_ dictionary ~~2~~ _}_


Combined Output:


**improve** ~~**m**~~ **erge** ~~**p**~~ **rompt:** _<_ Instruction _>_ The following 2 dictionaries were combined into the third dictionary below. However, some mistakes occured and the third dictionary is incorrect. Please fix the third dictionary so that it contains the correct
frequencies for each country. The correct frequencies are the sum of the frequencies from the first 2 dictionaries. If a country
is not present in one of the dictionaries, add it to the final dictionary with the frequency from the other dictionary.


_<_ /Instruction _>_


_<_ Example _>_ See Table 19 _<_ /Example _>_
Dictionary 1: _{_ dictionary ~~1~~ _}_


Dictionary 2: _{_ dictionary ~~2~~ _}_


Incorrectly Combined Dictionary: _{_ dictionary incorrect _}_


Output:


30


Table 18: Few-shot examples for **count** prompt used for the keyword counting task; some paragraphs and dictionaries are
truncated and formatting is slightly adjusted for brevity.


**count** ~~**p**~~ **rompt:**


_<_ Examples _>_


Input: Alexandra boarded the first flight of her grand journey, starting from Canada. With a globe-trotting ... (Omitted)


Paragraphs:


Alexandra boarded the first flight of her grand journey, starting from Canada. With a globe-trotting itinerary ... (Omitted)


Her first stop was Mexico, where she marveled at the Mayan ruins. From there, she explored the rainforests ... (Omitted)


Sublist frequencies:


_{{_ "Canada": 1 _}}_


_{{_ "Mexico": 1, "Brazil": 1, "Argentina": 1 _}}_


Output: _{{_ "Canada": 1, "Mexico": 1, "Brazil": 1, "Argentina": 1 _}}_


Input: The adventure led him to the peaks of Peru where he trekked to see the mysteries of Machu Picchu ... (Omitted)


Paragraphs:


The adventure led him to the peaks of Peru where he trekked to see the mysteries of Machu Picchu. He then ... (Omitted)


A quick detour to Uruguay and Paraguay allowed him to experience the vibrancy of the local cultures before ... (Omitted)


Sublists:


_{{_ "Peru": 1, "Chile": 1 _}}_


_{{_ "Uruguay": 1, "Paraguay": 1, "Canada": 1, "Peru": 1, "Brazil": 1, "Mexico": 1 _}}_


Output: _{{_ "Peru": 2, "Chile": 1, "Uruguay": 1, "Paraguay": 1, "Canada": 1, "Brazil": 1, "Mexico": 1 _}}_


Input: Journeying westward, she admired the art in Italy and sipped coffee in France. The music of ... (Omitted)


Paragraphs:


Journeying westward, she admired the art in Italy and sipped coffee in France.


The music of Spain and the history of Greece deepened her love for Europe. The Nordic beauty of Norway, ... (Omitted)


She danced in Ireland, explored castles in Scotland, and marveled at the architecture in Germany and Russia.


Italy, Norway, Sweden and Germany will always stay her favourite destinations to visit.


Sublists:


_{{_ "Italy": 1, "France": 1 _}}_


_{{_ "Spain": 1, "Greece": 1, "Norway": 1, "Sweden": 1, "Finland": 1, "Denmark": 1 _}}_


_{{_ "Ireland": 1, "Scotland": 1, "Germany": 1, "Russia": 1 _}}_


_{{_ "Italy": 1, "Norway": 1, "Sweden": 1, "Germany": 1 _}}_


Output: _{{_ "Italy": 2, "France": 1, "Spain": 1, "Greece": 1, "Norway": 2, "Sweden": 2, _. . ._ (Omitted) _}}_


_<_ /Examples _>_


31


Table 19: Few-shot examples for **split**, **merge** and **improve** ~~**m**~~ **erge** prompts used for the keyword counting task; some paragraphs and dictionaries are truncated and formatting is slightly adjusted for brevity.


**split** ~~**p**~~ **rompt:**


_<_ Examples _>_


Input: Journeying westward, she admired the art in Italy and sipped coffee in France. The music of Spain and the history of
Greece deepened her love for Europe. The Nordic beauty of Norway, Sweden, Finland, and Denmark took her breath away.
She danced in Ireland, explored castles in Scotland, and marveled at the architecture in Germany and Russia. Italy, Norway,
Sweden and Germany will always stay her favourite destinations to visit.


Output:


_{{_


"Paragraph 1": "Journeying westward, she admired the art in Italy and sipped coffee in France. ",


"Paragraph 2": "The music of Spain and the history of Greece deepened her love for _. . ._ (Omitted)”,


"Paragraph 3": "She danced in Ireland, explored castles in Scotland, and marveled _. . ._ (Omitted)”,


"Paragraph 4": "Italy, Norway, Sweden and Germany will always stay her favourite _. . ._ (Omitted)”


_}}_


_<_ /Examples _>_


**merge** ~~**p**~~ **rompt:** 

**improve** ~~**m**~~ **erge** ~~**p**~~ **rompt:**


_<_ Example _>_


Dictionary 1: _{{_ "Peru": 2, "Chile": 1, "Uruguay": 1, "Paraguay": 1 _}}_


Dictionary 2: _{{_ "Peru": 1, "Argentina": 1, "Canada": 1, "Chile": 3, "Germany": 2 _}}_


Incorrectly Combined Dictionary:


_{{_ "Peru": 3, "Chile": 2, "Uruguay": 1, "Paraguay": 1, "Argentina": 1, "Chile": 3, "Germany": 2 _}}_


Output:


_{{_ "Peru": 3, "Chile": 4, "Uruguay": 1, "Paraguay": 1, "Argentina": 1, "Canada": 1, "Germany": 2 _}}_


_<_ /Example _>_


Table 20: Keyword counting for an example 4-passage split (GoT4): Execution plan ( **GoO** )


**GoO:**


1. Split the input text into four paragraphs of roughly equal size (split ~~p~~ rompt)

2. For each paragraph: Count the occurrences of individual countries (count ~~p~~ rompt) 10 times; score each counting attempt;
keep the best

3. Merge the country counts into one dictionary (merge ~~p~~ rompt) 3 times; validate and improve invalid merge attempts
(improve ~~m~~ erge ~~p~~ rompt) up to 3 attempts each; score; keep the best


32


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
