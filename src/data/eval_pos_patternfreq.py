from data import DATAP
from json import load
from pandas import DataFrame, Series

f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
d = load(f)
f.close()
sl = d.keys()
print(len(sl))
sl = list(cl for cl in d if "Summary" not in d[cl])
print(len(sl))
print(len([l for l in d if "Summary" in d[l] and d[l]["POS"] == 1]))

# print([l for l in sl if "is a" not in d[l]["Summary"]])
sl_nopat = list(cl for cl in d if "Summary" in d[cl] and "POS_isa" in d[cl] and d[cl]["POS_isa"] == 0
                and "POS_isoneof" in d[cl] and d[cl]["POS_isoneof"] == 0
                and "POS_The" in d[cl] and d[cl]["POS_The"] == 0)
print(len(sl_nopat))
ind = ["URLPattern", "URLBracesPattern", "In_Wikipedia_List", "POS", "negativeSeed"]
sl_noind = [l for l in sl_nopat if d[l]["PlainTextKeyword"] == 1 and not any(d[l][p] == 1 for p in ind)]
print(len(sl_noind))
# for l in sl_noind:
#    if "file" in d[l]["Summary"]:
#        print("----"+l)

for x in range(10):
    l = sl_noind[x]
    print(l + ": " + d[l]["Summary"])
sl = list(cl for cl in d if "Summary" in d[cl] and "POS_isa" not in d[cl])
print(len(sl))

pset = []
for l in d:
    for p in d[l]:
        if p.startswith("POS_") and p not in pset:
            pset.append(p)
print(pset)
df = DataFrame(columns=['Formula', 'All', 'Positive'], index=pset)
for p in pset:
    pat = [l for l in d if "Summary" in d[l] and p in d[l] and d[l][p] == 1]
    pos = [l for l in pat if d[l]["POS"] == 1]
    print(len(pos))
    df.loc[p] = Series({'Formula': 0, 'All': len(pat), 'Positive': len(pos)})

print(df.to_latex())


