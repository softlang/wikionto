from mine.dbpedia import articles_semantic_distant,CLURI,CFFURI

def check_semantic_distance(langdict):
    print("Checking semantic distance")
    clsdistant = articles_semantic_distant(CLURI, 0, 6)
    cffsdistant = articles_semantic_distant(CFFURI, 0, 6)
    for cl in clsdistant + cffsdistant:
        langdict[cl]["SemanticallyDistant"] = True
    return langdict