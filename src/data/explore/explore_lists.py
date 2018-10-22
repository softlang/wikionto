from data import DATAP, KEYWORDS
from json import load

f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
ld = load(f)
for a in ld:
    if ("list" in a.lower() or "comparison" in a.lower()) and any(k in a for k in KEYWORDS):
        print(a)
