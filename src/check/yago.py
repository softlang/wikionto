from check.abstract_check import ArtdictCheck
from data import yago_articles


# This check depends on extracting the Wikidata ID
class Yago(ArtdictCheck):

    def check(self, articledict):
        print("Checking instance of 'Artificial language' in yago")
        yago = yago_articles()
        for title in articledict:
            articledict[title]["yago"] = int(title in yago)
        return articledict


if __name__ == "__main__":
    Yago().solo()
