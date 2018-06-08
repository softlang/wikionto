import pandas
import numpy as np
from decimal import Decimal, getcontext
import matplotlib.pyplot as plt
from data.plotting import load_langdict_csv


def depth_semdist_catnr():
    df = load_langdict_csv()
    print(df)
    df = df.sort_values(by=['SemanticDistance'])

    ax = df[df["CLDepth"] >= 0].plot(x='SemanticDistance', y='CLDepth', style='.', color='blue')
    df[df["CFFDepth"] >= 0].plot(x='SemanticDistance', y='CFFDepth', style='.', ax=ax, color='orange')
    ax.legend()
    plt.show()


def seed_similarity():
    df = load_langdict_csv()
    df = df.sort_values(by=['Seed_Similarity'])
    print(df)
    ax = df.plot(x='name', y='Seed_Similarity', style='.', color='blue')
    ax.legend()
    plt.show()


def seed_similarity_binned_range():
    df = load_langdict_csv()
    bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    ind = np.arange(10)
    width = 0.35

    df0 = df[(df["GitSeed"] == 0)
             & (df["TIOBE"] == 0)
             & (df["DbpediaHypernym"] == 0)
             & (df["PlainTextKeyword"] == 0)
             & (df["POS"] == 0)
             & (df["COP"] == 0)
             & (df["URLPattern"] == 0)
             & (df["URLBracesPattern"] == 0)
             & (df["Infobox programming language"] == -1)
             & (df["Infobox file format"] == -1)
             & (df["wikidata_CL"] == 0)
             & (df["yago_CL"] == 0)]
    df0 = df0.groupby(by=pandas.cut(df0['Seed_Similarity'], bins=bins)).Seed_Similarity.count()

    df1 = df[(df["GitSeed"] == 0)
             & (df["TIOBE"] == 0)
             & ((df["DbpediaHypernym"] == 1)
             | (df["PlainTextKeyword"] == 1)
             | (df["POS"] == 1)
             | (df["COP"] == 1)
             | (df["URLPattern"] == 1)
             | (df["URLBracesPattern"] == 1)
             | (df["Infobox programming language"] > -1)
             | (df["Infobox file format"] > -1)
             | (df["wikidata_CL"] == 1)
             | (df["yago_CL"] == 1))]
    df1 = df1.groupby(by=pandas.cut(df1['Seed_Similarity'], bins=bins)).Seed_Similarity.count()

    fig, ax = plt.subplots()
    rects0 = ax.bar(ind, df0, width, color='black')
    rects1 = ax.bar(ind + width, df1, width, color='lightgrey')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('')
    ax.set_title('Seed_Similarity')
    ax.set_xticks(ind + width / 2)
    getcontext().prec = 1
    ax.set_xticklabels(list(map(lambda b: "(" + str(b) + " to " + str(Decimal(b) + Decimal(0.1)) + "]", bins)))

    ax.legend((rects0[0], rects1[0]), ('Not Recognized', 'Recognized'))

    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.01 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects0)
    autolabel(rects1)

    plt.show()


if __name__ == '__main__':
    seed_similarity_binned_range()
