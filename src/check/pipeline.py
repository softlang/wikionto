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
from check.childtest import ChildCheck
from check.url_pattern_cat import CategoryURLPattern
from check.eponymous_cat import EponymousCat

from mine.miner import mine


def pipeline():
    indicators = [Seed, SumKeyWords, DbpediaHyp, HypNLPSent, URLPattern, InfoboxDbEx, WikiList,
                  SemDist]
    for i in indicators:
        i().solo()

    catindicator = [CategoryURLPattern, EponymousCat, ChildCheck]
    for c in catindicator:
        c().solo()


if __name__ == '__main__':
    mine()
    pipeline()
