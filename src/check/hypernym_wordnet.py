from nltk.corpus import wordnet
from nltk import download
import re
from check.langdictcheck import LangdictCheck


class WordNet(LangdictCheck):

    def check(self,langdict):
        print("Checking Wordnet Hypernym")
        for cl in langdict:
            langdict[cl]["WordnetHypernym"] = self.is_hyponym(cl)
        return langdict

    def is_hyponym(self,cl):
        cl = self.namenorm(cl)
        for syn in wordnet.synsets(cl):
            for hyp in syn.hypernyms():
                if('language' in str(hyp))|('format' in str(hyp))|('dsl' in str(hyp))|('dialect' in str(hyp)):
                    return 1
        return 0

    def namenorm(self,name):
        x = re.sub("\(.*?\)", "", name).lower().strip()
        x = re.sub("[_]","",x).strip()
        return x


if __name__ == '__main__':
    download('wordnet')
    WordNet().solo()
