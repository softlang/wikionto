from check.abstract_check import ArtdictCheck
from data import LIST_ARTICLES
from mine.wiki import getlinks


class WikiList(ArtdictCheck):
    def check(self, articledict):
        print("Checking Wikipedia's lists")
        for title in articledict:
            articledict[title]['In_Wikipedia_List'] = 0
            articledict[title]['Wikipedia_Lists'] = []
        for list_article in LIST_ARTICLES:
            links = getlinks(list_article)
            for link in links:
                link_norm = link.replace(' ', '_')
                if link_norm in articledict:
                    articledict[link_norm]['In_Wikipedia_List'] = 1
                    articledict[link_norm]['Wikipedia_Lists'].append(list_article)
        return articledict


if __name__ == "__main__":
    WikiList().solo()
