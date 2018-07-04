from data import DATAP
from check.langdictcheck import LangdictCheck
from json import load


class NegSeed(LangdictCheck):

    def check(self, langdict):
        print("Checking negative Seed")
        f = open(DATAP + "/seed_neg.json", 'r', encoding="UTF8")
        d = load(f)
        f.close()
        negseed = set(cl for cl in d if d[cl]["recall"] == 0)
        for cl in langdict:
            if cl in negseed:
                langdict[cl]["negativeSeed"] = 1
            else:
                langdict[cl]["negativeSeed"] = 0
        return langdict


if __name__ == '__main__':
    NegSeed().solo()
