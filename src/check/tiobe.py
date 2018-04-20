from data import DATAP
from json import load


def check_tiobe(langdict):
    f = open(DATAP+"/TIOBE_index_annotated.json",'r',encoding="UTF8")
    tiobedict = load(f)
    f.close()
    for tl, tld in tiobedict.items():
        if "recalledAs" in tld:
            rec = tld["recalledAs"]
            if rec in langdict:
                langdict[rec]["TIOBE"] = 1
            else:
                print(rec)
    return langdict
