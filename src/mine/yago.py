from SPARQLWrapper import SPARQLWrapper, JSON

YAGO = "http://lod2.openlinksw.com/sparql"


def get_artificial_languages():
    sparql = SPARQLWrapper(YAGO)
    sparql.setReturnFormat(JSON)

    query = """
SELECT ?s WHERE {
    SELECT DISTINCT ?s WHERE{
        ?s a ?t. 
        ?t <http://lod.openlinksw.com/describe/?url=http%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23subClassOf>* <http://dbpedia.org/class/yago/ArtificialLanguage106894544>.
    }
    ORDER BY ?s
} 
limit 10000
"""
    sparql.setQuery(query)
    res = sparql.query().convert()
    cls = []
    size = len(res["results"]["bindings"])
    for r in res["results"]["bindings"]:
        cls.append(r["s"]["value"].replace("http://dbpedia.org/resource/", ""))
    print(size)
    return cls


# - Yago
def yago_articles():
    return set(get_artificial_languages())
