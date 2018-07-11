import matplotlib.pyplot as plt
from json import load
from data import DATAP, CATS, DEPTH
from pandas import read_csv
from io import StringIO


def plot_allsl_depth(ton):
    f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    depthlist = []
    for c in CATS:
        depthlist.append(list(map(lambda d: len([cl for cl in langdict
                                                 if
                                                 ((c + "Depth" in langdict[cl]) and (langdict[cl][c + "Depth"] == d)
                                                  and check_sl(cl,langdict))])
                                  , range(ton))))

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

    ax.set_title('Articles per Depth')
    ax.legend(["FL", "CFF", "IS"])
    plt.show()

def check_sl(l,d):
    checks = ["POS", "ValidInfobox", "In_Wikipedia_List", "URLPattern", "URLBracesPattern", "PlainTextKeyword"]
    #checks = ["URLPattern"]
    return True #any(d[l][c]==1 for c in checks)

if __name__ == '__main__':
    plot_allsl_depth(DEPTH+1)