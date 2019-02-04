from check.abstract_check import ArtdictCheck
from stanford.custom_stanford_api import StanfordCoreNLP, index_keyvalue_to_key
from multiprocessing import Pool
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError
from data import DATAP


class SumLemmas(ArtdictCheck):
    def check(self, articledict):
        print("Extracting summary words")
        with open(DATAP + "/stopwords.txt", "r") as f:
            stopwords = set(line.replace("\n", "") for line in f)
        summarypairs = [(title, articledict[title]["Summary"], stopwords) for title in articledict if
                        "Summary" in articledict[title]]
        pool = Pool(processes=4)
        title_to_words = pool.map(get_lemmas, summarypairs)
        title_to_words = dict(title_to_words)
        for title in articledict:
            if title in title_to_words:
                words = title_to_words[title]
                articledict[title]["Lemmas"] = words
            else:
                articledict[title]["Lemmas"] = []
        return articledict


def get_lemmas(p):
    title = p[0]
    text = p[1]
    stopwords = p[2]
    parser = StanfordCoreNLP(url='http://localhost:9000')
    try:
        lemmas = []
        parsedict = parser.annotate(text, annotators="tokenize,ssplit,pos,lemma")
        if not parsedict['sentences']:
            return title, []
        for sentence in parsedict['sentences']:
            parsedict = sentence["tokens"]
            for index in range(1, len(parsedict)):
                wdict = parsedict[index]
                lemma = wdict['lemma']

                if lemma not in stopwords:
                    lemmas.append(lemma)
                """if '-' in lemma:
                    word1 = lemma.split('-')[0]
                    if word1 not in stopwords:
                        lemmas.append(word1)
                    word2 = lemma.split('-')[1]
                    if word2 not in stopwords:
                        lemmas.append(word2)
                else:
                    if lemma not in stopwords:
                        lemmas.append(lemma)"""
        return title, lemmas
    except JSONDecodeError:
        print("Decode Error at :" + title)
        return title, None
    except StopIteration:
        print("Stopped at " + title)
        return title, None
    except HTTPError:
        print("HTTPError " + title)
        return title, None


if __name__ == '__main__':
    SumLemmas().solo()
