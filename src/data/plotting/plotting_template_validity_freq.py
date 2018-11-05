import matplotlib.pyplot as plt
from json import load
from data import DATAP, ROOTS
from pandas import read_csv
from io import StringIO
from check.infobox_dbpedia_existence import validibs, nonnegibs

ton = 9
f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
langdict = load(f)
fig, ax = plt.subplots(nrows=1, ncols=1)
depthlist = []

csvtext = ""
for i in range(ton):
    csvtext += str(i)
    cls = set(cl for cl in langdict if any(cat +"Depth" in langdict[cl] and langdict[cl][cat+"Depth"] == i for cat in ROOTS))

    clspos = set(cl for cl in cls if "DbpediaInfoboxTemplate" in langdict[cl] and any(temp in validibs for temp in langdict[cl]["DbpediaInfoboxTemplate"]))
    clsneu = set(cl for cl in cls if "DbpediaInfoboxTemplate" in langdict[cl] and any(
        temp in nonnegibs for temp in langdict[cl]["DbpediaInfoboxTemplate"]))
    clsneg = set(cl for cl in cls if "DbpediaInfoboxTemplate" in langdict[cl] and "negativeSeed" in langdict[cl] and langdict[cl]["negativeSeed"]==1)
    csvtext += ","+str(len(clspos))+","+str(len(clsneu))+","+str(len(clsneg))+"\n"

columns = ["articles with positive template", "articles with neutral template", "#articles with negative template"]
dtypes = dict()
dtypes["depth"] = int
for ind in columns:
    dtypes[ind] = int

df = read_csv(StringIO(csvtext), delimiter=',', names=["depth"] + columns,
              dtype=dtypes)
print(df)
df.plot(x="depth", y=columns, kind="bar", ax=ax, logy=True, width=0.8)

ax.set_title('Template Frequency')
plt.show()
