from json import load

from check.langdictcheck import LangdictCheck
from data import DATAP


class SemDist(LangdictCheck):

    def check(self, langdict):
        print("Checking semantic distance")
        f = open(DATAP + '/catdict.json', 'r', encoding="UTF8")
        catdict = load(f)
        for cl in langdict:
            cats = langdict[cl]["cats"]
            total = len(cats)
            reachable_cats = 0
            for cat in cats:
                if cat in catdict:
                    reachable_cats += 1
            langdict[cl]["SemanticDistance"] = total - (reachable_cats * 2)
            langdict[cl]["SemanticallyRelevant"] = int(langdict[cl]["SemanticDistance"] < 1)
            langdict[cl]["NumberOfCategories"] = total
        return langdict


if __name__ == '__main__':
    SemDist().solo()
