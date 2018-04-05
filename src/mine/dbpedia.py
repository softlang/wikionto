from SPARQLWrapper import SPARQLWrapper, JSON
from argparse import ArgumentError
from collections import defaultdict
from time import sleep
from urllib.error import HTTPError

CLURI = "<http://dbpedia.org/resource/Category:Computer_languages>"
CFFURI = "<http://dbpedia.org/resource/Category:Computer_file_formats>"
DBPEDIA = "http://dbpedia.org/sparql"
DBPEDIALIVE = "http://dbpedia-live.openlinksw.com/sparql"


def query(query, url=DBPEDIA, use_offset=True):
    if use_offset and ("?offset" not in query):
        raise ArgumentError("Work with offset as dbpedia returns a limited amount of results.")
    sparql = SPARQLWrapper(url)
    sparql.setReturnFormat(JSON)
    offset = 0
    results = []
    while True:
        fquery = query
        if use_offset:
            fquery = fquery.replace("?offset", str(offset))
        sparql.setQuery(fquery)
        while True:
            try:
                res = sparql.query()
                break
            except HTTPError:
                print("    HTTP error! Sleeping 5 secs...")
                sleep(15)
        qres = res.convert()
        size = len(qres["results"]["bindings"])
        results = results + qres["results"]["bindings"]
        if size == 10000:
            offset += 10000
        if (size != 10000) or (not use_offset):
            break
    return results


def articles_below(root, mindepth, maxdepth):
    articles = []
    querytext = """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?article where { 
    SELECT DISTINCT ?article where {
        ?article dct:subject/skos:broader{?mindepth,?maxdepth} ?root.
    }
    ORDER BY ASC(?article)
}
limit 10000
offset ?offset
    """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(querytext)
    for result in results:
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        articles.append(article)
    return articles


def articles_with_property(root, mindepth, maxdepth, propertyname):
    articles = set()
    querytext = """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?article where { 
    SELECT DISTINCT ?article where {
        ?root ^skos:broader{?mindepth,?maxdepth}/^dct:subject ?article.
        FILTER EXISTS{ ?article ?property ?target. }
    }
    ORDER BY ASC(?article)
}
limit 10000
offset ?offset
    """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth)).replace(
        "?property", propertyname)
    results = query(querytext)
    for result in results:
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        articles.add(article)
    return articles

def articles_with_commons(root, mindepth, maxdepth):
    querytext = """
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT ?article ?c where { 
        SELECT DISTINCT ?article where {
            ?root ^skos:broader{?mindepth,?maxdepth}/^dct:subject ?article.
            ?article <http://dbpedia.org/property/commons> ?c.
        }
        ORDER BY ASC(?article)
    }
    limit 10000
    offset ?offset
        """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(querytext)
    acdict = dict()
    for result in results:
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        commons = result["article"]["value"].replace("Category:","")
        if article in acdict:
            acdict[article].append(commons)
        else:
            acdict[article] = [commons]
    return acdict

def get_properties(root, mindepth, maxdepth, langdict):
    sparql = SPARQLWrapper(DBPEDIA)
    sparql.setReturnFormat(JSON)
    offset = 0
    querytext = """
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT DISTINCT ?article ?property where { 
        SELECT DISTINCT ?article ?property WHERE{ 
            ?root ^skos:broader{?mindepth,?maxdepth}/^dct:subject ?article.
            FILTER(regex(str(?property),"dbpedia.org/property","i"))
            ?article ?property ?o .
        }
        GROUP BY ?property
        ORDER BY ASC(?property)
    }
    limit 10000
    offset ?offset
        """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    oldpropname = ""
    while True:
        fquery = querytext
        fquery = fquery.replace("?offset", str(offset))
        sparql.setQuery(fquery)
        while True:
            try:
                res = sparql.query()
                break
            except HTTPError:
                print("    HTTP error! Sleeping 5 secs...")
                sleep(15)
        qres = res.convert()

        size = len(qres["results"]["bindings"])

        for result in qres["results"]["bindings"]:
            article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
            propname = result["property"]["value"].replace("http://dbpedia.org/property/", "")
            if oldpropname != propname:
                oldpropname = propname
            if "properties" in langdict[article]:
                langdict[article]["properties"].append(propname)
            else:
                langdict[article]["properties"] = [propname]
        if size == 10000:
            offset += 10000
        if size != 10000:
            break
    return langdict


