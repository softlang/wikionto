from data import DATAP
from json import load
from pandas import DataFrame, Series

f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
ld = load(f)
inds = ["ValidInfobox", "URLPattern", "URLBracesPattern", "In_Wikipedia_List", "PlainTextKeyword", "POS"]
df = DataFrame(columns=['Articles', 'Ex', 'Positive', 'Solo'], index=inds)
for ind in inds:
    sls = [l for l in ld if ld[l][ind] == 1]
    sls_only = [l for l in ld if ld[l][ind] == 1 and not any(ld[l][p] == 1 for p in inds if p is not ind)]
    print(ind + ": " + str(len(sls_only)) + "/" + str(len(sls)))
    df.loc[ind] = Series({'Articles': len(ld.keys()),
                          'Ex': 0,
                          'Positive': len(sls),
                          'Solo': len(sls_only)})
print(df.to_latex())

print(len(ld.keys()))
sls = len([l for l in ld if "DbpediaInfoboxTemplate" in ld[l]])
print(sls)
sls = len([l for l in ld if '(' in l])
print(sls)
