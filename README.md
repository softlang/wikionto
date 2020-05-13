# wikionto
Wikipedia-based ontology engineering

## Indicator Discovery
This information is related to the paper accepted at SEKE2019.

```
@inproceedings{HeinzLA19,
  author    = {Marcel Heinz and
               Ralf L{\"{a}}mmel and
               Mathieu Acher},
  editor    = {Angelo Perkusich},
  title     = {Discovering Indicators for Classifying Wikipedia Articles in a Domain
               - {A} Case Study on Software Languages},
  booktitle = {The 31st International Conference on Software Engineering and Knowledge
               Engineering, {SEKE} 2019, Hotel Tivoli, Lisbon, Portugal, July 10-12,
               2019},
  pages     = {541--706},
  publisher = {{KSI} Research Inc. and Knowledge Systems Institute Graduate School},
  year      = {2019}
}
```

* Current datasets and evaluation data can be found at https://github.com/softlang/wikionto/tree/seke19/data/datasets.
* Added natural language tests based on Stanford Parser. CoreNLPServer must be started before using the tests. 
* See below for more instructions and manuals for reproduction.

### Reproduce the Dataset

* Required technology: 
  * Too many to list here, inspect the below referenced files. 
  * Download Stanford Core NLP: https://stanfordnlp.github.io/CoreNLP/index.html#download. You need to run a CoreNLP Server for reproducing results.
  
* How to reproduce results:
  1. The file **src/data/__init__.py** serves as the core configuration. You need to enter depth level, and root categories.
  2. Run **src/mine/pipeline.py**. The process creates an annotated dictionary of article titles. Most data is mined from DBpedia.
  3. Run **src/check/seed.py** for annotating whether an articles is a seed.
  4. **src/classify/decision_tree.py** configures the decision tree classifier.

Be careful when inspecting other scripts. Many scripts explore indication directly in an active learning manner.

### Querying the Dataset
Having the titles as keys of article dictionaries allows convenient querying in the Python Console of Pycharm. For example: 
```
from data import load_articledict`
ad = load_articledict()
# Get all articles with 'language' as the retrieved hypernym:
[a for a in ad if "COPHypernym" in ad[a] and "language" in ad[a]["COPHypernym"]]
# Get all articles classified as relevant for software languages.
[l for l,ld in ad.items() if ld["Class"]=='1']
```

For each entry in the two seed sets we ...
* ... annotate it on whether ...
  * ... we can match it with an article.
  * ... we find an article, but it does not provide traces of software language knowledge.
  * ... we cannot find a matching articles even by using variations of the name and Wikipedia's search engine.

### Github Seed

* For the original list, look at https://github.com/softlang/wikionto/blob/master/data/gitseed.txt
* For the matchings look at https://github.com/softlang/wikionto/blob/master/data/gitseed_annotated.json

### TIOBE Index

* For the original list, look at https://github.com/softlang/wikionto/blob/master/data/TIOBE_index_list.txt
* For the matchings look at https://github.com/softlang/wikionto/blob/master/data/TIOBE_index_annotated.json

### Merged Seed

See https://github.com/softlang/wikionto/blob/master/data/seed_annotated.json

### Survey Principles 
There are two main points that need to be analyzed. (1) Statistical significance, going from representative sample size (either of data for ML labiling or of people for social/opinion surveys). (2) Facial validation: Through the survey, do we measure what we intend to measure? This needs a discussion especially on threats to validity. Both points are intertwined.

For our survey, we intend to measure for each article, whether it can be detected as describing a software language. We want to take this measure to evaluate an ML classifier. So, the decision cannot be made based on background knowledge alone, but based on knowledge that is there in the text. If it is not made explicit in the text no machine can recognize it and the article should not be added even if the title is 'Java (programming language)'. If an expert still tells that it is a language even though it is not explicitly stated, this corrupts the measurement. The corruption is a threat to the usefulness of the survey. We tried to counter it by:

1. Providing an informal definition what a software language is. (This definition may not be final, because final definitions are complex. A final definition also depends on the task where such definition is used. If we want to recognize languages used in projects, then this implies a certain useful definition of a software language as well, which is why we state that there are digital artifacts and not sketches on paper. This thought goes into the direction on how ontologies are evaluated based on the task they are used for and multiple ontologies exist for the same domain.)

2. Mixing in 9 seed articles. 5 at the beginning and 4 randomly mixed in. This allows us to measure whether a participant has the ability to recognize a description of a software language. We only recall seed articles, where the summary explicitly describes a language. From such description we have to be able to learn further knowledge about the language. Otherwise it is just a casual mention and worthless information.

3. The mixed in seed articles reduce fatigue. As stated in the abstract `Be careful not to miss relevant articles.'. If less software language articles existed in a questionnaire, the reader might become more careless.

4. We recommend voting by tendency and commenting in difficult cases. Sometimes, even explicit descriptions may not be clearly formulated and are matter to interpretation. Natural language is context sensitive. Since natural language text provides the decision ground, we have to acknowledge that things may be a matter to interpretation.

5. Embedding the Wikipedia article also reduces fatigue and the risk that someone closes the tab where the survey is opened by accident.

6. The hints help with decision ground and prime towards a certain way of decision making. The participant is not supposed to become too careless and decide by an article's title or only based on the first sentence. The hints raise awareness of the issue that we are interested in a fine grained level of detection and multiple topics are described as major topics instead of one.

7. We tracked the time every participant took per page. The time spent on the page that contains the primer might tell us how well someone read what to look out for. The time should go up for difficult questions as well.

Altogether, the matter of subjectivity and personal understanding of when to say that an article describes a software language is reduced because a decision ground is provided. The only problem is that participants might not follow the hints and still decide by gut feeling (and the given definition alone).
