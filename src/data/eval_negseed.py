from data import DATAP
from json import load, dump
from random import randint


def count_negative_seed_candidates():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    d = load(f)
    print(len([cl for cl in d if d[cl]["negativeSeedCandidate"] == 1]))


def create_negative_seed_pre():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    d = load(f)
    tempd = dict()
    for cl in d:
        if d[cl]["negativeSeedCandidate"] == 1:
            for ib in list(set(d[cl]["DbpediaInfoboxTemplate"])):
                if ib not in tempd:
                    tempd[ib] = []
                tempd[ib].append(cl)
    f = open(DATAP + '/seed_neg_pre.json', 'w', encoding="UTF8")
    dump(tempd, f, indent=2)
    f.flush()
    f.close()


def create_negative_seed():
    f = open(DATAP + '/seed_neg_pre.json', 'r', encoding="UTF8")
    d = load(f)
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    ld = load(f)
    nsd = dict()
    for ib, cls in d.items():
        while True:
            c = randint(0, len(cls) - 1)
            if "Summary" not in ld[cls[c]]:
                if len(cls) == 1:
                    break
                else:
                    continue
            nsd[cls[c]] = dict()
            nsd[cls[c]]["recall"] = 0
            break
    f = open(DATAP + '/seed_neg.json', 'w', encoding="UTF8")
    dump(nsd, f, indent=2)
    f.flush()
    f.close()


def check_negative_seed():
    f = open(DATAP + '/seed_neg.json', 'r', encoding="UTF8")
    d = load(f)
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    ld = load(f)
    for cl in d:
        print(cl)
        if "Summary" in ld[cl]:
            print("  " + ld[cl]["Summary"])
        if "POS" in ld[cl]:
            print("  " + str(ld[cl]["POS"]))
        print("  " + str(set(ld[cl]["DbpediaInfoboxTemplate"])))
        print("  " + str(ld[cl]["cats"]))
        text = ""
        while text not in ["y", "n", "m"]:
            text = input("Decide y/n/m: ")
        if text is "y":
            d[cl]["recall"] = 2
        elif text is "m":
            d[cl]["recall"] = 1
    f = open(DATAP + '/seed_neg.json', 'w', encoding="UTF8")
    dump(d, f, indent=2)
    f.flush()
    f.close()


def count_negative_seed_strats():
    f = open(DATAP + '/seed_neg_pre.json', 'r', encoding="UTF8")
    d = load(f)
    c = 0.001
    x = 0
    print(len(d.keys()))
    for ib, ibd in d.items():
        x += 5 + c * (len(ibd))
    print(x)


if __name__ == "__main__":
    check_negative_seed()
