from SPARQLWrapper import SPARQLWrapper, JSON
from argparse import ArgumentError
from collections import defaultdict
from time import sleep
from urllib.error import HTTPError, URLError

URI = "<http://dbpedia.org/resource/"

DBPEDIA = "http://dbpedia.org/sparql"
DBPEDIALIVE = "http://dbpedia-live.openlinksw.com/sparql"


def to_uri(name):
    return URI + name + ">"


def query(qtext, url=DBPEDIALIVE, use_offset=True):
    if use_offset and ("?offset" not in qtext):
        raise ArgumentError("Work with offset as dbpedia returns a limited amount of results.")
    sparql = SPARQLWrapper(url)
    sparql.setReturnFormat(JSON)
    offset = 0
    results = []
    while True:
        fquery = qtext
        if use_offset:
            fquery = fquery.replace("?offset", str(offset))
        sparql.setQuery(fquery)
        while True:
            try:
                res = sparql.query()
                break
            except URLError:
                print("    URL error! Sleeping ...")
                print(qtext)
                sleep(15)
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
        commons = result["article"]["value"]
        if article in acdict:
            acdict[article].append(commons)
        else:
            acdict[article] = [commons]
    return acdict


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
def articles_with_NonLiveHypernyms(root, mindepth, maxdepth):
    querytext = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/resource/>
PREFIX dct: <http://purl.org/dc/terms/>
SELECT ?article ?hyp where { 
    SELECT DISTINCT ?article ?hyp where {
        ?root ^skos:broader{?mindepth,?maxdepth}/^dct:subject ?article.
        ?article <http://purl.org/linguistics/gold/hypernym> ?hyp .
    }
    ORDER BY ASC(?article)
}
limit 10000
offset ?offset
    """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(querytext, url=DBPEDIA)
    d = dict()
    for result in results:
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        hyp = result["hyp"]["value"].replace("http://dbpedia.org/resource/", "")
        if article not in d:
            d[article] = []
        d[article].append(hyp)
    return d


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


def get_templates(root, mindepth, maxdepth):
    querytext = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/resource/>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT ?article ?t where { 
      SELECT ?article ?t where {
        ?article dct:subject/skos:broader{?mindepth,?maxdepth} ?root .
        ?article <http://dbpedia.org/property/wikiPageUsesTemplate> ?t .
        FILTER(regex(str(?t),"Infobox","i"))
      }
      ORDER BY ASC(?article)
    }
    limit 10000
    offset ?offset
        """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    td = dict()
    for result in query(querytext):
        t = result["t"]["value"].replace("http://dbpedia.org/resource/Template:", "").lower()
        cl = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        if cl not in td:
            td[cl] = []
        td[cl].append(t)
    return td


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


def articles_with_revisions_live(root, mindepth, maxdepth):
    querytext = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/resource/>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT ?article ?rev where { 
        SELECT DISTINCT ?article (max(?revn) as ?rev) where {
            ?article dct:subject/skos:broader{?mindepth,?maxdepth} ?root.
            ?article <http://dbpedia.org/ontology/wikiPageRevisionID> ?revn .
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
    cat_subcat = dict()
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
        cat = result["cat"]["value"].replace("http://dbpedia.org/resource/", "")
        subcat = result["subcat"]["value"].replace("http://dbpedia.org/resource/", "")
        if cat not in cat_subcat:
            cat_subcat[cat] = []
        cat_subcat[cat].append(subcat)
    return cat_subcat


def category_to_supercategory_below(root, mindepth, maxdepth):
    cat_subcat = dict()
    querytext = """
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?cat ?supercat where { 
    SELECT DISTINCT ?cat ?supercat where {
        ?cat skos:broader{?mindepth,?maxdepth} ?root.
        ?supercat ^skos:broader ?cat.
    }
    ORDER BY ASC(?cat)
}
limit 10000
offset ?offset
    """.replace("?root", root).replace("?mindepth", str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(querytext)
    for result in results:
        cat = result["cat"]["value"].replace("http://dbpedia.org/resource/", "")
        supercat = result["supercat"]["value"].replace("http://dbpedia.org/resource/", "")
        if cat not in cat_subcat:
            cat_subcat[cat] = []
        cat_subcat[cat].append(supercat)
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
        cat = result["cat"]["value"].replace("http://dbpedia.org/resource/", "")
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
        cat = result["cat"]["value"].replace("http://dbpedia.org/resource/", "")
        if article not in article_cats:
            article_cats[article] = []
        article_cats[article].append(cat)
    return article_cats
