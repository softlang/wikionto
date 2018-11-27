from multiprocessing import Pool
from util.custom_stanford_api import StanfordCoreNLP
from nltk.tokenize import sent_tokenize
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError
from json import loads

from data import KEYWORDS, XKEYWORDS
from check.pos_pattern import cop_hypernym, pos_hypernyms
from check.cop_semgrex import COPSemgrex
from check.abstract_check import ArtdictCheck
import requests


class COPFirstSentence(ArtdictCheck):

    def check_single(self, triple):
        title = triple[0]
        summary = triple[1]
        session = triple[2]
        sents = sent_tokenize(summary)
        if len(sents) < 1:
            print(title + ":" + summary)
            return title, None
        first_sentence = sents[0]
        if sents[0] is "." or sents[0] is "" or sents[0].startswith("See also"):
            if len(sents) > 1:
                first_sentence = sents[1]
            else:
                return title, None
        try:
            cop = COPSemgrex(first_sentence).run()
            return title, cop
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
            artdict[a]["POS"] = 0
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
            hypdict = parsed_pairs[a]
            if hypdict is not None:
                for variant, hypernyms in hypdict.items():
                    artdict[a]["COP" + variant] = hypernyms
                pos = [hyp for hyplist in hypdict.values() for hyp in hyplist]
                artdict[a]["COPHypernym"] = pos
                if any(p.lower().endswith(kw) or p.lower().endswith(kw + 's') for p in pos for kw in KEYWORDS):
                    artdict[a]["COP"] = 1

                for k1, k2 in XKEYWORDS:
                    if any(p.lower().endswith(k1) or p.lower().endswith(k1 + 's') for p in pos) \
                            and any(p.lower().endswith(k2) or p.lower().endswith(k2 + 's') for p in pos):
                        artdict[a]["COPX_" + k1 + k2] = 1
                    else:
                        artdict[a]["COPX_" + k1 + k2] = 0
        return artdict


if __name__ == "__main__":
    COPFirstSentence().solo()
