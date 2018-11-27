from multiprocessing import Pool
from nltk.parse.corenlp import CoreNLPDependencyParser
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError
from check.pos_pattern import cop_hypernym, pos_hypernyms
from check.abstract_check import ArtdictCheck


class SummaryHypernyms(ArtdictCheck):

    def check(self, artdict):
        print("Checking Hypernym with Stanford")

        summaries = []
        for a in artdict:
            summaries.append((a, artdict[a]["Summary"]))
        pool = Pool(processes=8)
        parsed_pairs = pool.map(check_single, summaries)
        parsed_pairs = dict(parsed_pairs)
        for a in artdict:
            summary = artdict[a]["Summary"]
            hyp = parsed_pairs[a]
            if (summary == "No Summary") | (hyp is None):
                artdict[a]["SumPOSLanguage"] = 0
                artdict[a]["SumCOPLanguage"] = 0
                artdict[a]["SumPOSFormat"] = 0
                artdict[a]["SumCOPFormat"] = 0
            else:
                pos, cop = hyp
                artdict[a]["SumPOSHypernyms"] = pos
                artdict[a]["SumCOPHypernym"] = cop
                artdict[a]["SumPOSLanguage"] = int(bool(list(filter(lambda w: w.endswith("language"), pos)))
                                                   | bool(list(filter(lambda w: w.endswith("languages"), pos))))
                artdict[a]["SumCOPLanguage"] = int(str(cop).endswith("language") | str(cop).endswith("languages"))
                artdict[a]["SumPOSFormat"] = int(bool(list(filter(lambda w: w.endswith("format"), pos)))
                                                 | bool(list(filter(lambda w: w.endswith("formats"), pos))))
                artdict[a]["SumCOPFormat"] = int(str(cop).endswith("format") | str(cop).endswith("formats"))
        return artdict


def check_single(pair):
    title = pair[0]
    summary = pair[1]
    if summary.startswith('.'):
        summary = summary[1:]
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    while True:
        try:
            parsed = dep_parser.parse_text(summary)
            pos_list = []
            cop_list = []
            for p in parsed:
                pos_list += pos_hypernyms(p)
                cop_list += cop_hypernym(p)
            return title, (pos_list, cop_list)
        except JSONDecodeError:
            print("Decode Error at :" + title)
            return title, None
        except StopIteration:
            print("Stopped at " + title)
            return title, (pos_list, cop_list)
        except HTTPError:
            print("HTTPError " + title)
            return title, None


if __name__ == "__main__":
    SummaryHypernyms().solo()
