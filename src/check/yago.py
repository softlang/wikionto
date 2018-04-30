from check.langdictcheck import LangdictCheck
from mine.yago import get_artificial_languages


class Yago(LangdictCheck):

    def check(self, langdict):
        print("Checking instance of 'Artificial language' in yago")
        als = get_artificial_languages()
        for cl in langdict:
            langdict[cl]["yago_CL"] = int(cl in als)
        return langdict


if __name__ == "__main__":
    Yago().solo()
