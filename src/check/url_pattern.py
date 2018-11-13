from check.abstract_check import ArtdictCheck
from data import KEYWORDS


class URLPattern(ArtdictCheck):
    def check(self, artdict):
        print("Checking URL pattern")

        for title in artdict:
            artdict[title]["URLPattern"] = 0
            artdict[title]["URLBracesPattern"] = 0
        for title in artdict:
            if any(word.endswith(kw) for kw in KEYWORDS for word in title.split('_')):
                artdict[title]["URLPattern"] = 1

            if '(' in title:
                clbrack = title.split('(')[1].split(')')[0]
                if any(clbrack.endswith(kw) for kw in KEYWORDS):
                    artdict[title]["URLBracesPattern"] = 1

        return artdict


if __name__ == "__main__":
    URLPattern().solo()
