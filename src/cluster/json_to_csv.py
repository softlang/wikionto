from json import load
from data import DATAP

SEPA = '(^.^)'

def convert():
    ld = load(open(DATAP + '/olangdict.json', 'r', encoding='UTF-8'))
    csv = open(DATAP + '/olangdict.csv', 'w', encoding='UTF-8')
    hypernyms = []
    words = []
    categories = []
    infobox_names = []

    rev = dict()
    for l in ld:
        # flatten hypernyms
        for h in ld[l]["POSHypernyms"]:
            if "POSHypernyms"+h not in rev:
                rev["POSHypernyms" + h] = set()
            rev["POSHypernyms" + h].add(l)
        # flatten words
        for w in ld[l]["words"]:
            if "word"+w not in rev:
                rev["word" + w] = set()
            rev["word"+w].add(l)
        # flatten categories
        for c in ld[l]["transCats"]:
            if "cat"+c not in rev:
                rev["cat"+c] = set()
            rev["cat"+c].add(l)
        # flatten infobox names
        for i in ld[l]["infoboxnames"]:
            if "infobox"+i not in rev:
                rev["infobox"+i] = set()
            rev["infobox"+i].add(l)

    #TODO flatten articles linking to

    #TODO flatten articles linking from

    #write to csv
    for l in ld:
        csv.write(l + SEPA + ld[l]["Seed"])
        for key in rev:
            if l in rev[key]:
                csv.write(SEPA + str(1))
            else:
                csv.write(SEPA + str(0))