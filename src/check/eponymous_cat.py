from data import DATAP
from json import load, dump

def check_eponymous(catdict, langdict):
    print("Checking for Eponymous")
    for cat in catdict:
        if cat in langdict:
            catdict[cat]["Eponymous"] = 1
        else:
            catdict[cat]["Eponymous"] = 0
    return catdict

if __name__ == "__main__":
    f=open(DATAP+'/langdict.json', 'r',encoding="UTF8")
    langdict = load(f)
    with open(DATAP+'/catdict.json', 'r',encoding="UTF8") as f:
        catdict = load(f)
        catdict = check_eponymous(catdict,langdict)
        f.close()
    with open(DATAP+'/catdict.json', 'w',encoding="UTF8") as f:
        dump(obj=catdict, fp=f, indent=2)
        f.flush()
        f.close()