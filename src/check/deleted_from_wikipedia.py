from check.abstract_check import ArtdictCheck
from data import DATAP
from json import load

class IdentifyDeletedFromWikipedia(ArtdictCheck):

    def check(self, articledict):
        titles = set(articledict.keys())

        with open(DATAP+"/dump/article_ids_reverse.json", "r") as f:
            title_to_id = load(f)

        valid_titles = set(t for t in title_to_id.keys())
        invalid_titles = titles - valid_titles

        for it in invalid_titles:
            articledict[it]["DeletedFromWikipedia"] = 1
        return articledict

class DeleteNonExistentPages(ArtdictCheck):
    def check(self, articledict):
        invalid = [a for a in articledict if "DeletedFromWikipedia" in articledict[a]]
        for i in invalid:
            if "DeletedFromWikipedia" in articledict[i] and articledict[i]["DeletedFromWikipedia"]:
                del articledict[i]
        return articledict


if __name__ == '__main__':
    DeleteNonExistentPages().solo()
