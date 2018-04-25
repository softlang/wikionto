from mine.dbpedia import articles_below
from data import DATAP

ex_cat = [
    "<http://dbpedia.org/resource/Category:Songs>",
    "<http://dbpedia.org/resource/Category:Astronomical_objects>",
    "<http://dbpedia.org/resource/Category:People>",
    "<http://dbpedia.org/resource/Category:Software>",
    "<http://dbpedia.org/resource/Category:Hardware>"
]


def check_reachable_by(langdict):
    for c in ex_cat:
        print("Checking reachable by "+c)
        xs = []
        for i in range(20):
            xs = xs + articles_below(c, i, i)
        for x in xs:
            if x in langdict:
                langdict[x][c] = 1
    return langdict


def solo():
    import json
    with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
        langdict = json.load(f)
        langdict = check_reachable_by(langdict)
        f.close()
    with open(DATAP + '/langdict.json', 'w', encoding="UTF8") as f:
        json.dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()


if __name__ == "__main__":
    solo()
