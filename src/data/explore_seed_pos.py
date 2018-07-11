from data import DATAP
from json import load

f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
d = load(f)
f.close()
sl = list(cl for cl in d if (d[cl]["Seed"] == 1))
print(len(sl))
sl = list(cl for cl in d if d[cl]["Seed"] == 1 and "Summary" in d[cl] and d[cl]["POS_isa"]==1)
print(len(sl))
sl = list(cl for cl in d if (d[cl]["Seed"] == 1) and "Summary" in d[cl] and d[cl]["POS_isoneof"]==1)
print(len(sl))
sl = list(cl for cl in d if (d[cl]["Seed"] == 1) and "Summary" not in d[cl])
print(len(sl))
sl = list(cl for cl in d if (d[cl]["Seed"] == 1) and "Summary" in d[cl])
print(len(sl))
sl = list(cl for cl in d if (d[cl]["Seed"] == 1) and "Summary" in d[cl] and "POS_isa" not in d[cl])
print(len(sl))
for l in sl:
    print(l + ": " + str(d[l]))
    print("---")
