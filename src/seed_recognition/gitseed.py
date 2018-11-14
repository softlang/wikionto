import re
from json import load, dump
from data import DATAP


def namenorm(name):
    x = re.sub("\(.*?\)", "", name).lower().strip()
    x = re.sub("[_ /]", "", x).strip()
    return x


def recognize():
    f = open(DATAP+'/gitseed.txt', 'r', encoding="utf8")
    seeddict = dict()
    for line in f:
        if line.startswith("#"):
            continue
        l, t = line.split(',')
        l = l.strip()
        t = t.strip()
        seeddict[l] = dict()
        seeddict[l]["Type"] = t
    f.close()

    f = open(DATAP+'/articledict.json', 'r', encoding="utf8")
    langdict = load(f)
    f.close()
    for l in seeddict:
        if l in langdict:
            seeddict[l]['recall'] = 1
            seeddict[l]['recalledAs'] = l
            continue

        normdict = dict((namenorm(cl), cl) for cl in langdict)
        if namenorm(l) in normdict:
            seeddict[l]['recall'] = 1
            seeddict[l]['recalledAs'] = normdict[namenorm(l)]
            continue

    f = open(DATAP+'/gitseed_annotated.json','w',encoding='utf8')
    dump(seeddict,f, indent=2)
    f.flush()
    f.close()

def copy_paste():
    gitdict = dict()
    f = open(DATAP + '/gitseed_annotated.csv', 'r', encoding="utf8")
    for line in f:
        seed_language, comment, add = line.split(",")
        gitdict[seed_language] = dict()
        if "recalled" in comment:
            gitdict[seed_language]["recall"] = 1
        if "recalled redirect" in comment:
            gitdict[seed_language]["recalledAs"] = comment.split('"')[1]
        if "recalled as" in comment:
            gitdict[seed_language]["recalledAs"] = comment.split('"')[1]
        if "no mention" in comment:
            gitdict[seed_language]["recall"] = 0
        if "mentioned in" in comment:
            gitdict[seed_language]["recall"] = 0
            gitdict[seed_language]["mentionIn"] = comment.split('"')[1]
        if add is not "\n":
            gitdict[seed_language]["comment"] = add
    f.close()
    f = open(DATAP + '/gitseed_annotated.json', 'w', encoding='utf8')
    dump(gitdict,f,indent=2)
    f.flush()
    f.close()


if __name__ == '__main__':
    recognize()