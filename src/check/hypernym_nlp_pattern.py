def pos_hypernyms(parse):
    for index, wdict in parse.nodes.items():
        if ((wdict['tag'] == 'VBZ') & (wdict['word'] == 'is')) | ((wdict['tag'] == 'VBD') & (wdict['word'] == 'was')):
            return pos_is_an_one_nn(index, parse)
    return []


def pos_is_an_one_nn(index, parse):
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if (wdict['tag'] == 'DT') & (wdict['word'] in 'an'):
            return pos_family(x, parse)
        if (wdict['tag'] == 'CD') & (wdict['word'] in ['one', 'member']):
            return pos_of_nns(x, parse)
    return []


def pos_family(index,parse):
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if (wdict['tag'] == 'NN') & (wdict['word'] in 'family'):
            return pos_of_nns(x, parse)
    return pos_nn(index,parse)


def pos_nn(index, parse):
    nns = []
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if wdict['tag'] == 'NN':
            nns.append(wdict['word'])
    return nns


def pos_of_nns(index, parse):
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if (wdict['tag'] == 'IN') & (wdict['word'] == 'of'):
            return pos_nns(x, parse)
    return []


def pos_nns(index, parse):
    nns = []
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if wdict['tag'] == 'NNS':
            nns.append(wdict['word'])
    return nns


def cop_hypernym(parse):
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