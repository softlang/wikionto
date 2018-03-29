from mine.dbpedia import articles_below, articles_with_summaries, articles_to_categories_below \
    , category_to_subcategory_below, category_to_articles_below, CLURI, CFFURI
from mine.property_miner import add_properties
from json import dump
from data import DATAP


def init_langdict():
    print("Mining article names and depth of first appearance")
    cls_result = list(map(lambda x: (x, 0), articles_below(CLURI, 0, 0)))
    cffs_result = list(map(lambda x: (x, 0), articles_below(CFFURI, 0, 0)))
    for i in range(6):
        x = i + 1
        cls = articles_below(CLURI, x, x)
        cls_result = cls_result + [(cl, x) for cl in cls if cl not in list(zip(*cls_result))[0]]
        cffs = articles_below(CFFURI, x, x)
        cffs_result = cffs_result + [(cff, x) for cff in cffs if cff not in list(zip(*cffs_result))[0]]

    langdict = dict()
    for cl, d in cls_result:
        langdict[cl] = dict()
        langdict[cl]["CLDepth"] = d
        if cl not in list(zip(*cffs_result))[0]:
            langdict[cl]["CFFDepth"] = -1
    for cff, d in cffs_result:
        if cff not in langdict:
            langdict[cff] = dict()
            langdict[cff]["CLDepth"] = -1
        langdict[cff]["CFFDepth"] = d
    return langdict


def add_summaries(langdict):
    print("Mining article summaries")
    clarticles = articles_with_summaries(CLURI, 0, 6)
    cffarticles = articles_with_summaries(CFFURI, 0, 6)
    clarticles.update(cffarticles)
    for cl in langdict:
        if cl in clarticles:
            langdict[cl]["Summary"] = clarticles[cl]
        else:
            langdict[cl]["Summary"] = "No Summary"
    return langdict


def init_article_cats(langdict):
    print("Mining categories of articles")
    atc = articles_to_categories_below(CLURI, 0, 6)
    atc.update(articles_to_categories_below(CFFURI, 0, 6))
    for cl in atc:
        langdict[cl]['cats'] = atc[cl]['cats']
    return langdict


def init_cat_subcat():
    print("Mining subcategories of categories")
    cat_dict = category_to_subcategory_below(CLURI, 0, 0)
    cff_cat_subcat = category_to_subcategory_below(CFFURI, 0, 0)
    for cat in cat_dict:
        cat_dict[cat]["CLDepth"] = 0
    for cat in cff_cat_subcat:
        cff_cat_subcat[cat]["CFFDepth"] = 0

    for i in range(6):
        x = i + 1
        cls_cat_subcat_x = category_to_subcategory_below(CLURI, x, x)
        for cat in cls_cat_subcat_x:
            if not cat in cat_dict:
                cat_dict[cat]["CLDepth"] = x
                cat_dict[cat]["subcats"] = cls_cat_subcat_x[cat]["subcats"]

        cffs_cat_subcat_x = category_to_subcategory_below(CFFURI, x, x)
        for cat in cffs_cat_subcat_x:
            if not cat in cff_cat_subcat:
                cff_cat_subcat[cat]["CFFDepth"] = x
                cff_cat_subcat[cat]["subcats"] = cffs_cat_subcat_x[cat]["subcats"]
    cat_dict.update(cff_cat_subcat)
    return cat_dict


def init_cat_articles():
    print("Mining articles of categories")
    cl_cat_articles = category_to_articles_below(CLURI, 0, 0)
    cff_cat_articles = category_to_articles_below(CFFURI, 0, 0)
    for cat in cl_cat_articles:
        cl_cat_articles[cat]["CLDepth"] = 0
    for cat in cff_cat_articles:
        cff_cat_articles[cat]["CFFDepth"] = 0

    for i in range(6):
        x = i + 1
        cls_cat_articles_x = category_to_articles_below(CLURI, x, x)
        for cat in cls_cat_articles_x:
            if not cat in cl_cat_articles:
                cl_cat_articles[cat]["CLDepth"] = x
                cl_cat_articles[cat]["articles"] = cls_cat_articles_x[cat]["articles"]

        cffs_cat_articles_x = category_to_articles_below(CFFURI, x, x)
        for cat in cffs_cat_articles_x:
            if not cat in cff_cat_articles:
                cff_cat_articles[cat]["CFFDepth"] = x
                cff_cat_articles[cat]["articles"] = cffs_cat_articles_x[cat]["articles"]
    cl_cat_articles.update(cff_cat_articles)
    return cl_cat_articles


def mine():
    langdict = init_langdict()
    langdict = add_summaries(langdict)
    langdict = add_properties(langdict)
    langdict = init_article_cats(langdict)
    with open(DATAP + '/langdict.json', 'w', encoding='utf8') as f:
        dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()

    catdict = init_cat_subcat()
    catdict.update(init_cat_articles())
    f = open(DATAP + '/catdict.json', 'w', encoding='utf8')
    dump(obj=catdict, fp=f, indent=2)
    f.flush()
    f.close()


if __name__ == '__main__':
    mine()
