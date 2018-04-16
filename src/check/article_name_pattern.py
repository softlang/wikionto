def check_article_name(langdict):
    print("Checking article names")
    ex_pattern = ["List_of","comparison","Comparison"]
    ex_brack = ["song","video_game","TV_series"]
    in_pattern = ['format', 'language']

    for cl in langdict:
        matches = bool(list(filter(lambda p: p in cl,ex_pattern)))
        if matches:
            langdict[cl]["NamePattern"] = 0
        else:
            langdict[cl]["NamePattern"] = 1

        if '(' in cl:
            clbrack = cl.split('(')[1].split(')')[0]
            matches = bool(list((filter(lambda p: p in clbrack, ex_brack))))
            if matches:
                langdict[cl]["NamePattern"] = 0
            else:
                langdict[cl]["NamePattern"] = 1

        inmatches = bool(list(filter(lambda p: p in cl, in_pattern)))
        if inmatches:
            langdict[cl]["IncludedNamePattern"] = 1
        else:
            langdict[cl]["IncludedNamePattern"] = 0

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
