from json import load

from check.abstract_check import ArtdictCheck, CatdictCheck
from data import DATAP


class SemDist(ArtdictCheck):

    def check(self, articledict):
        print("Checking semantic distance of articles")
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
        return articledict


class SemDistCat(CatdictCheck):

    def check(self, catdict, articledict):
        print("Checking semantic distance of categories")
        for cat in catdict:
            if "supercats" not in catdict[cat]:
                continue
            supercats = catdict[cat]["supercats"]
            semdist = 0
            for supercat in supercats:
                semdist += 1 if supercat in catdict else -1
            catdict[cat]["SemanticDistance"] = semdist
        return catdict


if __name__ == '__main__':
    SemDist().solo()
