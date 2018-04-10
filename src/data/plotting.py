from data import DATAP
from json import load
import pandas
import matplotlib.pyplot as plt

plot_properties = ["CLDepth","CFFDepth","SemanticDistance","SemanticallyRelevant","NumberOfCategories","GitSeed"
    ,"DbpediaHypernym","StanfordPOSHypernym","StanfordCOPHypernym","PlainTextKeyword","NamePattern"
    ,"IncludedNamePattern","MultiInfobox","Infobox programming language","Infobox software","wikidata_CL","yago_CL"]


def langdict_to_csv():
    f = open(DATAP+'/langdict.json', 'r',encoding="UTF8")
    langdict = load(f)
    with open(DATAP+'/langdict.csv','w',encoding="UTF8") as fcsv:
        for cl in langdict:
            row = cl
            for p in plot_properties:
                row += '&&' + str(langdict[cl][p])
            fcsv.write(row+'\n')
        fcsv.flush()
        fcsv.close()


def plot_lang_dict():
    f = open(DATAP + '/langdict.csv', 'r', encoding="UTF8")
    plot_dtypes = {'name': object}
    for p in plot_properties:
        plot_dtypes[p] = int
    df = pandas.read_csv(f, delimiter='&&', names=['name']+plot_properties, dtype=plot_dtypes)
    print(df.describe().to_latex())

    fig, axes = plt.subplots(nrows=2, ncols=len(plot_properties))

    for x in range(len(plot_properties)):
        p = plot_properties[x]

        rfail = df[(df.CLDepth >= 0) & (df[p] == 0)].groupby(by=['CLDepth']).apply(lambda x: len(x))
        rfail.to_frame(p + 'Fails').plot(kind='bar', ax=axes[0, x], color='blue')

        rsuccess = df[(df.CLDepth >= 0) & (df[p] == 1)].groupby(by=['CLDepth']).apply(lambda x: len(x))
        rsuccess.to_frame(p + 'Succeeds').plot(kind='bar', ax=axes[1, x], color='blue', linestyle='dashed')

    for axar in axes:
        for ax in axar:
            for p in ax.patches:
                ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()


def depth_semdist_catnr():
    f = open(DATAP + '/langdict.csv',encoding="UTF8")
    headers = ['name', 'cldepth','cffdepth','semdist','#categories']
    df = pandas.read_csv(f, delimiter='&&',names=headers, dtype={'name': object,'cldepth':int,'cffdepth':int,'semdist':int,'#categories':int})
    print(df)
    df = df.sort_values(by=['semdist'])

    ax = df[df["cldepth"]>=0].plot(x='semdist', y='cldepth',style='.',color='blue',legend=True)
    df[df["cffdepth"]>=0].plot(x='semdist', y='cffdepth', style='.', ax=ax, color='orange')
    ax.legend()
    plt.show()


if __name__ == '__main__':
    langdict_to_csv()
    depth_semdist_catnr()
