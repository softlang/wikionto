from nltk.corpus import wordnet
from nltk import download
import re

download('wordnet')

def check_wordnet_hypernym(langdict):
    print("Checking Wordnet Hypernym")
    for cl in langdict:
        langdict[cl]["WordnetHypernym"] = is_hyponym(cl)
    return langdict

def is_hyponym(cl):
    cl = namenorm(cl)
    for syn in wordnet.synsets(cl):
        for hyp in syn.hypernyms():
            if('language' in str(hyp))|('format' in str(hyp))|('dsl' in str(hyp))|('dialect' in str(hyp)):
                return 1
    return 0

def namenorm(name):
    x = re.sub("\(.*?\)", "", name).lower().strip()
    x = re.sub("[_]","",x).strip()
    return x