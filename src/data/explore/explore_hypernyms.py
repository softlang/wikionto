from data import DATAP
from json import load, dump
import collections


def interactive():
    f = open(DATAP + '/catdict.json', 'r', encoding="UTF8")
    cd = load(f)
    f = open(DATAP + '/articledict.json', 'r', encoding="UTF8")
    ld = load(f)
    cats = [c for c in ld["In_the_Blue_of_Evening"]["cats"] if c in cd]
    noise = set()
    #repeat this line interactively
    cats = set(supercat for c in cats for supercat in cd[c]["supercats"] if
               cd[supercat]["Category:Formal_languagesDepth"] < cd[c]["Category:Formal_languagesDepth"]
               and c not in noise)


def dump_gt_1000():
    f = open(DATAP + '/articledict.json', 'r', encoding="UTF8")
    ld = load(f)
    hyps = [hyp for l in ld if "POSHypernyms" in ld[l] for hyp in ld[l]["POSHypernyms"]]
    counter = collections.Counter(hyps)
    hdict = [(n, count) for n, count in counter.items() if count > 1000]
    hdict = sorted(hdict, key=(lambda e: e[1]))
    f = open(DATAP + '/exploration/poshypernyms.csv', 'w', encoding="UTF8")
    for n, count in hdict:
        f.write(n + ', ' + str(count) + "\n")


if __name__ == "__main__":
    dump_gt_1000()
