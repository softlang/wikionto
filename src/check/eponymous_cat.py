from data import DEPTH, ROOTS
from mine.dbpedia import articles_with_commons, to_uri
from check.abstract_check import CatdictCheck

class EponymousCat(CatdictCheck):

    def check(self, catdict, artdict):
        print("Checking for Eponymous")
        for cat in catdict:
            catdict[cat]["Eponymous"] = int(cat in artdict)

        # TODO: http://live.dbpedia.org/property/commons for Java : Category:Java (en)
        for c in ROOTS:
            cls = articles_with_commons(to_uri(c), 0, DEPTH)
            for cl in cls:
                for cat in cls[cl]:
                    if cat in catdict:
                        catdict[cat]["Eponymous"] = 1
        return catdict


if __name__ == "__main__":
    EponymousCat().solo()
