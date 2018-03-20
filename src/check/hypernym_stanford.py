from nltk.parse.corenlp import CoreNLPDependencyParser
from mine.dbpedia import articles_with_summaries,CFFURI,CLURI
from data import DATAP

keywords = ['language','format','dsl','dialect']
def check_stanford(langdict):
    print("Checking Hypernym with Stanford")
    clarticles = articles_with_summaries(CLURI,0,6)
    cffarticles = articles_with_summaries(CFFURI, 0, 6)
    clarticles.update(cffarticles)
    zipped_art_sum = list(zip(*clarticles.items()))
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    dep_parsed = list(map(lambda s: dep_parser.raw_parse(s),zipped_art_sum[1]))
    cls_dep_parsed = dict(zip(zipped_art_sum[0],dep_parsed))
    
    for cl in langdict:
        if cl not in cls_dep_parsed:
            langdict[cl]["StanfordPOSHypernym"] = 0
            langdict[cl]["StanfordCOPHypernym"] = 0
            langdict[cl]["Summary"]="No Summary!"
        else: 
            langdict[cl]["Summary"] = clarticles[cl]
            parse, = cls_dep_parsed[cl]
            langdict[cl]["StanfordPOSHypernym"] = pos_language(parse)
            langdict[cl]["StanfordCOPHypernym"] = cop_language(parse)
    return langdict

def pos_language(parse):
    vbzs = list([s for (s,_,o) in parse.triples() if (s==('is','VBZ')) | (o==('is','VBZ'))])
    nns = list([s for (s,_,o) in parse.triples() if ((s[0].lower() in keywords) & (s[1]=='NN')) | ((o[0].lower() in keywords) & (o[1]=='NN'))])
    return int(bool(vbzs) & bool(nns))

def cop_language(parse):
    for subj, dep, obj in parse.triples():
        if (subj[1]=='NN')&(subj[0] in ['language','format','dsl','dialect']) & (dep=='cop') & (obj==('is','VBZ')):
            return 1
    return 0

if __name__ == '__main__':
    import json
    with open(DATAP+'/langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        langdict = check_stanford(langdict)
        f.close()
    with open(DATAP+'/langdict.json', 'w',encoding="UTF8") as f:
        json.dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()