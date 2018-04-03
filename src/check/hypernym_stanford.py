from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from data import DATAP
from json.decoder import JSONDecodeError

keywords = ['language', 'format', 'dsl', 'dialect']


def map_parse(pair):
    cl = pair[0]
    summary = pair[1]
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    try:
        parse, = dep_parser.raw_parse(summary)
        return (cl, parse)
    except JSONDecodeError:
        print("Decode Error at :" + summary)
        return (cl, None)
    except StopIteration:
        print("Stopped at " + summary)
        return (cl, None)


def check_stanford(langdict):
    print("Checking Hypernym with Stanford")

    cl_sums = []
    for cl in langdict:
        cl_sums.append((cl, langdict[cl]["Summary"]))
    pool = Pool(processes=8)
    parsed_pairs = pool.map(map_parse, cl_sums)
    parsed_pairs = dict(parsed_pairs)
    for cl in langdict:
        summary = langdict[cl]["Summary"].decode('UTF-8')
        if summary == "No Summary":
            langdict[cl]["StanfordPOSHypernym"] = 0
            langdict[cl]["StanfordCOPHypernym"] = 0
        else:
            parse = parsed_pairs[cl]
            if parse is not None:
                langdict[cl]["StanfordPOSHypernym"] = pos_language(parse)
                langdict[cl]["StanfordCOPHypernym"] = cop_language(parse)
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
              (any([k for k in keywords if s[0].lower().endswith(k)]) & (s[1] == 'NN'))
              | (any([k for k in keywords if o[0].lower().endswith(k)]) & (o[1] == 'NN'))]
    one = [s for (s, _, o) in parse.triples() if
           (s == ('one', 'CD')) | (o == ('one', 'CD'))]
    of = [s for (s, _, o) in parse.triples() if
          (s == ('of', 'IN')) | (o == ('of', 'IN'))]
    key_nns = [s for (s, _, o) in parse.triples() if
               (any([k for k in keywords if s[0].lower().endswith(k + 's')]) & (s[1] == 'NNS'))
               | (any([k for k in keywords if o[0].lower().endswith(k + 's')]) & (o[1] == 'NNS'))]
    p1 = (bool(is_VBZ) | bool(was_VBD)) & bool(key_nn)
    p2 = (bool(is_VBZ) | bool(was_VBD)) & bool(one) & bool(of) & bool(key_nns)
    return int(p1 | p2)


def cop_language(parse):
    for subj, dep, obj in parse.triples():
        if (subj[1] == 'NN') & (subj[0] in keywords) & (dep == 'cop') & (
                obj == ('is', 'VBZ')):
            return 1
    return 0


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


if __name__ == "__main__":
    solo()
    #test()
