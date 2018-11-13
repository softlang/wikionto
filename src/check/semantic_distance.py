from json import load

from check.abstract_check import ArtdictCheck
from data import DATAP


class SemDist(ArtdictCheck):

    def check(self, articledict):
        print("Checking semantic distance")
        f = open(DATAP + '/catdict.json', 'r', encoding="UTF8")
        catdict = load(f)
        for title in articledict:
            cats = articledict[title]["cats"]
            total = len(cats)
            reachable_cats = 0
            for cat in cats:
                if cat in catdict:
                    reachable_cats += 1
            articledict[title]["SemanticDistance"] = total - (reachable_cats * 2)
            articledict[title]["SemanticallyRelevant"] = int(articledict[title]["SemanticDistance"] < 1)
            articledict[title]["NumberOfCategories"] = total
        return articledict


if __name__ == '__main__':
    SemDist().solo()
