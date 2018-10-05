from data import DATAP
from json import dump, load
import csv


def tocatjson(csvname):
    with open(DATAP + '/dump/tocatlinks_'+csvname+'.csv', 'r', encoding="UTF8") as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        dialect.quoting = csv.QUOTE_MINIMAL
        f.seek(0)
        r = csv.reader(f, dialect, delimiter=',', quotechar='"')
        catdict = dict()
        for row in r:
            try:
                value = row[0]
                key = row[1]
                if key not in catdict:
                    catdict[key] = []
                catdict[key].append(value)
            except IndexError:
                print(row)
    with open(DATAP + '/dump/tocatlinks_'+csvname+'.json', 'w', encoding="UTF8") as f:
        dump(catdict, f)


def build_frontierdict(rootname):
    with open(DATAP + '/dump/tocatlinks_subcats.json', 'r', encoding="UTF8") as f:
        catdict = load(f)

        distances = dict()
        distances.update({1: catdict[rootname]})
        foundcats = set(c for c in catdict[rootname])

        for x in range(1,20):
            nextcats = [cat for supercat in distances[x] if supercat in catdict for cat in catdict[supercat] if cat not in foundcats]
            distances.update({(x+1): nextcats})
            foundcats = foundcats | set(nextcats)
    with open(DATAP + '/dump/frontier_'+rootname+'.json', 'w', encoding="UTF8") as f:
        dump(distances, f)


def build_scope(roots):
    fronts = {r: load(open(DATAP + '/dump/frontier_'+r+'.json', 'r', encoding="UTF8")) for r in roots}
    with open(DATAP + '/dump/tocatlinks_articles.json', 'r', encoding="UTF8") as f:
        cattoart = load(f)
    scope = dict()
    for r, front in fronts.items():
        d = 0
        for a in cattoart[r]:
            if a not in scope:
                scope[a] = dict()
            if r+'DEPTH' not in scope[a]:
                scope[a][r+'DEPTH'] = d
        for d, cats in front.items():
            for c in cats:
                if c in cattoart:
                    for a in cattoart[c]:
                        if a not in scope:
                            scope[a] = dict()
                        if r+'DEPTH' not in scope[a]:
                            scope[a][r+'DEPTH'] = d

    with open(DATAP + '/dump/articles.json', 'w', encoding="UTF8") as f:
        dump(scope,f)


if __name__ == '__main__':
    roots = ["Formal_languages", "Computer_file_formats", "Installation_software"]
    build_scope(roots)

    #cdict = load(open(DATAP + '/dump/frontier_Contents.json', 'r', encoding="UTF8"))
    #print([d for d, cats in cdict.items() if "Formal_languages" in cats])
    #print(len([cat for d,cats in cdict.items() for cat in cats if d=='6']))
