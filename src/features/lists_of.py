from check.abstract_check import ArtdictCheck
from json import load
from data import DATAP


class WikiList(ArtdictCheck):
    def check(self, articledict):
        print("Checking Wikipedia's lists")

        with open(DATAP + "/listlinks.json", "r") as f:
            lld = load(f)

        for article in articledict:
            articledict[article]['Wikipedia_Lists'] = []
            articledict[article]["IsList"] = 0

        for listtitle, articles in lld.items():
            if listtitle in articledict:
                articledict[listtitle]["IsList"] = 1
            for article in articles:
                if article in articledict:
                    articledict[article]["Wikipedia_Lists"].append(listtitle)

        return articledict


if __name__ == "__main__":
    WikiList().solo()
