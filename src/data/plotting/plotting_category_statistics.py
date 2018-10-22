from data import DATAP, CATS
from data.eval import check_sl
from collections import deque
from json import load
import matplotlib.pyplot as plt
from pandas import read_csv
from io import StringIO

def plot_statistics():
    f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
    ld = load(f)
    f = open(DATAP + '/ocatdict.json', 'r', encoding="UTF8")
    cd = load(f)

    csvtext = ""
    for c in cd:
        csvtext += c + "<->" + str(cd[c]["#SLs"]) + "<->" + str(cd[c]["#NonSLs"]) + "\n"


    dtypes = { "category": object,
        "#SL": int,
                  "#NonSL": int}

    #print(csvtext)

    df = read_csv(StringIO(csvtext), delimiter='<->', names=["category", "#SL", "#NonSL"],
                      dtype=dtypes)
    #print(df)
    df = df.fillna(0)
    print(df)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    df = df[df["#NonSL"]<10000]
    df.plot(x="#SL", y="#NonSL", kind="scatter", ax=ax, color="blue")

    ax.set_title('Assessing Categories')
    plt.show()

if __name__ == '__main__':
    plot_statistics()
