from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from requests.exceptions import HTTPError

from data import DATAP
from json.decoder import JSONDecodeError

keywords_s = ['language', 'format', 'dsl', 'dialect']
keywords_p = ['languages', 'formats', 'dsls', 'dialects']


def map_parse(pair):
    cl = pair[0]
    summary = pair[1]
    if summary.startswith('.'):
        summary = summary[1:]
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    while True:
        try:
            parse, = dep_parser.raw_parse(summary)
            pos = pos_language(parse)
            cop = cop_language(parse)
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
    parsed_pairs = pool.map(map_parse, cl_sums)
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


def pos_language(parse):
    is_VBZ = [s for (s, _, o) in parse.triples() if
              (s == ('is', 'VBZ')) | (o == ('is', 'VBZ'))]
    was_VBD = [s for (s, _, o) in parse.triples() if
               (s == ('was', 'VBD')) | (o == ('was', 'VBD'))]
    key_nn = [s for (s, _, o) in parse.triples() if
              (any([k for k in keywords_s if s[0].lower().endswith(k)]) & (s[1] == 'NN'))
              | (any([k for k in keywords_s if o[0].lower().endswith(k)]) & (o[1] == 'NN'))]
    one = [s for (s, _, o) in parse.triples() if
           (s == ('one', 'CD')) | (o == ('one', 'CD'))]
    of = [s for (s, _, o) in parse.triples() if
          (s == ('of', 'IN')) | (o == ('of', 'IN'))]
    key_nns = [s for (s, _, o) in parse.triples() if
               (any([k for k in keywords_p if s[0].lower().endswith(k)]) & (s[1] == 'NNS'))
               | (any([k for k in keywords_p if o[0].lower().endswith(k)]) & (o[1] == 'NNS'))]
    p1 = (bool(is_VBZ) | bool(was_VBD)) & bool(key_nn)
    p2 = (bool(is_VBZ) | bool(was_VBD)) & bool(one) & bool(of) & bool(key_nns)
    return int(p1 | p2)


def cop_language(parse):
    is_key = False
    was_key = False
    was_one = False
    is_one = False
    one_keys = False
    of_keys = False
    for s, d, o in parse.triples():
        is_key = is_key or ((s[1] == 'NN') & (s[0] in keywords_s) & (d == 'cop') & (o == ('is', 'VBZ')))
        was_key = was_key or (s[1] == 'NN') & (s[0] in keywords_s) & (d == 'cop') & (o == ('was', 'VBD'))
        is_one = is_one or ((s == ('is', 'VBZ')) & (d == 'cop') & (o == ('one', 'CD')))
        was_one = was_one or ((s == ('was', 'VBZ')) & (d == 'cop') & (o == ('one', 'CD')))
        one_keys = one_keys or ((s == ('one', 'CD')) & (d == 'nmod')
                                & (any([k for k in keywords_p if o[0].lower().endswith(k)]) & (o[1] == 'NNS')))
        of_keys = of_keys or ((any([k for k in keywords_p if s[0].lower().endswith(k)]) & (s[1] == 'NNS'))
                              & (d == 'case') & (o == ('of', 'CD')))
    one_of_keys = (is_one | was_one) & one_keys & of_keys
    return int(is_key or was_key or one_of_keys)


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


def test():
    summary = "S.O.S. is a Swedish English language hit for Swedish singer Ola Svensson written by Tony Nilsson, taken from his third album Good Enough, also appearing in Good Enough - The Feelgood Edition. The hit credited to just Ola was a #1 hit on the Swedish Singles Chart on the chart dated 22 November 2007, staying a total of 16 weeks in the charts including 6 weeks in the Top 5. Selling over 10,000 copies, the single was certified Gold by the IFPI."
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    parse, = dep_parser.raw_parse(summary)
    print(pos_language(parse))
    print(cop_language(parse))


if __name__ == "__main__":
    #solo()
    test()
