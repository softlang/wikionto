from data import DATAP
from json import load


def get_n(n):
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    for cl, p in langdict.items():
        if p["CLDepth"] == n or (p["CFFDepth"] == n):
            if p["TIOBE"] == 1 or (p["GitSeed"] == 1):
                print(cl)


if __name__ == "__main__":
    get_n(7)
