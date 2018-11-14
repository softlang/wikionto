from data import DATAP
from json import load


def get_high_wordcounts():
    f = open(DATAP + '/articledict.json', 'r', encoding="UTF8")
    d = load(f)
    f.close()
    sl = list(
        cl for cl in d if (d[cl]["Seed"] == 1) and "words" in d[cl] and (len(d[cl]["words"]) == 0))
    for cl in sl:
        print(cl + ":" + str(d[cl]["words"]))


if __name__ == '__main__':
    get_high_wordcounts()
