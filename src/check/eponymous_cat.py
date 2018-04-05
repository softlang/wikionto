from data import DATAP, CLDEPTH, CFFDEPTH
from json import load, dump
from mine.dbpedia import articles_with_commons, CLURI, CFFURI


def check_eponymous(catdict, langdict):
    print("Checking for Eponymous")
    for cat in catdict:
        catdict[cat]["Eponymous"] = int(cat in langdict)

    acdictcl = articles_with_commons(CLURI, 0, CLDEPTH)
    acdictcff = articles_with_commons(CFFURI, 0, CFFDEPTH)
    for cl in acdictcl:
        for cat in acdictcl[cl]:
            if cat in catdict:
                catdict[cat]["Eponymous"] = 1
    for cl in acdictcff:
        for cat in acdictcff[cl]:
            if cat in catdict:
                catdict[cat]["Eponymous"] = 1
    return catdict


if __name__ == "__main__":
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    with open(DATAP + '/catdict.json', 'r', encoding="UTF8") as f:
        catdict = load(f)
        catdict = check_eponymous(catdict, langdict)
        f.close()
    with open(DATAP + '/catdict.json', 'w', encoding="UTF8") as f:
        dump(obj=catdict, fp=f, indent=2)
        f.flush()
        f.close()
