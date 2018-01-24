from mine.dbpedia import articles_with_summaries,CFFURI,CLURI
from nltk.tag.stanford import CoreNLPPOSTagger
from nltk.parse.corenlp import CoreNLPDependencyParser


def check_stanford(langdict):
    print("Checking Hypernym with Stanford")
    clarticles = articles_with_summaries(CLURI,0,6)
    cffarticles = articles_with_summaries(CFFURI, 0, 6)
    for a,summary in clarticles + cffarticles:
        langdict[a]["StanfordPOSHypernym"] = pos_language(summary)
        langdict[a]["StanfordCOPHypernym"] = cop_language(summary)
    return langdict

def pos_language(summary):
    tagged = CoreNLPPOSTagger(url='http://localhost:9000').tag(summary.split())
    vbzs = {(w,p) for (w,p) in tagged if (p=="VBZ") & ("is" in w)}
    nns = {(w,p) for (w,p) in tagged if (p=="NN") & (("language" in w) | ("format" in w))}
    return bool(vbzs & nns) 

def cop_language(summary):
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    parse, = dep_parser.raw_parse(summary)
    for subj, dep, obj in parse.triples():
        if (subj[1]=='NN')&(subj[0] in ['language','format','dsl','dialect']) & (dep=='cop') & (obj==('is','VBZ')):
            return True
    return False
#You can run this for test purposes after starting the server
text = "Java is a programming language."
tagged = CoreNLPPOSTagger(url='http://localhost:9000').tag(text.split())
dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
parse, = dep_parser.raw_parse(text)
print(tagged)
print(parse.triples())