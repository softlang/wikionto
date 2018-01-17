from mine.dbpedia import articles_with_summaries,CFFURI,CLURI
from nltk.parse.corenlp import CoreNLPDependencyParser

def check_stanford_cop(langdict):
    print("Checking Hypernym with Stanford")
    # ('is', 'VBZ') and ('language', 'NN')
    clarticles = articles_with_summaries(CLURI,0,7)
    cffarticles = articles_with_summaries(CFFURI, 0, 7)
    for a,summary in clarticles + cffarticles:
        if is_language(summary):
            langdict[a]["StanfordHypernym"] = True
    return langdict

def is_language(summary):
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    tagged = dep_parser.raw_parse(summary)
    #TODO: Analyze dependencies
    return True