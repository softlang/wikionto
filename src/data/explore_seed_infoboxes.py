from multiprocessing.pool import Pool
from mine.wiki import getcontent
from data import DATAP
from json import load, dump


def get_infobox(rev):
    text= getcontent(rev).lower()
    if '{{infobox' not in text:
        return None
    parts = text.split('{{infobox')
    ibs = []
    for x in range(1,len(parts)):
        p = parts[x]
        ibs.append(p.split('|')[0].replace('\\n', '').strip())
    return ibs


def explore():
    print("Checking for infobox existence")
    pool = Pool(processes=10)
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    f.close()
    clrevs = []
    for cl in langdict:
        if langdict[cl]["GitSeed"] == 0 and (langdict[cl]["TIOBE"]==0):
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
