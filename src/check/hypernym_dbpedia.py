from mine.dbpedia import articles_with_hypernymContains,CLURI,CFFURI


def check_purlHypernymLanguage(langdict):
    print("Checking Dbpedia Hypernym")
    cls = articles_with_hypernymContains(CLURI, 0, 6, "Language") + articles_with_hypernymContains(CFFURI, 0, 6, "Language")
    cffs = articles_with_hypernymContains(CLURI,0,6,"Format") + articles_with_hypernymContains(CFFURI,0,6,"Format")
    for cl in langdict:
        langdict[cl]["DbpediaHypernymLanguage"] = cl in cls
        langdict[cl]["DbpediaHypernymFormat"] = cl in cffs
    return langdict