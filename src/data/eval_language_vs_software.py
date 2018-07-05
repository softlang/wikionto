from json import load
from data import DATAP


f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
ld = load(f)

ls_i = [l for l in ld if ld[l]["ValidInfobox"]==1 and "(software)" in l]
print(len(ls_i))

ls_u = [l for l in ld if (ld[l]["URLBracesPattern"]==1 or ld[l]["URLPattern"]==1)
                            and "DbpediaInfoboxTemplate" in ld[l]
                            and "infobox_software" in ld[l]["DbpediaInfoboxTemplate"]]
print(len(ls_u))

ls_ii = [l for l in ld if "DbpediaInfoboxTemplate" in ld[l]
         and "infobox_software" in ld[l]["DbpediaInfoboxTemplate"]
         and ld[l]["ValidInfobox"]==1]
print(len(ls_ii))

ls_pi = [l for l in ld if "POSHypernyms" in ld[l] and "software" in ld[l]["POSHypernyms"] and ld[l]["ValidInfobox"]==1]
print(len(ls_pi))

ls_ip = [l for l in ld if ld[l]["POS"] == 1 and "DbpediaInfoboxTemplate" in ld[l]
         and "infobox_software" in ld[l]["DbpediaInfoboxTemplate"]]
print(len(ls_ip))