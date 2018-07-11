'''
Created on 22.01.2018

@author: MarcelLocal

Stratification by Hypernym, Depth, SemanticRelevance

Infobox & not Hypernym
no test succeeds
how many tests succeed?
'''
import operator

import pandas as pd
from json import load
import matplotlib.pyplot as plt
from data import DATAP, KEYWORDS

def check_sl(l,d):
    checks = ["POS", "ValidInfobox", "In_Wikipedia_List", "URLPattern", "URLBracesPattern", "PlainTextKeyword"]
    return any(d[l][c]==1 for c in checks)

def pos_vs_cop():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    cldict = load(f)
    for cl in cldict:
        if (cldict[cl]["StanfordPOSHypernym"] == 0) and (cldict[cl]["StanfordCOPHypernym"] == 1):
            print(cl)


def dbpediahyp_vs_pos():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    cldict = load(f)
    for cl in cldict:
        if (cldict[cl]["StanfordPOSHypernym"] == 0) and (cldict[cl]["DbpediaHypernym"] == 1):
            print(cl + ':' + cldict[cl]["Summary"])


def dbpediaprop_vs_pos():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    lf = pd.DataFrame(langdict).transpose()
    catalog = lf.reindex(columns=["StanfordPOSHypernym", "DbpediaInfobox"])
    # print(catalog.describe().to_latex())

    fig, axes = plt.subplots(nrows=1, ncols=1)
    rfail = catalog.groupby(by=["StanfordPOSHypernym", "DbpediaInfobox"]).apply(lambda x: len(x))
    rfail.to_frame('Combis').plot(kind='bar', ax=axes, color='blue')
    for p in axes.patches:
        axes.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()
    for cl in langdict:
        if (langdict[cl]["StanfordPOSHypernym"] == 0) and (langdict[cl]["DbpediaInfobox"] == 1):
            print(cl)


def dbpediaprop_single_vs_pos():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    for cl in langdict:
        if "properties" not in langdict[cl]:
            continue
        if (langdict[cl]["StanfordPOSHypernym"] == 0) and ("paradigm" in langdict[cl]["properties"]):
            print("paradigm: " + cl + "  - " + langdict[cl]["Summary"])
        if (langdict[cl]["StanfordPOSHypernym"] == 0) and ("fileExt" in langdict[cl]["properties"]):
            print("fileExt: " + cl + "  - " + langdict[cl]["Summary"])
        if (langdict[cl]["StanfordPOSHypernym"] == 0) and ("implementations" in langdict[cl]["properties"]):
            print("implementations: " + cl + "  - " + langdict[cl]["Summary"])
        if (langdict[cl]["StanfordPOSHypernym"] == 0) and ("typing" in langdict[cl]["properties"]):
            print("typing: " + cl + "  - " + langdict[cl]["Summary"])


def versus():
    print("POS vs Gitseed")
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    for cl in langdict:
        if (langdict[cl]["GitSeed"] == 1) and ("POS" not in langdict[cl]) and ("POSX" not in langdict[cl]):
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


def count_pos_variants():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    pat = {p for cl in langdict for p in langdict[cl] if p.startswith('POS_')}
    pxdict = {p: {cl for (cl, cldict) in langdict.items() if p in cldict} for p in pat}
    for p, cls in pxdict.items():
        print(p + ':' + str(len(cls)))


def get_nohitpos():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    cls = [cl for cl in langdict if langdict[cl]["Summary"] == 'No Summary']
    print(len(cls))
    cls = [cl for cl in langdict if ("POS_" in langdict[cl]) and not (langdict[cl]["Summary"] == 'No Summary')
           and not cl.startswith('List') and not cl.startswith('Comparison') and any(
        k in langdict[cl]["Summary"] for k in KEYWORDS)]
    print(len(cls))
    for cl in cls:
        print(cl + ': ' + langdict[cl]["Summary"])
        text = input(">")
        if text == 'n':
            continue
        else:
            break


def topflop_pos_semdist():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)

    pattern = ["POS_isa",
               "POS_isanameof",
               "POS_isoneof",
               "POS_isafamilyof",
               "POS_The"]
    xpattern = ["POSX_theoremprover",
                "POSX_parsergenerator",
                "POSX_templateengine",
                "POSX_templatesystem",
                "POSX_templatingsystem",
                "POSX_typesettingsystem",
                "POSX_file",
                "POSX_filetype"]

    patdict = dict()
    for p in pattern:
        patdict[p] = []
        for cl in langdict:
            if p in langdict[cl] and langdict[cl][p] == 1 and ("POS" in langdict[cl] and langdict[cl]["POS"] == 1):
                patdict[p].append((cl, langdict[cl]["SemanticDistance"]))
    xpatdict = dict()
    for p in pattern:
        xpatdict[p] = []
        for cl in langdict:
            if p in langdict[cl] and langdict[cl][p] == 1 and \
                    any(xp in langdict[cl] and langdict[cl][xp] == 1 for xp in xpattern):
                xpatdict[p].append((cl, langdict[cl]["SemanticDistance"]))

    for p, cllist in patdict.items():
        cllist.sort(key=operator.itemgetter(1))
        print(p)
        if len(cllist) < 20:
            print("  all:")
            for cl in cllist:
                print("    " + str(cl))
            continue
        print("  top10: ")
        for x in range(0, 10):
            print("    " + str(cllist[x]))
        print("  flop10: ")
        for x in range(-10, 0):
            print("    " + str(cllist[x]))
    print("----Stretched pattern-----")
    for p,cllist in xpatdict.items():
        cllist.sort(key=operator.itemgetter(1))
        print(p)
        if len(cllist) < 20:
            print("  all:")
            for cl in cllist:
                print("    " + str(cl))
            continue
        print("  top10: ")
        for x in range(0, 10):
            print("    " + str(cllist[x]))
        print("  flop10: ")
        for x in range(-10, 0):
            print("    " + str(cllist[x]))

def POS_vs_URL():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    f.close()
    for cl, d in langdict.items():
        if (("No Summary" not in d) and ("POS" in d) and (d["POS"] == 0)) and ("URLBracesPattern" in d) and (
                d["URLBracesPattern"] == 1):
            print(cl)

if __name__ == "__main__":
    count_pos_variants()