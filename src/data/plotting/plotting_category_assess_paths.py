import matplotlib.pyplot as plt
from json import load
from data import DATAP, ROOTS
from pandas import read_csv
from io import StringIO
from collections import deque
from check.transitive_childtest import get_sls_nosls


def plot_cats(fromn=0, ton=9):
    f = open(DATAP + '/ocatdict.json', 'r', encoding="UTF8")
    catdict = load(f)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    depthlist = []
    for c in ROOTS:
        depthlist.append(list(map(lambda d: len([cat for cat in catdict
                                                 if
                                                 ((c + "Depth" in catdict[cat]) and (catdict[cat][c + "Depth"] == d)
                                                  and check_cat2(cat, catdict, c))])
                                  , range(fromn, ton))))

    csvtext = ""
    for n in range(fromn, ton):
        csvtext += str(n)
        for i in range(len(ROOTS)):
            csvtext += ", " + str(depthlist[i][n - fromn])
        csvtext += "\n"

    dtypes = dict()
    dtypes["depth"] = int
    for c in ROOTS:
        dtypes[c] = int

    df = read_csv(StringIO(csvtext), delimiter=',', names=["depth"] + ROOTS,
                  dtype=dtypes)
    print(df)
    df.plot(x="depth", y=ROOTS, kind="bar", ax=ax, logy=True, width=0.8)

    ax.set_title('#Strong valid Categories at Depth')
    ax.legend("FL", "CFF", "IS")
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()


def check_cat2(cat, catdict, root):
    f = open(DATAP + '/olangdict.json', 'r', encoding="UTF8")
    ld = load(f)
    root = root.split("Category:")[1]
    if catdict[cat]["#NonSLs"] > catdict[cat]["#SLs"]:
        sls, no_sls = get_sls_nosls(cat, catdict, ld)
        sls_other = [l for l in sls if has_way_toroot_avoiding(l, root, cat, catdict)]
        if len(sls) is len(sls_other):
            return False
        else:
            return True
    else:
        return True


def has_way_toroot_avoiding(l, r, ac, catdict):
    if ac is r:
        return True
    queue = deque()
    queue.appendleft(r)
    done = set()
    ways = set()
    while len(queue) != 0:
        c = queue.pop()
        if c is ac or c in done:
            continue
        if "articles" in catdict[c] and l in catdict[c]["articles"]:
            ways.add(c)
        if "subcats" in catdict[c]:
            for sc in catdict[c]["subcats"]:
                queue.appendleft(sc)
        done.add(c)
    return len(ways) > 0


if __name__ == '__main__':
    plot_cats(fromn=1)
