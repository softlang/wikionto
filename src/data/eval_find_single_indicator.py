from data import DATAP
from json import load

f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
ld = load(f)
inds = ["URLPattern", "URLBracesPattern", "In_Wikipedia_List", "PlainTextKeyword", "POS", "ValidInfobox"]

for ind in inds:
    sls = [l for l in ld if ld[l][ind] == 1]
    sls_only = [l for l in ld if ld[l][ind] == 1 and not any(ld[l][p] == 1 for p in inds if p is not ind)]
    print(ind + ": " + str(len(sls_only)) + "/" + str(len(sls)))
