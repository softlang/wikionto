from data import DATAP
from json import load, dump


def explore():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    f.close()
    freq = dict()
    for cl in langdict:
        if langdict[cl]["Seed"] == 0 or "DbpediaInfoboxTemplate" not in langdict[cl]:
            continue
        for i in set(langdict[cl]["DbpediaInfoboxTemplate"]):
            if i in freq:
                freq[i] += 1
            else:
                freq[i] = 1
    f = open(DATAP + '/explore_seed_infoboxes.json', 'w', encoding="UTF8")
    dump(freq,f,indent=2)
    f.flush()
    f.close()


def find_software_pl():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    f.close()
    cls = [cl for cl in langdict if "DbpediaInfoboxTemplate" in langdict[cl]
           and langdict[cl]["Seed"] == 1
           and "infobox_software" in langdict[cl]["DbpediaInfoboxTemplate"]
           and "infobox_programming_language" in langdict[cl]["DbpediaInfoboxTemplate"]]
    print(cls)


if __name__ == '__main__':
    find_software_pl()
