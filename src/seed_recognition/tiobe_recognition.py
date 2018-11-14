"""
Script support for recognizing Git languages in Wikipedia.
"""
import re
from data import DATAP
from json import load, dump


def namenorm(name):
    x = re.sub("\(.*?\)", "", name).lower().strip()
    x = re.sub("[_ /]", "", x).strip()
    return x


def recognize():
    f = open(DATAP+'/TIOBE_index_list.txt', 'r', encoding="utf8")
    tiobedict = dict()
    for line in f:
        if ':' in line:
            ls = line.split(':')
            tiobedict[ls[0]] = dict()
            tiobedict[ls[0]]['hints'] = ls[1]
        else:
            tiobedict[line[:-1]] = dict()
            tiobedict[line[:-1]]['hints'] = None
    f.close()

    f = open(DATAP+'/articledict.json', 'r', encoding="utf8")
    langdict = load(f)
    f.close()
    for tl in tiobedict:

        if tl in langdict:
            tiobedict[tl]['recall'] = 1
            tiobedict[tl]['recalledAs'] = tl
            continue

        tln = namenorm(tl)
        for cl in langdict:
            cln = namenorm(cl)
            if tln == cln:
                tiobedict[tl]['recall'] = 1
                tiobedict[tl]['recalledAs'] = cl
                break

        hints = tiobedict[tl]['hints']
        if hints is not None:
            hintsn = namenorm(hints)
            for hint in hintsn.split(','):
                hintn = hint.strip()
                if hintn in langdict:
                    tiobedict[tl]['recall'] = 1
                    tiobedict[tl]['recalledAs'] = hintn
                    break
                for cl in langdict:
                    cln = namenorm(cl)
                    if hintn == cln:
                        tiobedict[tl]['recall'] = 1
                        tiobedict[tl]['recalledAs'] = cl
                        break
    f = open(DATAP+'/TIOBE_index_annotatednew.json','w',encoding='utf8')
    dump(tiobedict,f, indent=2)
    f.flush()
    f.close()


if __name__ == '__main__':
    recognize()
