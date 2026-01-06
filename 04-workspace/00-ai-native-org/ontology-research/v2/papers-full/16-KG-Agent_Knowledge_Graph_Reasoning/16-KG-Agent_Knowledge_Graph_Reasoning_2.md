<!-- Source: 16-KG-Agent_Knowledge_Graph_Reasoning.pdf | Chunk 2/2 -->








**Limitations**


Although KG-Agent demonstrates remarkable performance across various complex factual question
answering tasks, there are some limitations of our
method. First, we only use the LLaMA2-7B as the
backbone LLM, which has a strong capability after
instruction tuning. Hence, more experiments are
required to evaluate other LLMs with comparable
parameter sizes, such as Mistral-7B (Jiang et al.,
2023a) or CodeLLaMA-7b (Rozière et al., 2023).
Second, we focus on reasoning over the KG to
answer the factual questions. We should consider
extending our framework to deal with more types of
knowledge sources, _e.g.,_ databases or tables. Third,
we only evaluate factual question answering tasks
based on KG. Future work should include wider
evaluation scenarios to evaluate the universality of
our method, _e.g.,_ data-to-text and formal-languageto-text (Xie et al., 2022). Finally, we have tried our
best to tune the LLM only to answer the questions
based on the KG information, and avoid generating
discriminatory and risky responses for user questions. However, we should add more rule-based
methods to post-process the predictions and filter
the illegal responses.


**References**


Vamsi Aribandi, Yi Tay, Tal Schuster, Jinfeng Rao,
Huaixiu Steven Zheng, Sanket Vaibhav Mehta, Honglei Zhuang, Vinh Q. Tran, Dara Bahri, Jianmo Ni,
Jai Prakash Gupta, Kai Hui, Sebastian Ruder, and
Donald Metzler. 2022. Ext5: Towards extreme multitask scaling for transfer learning. In _ICLR_ . OpenReview.net.


