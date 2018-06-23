from data import DATAP
from check.langdictcheck import LangdictCheck
from json import load


class Seed(LangdictCheck):

    def check(self, langdict):
        print("Checking Gitseed")
        f = open(DATAP + "/seed_annotated.json", 'r', encoding="UTF8")
        d = load(f)
        f.close()
        for cl in langdict:
            langdict[cl]["Seed"] = 0
        for l in d["recalled"]:
            if l in langdict:
                langdict[l]["Seed"] = 1
            else:
                print("recalled not in langdict:" + l)
        for l in d["mention"]:
            if l in langdict:
                langdict[l]["SeedMention"] = 1
            else:
                print("mention not in langdict: " + l)
        return langdict


if __name__ == '__main__':
    Seed().solo()
