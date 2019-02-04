import time
from nltk.parse.corenlp import CoreNLPDependencyParser
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError
from check.pos_pattern import pos_hypernyms
from stanford.custom_stanford_api import StanfordCoreNLP


def extract_nouns(first):
    try:
        if first is None:
            return ""
        time.sleep(0.1)
        output = StanfordCoreNLP(url='http://localhost:9000').annotate(first, properties={
            "annotators": "tokenize,ssplit,pos",
            "outputFormat": "json",
            # Only split the sentence at End Of Line. We assume that this method only takes in one single sentence.
            "ssplit.eolonly": "false",
            # Setting enforceRequirements to skip some annotators and make the process faster
            "enforceRequirements": "false"
        })
        nouns = [token['word'] for token in output['sentences'][0]['tokens'] if 'NN' in token['pos']]
        return ",".join(nouns)
    except JSONDecodeError:
        return ""
    except StopIteration:
        return ""
    except HTTPError:
        return ""


def extract_hypernyms(first):
    if first is None:
        return ""
    try:
        time.sleep(0.1)
        parses = CoreNLPDependencyParser(url='http://localhost:9000').parse_text(first)
        parse = next(parses, None)
        if parse is None:
            return ""
        pos, pattern = pos_hypernyms(parse)
        return ",".join(pos) + '; ' + pattern
    except JSONDecodeError:
        return ""
    except StopIteration:
        return ""
    except HTTPError:
        return ""