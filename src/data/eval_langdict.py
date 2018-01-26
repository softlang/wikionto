'''
Created on 22.01.2018

@author: MarcelLocal
'''
import json

def save_list(name, cllist):
    f = open(name+".txt","w")
    for cl in cllist:
        f.write(str(cl.encode('utf-8'))+"\n")
    f.flush()
    f.close()

def infobox_and_not_hypernym():
    with open('langdict.json', 'r',encoding="UTF8") as f:    
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            infobox = False
            hypernym = False
            for p in langdict[cl]:
                if "Hypernym" in p:
                    hypernym = hypernym | langdict[cl][p]
                if "infobox" in p:
                    infobox = infobox | langdict[cl][p]
            if infobox & (not hypernym):
                cls1.add(cl)
        save_list("eval/infoboxAndnothypernym", cls1)

def total():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        print(len(langdict))
        
def dbpedia_hypernym():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            hypernym = False
            for p in langdict[cl]:
                if "DbpediaHypernym" in p:
                    hypernym = hypernym | langdict[cl][p]
            if hypernym:
                cls1.add(cl)
        save_list("eval/DbpediaHypernym", cls1)
        
def wordnet_hypernym():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            hypernym = False
            for p in langdict[cl]:
                if "WordnetHypernym" in p:
                    hypernym = hypernym | langdict[cl][p]
            if hypernym:
                cls1.add(cl)
        save_list("eval/WordnetHypernym", cls1)
        
def stanford_hypernym():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            hypernym = False
            for p in langdict[cl]:
                if "Stanford" in p:
                    hypernym = hypernym | langdict[cl][p]
            if hypernym:
                cls1.add(cl)
        save_list("eval/StanfordHypernym", cls1)
        
def infobox():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            check = False
            for p in langdict[cl]:
                if "infobox" in p:
                    check = check | langdict[cl][p]
            if check:
                cls1.add(cl)
        save_list("eval/Infobox", cls1)
        
def sem_dist():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            check = True
            for p in langdict[cl]:
                if "Distant" in p:
                    check = check | langdict[cl][p]
            if not check:
                cls1.add(cl)
        save_list("eval/Distant", cls1)

def none():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            check = False
            for p in langdict[cl]:
                if isinstance(langdict[cl][p],bool) & (not(p == "SummaryExists")): 
                    check = check | langdict[cl][p]
            if not check:
                cls1.add(cl)
        save_list("eval/None", cls1)

total()
none()
dbpedia_hypernym()
wordnet_hypernym()
stanford_hypernym()
infobox()