from data import DATAP
from json import load

f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
d = load(f)
f.close()
sl = d.keys()
print(len(sl))
sl = list(cl for cl in d if "Summary" not in d[cl])
print(len(sl))
sl = list(cl for cl in d if "Summary" in d[cl] and "POS_isa" in d[cl] and d[cl]["POS_isa"]==1)
print(len(sl))
sl = list(cl for cl in d if "Summary" in d[cl] and "POS_isoneof" in d[cl] and d[cl]["POS_isoneof"]==1)
print(len(sl))
sl = list(cl for cl in d if "Summary" in d[cl] and "POS_The" in d[cl] and d[cl]["POS_The"]==1)
print(len(sl))
sl_nopat = list(cl for cl in d if "Summary" in d[cl] and "POS_isa" in d[cl] and d[cl]["POS_isa"]==0
                                               and "POS_isoneof" in d[cl] and d[cl]["POS_isoneof"]==0
                                               and "POS_The" in d[cl] and d[cl]["POS_The"]==0)
print(len(sl_nopat))
ind = ["URLPattern", "URLBracesPattern", "In_Wikipedia_List", "PlainTextKeyword", "POS", "negativeSeed"]
sl_noind = [l for l in sl_nopat if not any(d[l][p]==1 for p in ind)]
print(len(sl_noind))
#for l in sl_noind:
#    if "file" in d[l]["Summary"]:
#        print("----"+l)

for x in range(10):
    l = sl_noind[x]
    print(l+": "+d[l]["Summary"])
sl = list(cl for cl in d if "Summary" in d[cl] and "POS_isa" not in d[cl])
print(len(sl))
