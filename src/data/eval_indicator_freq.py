from data import DATAP
from json import load

f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
d = load(f)
f.close()

print(len(d.keys()))
sls = len([l for l in d if "DbpediaInfoboxTemplate" in d[l]])
print(sls)
sls = len([l for l in d if '(' in l])
print(sls)
