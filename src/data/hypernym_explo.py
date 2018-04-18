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


def map_pos(pair):
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


def map_cop(pair):
    cl = pair[0]
    summary = pair[1]
    if summary.startswith('.'):
        summary = summary[1:]
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    try:
        parse, = dep_parser.raw_parse(summary)
        return cl, word_isa_pattern(parse.nodes.items()), word_oneof_pattern(parse.nodes.items())
    except JSONDecodeError:
        print("Decode Error at :" + cl)
        return cl, None, None
    except StopIteration:
        print("Stopped at " + cl)
        return cl, None, None
    except HTTPError:
        print("HTTPError " + cl)
        return cl, None, None





def get_summaries():
    clarticles = articles_with_summaries(CLURI, 0, CLDEPTH)
    cffarticles = articles_with_summaries(CFFURI, 0, CFFDEPTH)
    clarticles.update(cffarticles)
    return clarticles.items()


def explo_pos(cl_sums):
    print("Exploring POS Hypernyms with Stanford")
    pool = Pool(processes=8)
    parsed_pairs = pool.map(map_pos, cl_sums)
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
    with open(DATAP + '/hyper_pos_nn.csv', 'w', encoding="UTF8") as f:
        for w, v in nndict['NN'].items():
            f.write(w + ', ' + str(v) + '\n')
        f.flush()
        f.close()
    with open(DATAP + '/hyper_pos_nns.csv', 'w', encoding="UTF8") as f:
        for w, v in nndict['NNS'].items():
            f.write(w + ', ' + str(v) + '\n')
        f.flush()
        f.close()


def explo_cops(cl_sums):
    print("Exploring COP Hypernyms with Stanford")
    pool = Pool(processes=8)
    parsed_pairs = pool.map(map_cop, cl_sums)
    nndict = dict()
    nndict["NN"] = dict()
    nndict["NNS"] = dict()
    for cl, nn_cop, nns_cop in parsed_pairs:
        if nn_cop is not None:
            try:
                nndict["NN"][nn_cop] += 1
            except KeyError:
                nndict["NN"][nn_cop] = 1
        if nns_cop is not None:
            try:
                nndict["NNS"][nns_cop] += 1
            except KeyError:
                nndict["NNS"][nns_cop] = 1
    with open(DATAP + '/hyper_cop_nn.csv', 'w', encoding="UTF8") as f:
        for w, v in nndict['NN'].items():
            f.write(w + ', ' + str(v) + '\n')
        f.flush()
        f.close()
    with open(DATAP + '/hyper_cop_nns.csv', 'w', encoding="UTF8") as f:
        for w, v in nndict['NNS'].items():
            f.write(w + ', ' + str(v) + '\n')
        f.flush()
        f.close()


def plot_top():
    f = open(DATAP + '/hyper_pos_nn.csv','r',encoding="UTF8")
    headers = ['word', '#articles']
    df = pandas.read_csv(f, names=headers)
    df = df[df['#articles']>0].sort_values(by='#articles')
    print(df)
    df.plot(x="word", y="#articles",style='-')
    # beautify the x-labels
    # plt.gcf().autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    plot_top()
