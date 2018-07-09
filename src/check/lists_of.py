from check.langdictcheck import LangdictCheck
from data import DATAP
from json import load
from mine.wiki import getlinks


def explore_all():
    f = open(DATAP + "/langdict.json", "r", encoding="UTF8")
    langdict = load(f)
    for cl in langdict:
        if ("list" in cl.lower()) & (("language" in cl.lower()) | ("format" in cl.lower())):
            print(cl)


class WikiList(LangdictCheck):
    def check(self,langdict):
        print("Checking Wikipedia's lists")
        for cl in langdict:
            langdict[cl]['In_Wikipedia_List'] = 0
        f = open(DATAP + "/Language_Lists.txt", "r", encoding="UTF8")
        for page in f:
            links = getlinks(page.strip())
            for l in links:
                ln = l.replace(' ', '_')
                if ln in langdict:
                    langdict[ln]['In_Wikipedia_List'] = 1
        return langdict


if __name__ == "__main__":
    WikiList().solo()
