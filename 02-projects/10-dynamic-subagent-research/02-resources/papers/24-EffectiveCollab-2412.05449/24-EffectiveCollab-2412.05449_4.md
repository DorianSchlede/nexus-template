<!-- Source: 24-EffectiveCollab-2412.05449.pdf | Chunk 4/4 -->


[17] Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize
Chen, Yusheng Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu, and Maosong Sun. ChatDev:
Communicative agents for software development. In _Annual Meeting of the Association for_
_Computational Linguistics_, 2024.


[18] Munindar P Singh. _Multiagent systems_ . Springer, 1994.


[19] Andries Petrus Smit, Nathan Grinsztajn, Paul Duckworth, Thomas D Barrett, and Arnu Pretorius.
Should we be going mad? a look at multi-agent debate strategies for llms. In _International_
_Conference on Machine Learning_, 2024.


[20] Katia P Sycara. Multiagent systems. _AI magazine_, 19(2):79–79, 1998.


[21] Yashar Talebirad and Amirhossein Nadiri. Multi-agent collaboration: Harnessing the power of
intelligent llm agents. _arXiv preprint arXiv:2306.03314_, 2023.


[22] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun
Zhang, Shaokun Zhang, Jiale Liu, Ahmed Hassan Awadallah, Ryen W White, Doug Burger,
and Chi Wang. AutoGen: Enabling next-gen llm applications via multi-agent conversation
framework. In _COLM_, 2024.


[23] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan
Cao. ReAct: Synergizing reasoning and acting in language models. In _International Conference_
_on Learning Representations_, 2023.


[24] Jintian Zhang, Xin Xu, Ningyu Zhang, Ruibo Liu, Bryan Hooi, and Shumin Deng. Exploring
collaboration mechanisms for LLM agents: A social psychology view. In _Annual Meeting of_
_the Association for Computational Linguistics_, 2024.


[25] Yang Zhang, Shixin Yang, Chenjia Bai, Fei Wu, Xiu Li, Zhen Wang, and Xuelong Li.
Towards efficient LLM grounding for embodied multi-agent collaboration. _arXiv preprint_
_arXiv:2405.14314_, 2024.


17


**Appendix**


**A** **Benchmarking Data Artifacts**


Table 13: Example artifacts from benchmarking data collection


Artifact Example


Scenario Goals:
```
          * User needs to book a ticket for a round-trip economy
          flight from DEN to RST, departing on June 23, and returning
          on June 30.
          * User needs to book a room in Rochester, Minnesota from
          June 23 to June 30.
          * User needs to obtain total estimated cost of flight,
          hotel, food, and local transportation for their 7-day trip,
          given their $2,500 weekly budget.

```

Background:
```
          * User’s full name is Gregory James Anderson.
          * Gregory is 36 years old.
          * Gregory resides in Denver, Colorado.
          * Gregory’s preferred class for flights is economy.

```

Input Problem `Please book a ticket for a round-trip economy flight from`
```
          DEN to RST, departing on June 23.

```

Assertions User-side assertions:
```
          * User is informed that a ticket for an economy flight from
          DEN to RST departing on June 23 have been booked.
          * User is informed that a ticket for an economy flight from
          RST to DEN have been booked. The flight from DEN to RST
          departs on June 30.
          * User is informed that a room in a hotel in Rochester,
          Minnesota from June 23 to June 30 has been booked
          * User is informed of the total estimated cost including
          flight, hotel, food, and local transportation for their
          7-day trip from Denver to Minnesota, given their $2,500
          weekly budget.

```

System-side assertions:
```
          * book_flight is executed to book two tickets for a
          round-trip economy flight from DEN to RST on June 23
          * book_hotel is executed to book a hotel in Minnesota from
          June 23 to June 30
          * search_flight is executed before book_flight to provide
          the user with flight options before performing the booking
          * search_hotel is executed before book_hotel to provide the
          user with options before booking
          * calculate is executed to get the total estimated cost for
          flight, hotel, food, and local transportation for his 7-day
          trip from Denver to Minnesota for one person, given their
          $2,500 weekly budget

```

