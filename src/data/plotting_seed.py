import matplotlib.pyplot as plt
from data.plotting import load_langdict_csv
import numpy as np
from json import load
from data import DATAP
from pandas import read_csv
from io import StringIO


def plot_allsl_depth(ton):
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    langdict["CLDepth"] = dict()
    langdict["CFFDepth"] = dict()
    cldepths = list(map(lambda d: len([cl for cl, feat in langdict.items()
                                       if (("CLDepth" in langdict[cl]) and (langdict[cl]["CLDepth"] == d))])
                        , range(ton)))
    cffdepths = list(map(lambda d: len([cl for cl, feat in langdict.items()
                                        if (("CFFDepth" in langdict[cl]) and (langdict[cl]["CFFDepth"] == d))])
                         , range(ton)))

    csvtext = ""
    for x in range(ton):
        csvtext += str(x) + ", " + str(cldepths[x]) + ", " + str(cffdepths[x]) + "\n"
    df = read_csv(StringIO(csvtext), delimiter=',', names=["depth", "#CL", "#CFF"],
                  dtype={'depth': int,
                         '#CL': int,
                         '#CFF': int})
    print(df)
    ax = df.plot(x="depth", y=["#CL", "#CFF"], kind="bar", logy=True, width=0.8, color=["black","grey"])

    ax.set_title('Articles at Depth')
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()

def plot_seed_depth(ton):
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    langdict["CLDepth"] = dict()
    langdict["CFFDepth"] = dict()
    cldepths = list(map(lambda d: len([cl for cl,feat in langdict.items()
                                       if (("CLDepth" in langdict[cl]) and (langdict[cl]["CLDepth"] == d))
                                       and (langdict[cl]["Seed"] == 1)])
                        , range(ton)))
    cffdepths = list(map(lambda d: len([cl for cl,feat in langdict.items()
                                       if (("CFFDepth" in langdict[cl]) and (langdict[cl]["CFFDepth"] == d))
                                       and (langdict[cl]["Seed"] == 1)])
                         , range(ton)))

    csvtext = ""
    for x in range(ton):
        csvtext += str(x) + ", " + str(cldepths[x]) + ", " + str(cffdepths[x]) + "\n"
    df = read_csv(StringIO(csvtext), delimiter=',', names=["depth", "#CL", "#CFF"],
                  dtype={'depth': int,
                         '#CL': int,
                         '#CFF': int})
    print(df)
    ax = df.plot(x="depth", y=["#CL", "#CFF"], kind="bar", logy=True, width=0.8, color=["black","grey"])

    ax.set_title('Seed_Depth')
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()


if __name__ == "__main__":
    plot_allsl_depth(8)
