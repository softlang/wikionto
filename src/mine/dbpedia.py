from SPARQLWrapper import SPARQLWrapper, JSON
from argparse import ArgumentError
from collections import defaultdict

CLURI = "<http://dbpedia.org/resource/Category:Computer_languages>"
CFFURI = "<http://dbpedia.org/resource/Category:Computer_file_formats>"

def query(query):
    if not "?offset" in query:
        raise ArgumentError("Work with offset as dbpedia returns a limited amount of results.")
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    offset = 0
    results = []
    while True:
        newquery = query.replace("?offset",str(offset))
        sparql.setQuery(newquery)
        qres = sparql.query().convert()
        size = len(qres["results"]["bindings"])
        results = results + qres["results"]["bindings"]
        if size==10000:
            offset += 10000
        else:
            break
    return results

def articles_below(root,mindepth,maxdepth):
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
    """.replace("?root", root).replace("?mindepth",str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(querytext)
    for result in results:
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        articles.append(article)
    return articles

def articles_with_property(root,mindepth,maxdepth,propertyname):
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
    """.replace("?root", root).replace("?mindepth",str(mindepth)).replace("?maxdepth", str(maxdepth)).replace("?property",propertyname)
    results = query(querytext)
    for result in results:
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        articles.add(article)
    return articles

def articles_with_redirects(root,mindepth,maxdepth):
    querytext="""
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
    """.replace("?root", root).replace("?mindepth",str(mindepth)).replace("?maxdepth", str(maxdepth))
    return query(querytext)

def articles_with_hypernymContains(root,mindepth,maxdepth,hypernym):
    articles = []
    querytext="""
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
    """.replace("?root", root).replace("?mindepth",str(mindepth)).replace("?maxdepth", str(maxdepth)).replace("?hypernym",hypernym)
    results = query(querytext)
    for result in results:
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        articles.append(article)
    return articles

def articles_with_summaries(root,mindepth,maxdepth):
    querytext="""
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
    """.replace("?root", root).replace("?mindepth",str(mindepth)).replace("?maxdepth", str(maxdepth))
    articles = dict()
    for result in query(querytext):
        if result["summary"]["xml:lang"] == "en":
            article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
            summary = result["summary"]["value"].split(". ")[0]+"."
            articles[article]=summary
    return articles

def articles_semantic_distant(root, mindepth,maxdepth):
    querytext="""
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT DISTINCT ?article ?howManyReachable ?howManyTotal WHERE { 
  SELECT DISTINCT ?article (COUNT(?rcat) as ?howManyReachable) (COUNT(?cat) as ?howManyTotal) WHERE {
    FILTER EXISTS{
        ?article dct:subject/skos:broader{?mindepth,?maxdepth} ?root.
    }
    
    {SELECT DISTINCT ?article ?rcat
     WHERE {
      ?article dct:subject ?rcat .
      FILTER EXISTS{
        ?rcat skos:broader{?mindepth,?maxdepth}  ?root.
      }
     }
    }
    UNION
    {SELECT DISTINCT ?article ?cat
     WHERE {
       ?article dct:subject ?cat .
     }
    }
  }
  GROUP BY ?article
  ORDER BY ASC(?article)
}
GROUP BY ?article
LIMIT 10000
OFFSET ?offset
    """.replace("?root", root).replace("?mindepth",str(mindepth)).replace("?maxdepth", str(maxdepth))
    articles = []
    for result in query(querytext):
        how_many_total = int(result["howManyTotal"]["value"])
        how_many_reachable = int(result["howManyReachable"]["value"])
        how_many_distant = how_many_total - how_many_reachable
        if (how_many_distant > how_many_reachable) & (how_many_total > 0):
            articles.append(result["article"]["value"].replace("http://dbpedia.org/resource/", ""))
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
    """.replace("?root", root).replace("?mindepth",str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(querytext)
    for result in results:
        cat = result["cat"]["value"].replace("http://dbpedia.org/resource/Category:", "")
        subcat = result["subcat"]["value"].replace("http://dbpedia.org/resource/Category:", "")
        if cat not in cat_subcat:
            cat_subcat[cat]["subcats"]=[]
        cat_subcat[cat]["subcats"].append(subcat)
    return cat_subcat

def category_to_articles_below(root,mindepth,maxdepth):
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
    """.replace("?root", root).replace("?mindepth",str(mindepth)).replace("?maxdepth", str(maxdepth))
    results = query(querytext)
    for result in results:
        cat = result["cat"]["value"].replace("http://dbpedia.org/resource/Category:", "")
        article = result["article"]["value"].replace("http://dbpedia.org/resource/", "")
        if cat not in cat_articles:
            cat_articles[cat]["articles"]=[]
        cat_articles[cat]["articles"].append(article)
    return cat_articles