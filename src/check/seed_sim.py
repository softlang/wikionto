from check.langdictcheck import LangdictCheck
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
from multiprocessing import Pool
import string


class SeedSim(LangdictCheck):

    def check(self, langdict):
        print("Annotating similarity to seed sentences")
        ssums = []
        for cl in langdict:
            if (langdict[cl]["Seed"] == 1) and ("Summary" in langdict[cl]):
                ssums.append(langdict[cl]["Summary"])

        pool = Pool(processes=4)
        cltuples = [(cl, langdict[cl]["Summary"], ssums) for cl in langdict if
                    "Summary" in langdict[cl] and langdict[cl]["Seed"] == 0]
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
        print("ERROR at " + cl + "with length " + len(cltuple))
        return cl, 0.0


def sim_word(text, texts):
    vect = HashingVectorizer(analyzer='char_wb', tokenizer=normalize, stop_words='english', ngram_range=(10, 10))
    texts.append(text)
    matrix = vect.fit_transform(texts)
    cosine_similarities = linear_kernel(matrix[0:1], matrix).flatten()
    simmax = max(cosine_similarities[1:])
    return simmax


def sim_char(text, texts):
    vect = HashingVectorizer(analyzer='char_wb', tokenizer=normalize, stop_words='english', ngram_range=(5, 5))
    texts.append(text)
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
    # SeedSim().solo()
    s1 = sim_word("Ruby is a programming language",
                  ["Python is a programming language", "Chiby is a song", "Esperanto is a constructed language"])
    s2 = sim_char("Ruby is a programming language",
                  ["Python is a programming language", "Chiby is a song", "Esperanto is a constructed language"])
    print(s1)
    print(s2)
