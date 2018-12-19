from check.abstract_check import ArtdictCheck
from mine.wiki import getlinks
from multiprocessing import Pool


class DeletedFromWikipedia(ArtdictCheck):

    def check(self, articledict):
        titles = articledict.keys()
        checked = Pool(20).map(self.check_single, titles)
        for title, value in checked:
            articledict[title]["DeletedFromWikipedia"] = int(value)
        return articledict

    def check_single(self, title):
        content = getlinks(title)
        return title, bool(content)


if __name__ == '__main__':
    DeletedFromWikipedia().solo()
