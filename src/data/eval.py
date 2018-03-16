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

properties = ['DbpediaInfobox','StanfordPOSHypernym','StanfordCOPHypernym','WordnetHypernym'
                              ,'SemanticallyRelevant']

def eval_lang_dict():
    f= open('langdict.json', 'r',encoding="UTF8")
    lf = pd.DataFrame(load(f)).transpose()
    catalog = lf.reindex(columns=properties+["CLDepth","CFFDepth",'GitSeed'])
    print(catalog.describe().to_latex())
    
    fig, axes = plt.subplots(nrows=2, ncols=len(properties))
    
    for x in range(len(properties)):
        p = properties[x]
        print(p)
        
        rtotal = catalog[(catalog.CLDepth>=0)].groupby(by=['CLDepth']).apply(lambda x: len(x))
        rtotal.to_frame('#articles').plot(kind='bar',ax=axes[0,x],color = 'orange')
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
    f= open('catdict.json', 'r',encoding="UTF8")
    cf = pd.DataFrame(load(f)).transpose()
    catalog = cf.reindex(columns=["CLDepth","CFFDepth",'NonEmptyCategory','IncludedNamePattern','Eponymous'])
    
    fig, axes = plt.subplots(nrows=1, ncols=1)
    
    categories = catalog[(catalog.CLDepth>=0)].groupby(by=['CLDepth']).apply(lambda x: len(x)).to_frame('#categories')
    categories.fillna(0)
    categories.plot(kind='bar',ax=axes,color = 'blue')
    cfail = catalog[(catalog.CLDepth>=0) & (catalog.NonEmptyCategory==0)].groupby(by=['CLDepth']).apply(lambda x: len(x)).to_frame('#failCategories')
    cfail.fillna(0)
    cfail.plot(kind='bar',ax=axes,color = 'orange')
    
    for p in axes.patches:
        axes.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()
    
if __name__ == '__main__':
    #eval_lang_dict()
    eval_cat_dict()