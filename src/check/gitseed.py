

def check_gitseed(langdict):
    f = open('data/gitseed_annotated.csv','r',encoding="utf8")
    for line in f:
        seed_language = line.split(",")[0]
        if seed_language in langdict:
            langdict[seed_language]["GitSeed"] = 1 
    return langdict