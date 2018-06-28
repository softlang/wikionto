from check.langdictcheck import LangdictCheck
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
from multiprocessing import Pool
import string


class SeedWordSetSim(LangdictCheck):

    def check(self, langdict):
        print("Annotating similarity to seed sentences")

        seedwordlists = list(langdict[cl]["words"] for cl in langdict
                             if "words" in langdict[cl] and langdict[cl]["Seed"] == 1)

        i = 0
        for cl in langdict:
            i += 1
            if "words" not in langdict[cl] or langdict[cl]["Seed"] == 1:
                continue
            words = set(langdict[cl]["words"])
            if not words:
                continue
            sims = map(lambda wordlist: len(set(wordlist) & set(words)), seedwordlists)
            langdict[cl]["WordSetSim"] = max(sims)
            if i % 1000 == 0:
                print(str(i) + "/" + str(len(langdict.items())))
        return langdict


if __name__ == '__main__':
    SeedWordSetSim().solo()
