import requests
from nltk.parse.corenlp import CoreNLPDependencyParser


class CustomParser(CoreNLPDependencyParser):

    def __init__(self, url='http://localhost:9000', session=requests.Session(), encoding='utf8', tagtype=None):
        self.url = url
        self.encoding = encoding

        if tagtype not in ['pos', 'ner', None]:
            raise ValueError("tagtype must be either 'pos', 'ner' or None")

        self.tagtype = tagtype

        self.session = session
