import matplotlib.pyplot as plt
from json import load
from data import DATAP, CATS
from pandas import read_csv
from io import StringIO

ton = 9
f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
langdict = load(f)
fig, ax = plt.subplots(nrows=1, ncols=1)
depthlist = []
indicators = ["ValidInfobox", "URLBracesPattern", "URLPattern", "In_Wikipedia_List", "PlainTextKeyword", "POS"]

csvtext = ""
for i in range(ton):
    csvtext += str(i)
    for ind in indicators:
        indlist = [cl for cl in langdict if any(cat+"Depth" in langdict[cl] and langdict[cl][cat+"Depth"]==i for cat in CATS)
                                                     and ind in langdict[cl] and langdict[cl][ind]==1]
        csvtext += ","+str(len(indlist))
    csvtext += "\n"


dtypes = dict()
dtypes["depth"] = int
for ind in indicators:
    dtypes[ind] = int

df = read_csv(StringIO(csvtext), delimiter=',', names=["depth"] + indicators,
              dtype=dtypes)
print(df)
df.plot(x="depth", y=indicators, kind="bar", ax=ax, logy=True, width=0.8)

ax.set_title('Positive Indicator Frequency')
plt.show()
