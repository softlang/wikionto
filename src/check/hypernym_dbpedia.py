from mine.dbpedia import articles_with_hypernymContains,CLURI,CFFURI

# always 0 as live.dbpedia.org doesn't contain the relationship
def check_purlHypernymLanguage(langdict):
    print("Checking Dbpedia Hypernym")
    cls = articles_with_hypernymContains(CLURI, 0, 6, "Language") + articles_with_hypernymContains(CFFURI, 0, 6, "Language")
    cffs = articles_with_hypernymContains(CLURI,0,6,"Format") + articles_with_hypernymContains(CFFURI,0,6,"Format")
    for cl in langdict:
        if (cl in cls) or (cl in cffs):
            langdict[cl]["DbpediaHypernym"] = 1
        else:
            langdict[cl]["DbpediaHypernym"] = 0
    return langdict

if __name__ == '__main__':
    import json
    with open('../data/langdict.json', 'r',encoding="UTF8") as f: 
        langdict = json.load(f)
        langdict = check_purlHypernymLanguage(langdict)
        f.close()
    with open('../data/langdict.json', 'w',encoding="UTF8") as f:
        json.dump(obj=langdict, fp=f, indent=2)
        f.flush()
        f.close()