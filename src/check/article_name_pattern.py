
def check_article_name(langdict):
    print("Checking article names")
    ex_pattern = ["list_of","comparison"]
    for cl in langdict:
        matches = filter(lambda p: p in cl,ex_pattern)
        if matches:
            langdict[cl]["IncludedNamePattern"] = 0
        else:
            langdict[cl]["IncludedNamePattern"] = 1
    return langdict