from nltk.corpus import wordnet as wn
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
    for syn in wn.synsets(cl):
        for hyp in syn.hypernyms():
            if('language' in str(hyp))|('format' in str(hyp))|('dsl' in str(hyp))|('dialect' in str(hyp)):
                return 1
    return 0

def namenorm(name):
    x = re.sub("\(.*?\)", "", name).lower().strip()
    x = re.sub("[_]","",x).strip()
    return x

if __name__ == '__main__':
    import json
    with open('../data/langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        langdict = check_wordnet_hypernym(langdict)
        f.close()
    with open('../data/langdict.json', 'w',encoding="UTF8") as f:
        json.dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()