from nltk.corpus import wordnet as wn
from nltk import download

download('wordnet')

def check_wordnet_hypernym(langdict):
    print("Checking Wordnet Hypernym")
    for cl in langdict:
        langdict[cl]["WordnetHypernym"] = is_hyponym(cl)
    return langdict

def is_hyponym(cl):
    for syn in wn.synsets(cl):
        for hyp in syn.hypernyms():
            if('language' in str(hyp))|('format' in str(hyp))|('dsl' in str(hyp))|('dialect' in str(hyp)):
                return True
    return False