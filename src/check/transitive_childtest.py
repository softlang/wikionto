from collections import deque
from data import DATAP
from data.eval.article_reduction import check_sl
from json import load, dump


def check_transitive_children():
    f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
    ld = load(f)
    f = open(DATAP + '/ocatdict.json', 'r', encoding="UTF8")
    cd = load(f)

    for c in cd:
        seed, sls, no_sls = get_sls_nosls(c, cd, ld)
        cd[c]["#Seed"] = len(seed)
        cd[c]["#SLs"] = len(sls)
        cd[c]["#NonSLs"] = len(no_sls)
    f = open(DATAP + '/ocatdict.json', 'w', encoding="UTF8")
    dump(cd, f, indent=2)
    f.flush()
    f.close()


def get_sls_nosls(c, cd, ld):
    catqueue = deque([c])
    cat_done = set()

    no_sls = set()
    sls = set()
    seed = set()

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
                if ld[a]["Seed"]==1:
                    seed.add(a)
        cat_done.add(cat)
    return seed, sls, no_sls


if __name__ == "__main__":
    check_transitive_children()
