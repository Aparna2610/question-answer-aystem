------------------------------------README--------------------------------------

>>>>>>>>>>>>>>>>>>>>>>>>>>>Question Answering System<<<<<<<<<<<<<<<<<<<<<<<<<<<<

Based on the information retrieval techniques from Chapter 23 of Speech and
Language Processing by Dan Jurafsky and Chris Martin.
This README has the following sections:
1. Running the System
2. Testing the System Performance
3. Dataset Used
4. Performance Measures
5. Querying Flow
6. Parsing the Text Flow
7. External libraries Used
8. Sample Questions for Each Dataset

--------------------------------------------------------------------------------
Running the System:
> python P2.py articles\Force.txt

--------------------------------------------------------------------------------
Testing the System Performance:

To get the accuracy for the system, for all datasets:
> python TestQas.py

--------------------------------------------------------------------------------
Dataset Used:
The datasets used have been extracted from The Stanford Question Answering
Dataset(SQUAD). The SQUAD set contains various topics and each topic has a set
of paragraphs associated to it. The system is fed with a concatenated form of
these paragraphs which serves as its knowledge base.

Ref: https://rajpurkar.github.io/SQuAD-explorer/

--------------------------------------------------------------------------------
Performance Measures:

System performance is measured by accuracy, i.e., the ratio of correct answers
and total questions in a dataset.
The average performance of the system is 77.19%.
The following are the performance for the datasets:

+---------------------------------------------------------------------+
|         Dataset       | No of Ques  | Correct Answers  |  Accuracy  |
+---------------------------------------------------------------------+
|   Amazon_rainforest   |    173      |       138        |   79.76%   |
|         Force         |    201      |       156        |   77.61%   |
|  Newcastle_upon_Tyne  |    250      |       193        |   77.2%    |
|     Construction      |    96       |       73         |   76.04%   |
| French_and_Indian_War |    150      |       113        |   75.33%   |
+---------------------------------------------------------------------+

--------------------------------------------------------------------------------
Querying Flow:

The system looks for keywords and identifies questions into the following types:
PERSON, LOCATION, TIME, SUMMARY
The first three types are factoid questions and return only a single value as
answer.
The Summary type returns a statement for an answer. Summary type questions
are based on keywords: what, how and why.

--------------------------------------------------------------------------------
Parsing the Text Flow:

Once the query is entered by the user, the paragraphs are ranked based on tf-idf
weighed cosine. The system then checks the k-most relevant paragraphs(k=3, for
this system). Ranks the sentences in the same format.

The sentences and paragraphs are parsed using NLTK for finding tf-idf weighed
cosine similarity. The sentence is tokenized, followed by removal of stop words.
The tokens are further filtered to discard the punctuations and empty tokens,
followed by stemming using Porter Stemmer. The tokens are the POS tagged and
Named Entity Recognition is applied to them. The system then retrieves the most
relevant named entity that matches the query type.

--------------------------------------------------------------------------------
Dependencies:

