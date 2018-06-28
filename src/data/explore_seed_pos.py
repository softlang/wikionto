from data import DATAP
from json import load


def get_refers_to():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    d = load(f)
    f.close()
    sl = list(
        cl for cl in d if (d[cl]["Seed"] == 0) and "POS_isoneof" in d[cl])
    print(sl)


if __name__ == '__main__':
    get_refers_to()
