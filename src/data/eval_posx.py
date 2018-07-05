from data import DATAP, XKEYWORDS
from json import load

f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
ld = load(f)

for k1, k2 in XKEYWORDS:
    ls = [l for l in ld if "POSX_"+k1+k2 in ld[l] and ld[l]["POSX_"+k1+k2] == 1]
    print(k1+k2+":"+str(len(ls)))
