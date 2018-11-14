from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist
from data import DATAP
from json import load


f = open(DATAP + '/articledict.json', 'r', encoding="UTF8")
langdict = load(f)
f.close()

text = " "
for cl in langdict:
    if ("GitSeed" in langdict[cl] and langdict[cl]["GitSeed"] == 1) \
            or ("TIOBE" in langdict[cl] and langdict[cl]["TIOBE"] == 1):
        text += langdict[cl]["Summary"] + " "

# stopwords
stop_words = set(stopwords.words('english'))
stop_words |= {',', '.', ';', '*', '-', '_', ':', "''", '#', '``'}
words = [w for s in sent_tokenize(text) for w in word_tokenize(s) if w.lower() not in stop_words]

# stem
stemmer = SnowballStemmer("english", ignore_stopwords=True)
words = list(map(lambda w: stemmer.stem(w), words))

# freq distribution
words_freq = FreqDist(words)
for w,f in words_freq.most_common(100):
    print(w+":"+str(f))