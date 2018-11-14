from data import DATAP
from json import load


def get_list_linked_seed():
    f = open(DATAP + '/articledict.json', 'r', encoding="UTF8")
    d = load(f)
    f.close()
    sl = list(
        cl for cl in d if (d[cl]["Seed"] == 1) and (d[cl]["In_Wikipedia_List"] == 1))
    sl0 = list(cl for cl in d if (d[cl]["Seed"] == 1))
    print(len(sl))
    print(len(sl0))


if __name__ == '__main__':
    get_list_linked_seed()
