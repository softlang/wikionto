from data import DATAP
from json import load, dump


def check_cat_name(catdict):
    print("Checking category names")
    ex_pattern = ["Data_types", "lists_of", "comparison", "companies"]
    for c in catdict:
        if any(w in c for w in ex_pattern):
            catdict[c]["ExCatNamePattern"] = 0
        else:
            catdict[c]["IncludedNamePattern"] = 1
    return catdict


if __name__ == "__main__":
    with open(DATAP + '/catdict.json', 'r', encoding="UTF8") as f:
        catdict = load(f)
        catdict = check_cat_name(catdict)
        f.close()
    with open(DATAP + '/catdict.json', 'w', encoding="UTF8") as f:
        dump(obj=catdict, fp=f, indent=2)
        f.flush()
        f.close()
