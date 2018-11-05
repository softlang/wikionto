from data import DATAP, ROOTS
from json import load, dump


def get_n(n):
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    for cl, p in langdict.items():
        if p["Seed"] == 1:
            for c in ROOTS:
                if c + "Depth" in p and p[c + "Depth"] == n:
                    print(c + ":" + cl)


def count_seed():
    f = open(DATAP + '/seed_annotated.json', 'r', encoding="UTF8")
    d = load(f)
    f.close()
    r = len(d["recalled"])
    m = len(d["mention"])
    u = len(d["unknown"])
    print(str(r) + "/" + str(m) + "/" + str(u))


def check_seed():
    f = open(DATAP + '/seed_annotated.json', 'r', encoding="UTF8")
    d = load(f)
    f.close()
    for l in d["recalled"]:
        if "tiobe" in d["recalled"][l] and "gitseed" in d["recalled"][l]:
            print("overlap:" + l + str(d["recalled"][l]))
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
    get_n(8)
