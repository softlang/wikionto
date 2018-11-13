from check.abstract_check import ArtdictCheck
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
from multiprocessing import Pool
import string


class SeedSim(ArtdictCheck):

    def check(self, articledict):
        print("Annotating similarity to seed sentences")
        seed_summaries = []
        for title in articledict:
            if (articledict[title]["Seed"] == 1) and ("Summary" in articledict[title]):
                seed_summaries.append(articledict[title]["Summary"])

        pool = Pool(processes=6)
        cltuples = [(cl, articledict[cl]["Summary"], seed_summaries) for cl in articledict if
                    "Summary" in articledict[cl] and articledict[cl]["Seed"] == 0]
        cltuples = list(pool.map(seedsim, cltuples))
        for title, simc5 in cltuples:
            articledict[title]["Seed_Similarity_Word"] = simc5
        return articledict


def seedsim(cltuple):
    try:
        cl = cltuple[0]
        text = cltuple[1]
        ssums = cltuple[2]
        simc5 = sim_texts(text, ssums)
        return cl, simc5
    except IndexError:
        print("ERROR at " + cl + "with length " + len(cltuple))
        return cl, 0.0


def sim_texts(text, texts):
    simc5 = 0
    for t in texts:
        sim = sim_char5(text, t)
        if simc5 < sim:
            simc5 = sim
    return simc5


def sim_char10(text1, text2):
    vect = HashingVectorizer(analyzer='char_wb', tokenizer=normalize, stop_words='english', ngram_range=(10, 10))
    texts = [text1, text2]
    matrix = vect.fit_transform(texts)
    cosine_similarities = linear_kernel(matrix[0:1], matrix).flatten()
    simmax = max(cosine_similarities[1:])
    return simmax


def sim_char5(text1, text2):
    vect = HashingVectorizer(analyzer='word', tokenizer=normalize, stop_words='english')
    texts = [text1, text2]
    matrix = vect.transform(texts)
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
