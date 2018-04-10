'''
Created on 22.01.2018

@author: MarcelLocal

Stratification by Hypernym, Depth, SemanticRelevance

Infobox & not Hypernym
no test succeeds
how many tests succeed?
'''
import pandas as pd
from json import load
import matplotlib.pyplot as plt
from data import DATAP


def pos_vs_cop():
    f= open(DATAP+'/langdict.json', 'r',encoding="UTF8")
    cldict = load(f)
    for cl in cldict:
        if (cldict[cl]["StanfordPOSHypernym"] == 0) and (cldict[cl]["StanfordCOPHypernym"] == 1):
            print(cl)


def dbpediahyp_vs_pos():
    f= open(DATAP+'/langdict.json', 'r',encoding="UTF8")
    cldict = load(f)
    for cl in cldict:
        if (cldict[cl]["StanfordPOSHypernym"] == 0) and (cldict[cl]["DbpediaHypernym"] == 1):
            print(cl + ':' + cldict[cl]["Summary"])    


def dbpediaprop_vs_pos():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    lf = pd.DataFrame(langdict).transpose()
    catalog = lf.reindex(columns=["StanfordPOSHypernym", "DbpediaInfobox"])
    #print(catalog.describe().to_latex())

    fig, axes = plt.subplots(nrows=1, ncols=1)
    rfail = catalog.groupby(by=["StanfordPOSHypernym", "DbpediaInfobox"]).apply(lambda x: len(x))
    rfail.to_frame('Combis').plot(kind='bar', ax=axes, color='blue')
    for p in axes.patches:
        axes.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()
    for cl in langdict:
        if (langdict[cl]["StanfordPOSHypernym"] == 0) and (langdict[cl]["DbpediaInfobox"]==1):
            print(cl)


def dbpediaprop_single_vs_pos():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    for cl in langdict:
        if "properties" not in langdict[cl]:
            continue
        if (langdict[cl]["StanfordPOSHypernym"] == 0) and ("paradigm" in langdict[cl]["properties"]):
            print("paradigm: "+cl +"  - "+langdict[cl]["Summary"])
        if (langdict[cl]["StanfordPOSHypernym"] == 0) and ("fileExt" in langdict[cl]["properties"]):
            print("fileExt: "+cl +"  - "+langdict[cl]["Summary"])
        if (langdict[cl]["StanfordPOSHypernym"] == 0) and ("implementations" in langdict[cl]["properties"]):
            print("implementations: "+cl +"  - "+langdict[cl]["Summary"])
        if (langdict[cl]["StanfordPOSHypernym"] == 0) and ("typing" in langdict[cl]["properties"]):
            print("typing: "+cl +"  - "+langdict[cl]["Summary"])


def versus():
    print("POS vs Gitseed")
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    for cl in langdict:
        if "GitSeed" in langdict[cl]:
            if (langdict[cl]["GitSeed"] == 1) and (langdict[cl]["StanfordPOSHypernym"]==0):
                print(cl + ': ' + langdict[cl]["Summary"])


def seed_depth():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    max_cl = 0
    max_cff = 0
    for cl in langdict:
        if "GitSeed" in langdict[cl]:
            if (langdict[cl]["GitSeed"] == 1) & (langdict[cl]["CLDepth"] > max_cl):
                max_cl = langdict[cl]["CLDepth"]
            if (langdict[cl]["GitSeed"] == 1) & (langdict[cl]["CFFDepth"] > max_cff):
                max_cff = langdict[cl]["CLDepth"]
    print(max_cl)
    print(max_cff)
