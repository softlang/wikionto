from mine.yago import get_artificial_languages
from data import DATAP


def extract_instance_of_yago(langdict):
    print("Checking instance of 'Artificial language' in yago")
    als = get_artificial_languages()
    for cl in langdict:
        langdict[cl]["yago_CL"] = int(cl in als)
    return langdict
