from data import NOISY_CATS, DATAP, ROOTS
from check.abstract_check import ArtdictCheck
from json import load


class InNoiseCategory(ArtdictCheck):

    def check(self, articledict):
        print("Checking Noisy Categories")
        with open(DATAP + "/catdict.json", 'r', encoding="UTF8") as f:
            catdict = load(f)
        count = 0
        for a in articledict:
            credibility = reaches_root_without_noise(
                ["Category:" + c for c in articledict[a]["cats"] if "Category:" + c not in NOISY_CATS], catdict)
            articledict[a]["NotExclusiveNoiseCategory"] = bool(credibility)
            count += 1
            if count % 1000 == 0:
                print("    " + str(count))
        return articledict


def reaches_root_without_noise(front, catdict):
    categories = front
    while categories and (not any(c in ROOTS or c in NOISY_CATS for c in categories)):
        categories = [supercat for c in categories if c in catdict for supercat in catdict[c]["supercats"]]
    return any(c in ROOTS for c in categories)


if __name__ == '__main__':
    InNoiseCategory().solo()
