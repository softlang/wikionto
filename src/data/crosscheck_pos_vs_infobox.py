from json import load
from data import DATAP


def pos_vs_infobox():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    ld = load(f)
    rs = [cl for cl in ld if ld[cl]["POS"] == 1 and ld[cl]]
