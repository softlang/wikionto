from mine.dbpedia import articles_below, articles_with_summaries, articles_to_categories_below, \
    category_to_subcategory_below, to_uri, articles_with_revisions_live, \
    articles_with_wikidataid, get_templates, articles_with_NonLiveHypernyms
from json import dump, load
from data import DATAP, DEPTH, ROOTS
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def init_langdict():
    print("Mining article names and depth of first appearance")
    langdict = dict()
    for c in ROOTS:
        for i in range(DEPTH + 1):
            articles = articles_below(to_uri(c), i, i)
            for cl in articles:
                if cl not in langdict:
                    langdict[cl] = dict()
                if c + "Depth" not in langdict[cl]:
                    langdict[cl][c + "Depth"] = i
    return langdict


def add_function(langdict, fun, name):
    print("Mining " + name)
    d = dict()
    for c in ROOTS:
        d.update(fun(to_uri(c), 0, DEPTH))
    for cl in langdict:
        if cl in d:
            langdict[cl][name] = d[cl]
    return langdict


def add_wordset(langdict):
    # stopwords
    stop_words = set(stopwords.words('english'))
    stop_words |= {',', '.', ';', '*', '-', '_', ':', "''", '#', '``'}
    stemmer = PorterStemmer(PorterStemmer.NLTK_EXTENSIONS)

    for cl in langdict:
        if "Summary" not in langdict[cl]:
            continue
        text = langdict[cl]["Summary"]
        if text is '':
            continue
        sents = sent_tokenize(text)
        s = sents[0]
        if s.lower().startswith("see also"):
            s = sents[1]
        langdict[cl]["words"] = list(set(stemmer.stem(w) for w in word_tokenize(s) if w.lower() not in stop_words))
    return langdict


def init_cat_subcat():
    print("Mining subcategories of categories")
    catdict = dict()
    for c in ROOTS:
        for i in range(DEPTH + 1):
            d2 = category_to_subcategory_below(to_uri(c), i, i)
            for cat, subcats in d2.items():
                if cat not in catdict:
                    catdict[cat] = dict()
                    catdict[cat][c + "Depth"] = i
                if "subcats" not in catdict[cat]:
                    catdict[cat]["subcats"] = subcats  # TODO possible bug
                    for sc in subcats:
                        if sc not in catdict:
                            catdict[sc] = dict()
                        if c + "Depth" not in catdict[sc]:
                            catdict[sc][c + "Depth"] = i + 1
                for subcat in subcats:
                    if subcat not in catdict:
                        catdict[subcat] = dict()
                        catdict[subcat]["supercats"] = [cat]
                    else:
                        if "supercats" not in catdict[subcat]:
                            catdict[subcat]["supercats"] = [cat]
                        else:
                            catdict[subcat]["supercats"].append(cat)
    return catdict


def init_cat_articles(catdict, langdict):
    print("Mining articles of categories")
    for cl in langdict:
        for c in langdict[cl]["cats"]:
            tc = "Category:"+c
            if tc not in catdict:
                #print(c)
                continue
            elif "articles" not in catdict[tc]:
                catdict[tc]["articles"] = []
            catdict[tc]["articles"].append(cl)
    return catdict


def mine():
    langdict = init_langdict()
    langdict = add_function(langdict, articles_with_summaries, "Summary")
    langdict = add_function(langdict, articles_with_revisions_live, "Revision")
    langdict = add_function(langdict, articles_with_wikidataid, "wikidataid")
    langdict = add_function(langdict, articles_with_NonLiveHypernyms, "DbpediaHypernyms")
    langdict = add_function(langdict, get_templates, "DbpediaInfoboxTemplate")
    langdict = add_function(langdict, articles_to_categories_below, "cats")
    # langdict = add_wordset(langdict)
    # langdict = add_properties(langdict)
    langdict = {key: values for key, values in langdict.items() if "Summary" in values}
    with open(DATAP + '/langdict.json', 'w', encoding='utf8') as f:
        dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()
    mine_cats(langdict)


def mine_cats(langdict):
    catdict = init_cat_subcat()
    catdict = init_cat_articles(catdict, langdict)
    with open(DATAP + '/catdict.json', 'w', encoding='utf8') as f:
        dump(obj=catdict, fp=f, indent=2)
        f.flush()
        f.close()


if __name__ == '__main__':
    with open(DATAP + '/langdict.json', 'r', encoding='utf8') as f:
        langdict = load(f)
    mine_cats(langdict)
