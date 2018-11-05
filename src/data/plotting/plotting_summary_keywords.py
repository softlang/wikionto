import matplotlib.pyplot as plt
from json import load
from data import DATAP, ROOTS
from pandas import read_csv
from io import StringIO


def plot_seed_depth(ton):
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    depthlist = []
    for c in ROOTS:
        depthlist.append(list(map(lambda d: len([cl for cl in langdict
                                                 if
                                                 ((c + "Depth" in langdict[cl]) and (langdict[cl][c + "Depth"] == d))
                                                 and langdict[cl]["PlainTextKeyword"] == 1])
                                  , range(ton))))

    csvtext = ""
    for n in range(ton):
        csvtext += str(n)
        for i in range(len(ROOTS)):
            csvtext += ", " + str(depthlist[i][n])
        csvtext += "\n"

    dtypes = dict()
    dtypes["depth"] = int
    for c in ROOTS:
        dtypes[c] = int

    df = read_csv(StringIO(csvtext), delimiter=',', names=["depth"] + ROOTS,
                  dtype=dtypes)
    print(df)
    df.plot(x="depth", y=ROOTS, kind="bar", ax=ax, logy=True, width=0.8, color=["red", "green", "blue"])

    ax.set_title('Articles with Keywords in Summary')
    #for p in ax.patches:
        #ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()


if __name__ == '__main__':
    plot_seed_depth(9)
