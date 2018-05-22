from mine.dbpedia import articles_with_hypernym,CLURI,CFFURI
from data import CLDEPTH, CFFDEPTH
from check.langdictcheck import LangdictCheck

class DbpediaHyp(LangdictCheck):

    def check(self,langdict):
        print("Checking Dbpedia Hypernym")
        cls = articles_with_hypernym(CLURI, 0, CLDEPTH, "Language") + articles_with_hypernym(CFFURI, 0, CFFDEPTH, "Language")
        cffs = articles_with_hypernym(CLURI, 0, CLDEPTH, "Format") + articles_with_hypernym(CFFURI, 0, CFFDEPTH, "Format")
        for cl in langdict:
            if (cl in cls) or (cl in cffs):
                langdict[cl]["DbpediaHypernym"] = 1
            else:
                langdict[cl]["DbpediaHypernym"] = 0
        return langdict


if __name__ == '__main__':
    DbpediaHyp().solo()
