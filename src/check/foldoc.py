from check.abstract_check import ArtdictCheck
from data import DATAP


class FoldocTopic(ArtdictCheck):

    def check(self, artdict):
        print("Checking against Foldoc dictionary")
        f = open(DATAP + "/temp/Foldoc_words.txt", "r", encoding="utf-8")
        words = []
        for line in f:
            words.append(line)
        symbols = [".", ",", ";", ""]
        for a in artdict:
            artdict[a]["Foldoc"] = 0
            if "Summary" in artdict[a]:
                summary = artdict[a]["Summary"]
                artdict[a]["Foldoc"] = int(any(word + symbol + " " in summary for word in words for symbol in symbols))
        return artdict


if __name__ == "__main__":
    FoldocTopic().solo()
