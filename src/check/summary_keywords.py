from check.abstract_check import ArtdictCheck
from data import KEYWORDS


class SumKeyWords(ArtdictCheck):
    def check(self, articledict):
        print("Checking summary for keyword mentions")
        for title in articledict:
            if "Summary" not in articledict[title]:
                articledict[title]["PlainTextKeyword"] = 0
                continue
            summary = articledict[title]["Summary"]
            if any(word in summary.lower() for word in KEYWORDS):
                articledict[title]["PlainTextKeyword"] = 1
            else:
                articledict[title]["PlainTextKeyword"] = 0
        return articledict


if __name__ == '__main__':
    SumKeyWords().solo()
