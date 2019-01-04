import requests
import time
from util.custom_stanford_api import StanfordCoreNLP, Exception500


class COPSemgrex():

    # processes the token dictionary for one sentence
    def __init__(self, text):
        self.semgrex_dict = {
            'Aisa': '{pos:/NN.*/}=hypernym >cop {pos:/VB.*/}=Verb >det {}=det >nsubj ({}=Subj >det {word:/A|An/}=det2)',
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
            time.sleep(5)
        cops = dict()
        for variant, semgrex in self.semgrex_dict.items():
            try:
                parser = StanfordCoreNLP(url='http://localhost:9000/semgrex/')
                responsedict = parser.annotate(text=self.text,
                                               annotators='tokenize, ssplit, pos, lemma, depparse',
                                               pattern=semgrex)
                cops[variant] = get_noun(responsedict)
            except Exception500:
                cops[variant] = []

        for hypernym in cops['isa']:
            if hypernym in cops['Aisa']:
                cops['isa'].remove(hypernym)
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
    sentence = "A programming language is a formal language."
    cop = COPSemgrex(sentence).run()
    print(cop)
