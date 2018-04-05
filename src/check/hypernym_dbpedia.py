from mine.dbpedia import articles_with_hypernym,CLURI,CFFURI
from data import DATAP, CLDEPTH, CFFDEPTH


def check_dbpedia_hypernym(langdict):
    print("Checking Dbpedia Hypernym")
    cls = articles_with_hypernym(CLURI, 0, CLDEPTH, "Language") + articles_with_hypernym(CFFURI, 0, CFFDEPTH, "Language")
    cffs = articles_with_hypernym(CLURI, 0, CLDEPTH, "Format") + articles_with_hypernym(CFFURI, 0, CFFDEPTH, "Format")
    for cl in langdict:
        if (cl in cls) or (cl in cffs):
            langdict[cl]["DbpediaHypernym"] = 1
        else:
            langdict[cl]["DbpediaHypernym"] = 0
    return langdict


if __name__ == '__main__':
    import json
    with open(DATAP+'/langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        langdict = check_dbpedia_hypernym(langdict)
        f.close()
    with open(DATAP+'/langdict.json', 'w',encoding="UTF8") as f:
        json.dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()