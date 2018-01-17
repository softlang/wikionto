

def check_gitseed(langdict):
    f = open('data/gitseed_annotated.csv','r',encoding="utf8")
    for line in f:
        seed_language = line.split(",")[0]
        langdict[seed_language]["GitSeed"] = True 
    return langdict