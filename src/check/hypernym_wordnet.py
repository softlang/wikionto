from nltk.corpus import wordnet
from nltk import download
import re
from check.abstract_check import ArtdictCheck


class WordNet(ArtdictCheck):

    def check(self, artdict):
        print("Checking Wordnet Hypernym")
        for a in artdict:
            artdict[a]["WordnetHypernym"] = self.is_hyponym(a)
        return artdict

    def is_hyponym(self, title):
        title = self.namenorm(title)
        for syn in wordnet.synsets(title):
            for hyp in syn.hypernyms():
                if ('language' in str(hyp)) | ('format' in str(hyp)) | ('dsl' in str(hyp)) | ('dialect' in str(hyp)):
                    return 1
        return 0

    def namenorm(self, name):
        x = re.sub("\(.*?\)", "", name).lower().strip()
        x = re.sub("[_]", " ", x).strip()
        return x


if __name__ == '__main__':
    download('wordnet')
    WordNet().solo()
