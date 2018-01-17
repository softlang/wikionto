import requests
URL = "http://en.wikipedia.org/w/api.php"
HEADER = {'User-Agent':'WikiOnto'}

def wiki_request(params):
    params['format']='json'
    params['action']='query'
    params['utf8']=''
    params['redirects']='1'
    try:
        r = requests.get(URL,params=params,headers=HEADER).json()
    except requests.ConnectionError:
        print("Connection Error")
        r = wiki_request(params)
    return r

def getfirstsentence(name):
    params = {'prop':'extracts'
              ,'exintro':''
              ,'exsentences':'1'
              ,'titles':name}
    wikijson = wiki_request(params)
    sentence = next(iter(wikijson["query"]["pages"].values()))["extract"]
    return sentence

def getsubcats(title):
    params = {'cmlimit':'500'
              ,'list':'categorymembers'
              ,'cmtype':'subcat'
              ,'cmtitle':title}
    wikijson = wiki_request(params)
    members = wikijson["query"]["categorymembers"]
    subcats = list(map(lambda d: d["title"].replace(" ","_"), members))
    
    return subcats


def getarticles(title):
    params = {'cmlimit':'500'
              ,'list':'categorymembers'
              ,'cmtype':'page'
              ,'cmtitle':title}
    wikijson = wiki_request(params)
    members = wikijson["query"]["categorymembers"]
    articles = list(map(lambda d: d["title"].replace(" ","_"), members))
    return articles

def getcategories(title):
    params = {'prop':'categories'
              ,'titles':title}
    wikijson = wiki_request(params)
    members = next(iter(wikijson["query"]["pages"].values()))["categories"]
    categories = list(map(lambda d: d["title"].replace(" ","_"), members))
    return categories
