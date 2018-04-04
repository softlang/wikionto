import requests

URL = "http://en.wikipedia.org/w/api.php"
HEADER = {'User-Agent': 'WikiOnto'}


def wiki_request(params):
    params['format'] = 'json'
    params['action'] = 'query'
    params['utf8'] = ''
    try:
        r = requests.get(URL, params=params, headers=HEADER).json()
    except requests.ConnectionError:
        print("Connection Error")
        r = wiki_request(params)
    return r


def getfirstsentence(name):
    params = {'prop': 'extracts'
        , 'exintro': ''
        , 'exsentences': '1'
        , 'titles': name
        , 'redirects': '1'}
    wikijson = wiki_request(params)
    sentence = next(iter(wikijson["query"]["pages"].values()))["extract"]
    return sentence


def getsubcats(title):
    params = {'cmlimit': '500'
        , 'list': 'categorymembers'
        , 'cmtype': 'subcat'
        , 'cmtitle': title
        , 'redirects': '1'}
    wikijson = wiki_request(params)
    members = wikijson["query"]["categorymembers"]
    subcats = list(map(lambda d: d["title"].replace(" ", "_"), members))

    return subcats


def getarticles(title):
    params = {'cmlimit': '500'
        , 'list': 'categorymembers'
        , 'cmtype': 'page'
        , 'cmtitle': title
        , 'redirects': '1'}
    wikijson = wiki_request(params)
    members = wikijson["query"]["categorymembers"]
    articles = list(map(lambda d: d["title"].replace(" ", "_"), members))
    return articles


def getcategories(title):
    params = {'prop': 'categories'
        , 'titles': title
        , 'redirects': '1'}
    wikijson = wiki_request(params)
    members = next(iter(wikijson["query"]["pages"].values()))["categories"]
    categories = list(map(lambda d: d["title"].replace(" ", "_"), members))
    return categories


def getcontent(revid):
    params = {'prop': 'revisions'
        , 'rvprop': 'content'
        , 'revids': revid}
    wikijson = wiki_request(params)
    try:
        return next(iter(wikijson["query"]["pages"].values()))["revisions"][0]['*']
    except KeyError:
        return None


if __name__ == "__main__":
    c = getcontent("743173085")  # this is Java_(programming_language)
    print(c)
