from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from requests.exceptions import HTTPError
from mine.dbpedia import articles_with_summaries, CLURI, CFFURI
from data import DATAP, CLDEPTH, CFFDEPTH
from json import dump, load
from json.decoder import JSONDecodeError
import operator
import pandas
import matplotlib.pyplot as plt

keywords_s = ['language', 'format', 'dsl', 'dialect']
keywords_p = ['languages', 'formats', 'dsls', 'dialects']


def map_parse(pair):
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
        return cl, nn_set, nns_set
    except JSONDecodeError:
        print("Decode Error at :" + cl)
        return cl, [], []
    except StopIteration:
        print("Stopped at " + cl)
        return cl, [], []
    except HTTPError:
        print("HTTPError " + cl)
        return cl, [], []


def explo_pos():
    print("Checking Hypernym with Stanford")
    clarticles = articles_with_summaries(CLURI, 0, CLDEPTH)
    cffarticles = articles_with_summaries(CFFURI, 0, CFFDEPTH)
    clarticles.update(cffarticles)
    cl_sums = clarticles.items()
    pool = Pool(processes=8)
    parsed_pairs = pool.map(map_parse, cl_sums)
    nndict = dict()
    nndict["NN"] = dict()
    nndict["NNS"] = dict()
    for cl, nn_list, nns_list in parsed_pairs:
        for nn in nn_list:
            try:
                nndict["NN"][nn] += 1
            except KeyError:
                nndict["NN"][nn] = 1
        for nns in nns_list:
            try:
                nndict["NNS"][nns] += 1
            except KeyError:
                nndict["NNS"][nns] = 1
    with open(DATAP + '/nndict.json', 'w', encoding="UTF8") as f:
        dump(obj=nndict, fp=f, indent=2)
        f.flush()
        f.close()




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

def get_top():
    f = open(DATAP+'/nndict.json')
    worddict = load(f)
    nndict = worddict["NN"]
    nnlist = list(nndict.items())
    nnlist.sort(key=operator.itemgetter(1))
    for w,n in nnlist:
        if n>100:
            print(w+', '+str(n))
    nnsdict = worddict["NNS"]
    nnslist = list(nnsdict.items())
    nnslist.sort(key=operator.itemgetter(1))
    for w, n in nnslist:
        if n>100:
            print(w+', '+str(n))

def plot_top():
    f = open(DATAP+'/top_nn.csv')
    headers = ['word','#articles']
    df = pandas.read_csv(f,names=headers)
    print(df)
    df.plot(x="word", y="#articles")
    # beautify the x-labels
    #plt.gcf().autofmt_xdate()
    plt.show()

if __name__ == "__main__":
    #explo_pos()
    #get_top()
    plot_top()