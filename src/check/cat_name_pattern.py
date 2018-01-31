
def check_cat_name(catdict):
    ex_pattern = ["Data_types","lists_of","comparison","companies"]
    for cl in catdict:
        matches = filter(lambda p: p in cl,ex_pattern)
        if matches:
            catdict[cl]["IncludedNamePattern"] = 0
        else:
            catdict[cl]["IncludedNamePattern"] = 1
    return catdict