from check.abstract_check import ArtdictCheck


class ExtractURLWords(ArtdictCheck):

    def check(self, articledict):
        for a in articledict:
            urlwords = []
            if '(' in a:
                urlwords = [word.lower() for word in a.split('(')[1].split(')')[0].split('_')]
            articledict[a]["URL_Braces_Words"] = urlwords
        return articledict


if __name__ == '__main__':
    ExtractURLWords().solo()
