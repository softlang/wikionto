from data import KEYWORDS
from check.abstract_check import ArtdictCheck


class DbpediaHyp(ArtdictCheck):

    def check(self, artdict):
        print("Checking Dbpedia Hypernym")
        for a in artdict:
            if "DbpediaHypernyms" not in artdict[a]:
                continue
            if any(hyp.endswith(kw) or hyp.endswith(kw+"s") for kw in KEYWORDS for hyp in artdict[a]["DbpediaHypernyms"]):
                artdict[a]["DbpediaHypernymCheck"] = 1
            else:
                artdict[a]["DbpediaHypernymCheck"] = 0
        return artdict


if __name__ == '__main__':
    DbpediaHyp().solo()
