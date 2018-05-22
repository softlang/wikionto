from check.langdictcheck import LangdictCheck
from sklearn.feature_extraction.text import TfidfVectorizer


class SeedSim(LangdictCheck):

    def check(self, langdict):
        print("Annotating similarity to seed sentences")
        sums = collect_sums(langdict)
        for cl in langdict:
            if ("TIOBE" not in langdict[cl] or langdict[cl]["TIOBE"] == 0) and (
                    "GitSeed" not in langdict[cl] or langdict[cl]["GitSeed"] == 0):
                langdict[cl]["Seed_Similarity"] = sim(langdict[cl]["Summary"], sums)
        return langdict


def collect_sums(langdict):
    sums = []
    for cl, feat in langdict.items():
        if ("TIOBE" in feat and feat["TIOBE"]==1) or ("GitSeed" in feat and feat["GitSeed"]==1):
            sums.append(feat["Summary"])
    return sums


def sim(text,texts):
    vect = TfidfVectorizer(min_df=1)

    tfidf = vect.fit_transform([text] + texts)
    simar = (tfidf * tfidf.T).A
    return max(simar[0][1:])


if __name__ == '__main__':
    SeedSim().solo()
