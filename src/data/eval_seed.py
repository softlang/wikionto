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

def count_seed():
    f = open(DATAP + '/seed_annotated.json', 'r', encoding="UTF8")
    d = load(f)
    f.close()
    r = len(d["recalled"])
    m = len(d["mention"])
    u = len(d["unknown"])
    print(str(r)+"/"+str(m)+"/"+str(u))

def check_seed():
    f = open(DATAP + '/seed_annotated.json', 'r', encoding="UTF8")
    d = load(f)
    f.close()
    for l in d["recalled"]:
        if "tiobe" in d["recalled"][l] and "gitseed" in d["recalled"][l]:
            print("overlap:"+l+str(d["recalled"][l]))
    for l in d["recalled"]:
        if l in d["mention"]:
            print(l)
    f = open(DATAP + '/gitseed_annotated.json', 'r', encoding="UTF8")
    gd = load(f)
    print(len(gd))
    f.close()
    f = open(DATAP + '/TIOBE_index_annotated.json', 'r', encoding="UTF8")
    td = load(f)
    print(len(td))
    f.close()

def merge_seeds():
    f = open(DATAP + '/gitseed_annotated.json', 'r', encoding="UTF8")
    gd = load(f)
    f.close()
    f = open(DATAP + '/TIOBE_index_annotated.json', 'r', encoding="UTF8")
    td = load(f)
    f.close()

    d = dict()
    d["recalled"] = dict()
    d["mention"] = dict()
    d["unknown"] = dict()

    for l in gd:
        if gd[l]["recall"] == 1:
            if "recalledAs" in gd[l]:
                rl = gd[l]["recalledAs"]
            else:
                rl = l
            d["recalled"][rl] = dict()
            d["recalled"][rl]["gitseed"] = []
            d["recalled"][rl]["gitseed"].append(l)
        elif "mention" in gd[l]:
            d["mention"][gd[l]["mention"]] = dict()
            d["mention"][gd[l]["mention"]]["gitseed"] = []
            d["mention"][gd[l]["mention"]]["gitseed"].append(l)
        else:
            d["unknown"][l] = "gitseed"
    for l in td:
        if td[l]["recall"] == 1:
            if "recalledAs" in td[l]:
                rl = td[l]["recalledAs"]
            else:
                rl = l
            if rl not in d["recalled"]:
                d["recalled"][rl] = dict()
            d["recalled"][rl]["tiobe"] = []
            d["recalled"][rl]["tiobe"].append(l)
        elif "mention" in td[l]:
            if td[l]["mention"] not in d["mention"]:
                d["mention"][td[l]["mention"]] = dict()
            d["mention"][td[l]["mention"]]["tiobe"] = []
            d["mention"][td[l]["mention"]]["tiobe"].append(l)
        else:
            if l in d["unknown"]:
                d["unknown"][l] += ", tiobe"
            else:
                d["unknown"][l] = "tiobe"
    f = open(DATAP + '/seed_annotated.json', 'w', encoding="UTF8")
    dump(d, f, indent=2)
    f.flush()
    f.close()

if __name__ == "__main__":
    merge_seeds()
    check_seed()
    count_seed()