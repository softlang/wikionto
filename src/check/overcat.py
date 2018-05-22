from check.langdictcheck import LangdictCheck


class OverCat(LangdictCheck):

    def check(self,langdict):
        print("Annotating number of categories")
        for cl in langdict:
            langdict[cl]["#Cats"] = len(langdict[cl]["cats"])
        return langdict


if __name__ == '__main__':
    OverCat().solo()
