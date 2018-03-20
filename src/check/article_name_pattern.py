def check_article_name(langdict):
    print("Checking article names")
    ex_pattern = ["List_of","comparison","Comparison"]
    in_pattern = ['format', 'language', 'dialect']
    for cl in langdict:
        matches = filter(lambda p: p in cl,ex_pattern)
        if matches:
            langdict[cl]["ExcludedNamePattern"] = 0
        else:
            langdict[cl]["ExcludedNamePattern"] = 1
        inmatches = filter(lambda p: p in cl, in_pattern)
        if inmatches:
            langdict[cl]["IncludedNamePattern"] = 0
        else:
            langdict[cl]["IncludedNamePattern"] = 1
    return langdict