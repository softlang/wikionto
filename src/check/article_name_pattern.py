def check_article_name(langdict):
    print("Checking article names")
    ex_pattern = ["List_of","comparison","Comparison"]
    ex_brack = ["song","video_game","TV_series"]
    in_pattern = ['format', 'language', 'dialect']

    for cl in langdict:
        matches = filter(lambda p: p in cl,ex_pattern)
        if matches:
            langdict[cl]["NamePattern"] = 0
        else:
            langdict[cl]["NamePattern"] = 1

        if '(' in cl:
            clbrack = cl.split('(')[1].split(')')[0]
            matches = filter(lambda p: p in clbrack, ex_brack)
            if matches:
                langdict[cl]["NamePattern"] = 0
            else:
                langdict[cl]["NamePattern"] = 1

        inmatches = filter(lambda p: p in cl, in_pattern)
        if inmatches:
            langdict[cl]["IncludedNamePattern"] = 0
        else:
            langdict[cl]["IncludedNamePattern"] = 1


    return langdict