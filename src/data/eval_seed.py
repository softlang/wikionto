from data import DATAP
from json import load


def get_n(n):
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    for cl, p in langdict.items():
        if p["CLDepth"] == n or (p["CFFDepth"] == n):
            if p["TIOBE"] == 1 or (p["GitSeed"] == 1):
                print(cl)


def get_list_linked_seed():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    d = load(f)
    f.close()
    sl = list(cl for cl in d if ((d[cl]["GitSeed"]==1) or (d[cl]["TIOBE"]==1)) and (d[cl]["In_Wikipedia_List"]==1))
    sl0 = list(cl for cl in d if ((d[cl]["GitSeed"] == 1) or (d[cl]["TIOBE"] == 1)))
    print(len(sl))
    print(len(sl0))


if __name__ == "__main__":
    get_list_linked_seed()
