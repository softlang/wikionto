def pos_hypernyms(parse):
    the_node = parse.nodes[1]
    if (the_node['tag'] == 'DT') and (the_node['word'] == 'The'):
        x = 2
        last = None
        while parse.nodes[x]['tag'] == 'JJ':
            x+=1
        if parse.nodes[x]['tag'] == 'NNP':
            x+=1
        nns = []
        while parse.nodes[x]['tag'] == 'NN':
            nns.append(parse.nodes[x]['word'])
            last = parse.nodes[x]['word']
            x += 1
        if last is not None and parse.nodes[x]['tag'] is not 'POS':
            return nns, 'The'

    for index, wdict in parse.nodes.items():
        if ((wdict['tag'] == 'VBZ') & (wdict['word'] in ['is', 'refers', 'denotes', 'specifies'])) | (
                (wdict['tag'] == 'VBD') & (wdict['word'] == 'was')):
            return pos_is_an_one_nn(index, 'is', parse)
    return [], ''


def pos_is_an_one_nn(index, s, parse):
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if (wdict['tag'] == 'DT') & any(wdict['word'] == w for w in ['a', 'an', 'the']):
            return pos_x(x, s + 'a', parse)
        if (wdict['tag'] == 'CD') & (wdict['word'] in ['one']):
            return pos_of_nns(x, s+'one', parse)
    return [], ''


def pos_x(index, s, parse):
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if (wdict['tag'] == 'NN') & any(wdict['word'] in w for w in ['family', 'member']):
            nns, snew = pos_of_nns(x, s+'family', parse)
            if not nns:
                continue
            else:
                return nns,snew
        if (wdict['tag'] == 'NN') & (wdict['word'] == 'name'):
            nns, snew = pos_of_nn(x, s + 'name', parse)
            if not nns:
                continue
            else:
                return nns, snew
    return pos_nn(index, s, parse)


def pos_of_nn(index, s, parse):
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if (wdict['tag'] == 'IN') & (wdict['word'] in ['of', 'for']):
            return pos_nn(x, s+'of', parse)
    return [], ''


def pos_of_nns(index, s, parse):
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if (wdict['tag'] == 'IN') & (wdict['word'] == 'of'):
            return pos_nns(x, s+'of', parse)
    return [], ''


def pos_nn(index, s, parse):
    nns = []
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if wdict['tag'] == 'NN' or wdict['tag'] == 'NNP':
            nns.append(wdict['word'])
    return nns, s


def pos_nns(index, s, parse):
    nns = []
    for x in range(index, len(parse.nodes.items()), 1):
        wdict = parse.nodes[x]
        if wdict['tag'] == 'NNS':
            nns.append(wdict['word'])
    return nns, s


def cop_hypernym(parse):
    p = cop_isa_pattern(parse.nodes.items())
    if p is not None:
        return p
    p = cop_oneof_pattern(parse.nodes.items())
    if p is not None:
        return p
    return []


def cop_isa_pattern(nodedict):
    nn_set = {key: value for (key, value) in nodedict if value['tag'] == 'NN'}
    for n, ndict in nn_set.items():
        if ('nsubj' not in ndict['deps']) & ('csubj' not in ndict['deps']):
            continue
        if 'cop' not in ndict['deps']:
            continue
        is_or_was = __get_node(nodedict, ndict['deps']['cop'][0])
        if not (((is_or_was['tag'] == 'VBZ') & (is_or_was['word'] == 'is')) |
                ((is_or_was['tag'] == 'VBD') & (is_or_was['word'] == 'was'))):
            continue
        cops = [ndict['word']]
        if 'conj' in ndict['deps']:
            for x in range(len(ndict['deps']['conj'])):
                conj_node = __get_node(nodedict, ndict['deps']['conj'][x])
                cops.append(conj_node['word'])
        return cops
    return []


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
            return [ndict['word']]
    return []


def __get_node(dict_items, index):
    for n, v in dict_items:
        if v["address"] == index:
            return v
    return None
