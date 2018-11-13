from data import DATAP
from check.abstract_check import ArtdictCheck
from json import load


class Seed(ArtdictCheck):

    def check(self, articledict):
        print("Checking Gitseed")
        f = open(DATAP + "/temp/seed_annotated.json", 'r', encoding="UTF8")
        seedmatches = load(f)
        f.close()
        for title in articledict:
            articledict[title]["Seed"] = 0
        for title in seedmatches["recalled"]:
            if title in articledict:
                articledict[title]["Seed"] = 1
            else:
                print("recalled not in articledict:" + title)
        for title in seedmatches["mention"]:
            if title in articledict:
                articledict[title]["SeedMention"] = 1
            else:
                print("mention not in articledict: " + title)
        return articledict


if __name__ == '__main__':
    Seed().solo()
