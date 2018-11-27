from multiprocessing import Pool
from util.custom_stanford_api import StanfordCoreNLP
from nltk.tokenize import sent_tokenize
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError
from json import loads

from data import KEYWORDS, XKEYWORDS
from check.pos_hearst_automaton import HearstAutomaton
from check.abstract_check import ArtdictCheck

import requests


class HypNLPSummary(ArtdictCheck):

    def check_single(self, triple):
        title = triple[0]
        summary = triple[1]
        session = triple[2]
        sents = sent_tokenize(summary)
        if len(sents) < 1:
            print(title + ":" + summary)
            return title, None
        parser = StanfordCoreNLP(url='http://localhost:9000', session=session)
        try:
            parsedict = loads(parser.annotate(summary))
            pos_list = []
            for x in range(len(parsedict["sentences"])):
                parsedict = index_keyvalue_to_key(parsedict["sentences"][x]["tokens"])
                pos_list.append(HearstAutomaton(parsedict).run())
            return title, pos_list
        except JSONDecodeError:
            print("Decode Error at :" + title)
            return title, None
        except StopIteration:
            print("Stopped at " + title)
            return title, None
        except HTTPError:
            print("HTTPError " + title)
            return title, None

    def check(self, artdict):
        print("Checking Hypernym with Stanford")
        session = requests.Session()
        for a in artdict:
            artdict[a]["SUMMARY_POS"] = 0
        summaries = []
        for a in artdict:
            if "Summary" in artdict[a]:
                summaries.append((a, artdict[a]["Summary"], session))
        pool = Pool(processes=4)

        parsed_pairs = pool.map(self.check_single, summaries)
        parsed_pairs = dict(parsed_pairs)
        for a in artdict:
            if "Summary" not in artdict[a]:
                continue
            pos_dict_list = parsed_pairs[a]
            if pos_dict_list is not None:
                artdict[a]["SUMMARY_POSHypernym"] = []
                for posdict in pos_dict_list:
                    for variant, hypernyms in posdict.items():
                        if "SUMMARY_POS" + variant not in artdict[a]:
                            artdict[a]["SUMMARY_POS" + variant] = []
                        artdict[a]["SUMMARY_POS" + variant].append(hypernyms)
                    pos = [hyp for hyplist in posdict.values() for hyp in hyplist]

                    artdict[a]["SUMMARY_POSHypernym"].append(pos)
                    if any(p.lower().endswith(kw) or p.lower().endswith(kw + 's') for p in pos for kw in KEYWORDS):
                        artdict[a]["SUMMARY_POS"] = 1

                    for k1, k2 in XKEYWORDS:
                        if any(p.lower().endswith(k1) or p.lower().endswith(k1 + 's') for p in pos) \
                                and any(p.lower().endswith(k2) or p.lower().endswith(k2 + 's') for p in pos):
                            artdict[a]["SUMMARY_POSX_" + k1 + k2] = 1
                        else:
                            artdict[a]["SUMMARY_POSX_" + k1 + k2] = 0
        return artdict


def index_keyvalue_to_key(parsedict_list):
    result = dict()
    for parsedict in parsedict_list:
        d = parsedict
        index = parsedict["index"]
        del d["index"]
        result[index] = d
    return result


if __name__ == "__main__":
    HypNLPSummary().solo()
