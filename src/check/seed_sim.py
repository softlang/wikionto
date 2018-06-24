from check.langdictcheck import LangdictCheck
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
from multiprocessing import Pool
import string


class SeedSim(LangdictCheck):

    def check(self, langdict):
        print("Annotating similarity to seed sentences")
        ssums = []
        for cl, feat in langdict.items():
            if (feat["Seed"] == 1) and ("Summary" in feat):
                ssums.append(feat["Summary"])

        pool = Pool(processes=4)
        cltuples = [(cl, langdict[cl]["Summary"], ssums) for cl in langdict if "Summary" in langdict[cl]]
        cltuples = list(pool.map(seedsim, cltuples))
        for cl, wsim, csim in cltuples:
            langdict[cl]["Seed_Similarity_Word"] = wsim
            langdict[cl]["Seed_Similarity_Char"] = csim
        return langdict


def seedsim(cltuple):
    try:
        cl = cltuple[0]
        text = cltuple[1]
        ssums = cltuple[2]
        return cl, sim_word(text, ssums), sim_char(text, ssums)
    except IndexError:
        print("ERROR at " + cl)
        return cl, 0.0


def sim_word(text, texts):
    vect = CountVectorizer(analyzer='word', tokenizer=normalize, min_df=0, stop_words='english')
    texts.append(text)
    matrix = vect.fit_transform(texts)
    cosine_similarities = linear_kernel(matrix[0:1], matrix).flatten()
    simmax = max(cosine_similarities[1:])
    return simmax


def sim_char(text, texts):
    vect = CountVectorizer(analyzer='char_wb', tokenizer=normalize, min_df=0, stop_words='english', ngram_range=(5, 5))
    texts.append(text)
    matrix = vect.fit_transform(texts)
    cosine_similarities = linear_kernel(matrix[0:1], matrix).flatten()
    simmax = max(cosine_similarities[1:])
    return simmax


def normalize(text):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    text = sent_tokenize(text)[0]
    return stem_tokens(word_tokenize(text.lower().translate(remove_punctuation_map)))


def stem_tokens(tokens):
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    return [stemmer.stem(item) for item in tokens]


if __name__ == '__main__':
    SeedSim().solo()
