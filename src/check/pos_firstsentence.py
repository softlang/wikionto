from multiprocessing import Pool
from util.CustomDependencyParser import CustomParser
from nltk.tokenize import sent_tokenize
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError

from data import KEYWORDS, XKEYWORDS
from check.pos_pattern import cop_hypernym, pos_hypernyms
from check.abstract_check import ArtdictCheck

import requests


class HypNLPSent(ArtdictCheck):

    def check_single(self, triple):
        title = triple[0]
        summary = triple[1]
        session = triple[2]
        sents = sent_tokenize(summary)
        if len(sents) < 1:
            print(title + ":" + summary)
            return title, None
        summary = sents[0]
        if sents[0] is "." or sents[0] is "" or sents[0].startswith("See also"):
            if len(sents) > 1:
                summary = sents[1]
            else:
                return title, None
        dep_parser = CustomParser(url='http://localhost:9000', session=session)
        try:
            parse, = dep_parser.raw_parse(summary)
            pos = pos_hypernyms(parse)
            cop = cop_hypernym(parse)
            return title, (pos, cop)
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
            artdict[a]["O_POS"] = 0
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
            hyp = parsed_pairs[a]
            if hyp is not None:
                (pos, s), cop = hyp
                artdict[a]["O_POSHypernyms"] = pos
                artdict[a]["O_COPHypernym"] = cop
                artdict[a]["O_POS_isa"] = 0
                artdict[a]["O_POS_isoneof"] = 0
                artdict[a]["O_POS_The"] = 0
                if len(s) > 0:
                    artdict[a]["O_POS_" + s] = 1
                if any(p.lower().endswith(kw) or p.lower().endswith(kw + 's') for p in pos for kw in KEYWORDS):
                    artdict[a]["O_POS"] = 1

                for k1, k2 in XKEYWORDS:
                    if any(p.lower().endswith(k1) or p.lower().endswith(k1 + 's') for p in pos) \
                            and any(p.lower().endswith(k2) or p.lower().endswith(k2 + 's') for p in pos):
                        artdict[a]["O_POSX_" + k1 + k2] = 1
                    else:
                        artdict[a]["O_POSX_" + k1 + k2] = 0

                if cop is not None:
                    if any(kw in c.lower() for c in cop for kw in KEYWORDS):
                        artdict[a]["O_COP"] = 1
        return artdict


if __name__ == "__main__":
    HypNLPSent().solo()
