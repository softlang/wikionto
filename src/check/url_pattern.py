from check.langdictcheck import LangdictCheck
from data import KEYWORDS

class URLPattern(LangdictCheck):
    def check(self,langdict):
        print("Checking URL pattern")

        for cl in langdict:
            if any(kw in cl for kw in KEYWORDS):
                langdict[cl]["URLPattern"] = 1

            if '(' in cl:
                clbrack = cl.split('(')[1].split(')')[0]
                if any(kw in clbrack for kw in KEYWORDS):
                    langdict[cl]["URLBracesPattern"] = 1

        return langdict


if __name__ == "__main__":
    URLPattern().solo()
