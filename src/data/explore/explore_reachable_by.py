from mine.dbpedia import articles_below
from data import DATAP, load_catdict

ex_cat = [
    "<http://dbpedia.org/resource/Category:Songs>",
    "<http://dbpedia.org/resource/Category:Astronomical_objects>",
    "<http://dbpedia.org/resource/Category:Software>",
    "<http://dbpedia.org/resource/Category:Hardware>",
    "<http://dbpedia.org/resource/Category:People>"
]


def check_reachable_by(langdict, c):
    print("Checking reachable by "+c)
    xs = set()
    for i in range(7):
        print("    Depth:"+str(i))
        xs = xs | set(articles_below(c, i, i))
    inter = xs & langdict.keys()
    for cl in inter:
        langdict[cl][c] = 1
    return langdict


def reachable_by(catdict, title, cat):
    if cat not in catdict:
        return False
    cat_front = set([cat])
    visited = set()
    while cat_front:
        visited |= cat_front
        article_in_front = [a for c in cat_front for a in catdict[c]["articles"]]
        if title in article_in_front:
            return True
        cat_front = [catdict[c]["supercats"] for c in cat_front if c in catdict and c not in visited]
    return False


def solo():
    import json
    for c in ex_cat:
        with open(DATAP + '/articledict.json', 'r', encoding="UTF8") as f:
            langdict = json.load(f)
            langdict = check_reachable_by(langdict,c)
            f.close()
        with open(DATAP + '/articledict.json', 'w', encoding="UTF8") as f:
            json.dump(obj=langdict, fp=f, indent=2)
            f.flush()
            f.close()


if __name__ == "__main__":
    b = reachable_by(load_catdict(), 'Augmented_Backus–Naur_Form', 'Category:Computer_languages')
    print(b)