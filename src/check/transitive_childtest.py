from collections import deque
from data import DATAP, INDICATORS
from json import load, dump


def check_transitive_children():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    ld = load(f)
    f = open(DATAP + '/catdict.json', 'r', encoding="UTF8")
    cd = load(f)

    for c in cd:
        seed, sls, no_sls = get_transitive_sls_nosls(c, cd, ld)
        cd[c]["#Seed-trans"] = len(seed)
        cd[c]["#SLs-trans"] = len(sls)
        cd[c]["#NonSLs-trans"] = len(no_sls)

        seed, sls, no_sls = get_direct_sls_nosls(c, cd, ld)
        cd[c]["#Seed"] = len(seed)
        cd[c]["#SLs"] = len(sls)
        cd[c]["#NonSLs"] = len(no_sls)

    f = open(DATAP + '/catdict.json', 'w', encoding="UTF8")
    dump(cd, f, indent=2)
    f.flush()
    f.close()


def get_transitive_sls_nosls(c, cd, ld):
    catqueue = deque([c])
    cat_done = set()

    no_sls = set()
    sls = set()
    seed = set()

    while not len(catqueue) == 0:
        proc_cat = catqueue.pop()
        if "subcats" in cd[proc_cat]:
            for subcat in cd[proc_cat]["subcats"]:
                if subcat not in cat_done:
                    catqueue.append(subcat)
        if "articles" in cd[proc_cat]:
            for a in cd[proc_cat]["articles"]:
                if any(ld[a][i] == 1 for i in INDICATORS):
                    sls.add(a)
                else:
                    no_sls.add(a)
                if ld[a]["Seed"] == 1:
                    seed.add(a)
        cat_done.add(proc_cat)
    return seed, sls, no_sls


def get_direct_sls_nosls(c, cd, ld):
    no_sls = set()
    sls = set()
    seed = set()
    if "articles" in cd[c]:
        for a in cd[c]["articles"]:
            if any(ld[a][i] == 1 for i in INDICATORS):
                sls.add(a)
            else:
                no_sls.add(a)
            if ld[a]["Seed"] == 1:
                seed.add(a)
    return seed, sls, no_sls


if __name__ == "__main__":
    check_transitive_children()
