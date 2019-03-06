from data import DATAP, start_time, stop_time
from json import dump, load
import csv


def id_dictionaries(csvname):
    with open(DATAP + '/dump/' + csvname + '.csv', 'r', encoding="UTF8") as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        dialect.quoting = csv.QUOTE_MINIMAL
        f.seek(0)
        r = csv.reader(f, dialect, delimiter=',', quotechar='|', lineterminator='\n')
        iddict = dict()
        iddictr = dict()
        for row in r:
            if len(row) != 2:
                print(len(row))
            assert len(row) == 2
            pid = int(row[0])
            ptitle = row[1].replace('’', "'")
            iddict[pid] = ptitle
            iddictr[ptitle] = pid
    with open(DATAP + '/dump/' + csvname + '.json', 'w', encoding="UTF8") as f:
        dump(iddict, f)
    with open(DATAP + '/dump/' + csvname + '_reverse.json', 'w', encoding="UTF8") as f:
        dump(iddictr, f)


def tocatjson(csvname):
    with open(DATAP + '/dump/tocatlinks_' + csvname + '.csv', 'r', encoding="UTF8") as f:
        f_id = open(DATAP + "/dump/category_ids.json", 'r', encoding="UTF8")
        id_to_title = load(f_id)
        title_to_id = {key: value for value, key in id_to_title.items()}
        dialect = csv.Sniffer().sniff(f.read(1024))
        dialect.quoting = csv.QUOTE_MINIMAL
        f.seek(0)
        r = csv.reader(f, dialect, delimiter=',', quotechar='|')
        catdict = dict()
        for row in r:
            try:
                to_title = row[0]
                from_id = row[1]
                from_title = row[2]
                if to_title not in title_to_id:
                    continue
                to_id = title_to_id[to_title]
                if to_id not in catdict:
                    catdict[to_id] = [from_id]
                catdict[to_id].append(from_id)
            except IndexError:
                print(row)
    with open(DATAP + '/dump/tocatlinks_' + csvname + '.json', 'w', encoding="UTF8") as f:
        dump(catdict, f)


def build_frontierdict(rootname):
    with open(DATAP + '/dump/category_ids.json', 'r', encoding="UTF8") as fid:
        id_to_title = load(fid)
        title_to_id = {ctitle: cid for cid, ctitle in id_to_title.items()}
    with open(DATAP + '/dump/tocatlinks_category.json', 'r', encoding="UTF8") as f:
        catdict = load(f)
    rootid = title_to_id[rootname]
    distances = dict()
    distances.update({1: catdict[rootid]})
    foundcats = set(c for c in catdict[rootid])

    for x in range(1, 20):
        nextcats = [cat for supercat in distances[x] if supercat in catdict for cat in catdict[supercat] if
                    cat not in foundcats]
        distances.update({(x + 1): nextcats})
        foundcats = foundcats | set(nextcats)
    with open(DATAP + '/dump/frontier_' + rootname + '.json', 'w', encoding="UTF8") as f:
        dump(distances, f)


def build_scope(roots):
    with open(DATAP + '/dump/category_ids_reverse.json', 'r', encoding="UTF8") as fid:
        ciddictr = load(fid)
        root_title_to_id = {rtitle: ciddictr[rtitle] for rtitle in roots}
        del ciddictr
    print("Loaded ids")
    fronts = dict()
    for r in roots:
        with open(DATAP + '/dump/frontier_' + r + '.json', 'r', encoding="UTF8") as f:
            frontdict = load(f)
            fronts[r] = frontdict
    print("Loaded fronts")
    # del id_to_title
    with open(DATAP + '/dump/tocatlinks_article.json', 'r', encoding="UTF8") as f:
        cattoart = load(f)
    print("loaded catlinks")
    scope = dict()
    for r_title, front in fronts.items():
        print("Processing " + r_title)
        d = 0
        rid = root_title_to_id[r_title]
        if rid in cattoart:
            for a in cattoart[rid]:
                if a not in scope:
                    scope[a] = dict()
                if r_title + 'DEPTH' not in scope[a]:
                    scope[a][r_title + 'DEPTH'] = d
        for d, cats in front.items():
            for c in cats:
                if c in cattoart:
                    for a in cattoart[c]:
                        if a not in scope:
                            scope[a] = dict()
                        if r_title + 'DEPTH' not in scope[a]:
                            scope[a][r_title + 'DEPTH'] = d
    print("Dumping")
    with open(DATAP + '/dump/articles_inscope_' + ('_'.join(roots)) + '.json', 'w', encoding="UTF8") as f:
        dump(scope, f)
        print("In scope:" + str(len(scope)))
    return scope


def reverse_cattocatlinks():
    with open(DATAP + '/dump/tocatlinks_category.json', 'r', encoding="UTF8") as f:
        cattosubcat = load(f)
    subcattocat = dict()
    for supercat, cats in cattosubcat.items():
        for cat in cats:
            if cat not in subcattocat:
                subcattocat[cat] = [supercat]
            else:
                subcattocat[cat].append(supercat)
    with open(DATAP + '/dump/tocatlinks_category_reverse.json', 'w', encoding="UTF8") as f:
        dump(subcattocat, f)


def count_articles_in_scope():
    with open(DATAP + '/dump/articles_inscope.json', 'r', encoding="UTF8") as f:
        scope = load(f)
        print(len(scope))


if __name__ == '__main__':
    t = start_time()
    # id_dictionaries('article_ids')
    # id_dictionaries('category_ids')
    # tocatjson('article')
    # tocatjson('category')
    # roots = ["Formal_languages", "Computer_file_formats", "Installation_software"]
    roots = ["Animals"]
    # for r in roots:
    #    build_frontierdict(r)
    build_frontierdict("Animals")
    scope = build_scope(roots)
    stop_time(t)
