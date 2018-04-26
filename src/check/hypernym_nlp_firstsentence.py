from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError

from data import DATAP
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
        if (summary == "No Summary") | (hyp is None):
            langdict[cl]["POSLanguage"] = 0
            langdict[cl]["COPLanguage"] = 0
            langdict[cl]["POSFormat"] = 0
            langdict[cl]["COPFormat"] = 0
        else:
            pos, cop = hyp
            langdict[cl]["POSHypernyms"] = pos
            langdict[cl]["COPHypernym"] = cop
            if any("language" in p for p in pos):
                langdict[cl]["POSLanguage"] = 1
            if any("format" in p for p in pos):
                langdict[cl]["POSLanguage"] = 1

            if cop is not None:
                if any("language" in c for c in cop):
                    langdict[cl]["COPLanguage"] = 1
                if any("format" in c for c in cop):
                    langdict[cl]["COPFormat"] = 1
            else:
                langdict[cl]["COPLanguage"] = 0
                langdict[cl]["COPFormat"] = 0
    return langdict


def solo():
    import json
    with open(DATAP + '/testdict.json', 'r', encoding="UTF8") as f:
        langdict = json.load(f)
        langdict = check_stanford(langdict)
        f.close()
    with open(DATAP + '/testdict.json', 'w', encoding="UTF8") as f:
        json.dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()


if __name__ == "__main__":
    print(("language" in "language"))
    solo()
