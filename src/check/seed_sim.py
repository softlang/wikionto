from check.langdictcheck import LangdictCheck
from sklearn.feature_extraction.text import TfidfVectorizer
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
            if ("TIOBE" in feat and feat["TIOBE"] == 1) or \
                    ("GitSeed" in feat and feat["GitSeed"] == 1):
                ssums.append(feat["Summary"])

        pool = Pool(processes=4)
        cltuples = [(cl, langdict[cl]["Summary"], ssums) for cl in langdict]
        cltuples = list(pool.map(seedsim, cltuples))
        for cl, rsim in cltuples:
            langdict[cl]["Seed_Similarity"] = rsim
        return langdict


def seedsim(cltuple):
    cl = cltuple[0]
    text = cltuple[1]
    ssums = cltuple[2]
    if text is "No Summary" or text is "":
        return cl, 0
    else:
        return cl, sim(text, ssums)


def sim(text, texts):
    vect = TfidfVectorizer(analyzer='word', tokenizer=normalize, min_df=0, stop_words='english')
    tfidf_matrix = vect.fit_transform([text] + texts)
    cosine_similarities = linear_kernel(tfidf_matrix[0:1], tfidf_matrix).flatten()
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
