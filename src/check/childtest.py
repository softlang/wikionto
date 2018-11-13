from collections import deque
from data import INDICATORS
from check.abstract_check import CatdictCheck


class ChildCheck(CatdictCheck):

    def check(self, catdict, articledict):
        for c in catdict:
            seed, sls, no_sls = get_transitive_positive_negative_children(c, catdict, articledict)
            catdict[c]["#Seed-trans"] = len(seed)
            catdict[c]["#Positive-trans"] = len(sls)
            catdict[c]["#Negative-trans"] = len(no_sls)

            seed, sls, no_sls = get_direct_sls_nosls(c, catdict, articledict)
            catdict[c]["#Seed"] = len(seed)
            catdict[c]["#Positive"] = len(sls)
            catdict[c]["#Negative"] = len(no_sls)
        return catdict


def get_transitive_positive_negative_children(c, cd, ad):
    catqueue = deque([c])
    cat_done = set()

    negatives = set()
    positives = set()
    seed = set()

    while not len(catqueue) == 0:
        proc_cat = catqueue.pop()
        if "subcats" in cd[proc_cat]:
            for subcat in cd[proc_cat]["subcats"]:
                if subcat not in cat_done:
                    catqueue.append(subcat)
        if "articles" in cd[proc_cat]:
            for a in cd[proc_cat]["articles"]:
                if any(ad[a][i] == 1 for i in INDICATORS):
                    positives.add(a)
                else:
                    negatives.add(a)
                if ad[a]["Seed"] == 1:
                    seed.add(a)
        cat_done.add(proc_cat)
    return seed, positives, negatives


def get_direct_sls_nosls(c, cd, ad):
    negatives = set()
    positives = set()
    seed = set()
    if "articles" in cd[c]:
        for a in cd[c]["articles"]:
            if any(ad[a][i] == 1 for i in INDICATORS):
                positives.add(a)
            else:
                negatives.add(a)
            if ad[a]["Seed"] == 1:
                seed.add(a)
    return seed, positives, negatives


if __name__ == "__main__":
    ChildCheck().solo()
