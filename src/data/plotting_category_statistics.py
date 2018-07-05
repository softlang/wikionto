from data import DATAP
from data.eval import check_sl
from collections import deque
from json import load
import matplotlib.pyplot as plt
from pandas import read_csv
from io import StringIO

def plot_statistics():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    ld = load(f)
    f = open(DATAP + '/catdict.json', 'r', encoding="UTF8")
    cd = load(f)

    csvtext = ""
    for c in cd:
        csvtext += c + "<->" + str(cd[c]["#SLs"]) + "<->" + str(cd[c]["#NonSLs"]) + "\n"


    dtypes = { "category": object,
        "#Classified as SL": int,
                  "#Classified as Non-SL": int}

    print(csvtext)

    df = read_csv(StringIO(csvtext), delimiter='<->', names=["category", "#Classified as SL", "#Classified as Non-SL"],
                      dtype=dtypes)
    print(df)
    df = df.fillna(0)
    df = df.sort_values(by=["#Classified as SL", "#Classified as Non-SL"])
    #print(df)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    df.plot(x="category", y="#Classified as Non-SL", kind="line", ax=ax, logy=True, color="red")
    df.plot(x="category", y="#Classified as SL", kind="line", ax=ax, logy=True, color="green")

    ax.set_title('Assessing Categories')
    plt.show()

if __name__ == '__main__':
    plot_statistics()
