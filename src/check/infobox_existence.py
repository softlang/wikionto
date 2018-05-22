from multiprocessing.pool import Pool
from mine.wiki import getcontent
from check.langdictcheck import LangdictCheck


class InfoboxEx(LangdictCheck):

    def get_text(self,clrev):
        return clrev[0], getcontent(clrev[1])

    def check(self,langdict):
        print("Checking for infobox existence")
        pool = Pool(processes=100)
        clrevs = []
        for cl in langdict:
            rev = langdict[cl]["Revision"].split('oldid=')[1].strip()
            clrevs.append((cl, rev))
        cltexts = dict(pool.map(self.get_text, clrevs))
        for cl in langdict:
            text = cltexts[cl]
            if text is None:
                langdict[cl]["MultiInfobox"] = -1
                langdict[cl]["Infobox programming language"] = -1
                langdict[cl]["Infobox software"] = -1
                langdict[cl]["Infobox file format"] = -1
            else:
                if 'infobox programming language' in text.lower():
                    langdict[cl]["Infobox programming language"] = text.lower().index('infobox programming language')
                else:
                    langdict[cl]["Infobox programming language"] = -1
                if 'infobox software' in text.lower():
                    langdict[cl]["Infobox software"] = text.lower().index('infobox software')
                else:
                    langdict[cl]["Infobox software"] = -1
                if 'infobox file format' in text.lower():
                    langdict[cl]["Infobox file format"] = text.lower().index('infobox file format')
                else:
                    langdict[cl]["Infobox file format"] = -1
                langdict[cl]["MultiInfobox"] = text.lower().count("{{infobox")
        return langdict


if __name__ == "__main__":
    InfoboxEx().solo()
