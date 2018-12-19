from check.abstract_check import ArtdictCheck
from mine.wiki import getlinks
from multiprocessing import Pool


class WikiList(ArtdictCheck):
    def check(self, articledict):
        print("Checking Wikipedia's lists")

        list_articles = []
        for article in articledict:
            articledict[article]['Wikipedia_Lists'] = []
            articledict[article]["IsList"] = 0
            if "List_of" or "Comparison_of" in article:
                list_articles.append(article)
                articledict[article]["IsList"] = 1

        pool = Pool(processes=30)
        linkdict = pool.map(get_linked_articles, list_articles)
        linkdict = dict(linkdict)

        for list_article, articles in linkdict.items():
            if article is None:
                continue
            articles_norm = [link.replace(' ', '_') for link in articles]
            for article in articles_norm:
                if article in articledict:
                    articledict[article]['Wikipedia_List_Indicator'] = 1
                    articledict[article]['Wikipedia_Lists'].append(list_article)
        return articledict


def get_linked_articles(list_article):
    links = getlinks(list_article)
    return list_article, links


if __name__ == "__main__":
    WikiList().solo()

