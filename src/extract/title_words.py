def extract_title_words(langdict):
    print("Extracting title words")
    for cl in langdict:
        for w in __get_title_words(cl):
            langdict[cl]["title_word_"+w] = 1
    return langdict


def __get_title_words(title):
    return list(map(lambda w: w.replace('(', "").replace(')', ''), title.split('_')))
