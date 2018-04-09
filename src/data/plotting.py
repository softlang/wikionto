from data import DATAP
from json import load
import pandas
import matplotlib.pyplot as plt


def langdict_to_csv():
    f = open(DATAP+'/langdict.json', 'r',encoding="UTF8")
    langdict = load(f)
    with open(DATAP+'/langdict.csv','w',encoding="UTF8") as fcsv:
        for cl in langdict:
            cl_depth = langdict[cl]["CLDepth"]
            cff_depth = langdict[cl]["CFFDepth"]
            sem_dist = langdict[cl]["SemanticDistance"]
            cat_nr = langdict[cl]["NumberOfCategories"]
            fcsv.write(cl+'&&'+str(cl_depth)+'&&'+str(cff_depth)+'&&'+str(sem_dist)+'&&'+str(cat_nr)+'\n')
        fcsv.flush()
        fcsv.close()


def depth_semdist_catnr():
    f = open(DATAP + '/langdict.csv',encoding="UTF8")
    headers = ['name', 'cldepth','cffdepth','semdist','#categories']
    df = pandas.read_csv(f, delimiter='&&',names=headers, dtype={'name': object,'cldepth':int,'cffdepth':int,'semdist':int,'#categories':int})
    print(df)
    df = df.sort_values(by=['semdist'])

    ax = df.plot(x='name', y='#categories')
    df.plot(x='name', y='semdist', ax=ax)
    df.plot(x='name', y='cffdepth', ax=ax)
    df.plot(x='name', y='cldepth',ax=ax)
    plt.show()


if __name__ == '__main__':
    langdict_to_csv()
    depth_semdist_catnr()
