from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from requests.exceptions import HTTPError
from mine.miner import get_summaries
from json.decoder import JSONDecodeError


def extract_summary_words(langdict):
    print("Exploring POS Hypernyms with Stanford")
    cl_sums = get_summaries().items()
    pool = Pool(processes=8)
    parse_results = pool.map(__map_parse, cl_sums)
    for cl,nn_set,nns_set,cop in parse_results:
        if nn_set is not None:
            for nn in nn_set:
                langdict[cl]["summary_nn_"+nn] = 1
            for nns in nns_set:
                langdict[cl]["summary_nns_"+nns] = 1
            if cop is not None:
                for c in cop:
                    if c is not None:
                        langdict[cl]['summary_cop_nn_'+c] = 1
    return langdict


def __map_parse(pair):
    cl = pair[0]
    summary = pair[1]
    if summary.startswith('.'):
        summary = summary[1:]
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    try:
        parse, = dep_parser.raw_parse(summary)
        nn_set = []
        nns_set = []
        for node in parse.nodes:
            if parse.nodes[node]["tag"] == 'NN':
                nn_set.append(parse.nodes[node]["word"])
            if parse.nodes[node]["tag"] == 'NNS':
                nns_set.append(parse.nodes[node]["word"])
        cop = __word_isa_pattern(parse.nodes.items()), __word_oneof_pattern(parse.nodes.items())
        return cl, nn_set, nns_set, cop
    except JSONDecodeError:
        print("Decode Error at :" + cl)
        return cl, None, None, None
    except StopIteration:
        print("Stopped at " + cl)
        return cl, None, None, None
    except HTTPError:
        print("HTTPError " + cl)
        return cl, None, None, None


def __word_isa_pattern(nodedict):
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


def __word_oneof_pattern(nodedict):
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
