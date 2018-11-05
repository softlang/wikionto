from data import NOISY_CATS, DATAP, ROOTS
from check.langdictcheck import LangdictCheck
from json import load


class InNoiseCategory(LangdictCheck):

    def check(self, langdict):
        print("Checking Noisy Categories")
        with open(DATAP + "/catdict.json", 'r', encoding="UTF8") as f:
            catdict = load(f)
        count = 0
        for cl in langdict:
            credibility = reaches_root_without_noise(["Category:"+c for c in langdict[cl]["cats"] if "Category:"+c not in NOISY_CATS], catdict)
            langdict[cl]["NotExclusiveNoiseCategory"] = bool(credibility)
            count += 1
            if count % 1000 == 0:
                print("    " + str(count))
        return langdict


def reaches_root_without_noise(front, catdict):
    categories = front
    while categories and (not any(c in ROOTS or c in NOISY_CATS for c in categories)):
        categories = [supercat for c in categories if c in catdict for supercat in catdict[c]["supercats"]]
    return any(c in ROOTS for c in categories)


if __name__ == '__main__':
    InNoiseCategory().solo()
