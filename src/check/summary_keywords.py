keywords = ['language','format']


def check_summary_for_keywords(langdict):
    print("Checking summary for keywords")
    for cl in langdict:
        summary = langdict[cl]["Summary"]
        if any(word in summary.lower() for word in keywords):
            langdict[cl]["PlainTextKeyword"] = 1
        else:
            langdict[cl]["PlainTextKeyword"] = 0
    return langdict
