from json import load
from data import DATAP


def pos_vs_neginfobox():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    ld = load(f)
    rs = [cl for cl in ld if ld[cl]["POS"] == 1 and ld[cl]["negativeSeed"] == 1]
    ns = [cl for cl in ld if ld[cl]["negativeSeed"] == 1]
    for l in rs:
        print(l + ": " + ld[l]["Summary"])
    print(str(len(rs)) + "/" + str(len(ns)) + "=" + str(len(rs) / len(ns)))


def pos_vs_posinfobox():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    ld = load(f)
    rs1 = [cl for cl in ld if "Summary" in ld[cl] and ld[cl]["POS"] == 0 and ld[cl]["ValidInfobox"] == 1]
    ns = [cl for cl in ld if "Summary" in ld[cl] and ld[cl]["ValidInfobox"] == 1]
    rs2 = [cl for cl in ld if "Summary" in ld[cl] and ld[cl]["POS"] == 0 and ld[cl]["ValidInfobox"] == 1
          and "infobox_software" in ld[cl]["DbpediaInfoboxTemplate"]]
    for l in rs2:
        print(l + ": " + ld[l]["Summary"])
    print(str(len(rs2)) + "/" + str(len(rs1)) + "/" + str(len(ns)) + "=" + str(len(rs1+rs2) / len(ns)))


if __name__ == '__main__':
    pos_vs_neginfobox()
