from mine.dbpedia import articles_below,category_to_subcategory_below,CLURI,CFFURI
from json import dump

def init_langdict():
    cls_result = list(map(lambda x: (x,0),articles_below(CLURI,0,0)))
    cffs_result = list(map(lambda x: (x,0),articles_below(CFFURI,0,0)))
    for i in range(6):
        x=i+1
        cls = articles_below(CLURI,x,x)
        cls_result = cls_result + [(cl,x) for cl in cls if cl not in list(zip(*cls_result))[0]]
        cffs = articles_below(CFFURI,x,x)
        cffs_result = cffs_result + [(cff,x) for cff in cffs if cff not in list(zip(*cffs_result))[0]]
    
    langdict = dict()
    for cl,d in cls_result:
        langdict[cl] = dict()
        langdict[cl]["CLDepth"] = d
        if cl not in list(zip(*cffs_result))[0]:
            langdict[cl]["CFFDepth"] = -1
    for cff,d in cffs_result:
        if not cff in langdict:
            langdict[cff] = dict()
            langdict[cff]["CLDepth"] = -1
        langdict[cff]["CFFDepth"] = d
    with open('../data/langdict.json', 'w',encoding='utf8') as f:
        dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()

def init_cat_subcat():
    cl_cat_subcat = category_to_subcategory_below(CLURI,0,0)
    cff_cat_subcat = category_to_subcategory_below(CFFURI,0,0)
    for cat in cl_cat_subcat:
        cl_cat_subcat[cat]["CLDepth"] = 0
    for cat in cff_cat_subcat:
        cff_cat_subcat[cat]["CFFDepth"] = 0
        
    for i in range(6):
        x=i+1
        cls_cat_subcat_x = category_to_subcategory_below(CLURI,x,x)
        for cat in cls_cat_subcat_x:
            if not cat in cl_cat_subcat:
                cl_cat_subcat[cat]["CLDepth"] = x
                cl_cat_subcat[cat]["subcats"] = cls_cat_subcat_x[cat]["subcats"]
            else:
                cl_cat_subcat[cat]["subcats"] = cl_cat_subcat[cat]["subcats"] + cls_cat_subcat_x[cat]["subcats"]
        
        cffs_cat_subcat_x = category_to_subcategory_below(CFFURI,x,x)
        for cat in cffs_cat_subcat_x:
            if not cat in cff_cat_subcat:
                cff_cat_subcat[cat]["CFFDepth"] = x
                cff_cat_subcat[cat]["subcats"] = cffs_cat_subcat_x[cat]["subcats"]
            else:
                cff_cat_subcat[cat]["subcats"] = cff_cat_subcat[cat]["subcats"] + cffs_cat_subcat_x[cat]["subcats"]
    cl_cat_subcat.update(cff_cat_subcat)
    with open('../data/cat_subcat.json', 'w',encoding='utf8') as f:
        dump(obj=cl_cat_subcat, fp=f, indent=2)
        f.flush()
        f.close()
init_cat_subcat()