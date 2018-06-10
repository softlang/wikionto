from data import DATAP
from json import load


def get_7():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    for cl, p in langdict.items():
        if p["CLDepth"] == 5 or (p["CFFDepth"] == 5):
            if p["TIOBE"] == 1 or (p["GitSeed"] == 1):
                print(cl)


if __name__ == "__main__":
    get_7()
