from features.cop_firstsentence import COPFirstSentence
from check.infobox_dbpedia_existence import InfoboxDbEx
from features.lists_of import WikiList
from features.urlwords import ExtractURLWords
from check.deleted_from_wikipedia import IdentifyDeletedFromWikipedia
from check.isstub import IdentifyStubs
from features.summary_words import SumNouns
from features.summary_lemma import SumLemmas
from mine.miner import mine
from check.seed import Seed


def article_indicators():
    extractors = [Seed, IdentifyDeletedFromWikipedia, IdentifyStubs, InfoboxDbEx, ExtractURLWords, WikiList, SumNouns, SumLemmas,
                  COPFirstSentence]
    for e in extractors:
        e().solo(backup=False)


if __name__ == '__main__':
    mine()
    article_indicators()
