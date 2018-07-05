from json import load
from data import DATAP
from collections import deque
from data.eval import check_sl

f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
ld = load(f)

f = open(DATAP + '/catdict.json', 'r', encoding="UTF8")
cd = load(f)

sdt = "Statistical_data_types"

catqueue = deque([sdt])
cat_done = set()

no_sls = set()
sls = set()

while not len(catqueue) == 0:
    cat = catqueue.pop()
    if "subcats" in cd[cat]:
        for subcat in cd[cat]["subcats"]:
            catqueue.append(subcat)
    if "articles" in cd[cat]:
        for a in cd[cat]["articles"]:
            if check_sl(a,ld):
                sls.add(a)
            else:
                no_sls.add(a)

print(len(no_sls))
print(len(sls))