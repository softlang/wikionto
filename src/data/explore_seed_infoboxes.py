from multiprocessing.pool import Pool
from mine.wiki import get_infobox
from data import DATAP
from json import load, dump


def explore():
    print("Checking for infobox existence")
    pool = Pool(processes=10)
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    f.close()
    clrevs = []
    for cl in langdict:
        if langdict[cl]["Seed"] == 0:
            continue
        rev = langdict[cl]["Revision"]
        clrevs.append(rev)
    ibs = list(pool.map(get_infobox, clrevs))
    freq = dict()
    for i_list in ibs:
        if i_list is None:
            continue
        for i in i_list:
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
