from check.abstract_check import CatdictCheck
from data import KEYWORDS

class CategoryURLPattern(CatdictCheck):

    def check(self, catdict, articledict):
        print("Checking category names")

        for c in catdict:
            catdict[c]["URLPattern"] = 0
            if any(word.endswith(kw) or word.endswith(kw+'s') for kw in KEYWORDS for word in c.split('_')):
                catdict[c]["URLPattern"] = 1
            catdict[c]["URLBracesPattern"] = 0
            if '(' in c:
                brack = c.split('(')[1].split(')')[0]
                if any(brack.endswith(kw) for kw in KEYWORDS):
                    catdict[c]["URLBracesPattern"] = 1
        return catdict


if __name__ == "__main__":
    CategoryURLPattern().solo()
