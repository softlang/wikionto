from json import load
from data import DATAP
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.stem import PorterStemmer
import collections
from multiprocessing import Pool

def get_nouns(text):
    return [PorterStemmer().stem(noun) for sent in sent_tokenize(text) for noun, tag in pos_tag(word_tokenize(sent))
            if 'NN' in tag]


if __name__ == '__main__':
    f = open(DATAP+'/olangdict.json', 'r')
    d = load(f)
    texts = [d[cl]["Summary"] for cl in d if "Summary" in d[cl]]
    pool = Pool(processes=4)
    nouns = list(pool.map(get_nouns,texts))
    nouns = [nn for nnlist in nouns for nn in nnlist]

    counter=collections.Counter(nouns)
    print(counter.most_common(10))

