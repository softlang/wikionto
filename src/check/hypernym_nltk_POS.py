from mine.dbpedia import articles_with_summaries,CFFURI,CLURI
from nltk.tag.stanford import CoreNLPPOSTagger

def check_nltk_pos(langdict):
    print("Checking Hypernym with Stanford")
    clarticles = articles_with_summaries(CLURI,0,7)
    cffarticles = articles_with_summaries(CFFURI, 0, 7)
    for a,summary in clarticles + cffarticles:
        if is_language(summary):
            langdict[a]["StanfordHypernym"] = True
    return langdict

def is_language(summary):
    tagged = CoreNLPPOSTagger(url='http://localhost:9000').tag(summary.split())
    vbzs = {(w,p) for (w,p) in tagged if (p=="VBZ") & ("is" in w)}
    nns = {(w,p) for (w,p) in tagged if (p=="NN") & (("language" in w) | ("format" in w))}
    return vbzs & nns # apply bool here

#You can run this for test purposes after starting the server
text = "Java is a programming language."
tagged = CoreNLPPOSTagger(url='http://localhost:9000').tag(text.split())
print(tagged)