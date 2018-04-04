from multiprocessing.pool import Pool

from mine.wiki import getcontent


def get_text(clrev):
    return clrev[0], getcontent(clrev[1])


def check_multi_infobox(langdict):
    print("Checking for multiple infoboxes")
    pool = Pool(processes=20)
    clrevs = []
    for cl in langdict:
        rev = langdict[cl]["Revision"].split('oldid=')[1].strip()
        clrevs.append((cl, rev))
    cltexts = dict(pool.map(get_text, clrevs))
    for cl in langdict:
        text = cltexts[cl]
        if text is None:
            langdict[cl]["MultiInfobox"] = 0
            langdict[cl]["Infobox programming language"] = 0
            langdict[cl]["Infobox software"] = 0
        else:
            nr = text.count("{{Infobox")
            pl_box = 'Infobox programming language' in text
            soft_box = 'Infobox software' in text
            langdict[cl]["MultiInfobox"] = nr
            langdict[cl]["Infobox programming language"] = int(pl_box)
            langdict[cl]["Infobox software"] = int(soft_box)
    return langdict
