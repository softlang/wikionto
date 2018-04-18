from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from requests.exceptions import HTTPError

from data import DATAP
from json.decoder import JSONDecodeError

keywords_s = ['language', 'format']
keywords_p = ['languages', 'formats']


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
            cop = cop_hypernyms(parse)
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
        if summary == "No Summary":
            langdict[cl]["StanfordPOSHypernym"] = 0
            langdict[cl]["StanfordCOPHypernym"] = 0
        else:
            tests = parsed_pairs[cl]
            if tests is not None:
                langdict[cl]["StanfordPOSHypernym"] = tests[0]
                langdict[cl]["StanfordCOPHypernym"] = tests[1]
            else:
                langdict[cl]["StanfordPOSHypernym"] = 0
                langdict[cl]["StanfordCOPHypernym"] = 0
    return langdict


def pos_hypernyms(parse):
    for index, wdict in parse.nodes.items():
        if ((wdict['tag'] == 'VBZ') & (wdict['word'] == 'is')) | ((wdict['tag'] == 'VBD') & (wdict['word'] == 'was')):
            nnlist = pos_a_NN(index + 1, parse)
            nnslist = pos_one_of_NNS(index + 1, parse)
    return nnlist, nnslist


def pos_a_nn(index, parse):
    nnlist = []
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if wdict['tag'] == 'NN':
            nnlist.append(wdict['word'])
    return nnlist


def pos_one_of_nns(index, parse):
    nnlist = []
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if wdict['tag'] == 'NNS':
            nnlist.append(wdict['word'])
    return nnlist


def cop_hypernyms(parse):
    p = cop_isa_pattern(parse.nodes.items())
    if p is not None:
        return p
    p = cop_oneof_pattern(parse.nodes.items())
    if p is not None:
        return p
    return None


def cop_isa_pattern(nodedict):
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


def cop_oneof_pattern(nodedict):
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
