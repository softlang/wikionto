import requests
import threading
VARIANT_IDS = ['The', 'isa', 'isoneof', 'isnameof', 'ismemberof', 'isfamilyof']


class COPSemgrex():

    # processes the token dictionary for one sentence
    def __init__(self, text):
        self.semgrex_dict = {
            'The': '{pos:/NN.*/}=hypernym >det {word:The}',
            'isa': '{pos:/NN.*/}=hypernym >cop {pos:/VB.*/}=Verb >det {}=det',
            'isoneof': '{pos:CD;word:one}=one >cop {pos:/VB.*/}=Verb >=rel {pos:/NN.*/}=hypernym',
            'isnameof': '{pos:NN;word:name}=name >cop {pos:/VB.*/}=Verb >=rel {pos:/NN.*/}=hypernym',
            'ismemberof': '{pos:NN;word:member}=name >>/nmod:of/ {pos:NNS}=hypernym',
            'isfamilyof': '{pos:NN;word:family} >cop {pos:/VB.*/} >/nmod:of/ {pos:NNS}=hypernym'
        }
        self.text = text

    def run(self):
        url = "http://localhost:9000/semgrex/"
        while not is_alive():
            print("Not alive")
            threading.sleep(50)
        cops = dict()
        for variant in VARIANT_IDS:
            properties = {'timeout': 6000000,
                          "enforceRequirements": "true",
                          'annotators': 'tokenize, ssplit, pos, lemma, depparse'}
            request_params = {"pattern": self.semgrex_dict[variant], 'properties': str(properties)}
            r = requests.post(url, data=self.text.encode(), params=request_params, headers={'Connection': 'close'})
            if r.status_code == 500:
                print(r.content)
                cops[variant] = []
            cops[variant] = get_noun(r.json())
        return cops


def get_noun(responsedict):
    if not responsedict:
        return []
    else:
        cops = []
        for sentence_result in responsedict['sentences']:
            for x in range(sentence_result['length']):
                cops.append(sentence_result[str(x)]['$hypernym']['text'])
        return cops


def is_alive():
    try:
        return requests.get("http://localhost:9000/ping").ok
    except requests.exceptions.ConnectionError:
        return False


if __name__ == '__main__':
    sentence = "Perl 6 is a member of the Perl family of programming languages."
    cop = COPSemgrex(sentence).run()
    print(cop)
