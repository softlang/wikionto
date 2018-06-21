import requests
from json.decoder import JSONDecodeError
from json import dumps

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
    except JSONDecodeError:
        return None
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
    if wikijson is None:
        return None
    try:
        return dumps(wikijson)
    except KeyError:
        return None


def getlinks(title):
    params = {'prop':'links'
              , 'titles': title}
    wikijson = wiki_request(params)
    links = []
    while True:
        ls = next(iter(wikijson["query"]["pages"].values()))['links']
        for l in ls:
            links.append(l['title'])
        if 'continue' not in wikijson:
            break
        plcontinue = wikijson['continue']['plcontinue']
        params['plcontinue'] = plcontinue
        wikijson = wiki_request(params)
    return links


def get_infobox(pair):
    l = pair[0]
    rev = pair[1]
    text = getcontent(rev).lower()
    if '{{infobox' not in text:
        return l, rev, []
    parts = text.split('{{infobox')
    ibs = []
    for x in range(1, len(parts)):
        p = parts[x]
        name = p.split('|')[0].replace('\\n', '').strip()
        ibs.append(name)
    return l, rev, ibs


if __name__ == "__main__":
    c = getcontent("741790515")  # this is Java_(programming_language)
    print(c)
    print("Infobox software" in c)
