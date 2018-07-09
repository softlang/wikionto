from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.tokenize import sent_tokenize
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError

from data import KEYWORDS, XKEYWORDS
from check.hypernym_nlp_pattern import cop_hypernym, pos_hypernyms
from check.langdictcheck import LangdictCheck


class HypNLPSent(LangdictCheck):

    def check_single(self, pair):
        cl = pair[0]
        summary = pair[1]
        sents = sent_tokenize(summary)
        if len(sents) < 1:
            print(cl+":"+summary)
            return cl, None
        summary = sents[0]
        if sents[0] is "." or sents[0] is "" or sents[0].startswith("See also"):
            if len(sents) > 1:
                summary = sents[1]
            else:
                return cl, None
        dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
        try:
            parse, = dep_parser.raw_parse(summary)
            pos = pos_hypernyms(parse)
            cop = cop_hypernym(parse)
            return cl, (pos, cop)
        except JSONDecodeError:
            print("Decode Error at :" + cl)
            return cl, None
        except StopIteration:
            print("Stopped at " + cl)
            return cl, None
        except HTTPError:
            print("HTTPError " + cl)
            return cl, None

    def check(self, langdict):
        print("Checking Hypernym with Stanford")
        for cl in langdict:
            langdict[cl]["POS"] = 0
        cl_sums = []
        for cl in langdict:
            if "Summary" in langdict[cl]:
                cl_sums.append((cl, langdict[cl]["Summary"]))
        pool = Pool(processes=4)
        parsed_pairs = pool.map(self.check_single, cl_sums)
        parsed_pairs = dict(parsed_pairs)
        for cl in langdict:
            if "Summary" not in langdict[cl]:
                continue
            hyp = parsed_pairs[cl]
            if hyp is not None:
                (pos, s), cop = hyp
                langdict[cl]["POSHypernyms"] = pos
                langdict[cl]["COPHypernym"] = cop
                langdict[cl]["POS_isa"] = 0
                langdict[cl]["POS_isoneof"] = 0
                langdict[cl]["POS_The"] = 0
                if len(s) > 0:
                    langdict[cl]["POS_" + s] = 1
                if any(p.lower().endswith(kw) or p.lower().endswith(kw + 's') for p in pos for kw in KEYWORDS):
                    langdict[cl]["POS"] = 1

                for k1, k2 in XKEYWORDS:
                    if any(p.lower().endswith(k1) or p.lower().endswith(k1 + 's') for p in pos) \
                            and any(p.lower().endswith(k2) or p.lower().endswith(k2 + 's') for p in pos):
                        langdict[cl]["POSX_" + k1 + k2] = 1
                    else:
                        langdict[cl]["POSX_" + k1 + k2] = 0

                if cop is not None:
                    if any(kw in c.lower() for c in cop for kw in KEYWORDS):
                        langdict[cl]["COP"] = 1
        return langdict


if __name__ == "__main__":
    HypNLPSent().solo()
