from data import DATAP
from json import dump, load
from extract.gitseed import extract_recalled
from extract.infobox import extract_properties
from extract.multi_infobox import extract_multi_infobox
from extract.summary_words import extract_summary_words
from extract.title_words import extract_title_words
from extract.wikidata import extract_instance_of_wikidata
from extract.yago import extract_instance_of_yago
from mine.miner import mine
from data.cluster import preprocess, cluster, is_valid

def extract():
    mine()
    with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
        langdict = load(f)
        langdict = extract_recalled(langdict)
        langdict = extract_properties(langdict)
        langdict = extract_multi_infobox(langdict)
        langdict = extract_summary_words(langdict)
        langdict = extract_title_words(langdict)
        langdict = extract_instance_of_wikidata(langdict)
        langdict = extract_instance_of_yago(langdict)
        f.close()

    with open(DATAP + '/langdict.json', 'w', encoding="UTF8") as f:
        dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()


if __name__ == '__main__':
    extract()
