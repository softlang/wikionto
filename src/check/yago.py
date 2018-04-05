from mine.yago import get_artificial_languages
from data import DATAP


def check_instance_of_yago(langdict):
    print("Checking instance of 'Artificial language' in yago")
    als = get_artificial_languages()
    for cl in langdict:
        langdict[cl]["yago_CL"] = int(cl in als)
    return langdict


def solo():
    import json
    with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
        langdict = json.load(f)
        langdict = check_instance_of_yago(langdict)
        f.close()
    with open(DATAP + '/langdict.json', 'w', encoding="UTF8") as f:
        json.dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()


if __name__ == "__main__":
    solo()
