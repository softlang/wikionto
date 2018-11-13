from check.abstract_check import ArtdictCheck
from data import POSITIVETEMPLATES, NEUTRALTEMPLATES


class InfoboxDbEx(ArtdictCheck):

    def check(self, artdict):
        print("Checking for infobox existence")

        for a in artdict:
            artdict[a]["PositiveInfobox"] = 0
            if "DbpediaInfoboxTemplate" not in artdict[a]:
                artdict[a]["negativeSeedCandidate"] = 0
                continue
            ibs = artdict[a]["DbpediaInfoboxTemplate"]
            artdict[a]["#Infobox"] = len(ibs)
            for ib in ibs:
                if ib in POSITIVETEMPLATES:
                    artdict[a]["PositiveInfobox"] = 1
                if ib in NEUTRALTEMPLATES:
                    artdict[a]["NeutralInfobox"] = 1
                if ib not in POSITIVETEMPLATES + NEUTRALTEMPLATES:
                    artdict[a]["NegativeInfobox"] = 1
        return artdict


if __name__ == "__main__":
    InfoboxDbEx().solo()
