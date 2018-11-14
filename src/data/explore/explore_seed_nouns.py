from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError
from json import load, dump
from data import DATAP


def get_single(summary):
    if summary.startswith('.'):
        summary = summary[1:]
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    try:
        parse, = dep_parser.raw_parse(summary)
        nouns = set()
        for x in range(1, len(parse.nodes.items())):
            wdict = parse.nodes[x]
            if "NN" in wdict["tag"]:
                nouns.add(wdict["word"])
        return nouns
    except JSONDecodeError:
        print("Decode Error at " + summary)
        return None
    except StopIteration:
        print("Stopped at " + summary)
        return None
    except HTTPError:
        print("HTTPError " + summary)
        return None


def explore():
    f = open(DATAP + '/articledict.json', 'r', encoding="utf8")
    d = load(f)
    f.close()
    cl_sums = list(d[cl]["Summary"] for cl in d if ("Summary" in d[cl]) and (d[cl]["Seed"] == 1))
    pool = Pool(processes=10)
    nnlists = pool.map(get_single, cl_sums)
    nouns_f = dict()
    for nnlist in nnlists:
        for nn in nnlist:
            if nn in nouns_f:
                nouns_f[nn] += 1
            else:
                nouns_f[nn] = 1
    f = open(DATAP + '/explore_seed_nouns.json', 'w', encoding='utf8')
    dump(nouns_f, f, indent=2)
    f.flush()
    f.close()


def get_top10():
    f = open(DATAP + '/explore_seed_nouns.json', 'r', encoding="utf8")
    nouns_f = load(f)
    f.close()
    import operator
    top10 = list((k, nouns_f[k]) for k in nouns_f)
    top10.sort(key=operator.itemgetter(1))
    for k, v in top10:
        print((k, v))


if __name__ == "__main__":
    get_top10()