Jonathan Berant, Andrew Chou, Roy Frostig, and Percy
[Liang. 2013. Semantic parsing on freebase from](https://aclanthology.org/D13-1160/)
[question-answer pairs. In](https://aclanthology.org/D13-1160/) _Proceedings of the 2013_
_Conference on Empirical Methods in Natural Lan-_
_guage Processing, EMNLP 2013, 18-21 October_
_2013, Grand Hyatt Seattle, Seattle, Washington, USA,_
_A meeting of SIGDAT, a Special Interest Group of the_
_ACL_, pages 1533–1544. ACL.


Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind
Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Askell, Sandhini Agarwal, Ariel Herbert-Voss,
Gretchen Krueger, Tom Henighan, Rewon Child,
Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,
Clemens Winter, Christopher Hesse, Mark Chen, Eric
Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
Jack Clark, Christopher Berner, Sam McCandlish,
Alec Radford, Ilya Sutskever, and Dario Amodei.
2020. Language models are few-shot learners. In _Ad-_
_vances in Neural Information Processing Systems 33:_



_Annual Conference on Neural Information Process-_
_ing Systems 2020, NeurIPS 2020, December 6-12,_
_2020, virtual_ .


Shulin Cao, Jiaxin Shi, Liangming Pan, Lunyiu Nie,
Yutong Xiang, Lei Hou, Juanzi Li, Bin He, and Hanwang Zhang. 2022. KQA pro: A dataset with explicit
compositional programs for complex question answering over knowledge base. In _Proceedings of the_
_60th Annual Meeting of the Association for Compu-_
_tational Linguistics (Volume 1: Long Papers), ACL_
_2022, Dublin, Ireland, May 22-27, 2022_, pages 6101–
6119. Association for Computational Linguistics.


Danqi Chen, Adam Fisch, Jason Weston, and Antoine
Bordes. 2017. Reading wikipedia to answer opendomain questions. In _Proceedings of the 55th Annual_
_Meeting of the Association for Computational Lin-_
_guistics, ACL 2017, Vancouver, Canada, July 30 -_
_August 4, Volume 1: Long Papers_, pages 1870–1879.
Association for Computational Linguistics.


Hyung Won Chung, Le Hou, Shayne Longpre, Barret
Zoph, Yi Tay, William Fedus, Eric Li, Xuezhi Wang,
Mostafa Dehghani, Siddhartha Brahma, Albert Webson, Shixiang Shane Gu, Zhuyun Dai, Mirac Suzgun, Xinyun Chen, Aakanksha Chowdhery, Sharan
Narang, Gaurav Mishra, Adams Yu, Vincent Y. Zhao,
Yanping Huang, Andrew M. Dai, Hongkun Yu, Slav
Petrov, Ed H. Chi, Jeff Dean, Jacob Devlin, Adam
Roberts, Denny Zhou, Quoc V. Le, and Jason Wei.
2022. Scaling instruction-finetuned language models.
_CoRR_, abs/2210.11416.


Yu Gu, Xiang Deng, and Yu Su. 2023. Don’t generate, discriminate: A proposal for grounding language
models to real-world environments. In _Proceedings_
_of the 61st Annual Meeting of the Association for_
_Computational Linguistics (Volume 1: Long Papers),_
_ACL 2023, Toronto, Canada, July 9-14, 2023_, pages
4928–4949. Association for Computational Linguistics.


Yu Gu, Sue Kase, Michelle Vanni, Brian M. Sadler,
Percy Liang, Xifeng Yan, and Yu Su. 2021. Beyond
I.I.D.: three levels of generalization for question answering on knowledge bases. In _WWW ’21: The Web_
_Conference 2021, Virtual Event / Ljubljana, Slovenia,_
_April 19-23, 2021_, pages 3477–3488. ACM / IW3C2.


Yu Gu and Yu Su. 2022. Arcaneqa: Dynamic program
induction and contextualized encoding for knowledge
base question answering. In _Proceedings of the 29th_
_International Conference on Computational Linguis-_
_tics, COLING 2022, Gyeongju, Republic of Korea,_
_October 12-17, 2022_, pages 1718–1731. International
Committee on Computational Linguistics.


Gaole He, Yunshi Lan, Jing Jiang, Wayne Xin Zhao, and
[Ji-Rong Wen. 2021. Improving multi-hop knowledge](https://doi.org/10.1145/3437963.3441753)
[base question answering by learning intermediate](https://doi.org/10.1145/3437963.3441753)
[supervision signals. In](https://doi.org/10.1145/3437963.3441753) _WSDM ’21, The Fourteenth_
_ACM International Conference on Web Search and_
_Data Mining, Virtual Event, Israel, March 8-12, 2021_,
pages 553–561. ACM.


Chenxu Hu, Jie Fu, Chenzhuang Du, Simian Luo, Junbo
Zhao, and Hang Zhao. 2023a. Chatdb: Augmenting
llms with databases as their symbolic memory. _CoRR_,
abs/2306.03901.


Xuming Hu, Junzhe Chen, Xiaochuan Li, Yufei Guo,
Lijie Wen, Philip S. Yu, and Zhijiang Guo. 2023b.
Do large language models know about facts? _CoRR_,
abs/2310.05177.


Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego
de Las Casas, Florian Bressand, Gianna Lengyel,
Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock,
Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. 2023a. Mistral
7b. _CoRR_, abs/2310.06825.


Jinhao Jiang, Kun Zhou, Zican Dong, Keming Ye,
Wayne Xin Zhao, and Ji-Rong Wen. 2023b. Structgpt: A general framework for large language
model to reason over structured data. volume
abs/2305.09645.


Jinhao Jiang, Kun Zhou, Wayne Xin Zhao, Yaliang Li,
and Ji-Rong Wen. 2023c. Reasoninglm: Enabling
structural subgraph reasoning in pre-trained language
models for question answering over knowledge graph.
In _Proceedings of the 2023 Conference on Empirical_
_Methods in Natural Language Processing, EMNLP_
_2023, Singapore, December 6-10, 2023_, pages 3721–
3735. Association for Computational Linguistics.


Jinhao Jiang, Kun Zhou, Xin Zhao, and Ji-Rong Wen.
2023d. Unikgqa: Unified retrieval and reasoning for
solving multi-hop question answering over knowledge graph. In _The Eleventh International Confer-_
_ence on Learning Representations, ICLR 2023, Ki-_
_gali, Rwanda, May 1-5, 2023_ . OpenReview.net.


Mandar Joshi, Eunsol Choi, Daniel S. Weld, and Luke
Zettlemoyer. 2017. Triviaqa: A large scale distantly
supervised challenge dataset for reading comprehension. In _Proceedings of the 55th Annual Meeting of_
_the Association for Computational Linguistics, ACL_
_2017, Vancouver, Canada, July 30 - August 4, Volume_
_1: Long Papers_, pages 1601–1611. Association for
Computational Linguistics.


Yunshi Lan, Gaole He, Jinhao Jiang, Jing Jiang,
Wayne Xin Zhao, and Ji-Rong Wen. 2023. Complex
knowledge base question answering: A survey. _IEEE_
_Trans. Knowl. Data Eng._, 35(11):11196–11215.


Tianle Li, Xueguang Ma, Alex Zhuang, Yu Gu, Yu Su,
[and Wenhu Chen. 2023. Few-shot in-context learning](https://doi.org/10.48550/arXiv.2305.01750)
[for knowledge base question answering.](https://doi.org/10.48550/arXiv.2305.01750) _CoRR_ .


Yudong Liu, Xu Zhang, Shilin He, Hongyu Zhang,
Liqun Li, Yu Kang, Yong Xu, Minghua Ma, Qingwei
Lin, Yingnong Dang, Saravan Rajmohan, and Dongmei Zhang. 2022. Uniparser: A unified log parser
for heterogeneous log data. In _WWW ’22: The ACM_
_Web Conference 2022, Virtual Event, Lyon, France,_
_April 25 - 29, 2022_, pages 1893–1901. ACM.



Linhao Luo, Yuan-Fang Li, Gholamreza Haffari, and
Shirui Pan. 2023. Reasoning on graphs: Faithful
and interpretable large language model reasoning.
volume abs/2310.01061.


Alexander H. Miller, Adam Fisch, Jesse Dodge, AmirHossein Karimi, Antoine Bordes, and Jason Weston.
2016. Key-value memory networks for directly reading documents. In _Proceedings of the 2016 Confer-_
_ence on Empirical Methods in Natural Language Pro-_
_cessing, EMNLP 2016, Austin, Texas, USA, Novem-_
_ber 1-4, 2016_, pages 1400–1409.


Reiichiro Nakano, Jacob Hilton, Suchir Balaji, Jeff Wu,
Long Ouyang, Christina Kim, Christopher Hesse,
Shantanu Jain, Vineet Kosaraju, William Saunders,
Xu Jiang, Karl Cobbe, Tyna Eloundou, Gretchen
Krueger, Kevin Button, Matthew Knight, Benjamin
Chess, and John Schulman. 2021. Webgpt: Browserassisted question-answering with human feedback.
_CoRR_, abs/2112.09332.


Shirui Pan, Linhao Luo, Yufei Wang, Chen Chen, Jiapu Wang, and Xindong Wu. 2023. Unifying large
language models and knowledge graphs: A roadmap.
_CoRR_, abs/2306.08302.


Adam Roberts, Colin Raffel, and Noam Shazeer. 2020.

[How much knowledge can you pack into the param-](https://doi.org/10.18653/v1/2020.emnlp-main.437)
[eters of a language model? In](https://doi.org/10.18653/v1/2020.emnlp-main.437) _Proceedings of the_
_2020 Conference on Empirical Methods in Natural_
_Language Processing, EMNLP 2020, Online, Novem-_
_ber 16-20, 2020_, pages 5418–5426. Association for
Computational Linguistics.


Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten
Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi,
Jingyu Liu, Tal Remez, Jérémy Rapin, Artyom
Kozhevnikov, Ivan Evtimov, Joanna Bitton, Manish Bhatt, Cristian Canton-Ferrer, Aaron Grattafiori,
Wenhan Xiong, Alexandre Défossez, Jade Copet,
Faisal Azhar, Hugo Touvron, Louis Martin, Nicolas Usunier, Thomas Scialom, and Gabriel Synnaeve.
2023. Code llama: Open foundation models for code.
_CoRR_, abs/2308.12950.


Apoorv Saxena, Aditay Tripathi, and Partha P. Talukdar. 2020. Improving multi-hop question answering
over knowledge graphs using knowledge base embeddings. In _Proceedings of the 58th Annual Meeting of_
_the Association for Computational Linguistics, ACL_
_2020, Online, July 5-10, 2020_, pages 4498–4507.


Michael Sejr Schlichtkrull, Thomas N. Kipf, Peter
Bloem, Rianne van den Berg, Ivan Titov, and Max
Welling. 2018. Modeling relational data with graph
convolutional networks. In _The Semantic Web - 15th_
_International Conference, ESWC 2018, Heraklion,_
_Crete, Greece, June 3-7, 2018, Proceedings_, volume
10843 of _Lecture Notes in Computer Science_, pages
593–607. Springer.


Noah Shinn, Federico Cassano, Beck Labash, Ashwin
Gopinath, Karthik Narasimhan, and Shunyu Yao.
2023. Reflexion: Language agents with verbal reinforcement learning.


Yiheng Shu, Zhiwei Yu, Yuhan Li, Börje F. Karlsson,
Tingting Ma, Yuzhong Qu, and Chin-Yew Lin. 2022.
TIARA: multi-grained retrieval for robust question
answering over large knowledge base. In _Proceed-_
_ings of the 2022 Conference on Empirical Methods_
_in Natural Language Processing, EMNLP 2022, Abu_
_Dhabi, United Arab Emirates, December 7-11, 2022_,
pages 8108–8121. Association for Computational
Linguistics.


Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit
Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox,
Jesse Thomason, and Animesh Garg. 2023. Progprompt: Generating situated robot task plans using
large language models. In _IEEE International Con-_
_ference on Robotics and Automation, ICRA 2023,_
_London, UK, May 29 - June 2, 2023_, pages 11523–
11530. IEEE.


Haitian Sun, Bhuwan Dhingra, Manzil Zaheer, Kathryn
Mazaitis, Ruslan Salakhutdinov, and William W. Cohen. 2018. Open domain question answering using
early fusion of knowledge bases and text. In _Proceed-_
_ings of the 2018 Conference on Empirical Methods_
_in Natural Language Processing, Brussels, Belgium,_
_October 31 - November 4, 2018_, pages 4231–4242.


Jiashuo Sun, Chengjin Xu, Lumingyuan Tang, Saizhuo
Wang, Chen Lin, Yeyun Gong, Heung-Yeung Shum,
and Jian Guo. 2023. Think-on-graph: Deep and
responsible reasoning of large language model with
knowledge graph. _CoRR_, abs/2307.07697.


Alon Talmor and Jonathan Berant. 2018. The web as
a knowledge-base for answering complex questions.
In _Proceedings of the 2018 Conference of the North_
_American Chapter of the Association for Computa-_
_tional Linguistics: Human Language Technologies,_
_NAACL-HLT 2018, New Orleans, Louisiana, USA,_
_June 1-6, 2018, Volume 1 (Long Papers)_, pages 641–
651. Association for Computational Linguistics.


Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay
Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti
Bhosale, Dan Bikel, Lukas Blecher, Cristian CantonFerrer, Moya Chen, Guillem Cucurull, David Esiobu,
Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller,
Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan
Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa,
Isabel Kloumann, Artem Korenev, Punit Singh Koura,
Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten,
Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu,
Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan,
Melanie Kambadur, Sharan Narang, Aurélien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas
[Scialom. 2023. Llama 2: Open foundation and fine-](https://doi.org/10.48550/ARXIV.2307.09288)
[tuned chat models.](https://doi.org/10.48550/ARXIV.2307.09288) _CoRR_, abs/2307.09288.



Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao
Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang,
Xu Chen, Yankai Lin, Wayne Xin Zhao, Zhewei
Wei, and Ji-Rong Wen. 2023a. A survey on large
language model based autonomous agents. volume
abs/2308.11432.


Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao
Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang,
Xu Chen, Yankai Lin, Wayne Xin Zhao, Zhewei
Wei, and Ji-Rong Wen. 2023b. A survey on large
language model based autonomous agents. _CoRR_,
abs/2308.11432.


Tianbao Xie, Chen Henry Wu, Peng Shi, Ruiqi Zhong,
Torsten Scholak, Michihiro Yasunaga, Chien-Sheng
Wu, Ming Zhong, Pengcheng Yin, Sida I. Wang, Victor Zhong, Bailin Wang, Chengzu Li, Connor Boyle,
Ansong Ni, Ziyu Yao, Dragomir Radev, Caiming
Xiong, Lingpeng Kong, Rui Zhang, Noah A. Smith,
Luke Zettlemoyer, and Tao Yu. 2022. Unifiedskg:
Unifying and multi-tasking structured knowledge
grounding with text-to-text language models. In _Pro-_
_ceedings of the 2022 Conference on Empirical Meth-_
_ods in Natural Language Processing, EMNLP 2022,_
_Abu Dhabi, United Arab Emirates, December 7-11,_
_2022_, pages 602–631.


Zhengyuan Yang, Linjie Li, Jianfeng Wang, Kevin
Lin, Ehsan Azarnasab, Faisal Ahmed, Zicheng Liu,
Ce Liu, Michael Zeng, and Lijuan Wang. 2023. MMREACT: prompting chatgpt for multimodal reasoning
and action. _CoRR_, abs/2303.11381.


Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
Shafran, Karthik R. Narasimhan, and Yuan Cao. 2023.
React: Synergizing reasoning and acting in language
models. In _The Eleventh International Conference_
_on Learning Representations, ICLR 2023, Kigali,_
_Rwanda, May 1-5, 2023_ . OpenReview.net.


Xi Ye, Semih Yavuz, Kazuma Hashimoto, Yingbo Zhou,
and Caiming Xiong. 2022. RNG-KBQA: generation
augmented iterative ranking for knowledge base question answering. In _Proceedings of the 60th Annual_
_Meeting of the Association for Computational Lin-_
_guistics (Volume 1: Long Papers), ACL 2022, Dublin,_
_Ireland, May 22-27, 2022_, pages 6032–6043. Association for Computational Linguistics.


Wen-tau Yih, Matthew Richardson, Christopher Meek,
[Ming-Wei Chang, and Jina Suh. 2016. The value of](https://doi.org/10.18653/v1/p16-2033)
[semantic parse labeling for knowledge base question](https://doi.org/10.18653/v1/p16-2033)
[answering. In](https://doi.org/10.18653/v1/p16-2033) _Proceedings of the 54th Annual Meet-_
_ing of the Association for Computational Linguistics,_
_ACL 2016, August 7-12, 2016, Berlin, Germany, Vol-_
_ume 2: Short Papers_ . The Association for Computer
Linguistics.


Pengcheng Yin, Graham Neubig, Wen-tau Yih, and Sebastian Riedel. 2020. Tabert: Pretraining for joint
understanding of textual and tabular data. In _Proceed-_
_ings of the 58th Annual Meeting of the Association_
_for Computational Linguistics, ACL 2020, Online,_
_July 5-10, 2020_, pages 8413–8426.


Jing Zhang, Xiaokang Zhang, Jifan Yu, Jian Tang, Jie
[Tang, Cuiping Li, and Hong Chen. 2022. Subgraph](https://doi.org/10.18653/v1/2022.acl-long.396)
[retrieval enhanced model for multi-hop knowledge](https://doi.org/10.18653/v1/2022.acl-long.396)
[base question answering. In](https://doi.org/10.18653/v1/2022.acl-long.396) _Proceedings of the 60th_
_Annual Meeting of the Association for Computational_
_Linguistics (Volume 1: Long Papers), ACL 2022,_
_Dublin, Ireland, May 22-27, 2022_, pages 5773–5784.
Association for Computational Linguistics.


Lingxi Zhang, Jing Zhang, Yanling Wang, Shulin Cao,
Xinmei Huang, Cuiping Li, Hong Chen, and Juanzi
[Li. 2023. FC-KBQA: A fine-to-coarse composition](https://doi.org/10.18653/v1/2023.acl-long.57)
[framework for knowledge base question answering.](https://doi.org/10.18653/v1/2023.acl-long.57)
In _Proceedings of the 61st Annual Meeting of the_
_Association for Computational Linguistics (Volume_
_1: Long Papers), ACL 2023, Toronto, Canada, July_
_9-14, 2023_, pages 1002–1017. Association for Computational Linguistics.


Yuyu Zhang, Hanjun Dai, Zornitsa Kozareva, Alexander J. Smola, and Le Song. 2018. Variational reasoning for question answering with knowledge graph. In
_Proceedings of the Thirty-Second AAAI Conference_
_on Artificial Intelligence, (AAAI-18), the 30th inno-_
_vative Applications of Artificial Intelligence (IAAI-_
_18), and the 8th AAAI Symposium on Educational_
_Advances in Artificial Intelligence (EAAI-18), New_
_Orleans, Louisiana, USA, February 2-7, 2018_, pages
6069–6076.


Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang,
Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen
Zhang, Junjie Zhang, Zican Dong, Yifan Du, Chen
Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang,
Ruiyang Ren, Yifan Li, Xinyu Tang, Zikang Liu,
Peiyu Liu, Jian-Yun Nie, and Ji-Rong Wen. 2023. A
survey of large language models. _CoRR_ .


Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and
[Yanlin Wang. 2023. Memorybank: Enhancing large](http://arxiv.org/abs/2305.10250)
[language models with long-term memory.](http://arxiv.org/abs/2305.10250) _CoRR_,
abs/2305.10250.


**A** **Experiment Setup**


**A.1** **Datasets**


We select four popular complex KGQA datasets
as in-domain datasets, _i.e., WebQuestionsSP (We-_
_bQSP)_ (Yih et al., 2016), _Complex WebQues-_
_tions 1.1 (CWQ)_ (Talmor and Berant, 2018), and
_GrailQA_ (Gu et al., 2021), which are based on
Freebase, and _KQA Pro_ (Cao et al., 2022), which
is based on Wikidata. And we select three representative ODQA datasets as out-domain datasets,
which are _WebQuestions (WQ)_ (Berant et al., 2013),
_Natural Questions (NQ)_ (Chen et al., 2017), and
_TriviaQA (TQ)_ (Joshi et al., 2017). Since we only
rely on the KG to answer questions, we filter the
questions in ODQA datasets that can not be linked
to any entity in KG, denoted as _WQ-Freebase_, _NQ-_
_Wiki_, and _TQ-Wiki_, respectively. Besides, we further select the _MetaQA_ (Zhang et al., 2018), which
is based on a domain-specific movie KG, to evaluate the generalibility of our method. The detail
description of these selected datasets is as follows:

_•_ **WebQSP** consists of 4,737 questions. The
answer entities are within a maximum of 2 hops
from the topic entity on the Freebase KG. We adopt
the train/valid/test splits from GraftNet (Sun et al.,
2018) for consistency.

_•_ **CWQ** is constructed based on WebQSP, which
is more challenging. It complicates WebQSP by extending the question entities or adding constraints
to restrict the answers. The answer entities are
within a maximum of 4 hops from the topic entity
on the Freebase KG.

_•_ **GrailQA** consists of 64,331 questions. Compared to WebQSP and CWQ, it focuses on a more
comprehensive generalization capability evaluation
from three levels ( _i.e.,_ i.i.d, compositional, and
zero-shot).

_•_ **KQA Pro** consists of 117,970 questions. The
above three datasets are based on Freebase, and it
is based on Wikidata, and require multiple reasoning capabilities including compositional reasoning,
multi-hop reasoning, quantitative comparison, set
operations, and etc.

_•_ **MetaQA** comprises over 400,000 questions
based on a movie domain KG, with answer entities located up to three hops away from the topic
entities. Based on the number of hops, the dataset
is divided into three sub-datasets: MetaQA-1hop,
MetaQA-2hop, and MetaQA-3hop. Following existing work (He et al., 2021), we randomly sample
just one training case for each question template



from the original training set, to form a one-shot
training dataset.

_•_ **WQ** consists of 6,642 questions. The questions
are mostly centered around a single named entity
and are supposed to be answerable by Freebase KG.
We extract xx questions from the original test set
to compose the WQ-freebase subset.

_•_ **NQ** consists of 323,045 questions. Each example contains a question from the Google search
and the corresponding answers, which are text
spans on the Wikipedia page. Following existing
work (Roberts et al., 2020), we use the open version
of this dataset which discards answers with more
than 5 tokens. We extract xx questions from the
original test set to compose the NQ-Wiki subset.

_•_ **TQ** consists of 110K questions. Each example
contains a question authored by trivia enthusiasts,
and the answers are text spans from the Web or
Wikipedia. Following existing work (Roberts et al.,

2020), we use its unfiltered version for evaluation.
We extract xx questions from the original test set
to compose the TQ-Wiki subset.


**A.2** **Evaluation Protocol**


For KGQA, following existing work (Sun et al.,
2018), we use Hits@1 and F1 metrics for WebQSP
and CWQ datasets, F1 metric for GrailQA dataset,
and Hits@1 for MetaQA. The Hits@1 evaluates
the correctness of the top-ranked answer while F1
considers coverage of all the predicted answers. It’s
worth noting that some baselines and our approach
would return all the unordered answers at the end,
which is not suitable for the Hist@1 metric. For
a comprehensive comparison, we randomly select
one answer per question as the top-ranked answer
and then calculate the average Hits@1 result by
repeating this process 100 times following existing
work (Shu et al., 2022). For ODQA, following
existing work (Roberts et al., 2020), we report the
EM metric, which evaluates whether the predicted
answer is the same as the gold one after performing
normalization.


**A.3** **Baselines for Comparison**


For KGQA, we consider the following three types
of baseline methods for performance comparison:

_•_ **subgraph-based reasoning** methods which
perform answer reasoning in a retrieval subgraph
form KG, including GrafeNet (Sun et al., 2018),
NSM (He et al., 2021), SubgraphRetrieval (Zhang
et al., 2022), UniKGQA (Jiang et al., 2023d), and
ReasoningLM (Jiang et al., 2023c) for datasets


on Freebase, and KVMemNet (Miller et al.,
2016), EmbedKGQA (Saxena et al., 2020), and
RGCN (Schlichtkrull et al., 2018) for datasets on
Wikidata;

_•_ **LM-based seq2seq generation** methods
which generate the final SPARQL query by finetuning a sequence-to-sequence language model,
including RNG-KBQA (Ye et al., 2022), UniParser (Liu et al., 2022), ArcaneQA (Gu and
Su, 2022), PanGu w/ T5-3B (Gu et al., 2023),
TIARA (Shu et al., 2022), and FC-KBQA (Zhang
et al., 2023) for datasets on Freebase, and RNN
SPARQL and BART SPARQL (Cao et al., 2022)
for datasets on Wikidata;

_•_ **LLM-based** methods which utilize the powerful zero-shot or few-shot capabilities of LLMs to
answer the question without fine-tuning, including
ROG (Luo et al., 2023), StructGPT (Jiang et al.,
2023b), gpt-3.5-turbo-instruct (Davinvi-003) [2], gpt3.5-turbo (ChatGPT) [3], and gpt-4 (GPT-4) [4] for
both in-domain datasets.
For ODQA, we focus on the closed-book setting
where no documents are provided and consider the
following two types of baseline methods:

_•_ **Fine-tune based** methods which learn to predict the answers, including T5-Base, T5-Large,
BART-base, and BART-Large from (Roberts et al.,
2020);

_•_ **LLM-based** methods which directly answer the questions in zero-shot setting, including
gpt-3.5-turbo-instruct (Davinvi-003) and gpt-3.5turbo (ChatGPT).


**A.4** **Implementation Details**


For instruction tuning data construction, we randomly sample a total of 10,000 training data from
in-domain datasets in a ratio of 1:5:5:10 for WebQSP, KQA Pro, GrailQA, and CWQ according
to some prior empirical studies. Since we focus
on the reasoning process over KG, we suppose the
entities have been given for each question following existing work (Sun et al., 2018; He et al., 2021;
Jiang et al., 2023b). For instruction tuning, we use
the LLaMA2-7B (Touvron et al., 2023) as our backbone LLM. We use a cosine learning rate schedule
with an initial learning rate of 2e-5, a weight decay
of 0.1, a batch size of 256, a maximum length of
1500, and finally fine-tune the model for 3 epochs.


2https://platform.openai.com/docs
3https://platform.openai.com/docs
4https://platform.openai.com/docs



For the relation retrieval model and entity disambiguation model in the semantic tool, we build
them following the existing work (Zhang et al.,
2022; Shu et al., 2022).
After instruction tuning, for in-domain datasets,
we evaluate the performance of our KG-Agent
on the test set of CWQ, WebQSP, KQA Pro, and
the dev set of GrailQA. For out-domain datasets,
we evaluate the zero-shot performance of our
KG-Agent on the NQ-Wiki, TQ-Wiki, and WQFreebase. For the domain specific dataset, _i.e.,_
MetaQA, we follow existing work (He et al., 2021;
Jiang et al., 2023b) to extract the one-shot tuning
subset from the original training set and fine-tune
our KG-Agent with it. When evaluating the performance of Davinci-003, ChatGPT, and GPT4,
we use the latest February version of APIs from
OpenAI. And for in-domain datasets, we provide
six demonstrations for each test question and parse
the prediction results following existing work (Sun
et al., 2023; Jiang et al., 2023b), we show the
prompt with demonstration for each dataset in Table 7. For the selection of demonstrations, we
randomly sample from the corresponding training
set for each dataset. For out-domain datasets, since
they are open-domain question answering tasks,
we directly input the question to LLMs with proper
prompt, as shown in Table 7.


**B** **Summary of Toolbox**


We summarize the tool name, tool description, and
the input argument and output of tools in Table 8.


**Dataset** **Prompt**



**WebQSP**


**CWQ**


**GrailQA**


**KQA Pro**


**NQ-Wiki**
**TQ-Wiki**
**WQ-Freebase**



Question: where is the syracuse university?
Answer: [New York | Syracuse | United States of America].
Question: where is the mtv headquarters?
Answer: [New York City].
Question: what are the 3 official languages of spain?
Answer: [Spanish Language].
Question: what timezone is new england usa in?
Answer: [Eastern Time Zone].
Question: who started southwest airlines?
Answer: [Herb Kelleher | Rollin King].
Question: what was irving langmuir famous for?
Answer: [Scientist].
Question: {test question}
Answer:


Question: Who is the president in the place where the government of Peru is located?
Answer: [Ollanta Humala].
Question: Where did Martin Luther King attend university, that has less than 2,586 undergraduates?
Answer: [Morehouse College].
Question: What movie produced by the company New Line Cinema was Taylor Lautner in?
Answer: [Valentine’s Day].
Question: Which year did the team that plays at Turner Field win the World Series?
Answer: [1995 World Series].
Question: Which airports are in the circulation area of Il Manifesto?
Answer: [Leonardo da Vinci–Fiumicino Airport | Ciampino–G. B. Pastine International Airport].
Question: What were the professions held by the publisher of "The Awakening?"?
Answer: [Businessperson | Novelist | Writer | Author].
Question: {test question}
Answer:


Question: what does the thiokol rocket do?
Answer: [Launch vehicle].
Question: what is the club interest of inverness yacht club?
Answer: [Sailing].
Question: who is the tour operator of kiribati?
Answer: [Fly Water Adventures | Kiribati Holidays | Otintaai Tours | Molloy’s Tours].
Question: 1998 marsala vergine terre arse contains what type of grapes?
Answer: [Catarratto | Grillo | Ansonica].

Question: [how many ice hockey coaches have coached the team]
that is currently coached by the eisbaren berlin?
Answer: [1].
Question: court of appeal of sri lanka has what inferior court?
Answer: [Supreme Court of Sri Lanka].
Question: {test question}
Answer:


Question: Which website officially represents Morgan Creek Productions?
Answer: [http://www.morgancreek.com/].

Question: [Which is shorter: The Killers, with a story set in Los Angeles,]
or Sherlock Holmes, produced by 20th Century Fox?
Answer: [Sherlock Holmes].
Question: What is the street address for the University of San Diego?
Answer: [5998 Alcala Park, San Diego, CA, 92110-2492].
Question: How is the Francis Bacon who died in New Haven related to the Yale School of Medicine?
Answer: [educated at].
Question: For the film titled Aladdin, where is it published on its publication date of 2019-05-24?
Answer: [United States of America].
Question: Who wrote The Postman which was published in 1985?
Answer: [David Brin].
Question: {test question}
Answer:


Answer the following question with one or few words. Question: {test question}



Table 7: The prompts used for each dataset when evaluating the ChatGPT, Davinci-003, and GPT-4 models. When
performing evaluation, just replace the “{test question}” with the test question.


**Type** **Tool** **Description**


get_relation Input: entity set _{e} →_ Output: one-hop relations _R{e}_
Return the incoming and outgoing relations of the given entity set _{e}_ on KG.


Input: entity set _{e}_, relation _r →_ Output: entity set _{e}_
get_head_entity
Return the head entity set of the given tail entity set _{e}_ along the relation _r_ .


Input: entity set _{e}_, relation _r →_ Output: entity set _{e}_
get_tail_entity
Return the tail entity set of the given head entity set _{e}_ along the relation _r_ .



Extraction
Tool


Logic
Tool


Semantic
Tool



Input: string type _t →_ Output: entity set _{e}_
get_entity_by_type
Return the entity set belonging to the given type _t_ .



Input: string entity mention _m →_ Output: entity set _{e}_
get_candidate_entity
Return the candidate linked entity set on the KG for the given entity mention _m_ .


Input: entity set _{e} →_ Output: integer
count
Return the number of entities in the given entity set _{e}_ .


Input: entity set list [ _{e}_ ] _→_ Output: entity set _{e}_
intersect
Return the intersection of the given list of entity sets.


Input: entity set list [ _{e}_ ] _→_ Output: entity set _{e}_
union
Return the union of the given list of entity sets.


Input: entity set _{e}_, relation _r_, operator _o_, string value _v →_ Output: boolean
judge
Return a boolean value indicating whether the comparison between the tail entity of
the given entity set _{e}_ along relation _r_ and the given value _v_ satisfies the operator _o_ .


Input: entity set _{e} →_ Output: entity set _{e}_
end
Return the entity set as the final answer and end the reasoning process.


Input: relation set _{r} →_ Output: relation set _{r}_
retrieve_relation Retrieve relations from the given relation set _{r}_ that are
semantically relevant to the question through neural network.


Input: entity set _{e} →_ Output: entity _e_
disambiguate_entity
Disambiguate the candidate linked entity _{e}_ based on the question semantics
and entity information on KG ( _e.g.,_ one-hop relations) through neural network.


Table 8: The detailed definition and usage of all the tools.



get_entity_by_constraint



Input: entity set _{e}_, relation _r_, operator _o_, string value _v →_ Output: entity set _{e}_
Return the new entity set whose tail entity along _r_ satisfies the constraint condition.
If _v_ is not empty, the _o_ should be one of {“=”,“>”,“>=”,“<”,“<=”}, which means
the comparison between the tail entity and string value should satisfy the operator.
Else, the _o_ should be one of {“argmax”,“argmin”}, which means the tail entity
should be the maximum or minimum value.


