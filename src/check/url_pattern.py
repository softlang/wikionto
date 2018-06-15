from check.langdictcheck import LangdictCheck
from data import KEYWORDS

class URLPattern(LangdictCheck):
    def check(self,langdict):
        print("Checking URL pattern")

        for cl in langdict:
            langdict[cl]["URLPattern"] = 0
            langdict[cl]["URLBracesPattern"] = 0
        for cl in langdict:
            if any(kw in cl for kw in KEYWORDS):
                langdict[cl]["URLPattern"] = 1

            if '(' in cl:
                clbrack = cl.split('(')[1].split(')')[0]
                if any(clbrack.endswith(kw) for kw in KEYWORDS):
                    langdict[cl]["URLBracesPattern"] = 1

        return langdict


if __name__ == "__main__":
    URLPattern().solo()
