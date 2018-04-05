# wikionto
Wikipedia-based ontology engineering

* New version using Python.
* Added natural language tests based on Stanford Parser.
* CoreNLPServer must be started before using the tests. 

# How to use:
* Required technology using pip: 
  * sparqlwrapper
  * nltk
  * requests
* Download Stanford Core NLP: https://stanfordnlp.github.io/CoreNLP/index.html#download
* Start Server
  * Open the folder, where you deployed Stanford Core NLP.
  * Open a Terminal here.
  * Start the server using: `java -cp "*" -Xmx4g edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 150000 -quiet`
  * (Be sure that your computer's network settings allow connection to the created local host server.)
* Start pipeline
... (More soon)