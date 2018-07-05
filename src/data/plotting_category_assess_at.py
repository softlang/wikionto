import matplotlib.pyplot as plt
from json import load
from data import DATAP, CATS
from pandas import read_csv
from io import StringIO


def plot_cats(fromn=0, ton=8):
    f = open(DATAP + '/catdict.json', 'r', encoding="UTF8")
    catdict = load(f)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    depthlist = []
    for c in CATS:
        depthlist.append(list(map(lambda d: len([cat for cat in catdict
                                                 if
                                                 ((c + "Depth" in catdict[cat]) and (catdict[cat][c + "Depth"] == d)
                                                  and check_cat(cat, catdict))])
                                  , range(fromn, ton))))

    csvtext = ""
    for n in range(ton):
        csvtext += str(n)
        for i in range(len(CATS)):
            csvtext += ", " + str(depthlist[i][n])
        csvtext += "\n"

    dtypes = dict()
    dtypes["depth"] = int
    for c in CATS:
        dtypes[c] = int

    df = read_csv(StringIO(csvtext), delimiter=',', names=["depth"] + CATS,
                  dtype=dtypes)
    print(df)
    df.plot(x="depth", y=CATS, kind="bar", ax=ax, logy=True, width=0.8, color=["red", "green", "blue"])

    ax.set_title('Articles at Depth')
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()


def check_cat(cat, catdict):
    return True
