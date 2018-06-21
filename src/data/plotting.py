from data import DATAP, CLDEPTH
from json import load
import pandas
from io import StringIO
import matplotlib.pyplot as plt

FEATURES = ["Seed", "DbpediaHypernym", "PlainTextKeyword", "POS", "COP", "URLPattern",
            "URLBracesPattern", "MultiInfobox", "Infobox programming language", "Infobox file format",
            "Infobox software", "wikidata_CL", "yago_CL"]

METRICS = ["CLDepth", "CFFDepth", "SemanticDistance", "NumberOfCategories", "Seed_Similarity"]

HEADERS = FEATURES + METRICS


def langdict_to_csv():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    with open(DATAP + '/langdict.csv', 'w', encoding="UTF8") as fcsv:
        for cl in langdict:
            row = cl
            for p in HEADERS:
                if p in langdict[cl]:
                    row += '<->' + str(langdict[cl][p])
                else:
                    row += '<->0'
            fcsv.write(row + '\n')
        fcsv.flush()
        fcsv.close()


def load_langdict_csv():
    f = open(DATAP + '/langdict.csv', 'r', encoding="UTF8")
    df = pandas.read_csv(f, delimiter='<->', names=["name"]+HEADERS,
                         dtype={'name': object,
                                "Seed": int,
                                "DbpediaHypernym": int,
                                "POS": int,
                                "COP": int,
                                "URLPattern": int,
                                "URLBracesPattern": int,
                                "MultiInfobox": int,
                                "Infobox programming language": int,
                                "Infobox file format": int,
                                "Infobox software": int,
                                "wikidata_CL": int,
                                "yago_CL": int,
                                "CLDepth": int,
                                "CFFDepth": int,
                                "SemanticDistance": int,
                                "NumberOfCategories": int,
                                "Seed_Similarity": float})
    return df


def plot_features():
    df = load_langdict_csv()
    # print(df.describe().to_latex())

    fig, axes = plt.subplots(nrows=2, ncols=(len(FEATURES)))

    for x in range(len(FEATURES)):
        p = FEATURES[x]
        print(p)
        rfail = df[(df.CLDepth >= 0) & (df[p] == 0)].groupby(by=['CLDepth']).apply(lambda x: len(x))
        rfail.plot(kind='bar', ax=axes[0, x], color='blue', linestyle='dashed')

        rsuccess = df[(df.CLDepth >= 0) & (df[p] == 1)].groupby(by=['CLDepth']).apply(lambda x: len(x))
        rsuccess.plot(kind='bar', ax=axes[1, x], color='blue', linestyle='dashed')

    for axar in axes:
        for ax in axar:
            for p in ax.patches:
                ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()


def plot_feature(feature,title,ton=(CLDEPTH+1)):
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    langdict["CLDepth"] = dict()
    langdict["CFFDepth"] = dict()
    cldepths = list(map(lambda d: len([cl for cl, feat in langdict.items()
                                       if (("CLDepth" in langdict[cl]) and (langdict[cl]["CLDepth"] == d))
                                       and (langdict[cl][feature] == 1)])
                        , range(ton)))
    cffdepths = list(map(lambda d: len([cl for cl, feat in langdict.items()
                                        if (("CFFDepth" in langdict[cl]) and (langdict[cl]["CFFDepth"] == d))
                                        and (langdict[cl][feature] == 1)])
                         , range(ton)))

    csvtext = ""
    for x in range(ton):
        csvtext += str(x) + ", " + str(cldepths[x]) + ", " + str(cffdepths[x]) + "\n"
    df = pandas.read_csv(StringIO(csvtext), delimiter=',', names=["depth", "#CL", "#CFF"],
                  dtype={'depth': int,
                         '#CL': int,
                         '#CFF': int})
    print(df)
    ax = df.plot(x="depth", y=["#CL", "#CFF"], kind="bar", logy=True, width=0.8, color=["black", "grey"])

    ax.set_title(title)
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()

def plot_articlesdepth(ton=(CLDEPTH+1)):
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
    df = pandas.read_csv(StringIO(csvtext), delimiter=',', names=["depth", "#CL", "#CFF"],
                  dtype={'depth': int,
                         '#CL': int,
                         '#CFF': int})
    print(df)
    ax = df.plot(x="depth", y=["#CL", "#CFF"], kind="bar", logy=True, width=0.8, color=["black", "grey"])

    ax.set_title("Articles per Depth")
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()


if __name__ == '__main__':
    plot_articlesdepth()
