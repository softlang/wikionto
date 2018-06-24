from data import DATAP, DEPTH, CATS
from json import load, dump
from mine.dbpedia import articles_with_commons, to_uri


def check_eponymous(catdict, langdict):
    print("Checking for Eponymous")
    for cat in catdict:
        catdict[cat]["Eponymous"] = int(cat in langdict)

    # TODO: http://live.dbpedia.org/property/commons for Java : Category:Java (en)
    for c in CATS:
        cls = articles_with_commons(to_uri(c), 0, DEPTH)
        for cl in cls:
            for cat in cls[cl]:
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
