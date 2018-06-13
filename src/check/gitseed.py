from data import DATAP
from check.langdictcheck import LangdictCheck
from json import load


class Gitseed(LangdictCheck):

    def check(self, langdict):
        print("Checking Gitseed")
        f = open(DATAP + "/gitseed_annotated.json", 'r', encoding="UTF8")
        tiobedict = load(f)
        f.close()
        for cl in langdict:
            langdict[cl]["GitSeed"] = 0
        for tl, tld in tiobedict.items():
            if "recall" not in tld:
                print(tl)
            if "recalledAs" in tld:
                rec = tld["recalledAs"]
                if rec in langdict:
                    langdict[rec]["GitSeed"] = 1
                else:
                    print(rec)
            elif tld["recall"]==1:
                langdict[tl]["GitSeed"] = 1
        return langdict


if __name__ == '__main__':
    Gitseed().solo()
