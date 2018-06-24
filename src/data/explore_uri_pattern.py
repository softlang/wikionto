from data import DATAP
from json import load
import operator


def words_in_titles(name, seed=True):
    f = open(DATAP + '/' + name + '.json', 'r', encoding="UTF8")
    langdict = load(f)
    pattern_freq = dict()
    for cl in langdict:
        if seed:
            if langdict[cl]["Seed"] == 0:
                continue
        text = cl
        words = text.split('_')
        for w in words:
            wn = w.replace('(', "").replace(')', '')
            if wn in pattern_freq:
                pattern_freq[wn] += 1
            else:
                pattern_freq[wn] = 1
    sorted_x = sorted(pattern_freq.items(), key=operator.itemgetter(1))
    for cl, v in sorted_x:
        print(cl + ', ' + str(v))


def tags_in_titles_braces(name, seed=True):
    f = open(DATAP + '/' + name + '.json', 'r', encoding="UTF8")
    langdict = load(f)
    pattern_freq = dict()
    for cl in langdict:
        if '(' not in cl:
            continue
        if seed:
            if langdict[cl]["Seed"] == 0:
                continue
        tag = cl.split('(')[1].split(')')[0]
        if tag in pattern_freq:
            pattern_freq[tag] += 1
        else:
            pattern_freq[tag] = 1
    sorted_x = sorted(pattern_freq.items(), key=operator.itemgetter(1))
    for cl, v in sorted_x:
        print(cl + ', ' + str(v))


def words_in_tags_in_titles_braces(name, seed=True):
    f = open(DATAP + '/' + name + '.json', 'r', encoding="UTF8")
    langdict = load(f)
    pattern_freq = dict()
    for cl in langdict:
        if '(' not in cl:
            continue
        if seed:
            if langdict[cl]["Seed"] == 0:
                continue
        tag = cl.split('(')[1].split(')')[0]
        tags = tag.split('_')
        for t in tags:
            if t in pattern_freq:
                pattern_freq[t] += 1
            else:
                pattern_freq[t] = 1
    sorted_x = sorted(pattern_freq.items(), key=operator.itemgetter(1))
    for cl, v in sorted_x:
        print(cl + ', ' + str(v))


if __name__ == '__main__':
    tags_in_titles_braces('langdict')
