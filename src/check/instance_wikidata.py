from mine.wikidata import get_computer_languages, get_computer_formats


def check_instance_of_wikidata(langdict):
    print("Checking instance of 'Computer languages' and 'data formats' in Wikidata")
    cls = get_computer_languages()
    cffs = get_computer_formats()
    for cl in langdict:
        qitem = langdict[cl]["wikidataid"]
        langdict[cl]["wikidata_CL"] = int(qitem in set(cls) | set(cffs))
    return langdict
