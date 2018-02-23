from json import load

def check_semantic_distance(langdict):
    print("Checking semantic distance")
    f = open('data/catdict.json', 'r',encoding="UTF8")
    catdict = load(f)
    for cl in langdict: 
        cats = langdict[cl]["cats"]
        total = len(cats)
        reachable_cats = 0
        for cat in cats:
            if cat in catdict:
                reachable_cats += 1
        langdict[cl]["SemanticallyRelevant"] = total - (reachable_cats*2)
        langdict[cl]["NumberOfCategories"] = total
    return langdict