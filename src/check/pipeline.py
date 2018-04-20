from check.gitseed import check_gitseed
from check.infobox import check_infobox
from check.hypernym_dbpedia import check_dbpedia_hypernym
from check.hypernym_stanford import check_stanford
from check.summary_keywords import check_summary_for_keywords
from check.semantic_distance import check_semantic_distance
from check.article_name_pattern import check_article_name
from check.empty_category import check_empty_cat
from json import dump, load
from check.cat_name_pattern import check_cat_name
from check.eponymous_cat import check_eponymous
from check.multi_infobox import check_multi_infobox
from check.instance_wikidata import check_instance_of_wikidata
from check.yago import check_instance_of_yago

from mine.miner import mine
from data import DATAP


def pipeline():
    with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
        langdict = load(f)
        langdict = check_gitseed(langdict)
        langdict = check_infobox(langdict)
        langdict = check_dbpedia_hypernym(langdict)
        langdict = check_stanford(langdict)
        langdict = check_summary_for_keywords(langdict)
        langdict = check_semantic_distance(langdict)
        langdict = check_article_name(langdict)
        langdict = check_multi_infobox(langdict)
        langdict = check_instance_of_wikidata(langdict)
        langdict = check_instance_of_yago(langdict)
        f.close()

    with open(DATAP + '/langdict.json', 'w', encoding="UTF8") as f:
        dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()

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


if __name__ == '__main__':
    mine()
    pipeline()