def properties_in(root, mindepth, maxdepth):
    queryText = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT ?prop, (COUNT(?article) as ?count) where { 
        SELECT DISTINCT ?article ?prop where {
            ?root ^skos:broader{?mindepth,?maxdepth}/^dct:subject ?article.

            FILTER(regex(str(?prop),"http://dbpedia.org/property","i"))
            ?article ?prop ?object .   
        }
        GROUP BY ?prop
    }
    GROUP BY ?prop
    HAVING(COUNT(?article) > 50)
    ORDER BY DESC(?count)
        """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(queryText, use_offset=False)
    propdict = dict()
    for result in results:
        propname = result["prop"]["value"].replace("http://dbpedia.org/property/", "")
        in_count = int(result["count"]["value"])
        propdict[propname] = dict()
        propdict[propname]["in_count"] = in_count
    return propdict


def reverse_properties_in(root, mindepth, maxdepth):
    queryText = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT ?prop, (COUNT(?article) as ?count) where { 
        SELECT DISTINCT ?article ?prop where {
            ?root ^skos:broader{?mindepth,?maxdepth}/^dct:subject ?article.

            FILTER(regex(str(?prop),"http://dbpedia.org/property","i"))
            ?o ?prop ?article .   
        }
        GROUP BY ?prop
    }
    GROUP BY ?prop
    HAVING(COUNT(?article) > 50)
    ORDER BY DESC(?count)
        """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(queryText, use_offset=False)
    propdict = dict()
    for result in results:
        propname = result["prop"]["value"].replace("http://dbpedia.org/property/", "")
        in_count = int(result["count"]["value"])
        propdict[propname] = dict()
        propdict[propname]["in_count"] = in_count
    return propdict


def articles_out_with(propname, mindepthcl, maxdepthcl, mindepthcff, maxdepthcff):
    prop_out_query = """
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT DISTINCT ?article where {
        ?article ?property ?object . 
        FILTER NOT EXISTS {
            ?article dct:subject/skos:broader{?mindepthcl,?maxdepthcl} <http://dbpedia.org/resource/Category:Computer_languages>.
        }
        FILTER NOT EXISTS {
            ?article dct:subject/skos:broader{?mindepth,?maxdepth} <http://dbpedia.org/resource/Category:Computer_file_formats>.
        }  
    }
    LIMIT 10000
    """.replace("?property", '<http://dbpedia.org/property/' + propname + '>')\
        .replace("?mindepthcl",str(mindepthcl)).replace("?maxdepthcl", str(maxdepthcl))\
        .replace("?mindepthcff", str(mindepthcff)).replace("?maxdepthcff", str(maxdepthcff))
    return len(query(query=prop_out_query, use_offset=False))


def articles_out_with_reverse(propname, mindepthcl, maxdepthcl, mindepthcff, maxdepthcff):
    prop_out_query = """
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT DISTINCT ?article where {
        FILTER(regex(str(?article),"dbpedia.org/resource","i"))
        ?object ?property ?article . 
        FILTER NOT EXISTS {
            ?article dct:subject/skos:broader{?mindepthcl,?maxdepthcl} <http://dbpedia.org/resource/Category:Computer_languages>.
        }
        FILTER NOT EXISTS {
            ?article dct:subject/skos:broader{?mindepthcff,?maxdepthcff} <http://dbpedia.org/resource/Category:Computer_file_formats>.
        }  
    }
    LIMIT 10000
    """.replace("?property", '<http://dbpedia.org/property/' + propname + '>')\
        .replace("?mindepthcl",str(mindepthcl)).replace("?maxdepthcl", str(maxdepthcl))\
        .replace("?mindepthcff", str(mindepthcff)).replace("?maxdepthcff", str(maxdepthcff))
    return len(query(query=prop_out_query, use_offset=False))


def articles_with_redirects(root, mindepth, maxdepth):
    querytext = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/resource/>
PREFIX dct: <http://purl.org/dc/terms/>
SELECT ?article ?redirect where { 
    SELECT DISTINCT ?article ?redirect where {
        ?root ^skos:broader{?mindepth,?maxdepth}/^dct:subject ?article.
        ?redirect dbo:wikiPageRedirects ?article .
    }
    ORDER BY ASC(?article)
}
limit 10000
offset ?offset
    """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    return query(querytext)


# Only dbpedia.org holds the hypernym relation
def articles_with_hypernym(root, mindepth, maxdepth, hypernym):
    articles = []
    querytext = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/resource/>
PREFIX dct: <http://purl.org/dc/terms/>
SELECT ?article where { 
    SELECT DISTINCT ?article where {
        ?root ^skos:broader{?mindepth,?maxdepth}/^dct:subject ?article.
        FILTER(regex(str(?hyp),"?hypernym","i"))
        ?article <http://purl.org/linguistics/gold/hypernym> ?hyp .
    }
    ORDER BY ASC(?article)
}
limit 10000
offset ?offset
    """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth)).replace(
        "?hypernym", hypernym)
    results = query(querytext, url=DBPEDIA)
    for result in results:
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        articles.append(article)
    return articles


