# wikionto
Wikipedia-based ontology engineering

## Projects

This project addresses multiple challenges:
* How to recognize relevant articles based on a learned decision tree classifier?
* How to recognize subclasses based on clustering?
* How to recover classification information only by processing natural language text?

### Discovering Indicators for Classifying Wikipedia Articles in a Domain
This information is related to the paper accepted at SEKE2019 with regards to the challenge 
_How to recognize relevant articles based on a learned decision tree classifier?_

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
* We moved datasets and original scripts to the branch 'seke19'.
* Current datasets and evaluation data can be found at https://github.com/softlang/wikionto/tree/seke19/data/datasets.
* Added natural language tests based on Stanford Parser. CoreNLPServer must be started before using the tests. 
* See https://github.com/softlang/wikionto/tree/seke19/README.md for more instructions and manuals for reproduction.
