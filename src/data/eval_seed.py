from data import DATAP
from json import load, dump
from mine.dbpedia import get_summary

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

def annotate_summary():
    f = open(DATAP + '/gitseed_annotated.json', 'r', encoding="UTF8")
    d = load(f)
    f.close()
    for l in d:
        s = "Unknown"
        if "recalledAs" in d[l]:
            rl = d[l]["recalledAs"]
            s = get_summary(rl)
        elif "recall"==1:
            s = get_summary(l)
        elif "mentionIn" in d[l]:
            ml = d[l]["mentionIn"]
            s = get_summary(ml)
        d[l]["Summary"] = s
    f = open(DATAP + '/gitseed_annotated.json', 'w', encoding="UTF8")
    dump(d,f,indent=2)
    f.flush()
    f.close()


if __name__ == "__main__":
    annotate_summary()
