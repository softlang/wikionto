from data import DATAP
from json import load, dump
import operator

def compute_pattern_freq():
    f = open(DATAP + '/langdict.json', 'r', encoding="UTF8")
    langdict = load(f)
    pattern_freq = dict()
    for cl in langdict:
        if '(' not in cl:
            continue
        tag = cl.split('(')[1].split(')')[0]
        tags = tag.split('_')
        for t in tags:
            if t in pattern_freq:
                pattern_freq[t] += 1
            else:
                pattern_freq[t] = 1
    sorted_x = sorted(pattern_freq.items(), key=operator.itemgetter(1))
    for cl,v in sorted_x:
        print(cl + ' ' + str(v))

if __name__ == '__main__':
    compute_pattern_freq()