from mine.dbpedia import articles_below, articles_with_summaries, articles_to_categories_below, \
    category_to_subcategory_below, to_uri, articles_with_revisions_live, \
    articles_with_wikidataid, get_templates, articles_with_NonLiveHypernyms, category_to_supercategory_below
from json import dump, load
from data import DATAP, DEPTH, ROOTS
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def init_articledict():
    print("Mining article names and depth of first appearance")
    articledict = dict()
    for c in ROOTS:
        for i in range(DEPTH + 1):
            articles = articles_below(to_uri(c), i, i)
            for title in articles:
                if title not in articledict:
                    articledict[title] = dict()
                if c + "Depth" not in articledict[title]:
                    articledict[title][c + "Depth"] = i
    return articledict


def add_function(articledict, fun, name):
    print("Mining " + name)
    d = dict()
    for c in ROOTS:
        d.update(fun(to_uri(c), 0, DEPTH))
    for cl in articledict:
        if cl in d:
            articledict[cl][name] = d[cl]
    return articledict


def add_wordset(articledict):
    # stopwords
    stop_words = set(stopwords.words('english'))
    stop_words |= {',', '.', ';', '*', '-', '_', ':', "''", '#', '``'}
    stemmer = PorterStemmer(PorterStemmer.NLTK_EXTENSIONS)

    for title in articledict:
        if "Summary" not in articledict[title]:
            continue
        text = articledict[title]["Summary"]
        if text is '':
            continue
        sents = sent_tokenize(text)
        s = sents[0]
        if s.lower().startswith("see also"):
            s = sents[1]
        articledict[title]["words"] = list(
            set(stemmer.stem(w) for w in word_tokenize(s) if w.lower() not in stop_words))
    return articledict


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
                    catdict[cat]["subcats"] = subcats
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


def init_cat_supercat(catdict):
    print("Mining supercategories of categories")
    for c in ROOTS:
        for i in range(DEPTH + 1):
            results = category_to_supercategory_below(to_uri(c), i, i)
            for cat, supercats in results.items():
                catdict[cat]["supercats"] = supercats
    return catdict


def init_cat_articles(catdict, articledict):
    print("Mining articles of categories")
    for title in articledict:
        for c in articledict[title]["cats"]:
            if c not in catdict:
                # print(c)
                continue
            elif "articles" not in catdict[c]:
                catdict[c]["articles"] = []
            catdict[c]["articles"].append(title)
    return catdict


def mine():
    articledict = init_articledict()
    articledict = add_function(articledict, articles_with_summaries, "Summary")
    articledict = add_function(articledict, articles_with_revisions_live, "Revision")
    articledict = add_function(articledict, articles_with_wikidataid, "wikidataid")
    articledict = add_function(articledict, articles_with_NonLiveHypernyms, "DbpediaHypernyms")
    articledict = add_function(articledict, get_templates, "DbpediaInfoboxTemplate")
    articledict = add_function(articledict, articles_to_categories_below, "cats")
    # articledict = add_wordset(articledict)
    # articledict = add_properties(articledict)
    articledict = {key: values for key, values in articledict.items() if "Summary" in values}
    with open(DATAP + '/articledict.json', 'w', encoding='utf8') as f:
        dump(obj=articledict, fp=f, indent=2)
        f.flush()
        f.close()
    mine_cats(articledict)


def mine_cats(articledict):
    catdict = init_cat_subcat()
    catdict = init_cat_articles(catdict, articledict)
    catdict = init_cat_supercat(catdict)
    with open(DATAP + '/catdict.json', 'w', encoding='utf8') as f:
        dump(obj=catdict, fp=f, indent=2)
        f.flush()
        f.close()


if __name__ == '__main__':
    with open(DATAP + '/articledict.json', 'r', encoding='utf8') as f:
        articledict = load(f)
    mine_cats(articledict)
