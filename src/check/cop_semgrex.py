import requests
import threading
from util.custom_stanford_api import StanfordCoreNLP, Exception500

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
        while not is_alive():
            print("Not alive")
            threading.sleep(50)
        cops = dict()
        for variant in VARIANT_IDS:
            try:
                parser = StanfordCoreNLP(url='http://localhost:9000/semgrex/')
                responsedict = parser.annotate(text=self.text,
                                               annotators='tokenize, ssplit, pos, lemma, depparse',
                                               pattern=self.semgrex_dict[variant])
                cops[variant] = get_noun(responsedict)
            except Exception500:
                cops[variant] = []

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
