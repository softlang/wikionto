import requests
import json
from requests.sessions import Session


class StanfordCoreNLP:
    """
    Modified from https://github.com/smilli/py-corenlp
    """

    def __init__(self, url, session=Session()):
        self.server_url = url
        self.session = session

    def annotate(self, text, annotators="tokenize,ssplit,pos", pattern=None):
        assert isinstance(text, str)

        properties = {
            "annotators": annotators,
            # Setting enforceRequirements to skip some annotators and make the process faster
            "enforceRequirements": "false",
            #'timeout': 6000000,
            'tokenize.options': 'untokenizable=allDelete'
        }
        params = dict()
        params['properties'] = str(properties)

        if pattern is not None:
            params['pattern'] = pattern

        try:
            with self.session.get(self.server_url) as req:
                data = text.encode('utf-8')
                r = requests.post(
                    self.server_url, params=params, data=data, headers={'Connection': 'close'})
                if r.status_code == 500:
                    print(r.content)
                    raise Exception500
                output = r.json()
                # output = json.loads(r.text, encoding='utf-8', strict=True)

        except requests.exceptions.ConnectionError:
            return self.annotate(text, properties)
        return output


class Exception500(Exception):
    pass
