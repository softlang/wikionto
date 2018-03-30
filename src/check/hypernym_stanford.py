from nltk.parse.corenlp import CoreNLPDependencyParser
from mine.dbpedia import articles_with_summaries, CFFURI, CLURI
from data import DATAP
import re

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
    vbzs = list([s for (s, _, o) in parse.triples() if
                 (s == ('is', 'VBZ')) | (s == ('was', 'VBZ')) | (o == ('is', 'VBZ')) | (o == ('was', 'VBZ'))])
    nns = list([s for (s, _, o) in parse.triples() if
                ((s[0].lower() in keywords) & (s[1] == 'NN')) | ((o[0].lower() in keywords) & (o[1] == 'NN'))])
    return int(bool(vbzs) & bool(nns))


def cop_language(parse):
    for subj, dep, obj in parse.triples():
        if (subj[1] == 'NN') & (subj[0] in ['language', 'format', 'dsl', 'dialect']) & (dep == 'cop') & (
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


if __name__ == "__main__":
    solo()
