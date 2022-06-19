## 报告提纲

### 1.选题背景

<u>说明本课题应解决的主要问题及应达到的技术要求，简述本设计的指导思想。</u>

直接照抄要求即可。

### 2.方案论证

<u>说明设计原理（理念）并进行方案选择，阐明为什么要选择这个设计方案以及所采用方案的特点。重点说明要实现的功能及其要求、系统的安全性、数据的完整性、应用的运行环境及其性能等要求。</u>

按软工课说的那样，先写我们有什么需求（比如分词需要有效率，需要分词准确度高，需要便于用户操作，数据完整性、系统安全性balabala），而我们选用的算法/模块有什么优势（比如jieba分词效率高，准确度高，封装性好，便于操作）

#### scheme design和parameter

- [ ] 修改workflow图
- [ ] 画一个数据流图
- [ ] 表格重要的参数与说明

#### 粒度控制

论证每次迭代读取的语料库大小，从迭代用时、新词发现数量、分出的词的总量等指标来看，做一个对比表格

#### 字典数据库的存储与更新

用txt?用mysql?关于如何维护，谈谈为什么要建立数据库。

#### 初始词库的考虑

清华的词库给我们提供分类

搜狗的词库给我们提供词性

虽然结巴分词也自带词性，但是（摆出具体词性数量的对比，举一些例子）没有搜狗词库的效果好

给出训练的准确度（也可能放到结果分析那里）

#### 爬取语料库的理念

效率问题，选取语料库的考虑

#### 分词的工具：结巴分词

扯一下结巴分词的算法优越在哪里

As the massive words dictionary construction tool is required to obtain separated words from tens of millions of words in the corpus, there is no doubt that the Chinese text segmentation is a module of vital significance in the software. Among those famous text segmentation tools, we chose Jieba Chinese text segmentation, considering both the performance and the function.

Specifically speaking, our requirements for the text segmentation module include these aspects. First of all, the word segmentation should be accurate enough so that the subsequent word sorting and dictionary construction can be accurate. Secondly, the word segmentation should support user defined dictionary so that the word segmentation can evolve as the dictionary updated iteratively. Last but not least, the efficiency of both the loading of dictionary and segmentation should be ensured, so that the massive dictionary construction can be efficient enough to meet the users' demand.

With 28.8k stars on GitHub and used by 13.2k GitHub developers, Jieba Chinese text segmentation has been one of the most popular Chinese Natural Language Processing tools since its birth on last decade. Jieba Chinese text segmentation is built to be the best Python Chinese word segmentation module, with an MIT license. The details of the word segmentation tool is available at https://github.com/fxsjy/jieba.

From the aspects of functions, jieba Chinese word segmentation support 3 types of segmentation mode including Accurate Mode, Full Mode and Search Engine Mode. In addition, it supports traditional Chinese as well as customized dictionaries. The segmentation tool realize these functions with these fundamental designs:

- Based on a prefix dictionary structure to achieve efficient word graph scanning. Build a directed acyclic graph (DAG) for all possible word combinations.
- Use dynamic programming to find the most probable combination based on the word frequency.
- For unknown words, a HMM-based model is used with the Viterbi algorithm.

From the aspect of performance, the segmentation speed is fast enough to meet our needs of efficient massive dictionary construction:

- 1.5 MB / Second in Full Mode
- 400 KB / Second in Default Mode
- Test Env: Intel(R) Core(TM) i7-2600 CPU @ 3.4GHz；《围城》.txt

#### 分类的工具：gensim

Gensim（generate similarity）是一个简单高效的自然语言处理Python库，用于抽取文档的语义主题（semantic topics）。Gensim的输入是原始的、无结构的数字文本（纯文本），内置的算法包括Word2Vec，FastText，潜在语义分析（Latent Semantic Analysis，LSA），潜在狄利克雷分布（Latent Dirichlet Allocation，LDA）等，通过计算训练语料中的统计共现模式自动发现文档的语义结构。这些算法都是非监督的，这意味着不需要人工输入——仅仅需要一组纯文本语料。一旦发现这些统计模式后，任何纯文本（句子、短语、单词）就能采用语义表示简洁地表达。

##### 特点
-Memory independence： 不需要一次性将整个训练语料读入内存，Gensim充分利用了Python内置的生成器（generator）和迭代器（iterator）用于流式数据处理，内存效率是Gensim设计目标之一。
-Memory sharing： 训练好的模型可以持久化到硬盘，和重载到内存。多个进程之间可以共享相同的数据，减少了内存消耗。
-多种向量空间算法的高效实现： 包括Word2Vec，Doc2Vec，FastText，TF-IDF，LSA，LDA，随机映射等。
-支持多种数据结构。
-基于语义表示的文档相似度查询。

#### 监控系统

（抄PPT里的模板）

### 3.过程论述

<u>重点说明设计是如何实现的，包括：对设计工作的详细表述。要求层次分明、表达确切。要求：每个图都必须有文字说明，图前说明为什么使用该图、图的主要作用；图后说明图中各成分的作用，和成分之间的交互或图所表达的流程。</u>

把**各个模块**，**各个函数**的**input**和**output**都写一下，把代码里的逻辑说明一下即可。围绕着workflow图和数据流图写即可。

用语言难以描述的可以搞几个示意图。

#### 爬取语料库

#### 分词

#### 新词发现

#### 分类

##### 获取训练数据
1. SougouLabDic: 提供共157202个词语的文本，词频以及词性信息
2. THUOCL（清华大学开源词库）：提供11个分类下词语的文本及词频信息。11个分类分别为：animal,caijing,car,chenyu,diming,food,it,law,lishimingren,medical,poem

##### 训练数据处理
- 词语分类：将THUOCL中词语提取出来，将词频的对数作为个数插入进列表，并赋予文件夹名作为标签。同时将SougouDic中的词语依照同样方式插入列表，区别在于标签设为"other"
- 词性分类：只讲将SougouDic插入进列表，同时将第三列的词性转化为列表，列表长度为17，与SougouDic中提供的17种词性对应，存在的词性设为1，其余设为0。

##### word2vec
导入腾讯ailab提供的预训练好的word2vec模型。直接导入时间过久，便将模型转换为二进制文件保存便于后续读取。导入后的文件可被视作字典。若文本存在于键中，则直接导出一个100维的列表，否则随机生成一个100维的列表。

##### 训练模型
#### 构建新词典

#### 对数据库的初始化与数据库的访问

### 4.结果分析

<u>对研究过程中所获得的主要的数据、现象进行定性或定量分析，得出结论和推论。</u>

设计测试用例，定量说明

#### 功能测试

把各个模块测试的测试用例列一下，把结果图截下来

#### 性能测试

测各个模块的时间

#### 压力测试

1.跟方案论证里的粒度的测试很像，看看一次迭代要读取很大的文件时会发生什么事情

2.试一下输入很大的迭代次数（超过最大迭代次数，比如100000与不超过最大迭代次数的，比如100），看看输出的各项指标，跟一个普通的迭代次数（比如10）的各项指标对比

### 5.课程设计总结

<u>课程设计过程的收获、遇到的问题，遇到问题解决问题过程的思考、程序调试能力的思考，课程设计实现过程中的收获和体会等。</u>