1. NLTK: for tokenizing, stemming, getting a list of stop words, pos_tagging and
NER(Named Entity Recognition) via ne_chunk.
2. Timex: Code for tagging temporal expressions in text by eGenix.com,
explicitly submitted as TemporalValGetter.py
        (https://github.com/openeventdata/phoenix_pipeline/blob/master/timex.py)

--------------------------------------------------------------------------------
Sample Questions for each Dataset:

The questions include who, what, how, where, how many, etc. kind of types extracted from
the dataset.

>>>>>>>>For Amazon_rainforest.txt:


Q: How many nations control this region in total?
A: This region includes territory belonging to nine nations.
Q: What is the estimate for the amount of tree species in the amazon tropical rain forest?
A: the total number of tree species in the region is estimated at 16,000.
Q: During what time did the rainforest spanned a narrow band?
A: during the oligocene, for example, the rainforest spanned a relatively narrow band.
Q: Savannah areas expanded over the last how many years?
A: climate fluctuations during the last 34 million years have allowed savanna regions to expand into the tropics.
Q: How many nations contain "Amazonas" in their names?
A: states or departments in four nations contain "amazonas" in their names.
Q: Who was the first European to travel the Amazon River?
A: francisco de orellana
Q: Why is it difficult to resolve disagreements about the changes in the Amazon rainforest?
A: this debate has proved difficult to resolve because the practical limitations of working
in the rainforest mean that data sampling is biased away from the center of the amazon basin,
and both explanations are reasonably well supported by the available data.
Q: In which point did the drainage basin of the Amazon split?
A: question type not supported. do you have any other question ?
Q: Did the rainforest managed to thrive during the glacial periods?
A: question type not supported. do you have any other question ?
Q: What basin was formed when the Andes Mountains rose?
A: could not find the answer to your query.. do you have any another question


>>>>>>>>For Force.txt:


Q: Who discovered that magnetic and electric could self-generate?
A: maxwell
Q: Who expounded the Three Laws of Motion?
A: isaac
Q: When did the origins of magnetic and electric fields occur?
A: 1864
Q: Who made the first to measure value of the Newton Universal Gravitation Constant?
A: henry
Q: Who developed the theory of relativity?
A: einstein
Q: Who first described dynamic equilibrium?
A: galileo
Q: How long did it take to improve on Sir Isaac Newton's laws of motion?
A: with his mathematical insight, sir isaac newton formulated laws of motion
that were not improved-on for nearly three hundred years.
Q: Whatare the electrostatic and magnetic force awritten as the sum of?
A: question type not supported. do you have any other question ?
Q: What is the intrisic angular variable called when particles act upon one another?
A: could not find the answer to your query.. do you have any another question
Q: What includes pressure terms when calculating area in volume?
A: could not find the answer to your query.. do you have any another question


>>>>>>>>For Newcastle_upon_Tyne.txt:


Q: When did the DFDS ferry service to Sweden case operation?
A: 2006
Q: How many LEA-funded 11 to 18 schools are there in Newcastle?
A there are eleven lea-funded 11 to 18 schools and seven independent schools with sixth forms in newcastle.
Q: Who constructed Newcastle's station?
A: robert
Q: When did Newcastle's first indoor market open?
A: 1835
Q: Who granted Newcastle a new charter in 1589?
A: elizabeth
Q: What bus company in Newcastle provides the majority of services south of the river?
A: go-ahead operates from eldon square bus station, providing the majority of
services south of the river in gateshead, south tyneside, sunderland, and county durham.
Q: How many phases was the Metro opened in between 1980 and 1984?
A: it was opened in five phases between 1980 and 1984, and was britain's first urban
light rail transit system; two extensions were opened in 1991 and 2002.
Q: When is the Evolution Festival hosted?
A: could not find the answer to your query.. do you have any another question


>>>>>>>>For Construction.txt:


Q: Infrastructure is often called what?
A: infrastructure is often called heavy/highway, heavy civil or heavy engineering.
Q: In what year did ENR compile data in nine market segments?
A: in 2014, enr compiled the data in nine market segments.
Q: How many firms were existing in 2005?
A: as of 2005, there were about 667,000 firms employing 1 million contractors
Q: What is the most common cause of injury on site?
A: falls are one of the most common causes of fatal and non-fatal injuries among construction workers.
Q: How many women were employed in construction in 2011?
A: in the united states, approximately 828,000 women were employed in the construction industry as of 2011.
Q: What happens as they build phase 1?
A: as they build phase 1, they design phase 2.
Q: In the most common construction procurement, who acts as the project coordinator?
A: could not find the answer to your query.. do you have any another question


>>>>>>>>For French_and_Indian_War.txt:


Q: What was Marin's orders?
A: his orders were to protect the king's land in the ohio valley from the british.
Q: Why did British operation fail in 1755, 56, 57?
A: british operations in 1755, 1756 and 1757 in the frontier areas of
pennsylvania and new york all failed, due to a combination of poor management,
internal divisions, and effective canadian scouts, french regular forces, and indian warrior allies.
Q: What territory was ceded to Britain?
A: france ceded its territory east of the mississippi to great britain.
Q: What areas did French recruit natives from?
A: when war broke out, the french used their trading connections to recruit
fighters from tribes in western portions of the great lakes region (an area not
directly subject to the conflict between the french and british), including the
huron, mississauga, ojibwa, winnebago, and potawatomi.
Q: What was Old Briton's response to Celeron?
A: "old briton" ignored the warning.
Q: When did British government give land for development of Ohio Country?
A: 1749
Q: What title did Iroquois give Johnson?
A: in 1746, johnson was made a colonel of the iroquois.
Q: When did British begin to build fort under William Trent?
A: 1754
Q: Was was the plan for Langlades mission?
A: question type not supported. do you have any other question?
Q: When did French learn about Braddock's plans?
A: could not find the answer to your query.. do you have any another question?
