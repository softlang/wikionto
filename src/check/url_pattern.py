from data import KEYWORDS

def check_article_name(langdict):
    print("Checking article names")

    for cl in langdict:
        if any(kw in cl for kw in KEYWORDS):
            langdict[cl]["URLPattern"] = 1

        if '(' in cl:
            clbrack = cl.split('(')[1].split(')')[0]
            if any(kw in clbrack for kw in KEYWORDS):
                langdict[cl]["URLBracesPattern"] = 1

    return langdict


def solo():
    import json
    from data import DATAP
    with open(DATAP + '/langdict.json', 'r', encoding="UTF8") as f:
        langdict = json.load(f)
        langdict = check_article_name(langdict)
        f.close()
    with open(DATAP + '/langdict.json', 'w', encoding="UTF8") as f:
        json.dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()


if __name__ == "__main__":
    solo()
