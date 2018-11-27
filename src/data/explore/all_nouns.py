from json import load
from data import DATAP
from nltk.stem import PorterStemmer
import collections
from multiprocessing import Pool
from util.custom_stanford_api import StanfordCoreNLP
from json import loads, dump
from json.decoder import JSONDecodeError

def get_nouns(cl_to_texts):
    cl = cl_to_texts[0]
    text = cl_to_texts[1]
    nlp = StanfordCoreNLP('http://localhost:9000')
    output = nlp.annotate(text, properties={
        "annotators": "tokenize,ssplit,pos",
        # "outputFormat": "json",
        # Only split the sentence at End Of Line. We assume that this method only takes in one single sentence.
        "ssplit.eolonly": "true",
        # Setting enforceRequirements to skip some annotators and make the process faster
        "enforceRequirements": "false"
    })
    # print(str(output['sentences'][0]['tokens'][0]['pos']))
    try:
        outdict = loads(output)
    except JSONDecodeError:
        print("------------ FAILED OUTPUT")
        print(output)
        return {}
    if len(outdict['sentences']) == 0:
        print("------------ FAILED TEXT")
        print(text)
        return {}
    nouns = list(
        set(PorterStemmer().stem(tdict['word']) for tdict in outdict['sentences'][0]['tokens'] if 'NN' in tdict['pos']))
    return {cl: {"nouns": nouns}}


if __name__ == '__main__':
    f = open(DATAP + '/articledict.json', 'r', encoding="UTF8")
    d = load(f)
    cl_to_texts = [(cl, d[cl]["Summary"]) for cl in d if "Summary" in d[cl]]
    pool = Pool(processes=4)
    cldict_nouns = pool.map(get_nouns, cl_to_texts)

    nouns = [nn for dictentry in cldict_nouns for cl in dictentry for nn in dictentry[cl]["nouns"]]
    for cldict_noun_entry in cldict_nouns:
        d.update(cldict_noun_entry)
    f = open(DATAP + '/olangdict.json', 'w', encoding="UTF8")
    dump(d, f)

    counter = collections.Counter(nouns)
    ndict = {n: count for n, count in counter.items() if count > 10000}
    f = open(DATAP + '/exploration/nouns.json', 'w', encoding="UTF8")
    dump(ndict, f, indent=2)
    print(counter.most_common(10))
