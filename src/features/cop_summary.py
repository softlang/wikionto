from multiprocessing import Pool
from nltk.tokenize import sent_tokenize
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError

from features.cop_semgrex import COPSemgrex
from check.abstract_check import ArtdictCheck
import requests


class COPSummary(ArtdictCheck):

    def check_single(self, triple):
        title = triple[0]
        summary = triple[1]
        session = triple[2]
        sents = sent_tokenize(summary)
        if len(sents) < 1:
            print(title + ":" + summary)
            return title, None
        try:
            cop = COPSemgrex(summary).run()
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
        pool = Pool(processes=16)

        parsed_pairs = pool.map(self.check_single, summaries)
        parsed_pairs = dict(parsed_pairs)
        for a in artdict:
            if "Summary" not in artdict[a]:
                continue
            hypdict = parsed_pairs[a]
            if hypdict is not None:
                for variant, hypernyms in hypdict.items():
                    artdict[a]["Summary::COP" + variant] = hypernyms
                cop = [hyp for hyplist in hypdict.values() for hyp in hyplist]
                artdict[a]["Summary:COPHypernym"] = cop

        return artdict


if __name__ == "__main__":
    COPSummary().solo()
