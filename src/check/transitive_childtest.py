from collections import deque
from data import DATAP
from data.eval import check_sl
from json import load, dump

def check_transitive_children():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    ld = load(f)
    f = open(DATAP + '/catdict.json', 'r', encoding="UTF8")
    cd = load(f)

    for c in cd:
        catqueue = deque([c])
        cat_done = set()

        no_sls = set()
        sls = set()

        while not len(catqueue) == 0:
            cat = catqueue.pop()
            if "subcats" in cd[cat]:
                for subcat in cd[cat]["subcats"]:
                    if subcat not in cat_done:
                        catqueue.append(subcat)
            if "articles" in cd[cat]:
                for a in cd[cat]["articles"]:
                    if check_sl(a, ld):
                        sls.add(a)
                    else:
                        no_sls.add(a)
            cat_done.add(cat)
        cd[c]["#SLs"] = len(sls)
        cd[c]["#NonSLs"] = len(no_sls)
    f = open(DATAP + '/catdict.json', 'w', encoding="UTF8")
    dump(cd,f,indent=2)
    f.flush()
    f.close()


if __name__ == "__main__":
    check_transitive_children()
