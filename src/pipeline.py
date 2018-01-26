from check.gitseed import check_gitseed
from check.infobox import check_infobox
from check.hypernym_dbpedia import check_purlHypernymLanguage
from check.hypernym_stanford import check_stanford
from check.hypernym_wordnet import check_wordnet_hypernym
from check.semantic_distance import check_semantic_distance
from json import dump, load
import timeit

with open('data/langdict.json', 'r',encoding="UTF8") as f: 
    langdict = load(f)
    #langdict = check_gitseed(langdict)
    langdict = check_infobox(langdict)
    langdict = check_purlHypernymLanguage(langdict)
    start_time = timeit.default_timer()
    langdict = check_stanford(langdict)
    print(timeit.default_timer()-start_time)
    langdict = check_wordnet_hypernym(langdict)
    langdict = check_semantic_distance(langdict)
    f.close()

with open('data/langdict.json', 'w',encoding="UTF8") as f:
    dump(obj=langdict, fp=f, indent=2)
    f.flush()
    f.close()