'''
Created on 22.01.2018

@author: MarcelLocal
'''
import json

properties = ['<http://dbpedia.org/property/dialects>'
                  ,'<http://dbpedia.org/property/paradigm>','<http://dbpedia.org/property/typing>'
                  ,'^<http://dbpedia.org/ontology/language>','^<http://dbpedia.org/property/language>'
                  ,'^<http://dbpedia.org/ontology/programmingLanguage>','DbpediaHypernymLanguage'
                  ,'DbpediaHypernymFormat','StanfordPOSHypernym','StanfordCOPHypernym','WordnetHypernym'
                  ,'SemanticallyRelevant',"IncludedNamePattern"]

def save_list(name, cllist):
    f = open(name+".txt","w",encoding='utf8')
    for cl in cllist:
        f.write(cl + '\n')
    f.flush()
    f.close()

def infobox_and_not_hypernym():
    with open('langdict.json', 'r',encoding="UTF8") as f:    
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            infobox = 0
            hypernym = 0
            for p in langdict[cl]:
                if "hypernym" in p.lower():
                    hypernym = hypernym + langdict[cl][p]
                if "dbpedia.org" in p:
                    infobox = infobox + langdict[cl][p]
            if (infobox>0) & (hypernym==0):
                cls1.add(cl)
        cls1 = list(map(lambda cl:cl+"\t"+langdict[cl]["Summary"],cls1))
        save_list("eval/infoboxAndnothypernym", cls1)

def total():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        print("Wikipedia lists "+str(len(langdict))+" candidates.")
        
def dbpedia_hypernym():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            hypernym = 0
            for p in langdict[cl]:
                if "DbpediaHypernym" in p:
                    hypernym = hypernym + langdict[cl][p]
            if hypernym:
                cls1.add(cl)
        save_list("eval/DbpediaHypernym", cls1)
        
def wordnet_hypernym():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            hypernym = 0
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
            hypernym = 0
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
            check = 0
            for p in langdict[cl]:
                if "dbpedia.org" in p:
                    check = check + langdict[cl][p]
            if check:
                cls1.add(cl)
        save_list("eval/Infobox", cls1)
        
def sem_dist():
    with open('langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        cls1 = set()
        for cl in langdict:
            check = 0
            for p in langdict[cl]:
                if "Relevant" in p:
                    check = check + langdict[cl][p]
            if check:
                cls1.add(cl)
        save_list("eval/Relevant", cls1)

def lang_succeeds_at_none(cl,langdict):
    check = 0
    for p in properties:
        check = check + langdict[cl][p]
    return (check==0)

def none_to_all():
    f=open('langdict.json', 'r',encoding="UTF8")
    langdict = json.load(f)
    evaldict = dict()
    for c in range(len(properties)):
        evaldict[c] = []
    for cl in langdict:
        check = 0
        for p in properties:
            check = check + langdict[cl][p]
        if check in range(len(properties)):
            if "Summary" in langdict[cl]:
                evaldict[check].append(cl+"\t"+langdict[cl]["Summary"])
            else:
                evaldict[check].append(cl)
    for c in evaldict:
        save_list("eval/Check"+str(c), evaldict[c])
        
def langdict_to_csv():
    f= open('langdict.json', 'r',encoding="UTF8")
    fcsv = open('langdict.csv','w',encoding="UTF8")
    langdict = json.load(f)
    fcsv.write('name§')
    fcsv.write('§'.join(properties))
    fcsv.write('\n')
    for cl in langdict:
        fcsv.write(cl+'§')
        for p in properties:
            if p in langdict[cl]:
                fcsv.write(str(langdict[cl][p])+'§')
            else:
                fcsv.write('§')
        fcsv.write('\n')
    f.close()
    fcsv.flush()
    fcsv.close()
    
def catdict_to_csv():
    f= open('catdict.json', 'r',encoding="UTF8")
    fcsv = open('catdict.csv','w',encoding="UTF8")
    catdict = json.load(f)
    fcsv.write('§'.join(["name","CLDepth","CFFDepth","#articles","NonEmptyCategory"]))
    fcsv.write('\n')
    for cl in catdict:
        fcsv.write(cl+'§')
        for p in properties:
            if p in catdict[cl]:
                fcsv.write(str(catdict[cl][p])+'§')
        fcsv.write('\n')
    f.close()
    fcsv.flush()
    fcsv.close()

def eval():
    total()
    infobox()
    infobox_and_not_hypernym()
    dbpedia_hypernym()
    wordnet_hypernym()
    stanford_hypernym()
    sem_dist()
    none_to_all()          
    langdict_to_csv()