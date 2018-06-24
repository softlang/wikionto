from data import DATAP
from json import load, dump


def explore():
    print("Checking for infobox existence")
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    f.close()
    freq = dict()
    for cl in langdict:
        if langdict[cl]["Seed"] == 0:
            continue
        for i in langdict[cl]["DbpediaInfoboxTemplate"]:
            if i in freq:
                freq[i] += 1
            else:
                freq[i] = 1
    f = open(DATAP + '/explore_seed_infoboxes.json', 'w', encoding="UTF8")
    dump(freq,f,indent=2)
    f.flush()
    f.close()


if __name__ == '__main__':
    explore()
