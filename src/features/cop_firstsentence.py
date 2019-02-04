from multiprocessing import Pool
from nltk.tokenize import sent_tokenize
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError

from features.cop_semgrex import COPSemgrex
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
            del cop['Aisa']
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
        print("Checking dependency-based Hypernym with Stanford")
        session = requests.Session()
        summaries = []
        for a in artdict:
            if "Summary" in artdict[a]:
                summaries.append((a, artdict[a]["Summary"], session))
        pool = Pool(processes=4)

        parsed_pairs = pool.map(self.check_single, summaries)
        parsed_pairs = dict(parsed_pairs)
        for a in artdict:
            artdict[a]["COP"] = 0
            if "Summary" not in artdict[a]:
                continue
            hypdict = parsed_pairs[a]
            if hypdict is not None:
                for variant, hypernyms in hypdict.items():
                    artdict[a]["COP" + variant] = hypernyms
                cop = [hyp for hyplist in hypdict.values() for hyp in hyplist]
                artdict[a]["COPHypernym"] = cop
                #if any(hyp.lower().endswith(kw) or hyp.lower().endswith(kw + 's') for hyp in cop for kw in KEYWORDS):
                #    artdict[a]["COP"] = 1

        return artdict


if __name__ == "__main__":
    COPFirstSentence().solo()
