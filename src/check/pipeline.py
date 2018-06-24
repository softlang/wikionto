from check.seed import Seed
from check.seed_sim import SeedSim
from check.hypernym_dbpedia import DbpediaHyp
from check.hypernym_nlp_firstsentence import HypNLPSent
from check.summary_keywords import SumKeyWords
from check.url_pattern import URLPattern
from check.infobox_dbpedia_existence import InfoboxDbEx
from check.lists_of import WikiList
from check.wikidata import Wikidata
from check.yago import Yago
from check.hypernym_wordnet import WordNet
from check.semantic_distance import SemDist
from check.empty_cat import check_empty_cat
from check.url_pattern_cat import check_cat_name
from check.eponymous_cat import check_eponymous
from json import dump, load

from mine.miner import mine
from data import DATAP


def pipeline():
    ans = [Seed, SumKeyWords, DbpediaHyp, HypNLPSent, URLPattern, InfoboxDbEx, WikiList,
           Wikidata, Yago, WordNet, SemDist, SeedSim]
    for c in ans:
        try:
            c().solo()
        except:
            print("Error")


"""
    with open(DATAP + '/catdict.json', 'r', encoding="UTF8") as f:
        catdict = load(f)
        catdict = check_empty_cat(catdict, langdict)
        catdict = check_cat_name(catdict)
        catdict = check_eponymous(catdict, langdict)
        f.close()

    with open(DATAP + '/catdict.json', 'w', encoding="UTF8") as f:
        dump(obj=catdict, fp=f, indent=2)
        f.flush()
        f.close()
"""

if __name__ == '__main__':
    mine()
    pipeline()
