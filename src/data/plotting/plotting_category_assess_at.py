import matplotlib.pyplot as plt
from json import load
from data import DATAP, CATS
from pandas import read_csv
from io import StringIO

def plot_cats(fromn=0, ton=9):
    f = open(DATAP + '/ocatdict.json', 'r', encoding="UTF8")
    catdict = load(f)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    depthlist = []
    for c in CATS:
        depthlist.append(list(map(lambda d: len([cat for cat in catdict
                                                 if
                                                 ((c + "Depth" in catdict[cat]) and (catdict[cat][c + "Depth"] == d)
                                                  and check_cat(cat, catdict,True))])
                                  , range(fromn, ton))))

    csvtext = ""
    for n in range(fromn, ton):
        csvtext += str(n)
        for i in range(len(CATS)):
            csvtext += ", " + str(depthlist[i][n - fromn])
        csvtext += "\n"

    dtypes = dict()
    dtypes["depth"] = int
    for c in CATS:
        dtypes[c] = int

    df = read_csv(StringIO(csvtext), delimiter=',', names=["depth"] + CATS,
                  dtype=dtypes)
    print(df)
    df.plot(x="depth", y=CATS, kind="bar", ax=ax, logy=True, width=0.8)

    ax.set_title('#Strong valid Categories at Depth')
    ax.legend(["FL","CFF","IS"])
    #for p in ax.patches:
    #    ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()


def check_cat(cat, catdict, check=False):
    if check:
        return catdict[cat]["#NonSLs"] == 0
    else:
        return True


if __name__ == '__main__':
    plot_cats(fromn=1)
