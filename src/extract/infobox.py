def extract_properties(langdict):
    print("Checking Infobox properties")
    for cl in langdict:
        if "properties" not in langdict[cl]:
            continue
        for p in langdict[cl]["properties"]:
            langdict[cl]["infobox"+p] = 1
    return langdict
