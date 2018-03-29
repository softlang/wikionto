keywords = ['language','format','dsl','dialect']
def check_summary_for_keywords(langdict):
    for cl in langdict:
        summary = langdict[cl]["Summary"]
        if any(word in summary.lower() for word in keywords):
            langdict[cl]["PlainTextKeyword"] = 1
        else:
            langdict[cl]["PlainTextKeyword"] = 0
    return langdict
