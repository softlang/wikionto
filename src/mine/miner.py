from mine.dbpedia import articles_below, articles_with_summaries, articles_to_categories_below, \
    category_to_subcategory_below, to_uri, articles_with_revisions_live, \
    articles_with_wikidataid, get_templates, articles_with_NonLiveHypernyms
from json import dump, load
from data import DATAP, DEPTH, CATS


def init_langdict():
    print("Mining article names and depth of first appearance")
    langdict = dict()
    for c in CATS:
        for i in range(DEPTH + 1):
            articles = articles_below(to_uri(c), 0, 0)
            for cl in articles:
                if cl not in langdict:
                    langdict[cl] = dict()
                langdict[cl][c + "Depth"] = i
    return langdict


def add_function(langdict, fun, name):
    d = dict()
    for c in CATS:
        d.update(fun(to_uri(c), 0, DEPTH))
    for cl in langdict:
        if cl in d:
            langdict[cl][name] = d[cl]
    return langdict


def init_cat_subcat():
    print("Mining subcategories of categories")
    catdict = dict()
    for c in CATS:
        for i in range(DEPTH + 1):
            d2 = category_to_subcategory_below(to_uri(c), i, i)
            for cat, subcats in d2.items():
                if cat not in catdict:
                    catdict[c] = dict()
                    catdict[c][c + "Depth"] = i
                    catdict[c]["subcats"] = subcats
    return catdict


def init_cat_articles(catdict, langdict):
    print("Mining articles of categories")
    for cl in langdict:
        for c in langdict[cl]["cats"]:
            if "articles" not in catdict[c]:
                catdict[c]["articles"] = []
            catdict[c]["articles"].append(cl)
    return catdict


def mine():
    langdict = init_langdict()
    langdict = add_function(langdict, articles_with_summaries, "Summary")
    langdict = add_function(langdict, articles_with_revisions_live, "Revision")
    langdict = add_function(langdict, articles_with_wikidataid, "wikidataid")
    langdict = add_function(langdict, articles_with_NonLiveHypernyms, "DbpediaHypernyms")
    langdict = add_function(langdict, get_templates, "DbpediaInfoboxTemplate")
    langdict = add_function(langdict, articles_to_categories_below, "cats")
    # langdict = add_properties(langdict)
    with open(DATAP + '/langdict.json', 'w', encoding='utf8') as f:
        dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()

    catdict = init_cat_subcat()
    catdict = init_cat_articles(catdict, langdict)
    with open(DATAP + '/catdict.json', 'w', encoding='utf8') as f:
        dump(obj=catdict, fp=f, indent=2)
        f.flush()
        f.close()


if __name__ == '__main__':
    with open(DATAP + '/langdict.json', 'r', encoding='utf8') as f:
        ld = load(f)
        ld = add_function(ld, get_templates, "DbpediaInfoboxTemplate")
    with open(DATAP + '/langdict.json', 'w', encoding='utf8') as f:
        dump(obj=ld, fp=f, indent=2)
        f.flush()
        f.close()
