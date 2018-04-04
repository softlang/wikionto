from SPARQLWrapper import SPARQLWrapper, JSON

def get_computer_languages():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    query = "SELECT ?cl WHERE { ?cl wdt:P31 ?t. ?t wdt:P279* wd:Q9143. }"
    sparql.setQuery(query)
    res = sparql.query().convert()
    cls = []
    size = len(res["results"]["bindings"])
    for r in res["results"]["bindings"]:
        cls.append(r["cl"]["value"])
    print(size)
    return cls

def get_computer_formats():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)

    query = "SELECT ?cl WHERE { ?cl wdt:P31 ?t. ?t wdt:P279* wd:Q494823. }"
    sparql.setQuery(query)
    res = sparql.query().convert()
    cls = []
    size = len(res["results"]["bindings"])
    for r in res["results"]["bindings"]:
        cls.append(r["cl"]["value"])
    print(size)
    return cls

