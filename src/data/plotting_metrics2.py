from data import CATS, DATAP, DEPTH
from json import load
from pandas import read_csv
import matplotlib.pyplot as plt
from io import StringIO


def boxplot(m):
    f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
    d = load(f)
    f.close()
    fig, ax = plt.subplots(nrows=1, ncols=len(CATS))
    for i in range(len(CATS)):
        # columns: Article, Depth, Metric m
        cat = CATS[i]
        csvtext = ""
        for cl in d:
            if cat + "Depth" in d[cl] and m in d[cl] and d[cl]["ValidInfobox"]==1:
                csvtext += str(d[cl][cat + "Depth"]) + ", " + str(d[cl][m]) + "\n"
        if not csvtext:
            continue
        #print(csvtext)
        dtypes = {"Depth": int, m: int}
        df = read_csv(StringIO(csvtext), delimiter=',', names=["Depth", m],
                      dtype=dtypes)
        ax[i].set_title('')
        df.boxplot(by="Depth", ax=ax[i])
    plt.show()


if __name__ == '__main__':
    boxplot("SemanticDistance")
