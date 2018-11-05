from data import DATAP
from json import load

f = open(DATAP + "/langdict.json", "r")
langdict = load(f)
inspect = [(l, langdict[l]["Category:Formal_languagesDepth"]) for l in langdict if 'Category:Formal_languagesDepth' in langdict[l] and
           langdict[l]['NotExclusiveNoiseCategory'] and not (langdict[l]['POS'])]
for i in inspect:
    print(i)