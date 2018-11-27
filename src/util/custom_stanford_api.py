import requests
import json
from requests.sessions import Session


class StanfordCoreNLP:
    """
    Modified from https://github.com/smilli/py-corenlp
    """

    def __init__(self, url, session=Session()):
        if url[-1] == '/':
            url = url[:-1]
        self.server_url = url
        self.session = session

    def annotate(self, text, annotators="tokenize,ssplit,pos", pattern=None):
        assert isinstance(text, str)

        properties = {
            "annotators": annotators,
            # "outputFormat": "json",
            # Only split the sentence at End Of Line. We assume that this method only takes in one single sentence.
            # "ssplit.eolonly": "true",
            # Setting enforceRequirements to skip some annotators and make the process faster
            "enforceRequirements": "true"
        }
        params = dict()
        params['properties'] = str(properties)

        if pattern is not None:
            params['pattern'] = pattern.encode()

        try:
            with self.session.get(self.server_url) as req:
                data = text.encode()
                r = requests.post(
                    self.server_url, params=params, data=data, headers={'Connection': 'close'})
                output = r.text
                if ('outputFormat' in properties
                        and properties['outputFormat'] == 'json'):
                    output = json.loads(output, encoding='utf-8', strict=True)
        except requests.exceptions.ConnectionError:
            return self.annotate(text, properties)
        return output
