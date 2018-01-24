from nltk.corpus import wordnet as wn
from nltk import download
from mine.dbpedia import articles_below,CLURI,CFFURI

download('wordnet')

def check_wordnet_hypernym(langdict):
    print("Checking Wordnet Hypernym")
    cls = articles_below(CLURI,0,6)
    cffs = articles_below(CFFURI,0,6)
    for cl in cls+cffs:
        langdict[cl]["WordnetHypernym"] = is_hyponym(cl)
    return langdict

def is_hyponym(cl):
    for syn in wn.synsets(cl):
        for hyp in syn.hypernyms():
            if('language' in str(hyp))|('format' in str(hyp))|('dsl' in str(hyp))|('dialect' in str(hyp)):
                return True
    return False