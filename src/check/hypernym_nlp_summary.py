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
            parsed = dep_parser.parse_text(summary)
            pos_list = []
            cop_list = []
            for p in parsed:
                pos_list += pos_hypernyms(p)
                cop_list += cop_hypernym(p)
            return cl, (pos_list, cop_list)
        except JSONDecodeError:
            print("Decode Error at :" + cl)
            return cl, None
        except StopIteration:
            print("Stopped at " + cl)
            return cl, (pos_list, cop_list)
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
            langdict[cl]["SumPOSLanguage"] = 0
            langdict[cl]["SumCOPLanguage"] = 0
            langdict[cl]["SumPOSFormat"] = 0
            langdict[cl]["SumCOPFormat"] = 0
        else:
            pos, cop = hyp
            langdict[cl]["SumPOSHypernyms"] = pos
            langdict[cl]["SumCOPHypernym"] = cop
            langdict[cl]["SumPOSLanguage"] = int(bool(list(filter(lambda w: w.endswith("language"), pos)))
                                              | bool(list(filter(lambda w: w.endswith("languages"), pos))))
            langdict[cl]["SumCOPLanguage"] = int(str(cop).endswith("language") | str(cop).endswith("languages"))
            langdict[cl]["SumPOSFormat"] = int(bool(list(filter(lambda w: w.endswith("format"), pos)))
                                            | bool(list(filter(lambda w: w.endswith("formats"), pos))))
            langdict[cl]["SumCOPFormat"] = int(str(cop).endswith("format") | str(cop).endswith("formats"))
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
    solo()
