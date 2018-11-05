import requests
import json
from socket import SOL_SOCKET, SO_REUSEADDR
from requests.sessions import Session


class StanfordCoreNLP:
    """
    Modified from https://github.com/smilli/py-corenlp
    """

    def __init__(self, server_url):
        if server_url[-1] == '/':
            server_url = server_url[:-1]
        self.server_url = server_url

    def annotate(self, text, properties=None):

        assert isinstance(text, str)
        if properties is None:
            properties = {}
        else:
            assert isinstance(properties, dict)

        # Checks that the Stanford CoreNLP server is started.

        s = Session()
        # s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        output = ""
        try:
            with requests.get(self.server_url) as req:
                data = text.encode()
                r = requests.post(
                    self.server_url, params={
                        'properties': str(properties)
                    }, data=data, headers={'Connection': 'close'})
                output = r.text
                if ('outputFormat' in properties
                        and properties['outputFormat'] == 'json'):
                    output = json.loads(output, encoding='utf-8', strict=True)
        except requests.exceptions.ConnectionError:
            return self.annotate(text, properties)
        return output


if __name__ == "__main__":
    nlp = StanfordCoreNLP('http://localhost:9000')
    summary = "Java is a language."
    output = nlp.annotate(summary, properties={
        "annotators": "tokenize,ssplit,pos",
        # "outputFormat": "json",
        # Only split the sentence at End Of Line. We assume that this method only takes in one single sentence.
        "ssplit.eolonly": "true",
        # Setting enforceRequirements to skip some annotators and make the process faster
        "enforceRequirements": "false"
    })
    # print(str(output['sentences'][0]['tokens'][0]['pos']))
    print(str(output))
