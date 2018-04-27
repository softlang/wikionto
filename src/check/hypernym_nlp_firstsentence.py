from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError

from data import DATAP, KEYWORDS
from check.hypernym_nlp_pattern import cop_hypernym, pos_hypernyms

def check(pair):
    cl = pair[0]
    summary = pair[1]
    if summary.startswith('.'):
        summary = summary[1:]
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    while True:
        try:
            parse, = dep_parser.raw_parse(summary)
            pos = pos_hypernyms(parse)
            cop = cop_hypernym(parse)
            return cl, (pos, cop)
        except JSONDecodeError:
            print("Decode Error at :" + cl)
            return cl, None
        except StopIteration:
            print("Stopped at " + cl)
            return cl, None
        except HTTPError:
            print("HTTPError " + cl)
            return cl, None


def check_stanford(langdict):
    print("Checking Hypernym with Stanford")

    cl_sums = []
    for cl in langdict:
        cl_sums.append((cl, langdict[cl]["Summary"]))
    pool = Pool(processes=8)
    parsed_pairs = pool.map(check, cl_sums)
    parsed_pairs = dict(parsed_pairs)
    for cl in langdict:
        summary = langdict[cl]["Summary"]
        hyp = parsed_pairs[cl]
        if not((summary == "No Summary") | (hyp is None)):
            pos, cop = hyp
            langdict[cl]["POSHypernyms"] = pos
            langdict[cl]["COPHypernym"] = cop
            if any(kw in p for p in pos for kw in KEYWORDS):
                langdict[cl]["POS"] = 1
            if ("template" in pos) & ("engine" in pos):
                langdict[cl]["POSX"] = 1
            if ("Template" in pos) & ("Engine" in pos):
                langdict[cl]["POSX"] = 1
            if("templating" in pos) & ("system" in pos):
                langdict[cl]["POSX"] = 1
            if ("theorem" in pos) & ("prover" in pos):
                langdict[cl]["POSX"] = 1
            if ("parser" in pos) & ("generator" in pos):
                langdict[cl]["POSX"] = 1
            if ("build" in pos) & ("tool" in pos):
                langdict[cl]["POSX"] = 1
            if cop is not None:
                if any(kw in c for c in cop for kw in KEYWORDS):
                    langdict[cl]["COP"] = 1
    return langdict


def solo():
    import json
    with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
        langdict = json.load(f)
        langdict = check_stanford(langdict)
        f.close()
    with open(DATAP + '/langdict.json', 'w', encoding="UTF8") as f:
        json.dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()


if __name__ == "__main__":
    solo()
