from json import load, dump
from data import DATAP


def create_testdict():
    with open(DATAP + '/articledict.json', 'r', encoding="UTF8") as f:
        langdict = load(f)
        f.close()

    testset = []
    testseedset = []
    testnegseedset = []
    testdict = dict()
    for cl, feat in langdict.items():
        if feat["Seed"] == 1:
            testseedset.append(cl)
            testdict[cl] = feat
        elif feat["negativeSeed"] == 1 and len(testset) < 10:
            testset.append(cl)
            testdict[cl] = feat
        elif feat["Seed"] == 0 and feat["negativeSeed"] == 0 and len(testnegseedset) < 10:
            testnegseedset.append(cl)
            testdict[cl] = feat

    with open(DATAP + '/testdict.json', 'w', encoding="UTF8") as f:
        dump(obj=testdict, fp=f, indent=2)
        f.flush()
        f.close()


if __name__ == "__main__":
    create_testdict()
