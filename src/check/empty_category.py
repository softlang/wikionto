from json import load

def check_empty_cat(catdict,langdict):
    print("Checking for categories with no relevant articles")
    for cat in catdict:
        if not "articles" in catdict[cat]:
            catdict[cat]["NonEmptyCategory"] = 0
        else:
            some = list(filter(lambda cl: not lang_succeeds_at_none(cl,langdict),catdict[cat]["articles"]))
            if not some:
                catdict[cat]["NonEmptyCategory"] = 0
            else:
                catdict[cat]["NonEmptyCategory"] = 1
    return catdict

def lang_succeeds_at_none(lang,langdict):
    properties01 = ['DbpediaInfobox','DbpediaHypernym'
                    ,'StanfordPOSHypernym','StanfordCOPHypernym','WordnetHypernym'
                    ,'IncludedNamePattern']
    flag = bool(sum(map(lambda p:langdict[lang][p],properties01)))
    sr = langdict[lang]['SemanticallyRelevant'] > 1
    return flag | sr
    
def run_solo():
    import json
    f=open('../data/langdict.json', 'r',encoding="UTF8")
    langdict = load(f)
    with open('../data/catdict.json', 'r',encoding="UTF8") as f: 
        catdict = json.load(f)
        catdict = check_empty_cat(catdict,langdict)
        f.close()
    with open('../data/catdict.json', 'w',encoding="UTF8") as f:
        json.dump(obj=catdict, fp=f, indent=2)
        f.flush()
        f.close()
#run_solo()