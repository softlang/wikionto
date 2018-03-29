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

properties = ['DbpediaInfobox','StanfordPOSHypernym','StanfordCOPHypernym','SemanticallyRelevant','DbpediaHypernym']

def eval_lang_dict():
    f= open(DATAP+'/langdict.json', 'r',encoding="UTF8")
    lf = pd.DataFrame(load(f)).transpose()
    catalog = lf.reindex(columns=properties+["CLDepth","CFFDepth",'GitSeed'])
    print(catalog.describe().to_latex())
    
    fig, axes = plt.subplots(nrows=2, ncols=len(properties))
    
    for x in range(len(properties)):
        p = properties[x]
        
        rfail = catalog[(catalog.CLDepth>=0) & (catalog[p]==0)].groupby(by=['CLDepth']).apply(lambda x: len(x))
        rfail.to_frame(p+'Fails').plot(kind='bar',ax=axes[0,x],color = 'blue')
        
        rsuccess = catalog[(catalog.CLDepth>=0) & (catalog[p]==1)].groupby(by=['CLDepth']).apply(lambda x: len(x))
        rsuccess.to_frame(p+'Succeeds').plot(kind='bar',ax=axes[1,x],color = 'blue', linestyle='dashed')
    
    for axar in axes:
        for ax in axar:
            for p in ax.patches:
                ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()
    
def eval_cat_dict():
    f= open(DATAP+'/catdict.json', 'r',encoding="UTF8")
    cf = pd.DataFrame(load(f)).transpose()
    catalog = cf.reindex(columns=["CLDepth","CFFDepth",'NonEmptyCategory','IncludedNamePattern','Eponymous'])
    
    fig, axes = plt.subplots(nrows=1, ncols=1)
    
    categories = catalog[(catalog.CLDepth>=0)].groupby(by=['CLDepth']).apply(lambda x: len(x)).to_frame('#fail-categories')
    categories.fillna(0)
    categories.plot(kind='bar',ax=axes,color = 'blue')
    cfail = catalog[(catalog.CLDepth>=0) & (catalog.NonEmptyCategory==1)].groupby(by=['CLDepth']).apply(lambda x: len(x)).to_frame('#ok-Categories')
    cfail.fillna(0)
    cfail.plot(kind='bar',ax=axes,color = 'orange')
    
    for p in axes.patches:
        axes.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()
    
def sampling_buckets():
    f= open(DATAP+'/langdict.json', 'r',encoding="UTF8")
    lf = pd.DataFrame(load(f)).transpose()
    catalog = lf.reindex(columns=properties+["CLDepth","CFFDepth",'GitSeed'])
    
    fig, axes = plt.subplots(nrows=1, ncols=2)
    rtotal = catalog[(catalog.CLDepth>=0)].groupby(by=['CLDepth','StanfordPOSHypernym','SemanticallyRelevant']).apply(lambda x: len(x))
    rtotal.to_frame('#language-articles').plot(kind='bar',ax=axes[0],color = 'blue')
    rtotal = catalog[(catalog.CFFDepth>=0)].groupby(by=['CFFDepth','StanfordPOSHypernym','SemanticallyRelevant']).apply(lambda x: len(x))
    rtotal.to_frame('#format-articles').plot(kind='bar',ax=axes[1],color = 'orange')
    for ax in axes:
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()
    
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

if __name__ == '__main__':
    #eval_lang_dict()
    #eval_cat_dict()
    #sampling_buckets()
    dbpediahyp_vs_pos()
    #dbpediaprop_vs_pos()
    #dbpediaprop_single_vs_pos()
