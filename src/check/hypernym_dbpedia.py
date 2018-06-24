from data import KEYWORDS
from check.langdictcheck import LangdictCheck


class DbpediaHyp(LangdictCheck):

    def check(self, langdict):
        print("Checking Dbpedia Hypernym")

        for cl in langdict:
            if any(k in hyp for k in KEYWORDS for hyp in langdict[cl]["DbpediaHypernyms"]):
                langdict[cl]["DbpediaHypernymCheck"] = 1
            else:
                langdict[cl]["DbpediaHypernymCheck"] = 0
        return langdict


if __name__ == '__main__':
    DbpediaHyp().solo()
