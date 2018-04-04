from mine.wiki import getcontent


def check_multi_infobox(langdict):
    print("Checking for multiple infoboxes")
    for cl in langdict:
        rev = langdict[cl]["Revision"].split('oldid=')[1].strip()
        text = getcontent(rev)
        nr = text.count("{{Infobox")
        pl_box = 'Infobox programming language' in text
        soft_box = 'Infobox software' in text
        langdict[cl]["MultiInfobox"] = nr
        langdict[cl]["Infobox programming language"] = int(pl_box)
        langdict[cl]["Infobox software"] = int(soft_box)
    return langdict