18


**B** **Agent Profiles**


Table 14: List of agents for each benchmarking domain. Supervisor agents are **bolded** . We also list
their action groups, which are sets of tools that the agents have access to.


Domain/Usecase Agent Name Action Groups



Travel Planning


Mortgage Financing


Software Development



**Travel agent**
Weather agent Weather
Location search agent LocationService
Car rental agent CarRental
Flight agent BookFlight
Hotel agent BookHotel
Travel budget agent Calculator
Restaurant agent RestaurantSearch, FoodDelivery
Local expert agent Eventbrite, NewsSeartch
Airbnb agent BookAirbnb


**Mortgage agent** MortgageLoans
Property agent LocationService, RealEstateManagement
Credit agent Banking, CreditReport
Income agent HRPayrollBenefits, Calculator
Payment agent Calculator
Closing agent Calculator, RealEstateManagement


**Software agent**
Design agent
Code agent
Test agent SoftwareDevelopment
Review agent SoftwareDevelopment
Deploy agent
Infrastructure agent CodeDeployment
Application agent CodeDeployment



**C** **Full results of Coordination Mode**


Table 15: Full End-to-end evaluation of Coordination Mode


Setting Dataset Overall Supervisor UserGSR GSR side
GSR



Systemside
GSR



Supervisor: Sonnet 3.5 (20241022)
Specialists: Sonnet 3.5 (20241022)


Supervisor: Sonnet 3.5 (20241022)
Specialists: Sonnet 3.0


Supervisor: Sonnet 3.5 (20241022)
Specialists: Haiku 3.5



Travel 0.90 0.90 1.00 0.90
Mortgage 0.90 0.93 0.93 0.90
Software 0.90 1.00 1.00 0.90


Travel 0.87 0.90 0.90 0.87
Mortgage 0.90 0.97 0.90 0.87
Software 0.77 0.90 0.80 0.83


Travel 0.80 0.87 0.83 0.83
Mortgage 0.83 0.90 0.90 0.87
Software 0.87 0.93 0.90 0.97



Travel 0.60                     - 0.67 0.67
Single-agent: Sonnet 3.5 (20241022) Mortgage 0.80 - 0.80 0.83
Software 0.53                    - 0.67 0.60


19


Table 16: Full Latency Performance of Coordination Mode



Avg.
communications
per session



Avg.
user-perceived
turn latency
per session (s)



Avg. output
tokens per
communication



Setting Dataset



Avg.
communication
overhead
per turn (s)



Supervisor: Sonnet 3.5 (20241022)
Specialists: Sonnet 3.5 (20241022)


Supervisor: Sonnet 3.5 (20241022)
Specialists: Sonnet 3.0


Supervisor: Sonnet 3.5 (20241022)
Specialists: Haiku 3.5



Travel 13.75 31.46 8.63 225.88
Mortgage 13.39 24.42 7.27 201.66
Software 35.44 168.73 7.59 373.77


Travel 15.43 42.12 7.51 276.18
Mortgage 15.97 29.90 6.69 286.21
Software 53.48 137.31 9.11 490.78


Travel 12.95 23.98 9.73 236.27
Mortgage 11.03 18.13 6.93 202.87
Software 36.65 125.31 8.07 388.79



Travel                     - 14.12                     -                     Single-agent: Sonnet 3.5 (20241022) Mortgage  - 9.12  -  Software                    - 52.61                    -                    

**D** **Human Evaluation Results**


Table 17: The automatic and human evaluation results. Note that these set of experiments were from
an intermediate milestone checkpoint of MAC.


Dataset Overall GSR Supervisor GSR User-side GSR System-side GSR


Travel 0.87 0.90 0.90 0.87
Automatic Evaluation Mortgage 0.90 0.97 0.97 0.90
Software 0.77 0.90 0.80 0.83


Travel 0.93 0.90 0.97 0.93
Human Evaluation Mortgage 0.97 0.97 0.97 0.97
Software 0.73 0.87 0.80 0.73


20


