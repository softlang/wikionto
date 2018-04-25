from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from requests.exceptions import HTTPError

from data import DATAP
from json.decoder import JSONDecodeError


def check(pair):
    cl = pair[0]
    summary = pair[1]
    if summary.startswith('.'):
        summary = summary[1:]
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    while True:
        try:
            parses = dep_parser.raw_parse(summary)
            pos_list = []
            cop_list = []
            for parse in parses:
                pos_list.append(__pos_hypernyms(parse))
                cop_list.append(__cop_hypernym(parse))
            return cl, (pos_list, cop_list)
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
            (nn, nns), cop = hyp
            langdict[cl]["POSHypernyms"] = nn + nns
            langdict[cl]["COPHypernym"] = cop
            langdict[cl]["POSLanguage"] = int(bool(list(filter(lambda w: w.endsWith("language"), nn)))
                                              | bool(list(filter(lambda w: w.endsWith("languages"), nns))))
            langdict[cl]["COPLanguage"] = int(str(cop).endswith("language") | str(cop).endswith("languages"))
            langdict[cl]["POSFormat"] = int(bool(list(filter(lambda w: w.endsWith("format"), nn)))
                                            | bool(list(filter(lambda w: w.endsWith("formats"), nns))))
            langdict[cl]["COPFormat"] = int(str(cop).endswith("format") | str(cop).endswith("formats"))
    return langdict


def __pos_hypernyms(parse):
    for index, wdict in parse.nodes.items():
        if ((wdict['tag'] == 'VBZ') & (wdict['word'] == 'is')) | ((wdict['tag'] == 'VBD') & (wdict['word'] == 'was')):
            return __pos_is_an_one_nn(index, parse)
    return []


def __pos_is_an_one_nn(index, parse):
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if (wdict['tag'] == 'DT') & (wdict['word'] in 'an'):
            return __pos_nn(x, parse)
        if (wdict['tag'] == 'CD') & (wdict['word'] == 'one'):
            return __pos_of_nns(x, parse)
    return []


def __pos_nn(index, parse):
    nns = []
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if wdict['tag'] == 'NN':
            nns.append(wdict['word'])
    return nns


def __pos_of_nns(index, parse):
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if (wdict['tag'] == 'IN') & (wdict['word'] == 'of'):
            return __pos_nns(x, parse)
    return []


def __pos_nns(index, parse):
    nns = []
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if wdict['tag'] == 'NNS':
            nns.append(wdict['word'])
    return nns


def __cop_hypernym(parse):
    p = __cop_isa_pattern(parse.nodes.items())
    if p is not None:
        return p
    p = __cop_oneof_pattern(parse.nodes.items())
    if p is not None:
        return p
    return None


def __cop_isa_pattern(nodedict):
    nn_set = {key: value for (key, value) in nodedict if value['tag'] == 'NN'}
    for n, ndict in nn_set.items():
        if 'nsubj' not in ndict['deps']:
            continue
        subject = __get_node(nodedict, ndict['deps']['nsubj'][0])
        if not (subject['tag'] == 'NNP'):
            continue
        if 'cop' not in ndict['deps']:
            continue
        is_or_was = __get_node(nodedict, ndict['deps']['cop'][0])
        if not (((is_or_was['tag'] == 'VBZ') & (is_or_was['word'] == 'is')) |
                ((is_or_was['tag'] == 'VBD') & (is_or_was['word'] == 'was'))):
            continue
        return ndict['word']
    return None


def __cop_oneof_pattern(nodedict):
    nns_set = {key: value for (key, value) in nodedict if value['tag'] == 'NNS'}
    cd_set = {key: value for (key, value) in nodedict if value['tag'] == 'CD'}
    for n, ndict in nns_set.items():
        if 'case' not in ndict['deps']:
            continue
        nmod_check = False
        for cd, cddict in cd_set.items():
            if 'nmod' not in cddict['deps']:
                continue
            if cddict['deps']['nmod'][0] is not ndict['address']:
                continue
            if 'cop' not in cddict['deps']:
                continue
            vbnode = __get_node(nodedict, cddict['deps']['cop'][0])
            if not (((vbnode['tag'] == 'VBZ') & (vbnode['word'] == 'is')) | (
                    (vbnode['tag'] == 'VBD') & (vbnode['word'] == 'was'))):
                continue
            if 'nsubj' not in cddict['deps']:
                continue
            nsubj = __get_node(nodedict, cddict['deps']['nsubj'][0])
            if not nsubj['tag'] == 'NNP':
                continue
            nmod_check = True
            break
        if nmod_check:
            return ndict['word']
    return None


def __get_node(dict_items, index):
    for n, v in dict_items:
        if v["address"] == index:
            return v
    return None


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
