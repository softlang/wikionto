from check.abstract_check import ArtdictCheck
from data import wikidata_articles

# This check depends on extracting the Wikidata ID
class Wikidata(ArtdictCheck):

    def check(self, articledict):
        print("Checking instance of 'Computer languages' and 'data formats' in Wikidata")
        wikidataset = wikidata_articles()
        for title in articledict:
            if "wikidataid" in articledict[title]:
                qitem = articledict[title]["wikidataid"]
            articledict[title]["wikidata_CL"] = int(qitem in wikidataset)
        return articledict


if __name__ == '__main__':
    Wikidata().solo()
