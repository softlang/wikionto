from mine.dbpedia import articles_with_property,CLURI,CFFURI

def check_infobox(langdict):
    print("Checking Infobox properties")
    propertylist = [
        "<http://dbpedia.org/property/dialects>",
        "<http://dbpedia.org/property/paradigm>",
        "<http://dbpedia.org/property/typing>",
        "^<http://dbpedia.org/ontology/language>",
        "^<http://dbpedia.org/property/language>",
        "^<http://dbpedia.org/ontology/programmingLanguage>"
        ]
    cls = set()
    for p in propertylist:
        cls = cls.union(articles_with_property(CLURI, 0, 6, p))
        cls = cls.union(articles_with_property(CFFURI, 0, 6, p))
    for cl in langdict:
        langdict[cl]["DbpediaInfobox"] = int(cl in cls)
    return langdict