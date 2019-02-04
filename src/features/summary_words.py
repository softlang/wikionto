from check.abstract_check import ArtdictCheck
from stanford.custom_stanford_api import StanfordCoreNLP, index_keyvalue_to_key
from multiprocessing import Pool
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError

class SumNouns(ArtdictCheck):
    def check(self, articledict):
        print("Extracting summary words")

        summarypairs = [(title, articledict[title]["Summary"]) for title in articledict if
                        "Summary" in articledict[title]]
        pool = Pool(processes=4)
        title_to_words = pool.map(get_words, summarypairs)
        title_to_words = dict(title_to_words)
        for title in articledict:
            if title in title_to_words:
                words = title_to_words[title]
                articledict[title]["Words"] = words
            else:
                articledict[title]["Words"] = []
        return articledict


def get_words(pair):
    title = pair[0]
    text = pair[1]
    parser = StanfordCoreNLP(url='http://localhost:9000')
    try:
        nouns = []
        parsedict = parser.annotate(text)
        if not parsedict['sentences']:
            return title, []
        for sentence in parsedict['sentences']:
            parsedict = sentence["tokens"]
            nouns += [wdict['word'] for wdict in parsedict if 'NN' in wdict['pos']]
            #for index in range(1, len(parsedict)):
            #    wdict = parsedict[index]
            #    if 'NN' in wdict['pos']:
            #        nouns.append(wdict['word'])
        return title, nouns
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
    SumNouns().solo()
