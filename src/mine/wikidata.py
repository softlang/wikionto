from SPARQLWrapper import SPARQLWrapper, JSON

WIKIDATA = "https://query.wikidata.org/sparql"


def get_computer_languages():
    sparql = SPARQLWrapper(WIKIDATA)
    sparql.setReturnFormat(JSON)

    query = "SELECT ?cl WHERE { ?cl wdt:P31/wdt:P279* wd:Q9143. }"
    sparql.setQuery(query)
    res = sparql.query().convert()
    cls = []
    size = len(res["results"]["bindings"])
    for r in res["results"]["bindings"]:
        cls.append(r["cl"]["value"])
    print(size)
    return cls


def get_computer_formats():
    sparql = SPARQLWrapper(WIKIDATA)
    sparql.setReturnFormat(JSON)

    query = "SELECT ?cl WHERE { ?cl wdt:P31/wdt:P279* wd:Q494823. }"
    sparql.setQuery(query)
    res = sparql.query().convert()
    cls = []
    size = len(res["results"]["bindings"])
    for r in res["results"]["bindings"]:
        cls.append(r["cl"]["value"])
    print(size)
    return cls
