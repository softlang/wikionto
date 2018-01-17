from mine.dbpedia import articles_with_hypernymContains,CLURI,CFFURI


def check_purlHypernymLanguage(langdict):
    print("Checking Dbpedia Hypernym")
    articles = articles_with_hypernymContains(CLURI, 0, 7, "Language") + articles_with_hypernymContains(CFFURI, 0, 7, "Language")
    for a in articles:
        langdict[a]["DbpediaHypernym"]=True
    return langdict