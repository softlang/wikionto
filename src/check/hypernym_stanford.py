from nltk.parse.corenlp import CoreNLPDependencyParser
from data import DATAP

keywords = ['language', 'format', 'dsl', 'dialect']


def check_stanford(langdict):
    print("Checking Hypernym with Stanford")
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    for cl in langdict:
        summary = langdict[cl]["Summary"]
        if summary == "No Summary":
            langdict[cl]["StanfordPOSHypernym"] = 0
            langdict[cl]["StanfordCOPHypernym"] = 0
        else:
            parse, = dep_parser.raw_parse(norm(summary))
            langdict[cl]["StanfordPOSHypernym"] = pos_language(parse)
            langdict[cl]["StanfordCOPHypernym"] = cop_language(parse)
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
                (any([k for k in keywords if s[0].lower().endswith(k+'s')]) & (s[1] == 'NNS')) 
                | (any([k for k in keywords if o[0].lower().endswith(k+'s')]) & (o[1] == 'NNS'))]
    p1 = (bool(is_VBZ) | bool(was_VBD)) & bool(key_nn)
    p2 = (bool(is_VBZ) | bool(was_VBD)) & bool(one) & bool(of) & bool(key_nns)
    return int(p1 | p2)


def cop_language(parse):
    for subj, dep, obj in parse.triples():
        if (subj[1] == 'NN') & (subj[0] in keywords) & (dep == 'cop') & (
                obj == ('is', 'VBZ')):
            return 1
    return 0


def norm(summary):
    return summary.replace(".", "")+'.'


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
    summary = "Short Code was one of the first higher-level languages ever developed for an electronic computer."
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    parse, = dep_parser.raw_parse(norm(summary))
    print(pos_language(parse))

if __name__ == "__main__":
    #solo()
    test()
