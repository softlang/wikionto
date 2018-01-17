from collections import defaultdict
from check.gitseed import check_gitseed
from check.infobox import check_infobox
from check.hypernym_dbpedia import check_purlHypernymLanguage
from check.hypernym_nltk_POS import check_nltk_pos
from check.hypernym_stanford_cop import check_stanford_cop
from check.semantic_distance import check_semantic_distance
import json

f = open('data/softwarelanguages.csv','r',encoding="utf8")
langdict = defaultdict(dict)
for line in f:
    cl = line.split("\t")[0]
    langdict[cl]["ClDepth"] = line.split("\t")[1]
    langdict[cl]["CffDepth"] = line.split("\t")[2]
f.close
    
langdict = check_gitseed(langdict)
langdict = check_infobox(langdict)
langdict = check_purlHypernymLanguage(langdict)
langdict = check_nltk_pos(langdict)
#langdict = check_stanford_cop(langdict)
langdict = check_semantic_distance(langdict)

with open('langdict.json', 'w') as f:
    json.dump(langdict, f)
    f.flush()
    f.close()