def articles_with_summaries(root, mindepth, maxdepth):
    querytext = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/resource/>
PREFIX dct: <http://purl.org/dc/terms/>
SELECT ?article ?summary where { 
    SELECT DISTINCT ?article ?summary where {
        ?article dct:subject/skos:broader{?mindepth,?maxdepth} ?root .
        ?article dbo:abstract ?summary .
    }
    ORDER BY ASC(?article)
}
limit 10000
offset ?offset
    """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    articles = dict()
    for result in query(querytext):
        if result["summary"]["xml:lang"] == "en":
            article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
            summary = result["summary"]["value"]
            result = ""
            lvl = 0
            for c in summary:
                if c == '(':
                    lvl += 1
                    continue
                if c == ')':
                    lvl -= 1
                    continue
                if lvl == 0:
                    result += c
            summary = result.strip()
            articles[article] = summary
    return articles


def articles_with_revisions(root, mindepth, maxdepth):
    querytext = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/resource/>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT ?article ?rev where { 
        SELECT DISTINCT ?article ?rev where {
            ?article dct:subject/skos:broader{?mindepth,?maxdepth} ?root .
            ?article <http://www.w3.org/ns/prov#wasDerivedFrom> ?rev .
        }
        ORDER BY ASC(?article)
    }
    limit 10000
    offset ?offset
        """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    articles = dict()
    for result in query(querytext):
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        rev = result["rev"]["value"]
        articles[article] = rev
    return articles


def articles_with_wikidataid(root, mindepth, maxdepth):
    querytext = """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/resource/>
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT ?article ?qid where { 
            SELECT DISTINCT ?article ?qid where {
                ?article dct:subject/skos:broader{?mindepth,?maxdepth} ?root .
                FILTER(regex(str(?qid),"wikidata","i"))
                ?article <http://www.w3.org/2002/07/owl#sameAs> ?qid .
            }
            ORDER BY ASC(?article)
        }
        limit 10000
        offset ?offset
            """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    articles = dict()
    for result in query(querytext):
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        qid = result["qid"]["value"]
        articles[article] = qid
    return articles

def category_to_subcategory_below(root, mindepth, maxdepth):
    cat_subcat = defaultdict(dict)
    querytext = """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?cat ?subcat where { 
    SELECT DISTINCT ?cat ?subcat where {
        ?cat skos:broader{?mindepth,?maxdepth} ?root.
        ?subcat skos:broader ?cat.
    }
    ORDER BY ASC(?cat)
}
limit 10000
offset ?offset
    """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(querytext)
    for result in results:
        cat = result["cat"]["value"].replace("http://dbpedia.org/resource/Category:", "")
        subcat = result["subcat"]["value"].replace("http://dbpedia.org/resource/Category:", "")
        if cat not in cat_subcat:
            cat_subcat[cat]["subcats"] = []
        cat_subcat[cat]["subcats"].append(subcat)
    return cat_subcat


def category_to_articles_below(root, mindepth, maxdepth):
    cat_articles = defaultdict(dict)
    querytext = """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?cat ?article where { 
    SELECT DISTINCT ?cat ?article where {
        ?cat skos:broader{?mindepth,?maxdepth} ?root.
        ?article dct:subject ?cat.
    }
    ORDER BY ASC(?cat)
}
limit 10000
offset ?offset
    """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(querytext)
    for result in results:
        cat = result["cat"]["value"].replace("http://dbpedia.org/resource/Category:", "")
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        if cat not in cat_articles:
            cat_articles[cat]["articles"] = []
        cat_articles[cat]["articles"].append(article)
    return cat_articles


def articles_to_categories_below(root, mindepth, maxdepth):
    article_cats = defaultdict(dict)
    querytext = """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT DISTINCT ?article ?cat where { 
    SELECT DISTINCT ?article ?cat where {
        ?article dct:subject/skos:broader{?mindepth,?maxdepth} ?root.
        ?article dct:subject ?cat.
    }
    ORDER BY ASC(?article)
}
limit 10000
offset ?offset
    """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(querytext)
    for result in results:
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        cat = result["cat"]["value"].replace("http://dbpedia.org/resource/Category:", "")
        if article not in article_cats:
            article_cats[article]["cats"] = []
        article_cats[article]["cats"].append(cat)
    return article_cats
