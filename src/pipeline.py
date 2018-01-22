from collections import defaultdict
from check.gitseed import check_gitseed
from check.infobox import check_infobox
from check.hypernym_dbpedia import check_purlHypernymLanguage
from check.hypernym_stanford import check_stanford
from check.hypernym_wordnet import check_wordnet_hypernym
from check.semantic_distance import check_semantic_distance
from json import dump

f = open('data/softwarelanguages.csv','r',encoding="utf8")
next(f) 
langdict = defaultdict(dict)
for line in f:
    cl = line.split("\t")[0]
    langdict[cl]["ClDepth"] = line.split("\t")[1]
    langdict[cl]["CffDepth"] = line.split("\t")[2]
f.close
    
langdict = check_gitseed(langdict)
langdict = check_infobox(langdict)
langdict = check_purlHypernymLanguage(langdict)
langdict = check_stanford(langdict)
langdict = check_wordnet_hypernym(langdict)
langdict = check_semantic_distance(langdict)

with open('langdict.json', 'w') as f:
    dump(obj=langdict, fp=f, indent=2)
    f.flush()
    f.close()