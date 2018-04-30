from data import DATAP
from check.langdictcheck import LangdictCheck


class Gitseed(LangdictCheck):

    def check(self, langdict):
        print("Checking Gitseed")
        f = open(DATAP+'/gitseed_annotated.csv','r',encoding="utf8")
        for line in f:
            comment = line.split(",")[1]
            if comment == "recalled":
                seed_language = line.split(",")[0]
            if "recalled redirect" in comment:
                seed_language = comment.split('"')[1]
            if "recalled as" in comment:
                seed_language = comment.split('"')[1]
            if "recalled" in comment and seed_language in langdict:
                langdict[seed_language]["GitSeed"] = 1
            if "recalled" in comment and not seed_language in langdict:
                print(seed_language)
        for cl in langdict:
            if "GitSeed" not in langdict[cl]:
                langdict[cl]["GitSeed"] = 0
        return langdict


if __name__ == '__main__':
    Gitseed().solo()
