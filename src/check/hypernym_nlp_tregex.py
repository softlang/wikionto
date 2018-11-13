import requests


def get(tregex, text):
    url = "http://localhost:9000/tregex"
    request_params = {"pattern": tregex}
    r = requests.post(url, data=text, params=request_params)
    return r.json()['sentences'][0]


def pos_1a(text):
    tregex = "VBZ=is .. DT=title .. NN=language"
    resp = get(tregex, text)
    result = []
    for _, rdict in resp.items():
        nodes = {k: v for d in rdict['namedNodes'] for k, v in d.items()}
        if nodes['is'] == '(VBZ is)\r\n' \
                and ((nodes['title'] == '(DT title)\r\n') or (nodes['title'] == '(DT an)\r\n') or (nodes['title'] == '(DT the)\r\n')):
            result.append(nodes['language'].split('(')[1].split(')')[0].replace('NN', '').strip())
    return result, 'isalanguage'


def pos_1b(text):
    tregex = "VBD=was .. DT=title .. NN=language"
    resp = get(tregex, text)
    result = []
    for _, rdict in resp.items():
        nodes = {k: v for d in rdict['namedNodes'] for k, v in d.items()}
        if nodes['was'] == '(VBD was)\r\n' \
                and ((nodes['title'] == '(DT title)\r\n') or (nodes['title'] == '(DT an)\r\n') or (nodes['title'] == '(DT the)\r\n')):
            result.append(nodes['language'].split('(')[1].split(')')[0].replace('NN', '').strip())
    return result, 'wasalanguage'


def pos_2a(text):
    tregex = "VBZ=is .. DT=title .. NN=member . IN=of .. NNS=languages"
    resp = get(tregex, text)
    result = []
    for _, rdict in resp.items():
        nodes = {k: v for d in rdict['namedNodes'] for k, v in d.items()}
        if nodes['is'] == '(VBZ is)\r\n' \
                and ((nodes['title'] == '(DT title)\r\n') or (nodes['title'] == '(DT an)\r\n') or (nodes['title'] == '(DT the)\r\n')) \
                and (nodes['member'] == '(NN member)\r\n') \
                and (nodes['of'] == '(IN of)\r\n'):
            result.append(nodes['languages'].split('(')[1].split(')')[0].replace('NNS', '').strip())
    return result, 'isamemberoflanguages'


def pos_2b(text):
    tregex = "VBD=was .. DT=title .. NN=member . IN=of .. NNS=languages"
    resp = get(tregex, text)
    result = []
    for _, rdict in resp.items():
        nodes = {k: v for d in rdict['namedNodes'] for k, v in d.items()}
        if nodes['was'] == '(VBD was)\r\n' \
                and ((nodes['title'] == '(DT title)\r\n') or (nodes['title'] == '(DT an)\r\n') or (nodes['title'] == '(DT the)\r\n')) \
                and (nodes['member'] == '(NN member)\r\n') \
                and (nodes['of'] == '(IN of)\r\n'):
            result.append(nodes['languages'].split('(')[1].split(')')[0].replace('NNS', '').strip())
    return result, 'wasamemberoflanguages'


def pos_3(text):
    tregex = "VBZ=is .. CD=one . IN=of .. NNS=languages"
    resp = get(tregex, text)
    result = []
    for _, rdict in resp.items():
        nodes = {k: v for d in rdict['namedNodes'] for k, v in d.items()}
        if nodes['is'] == '(VBZ is)\r\n' \
                and (nodes['one'] == '(CD one)\r\n') \
                and (nodes['of'] == '(IN of)\r\n'):
            result.append(nodes['languages'].split('(')[1].split(')')[0].replace('NNS', '').strip())
    return result, 'isoneoflanguages'


def pos_4(text):
    tregex = "DT=The .+(NN | JJ) NN=language"
    r = get(tregex, text)


print(pos_1b("Java was title computer language."))
