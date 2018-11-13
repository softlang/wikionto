from multiprocessing.pool import Pool
from mine.wiki import getcontent
from check.abstract_check import ArtdictCheck


class InfoboxPosition(ArtdictCheck):

    def get_text(self, rev):
        return rev[0], getcontent(rev[1])

    #TODO: Generalize to list of infoboxes
    def check(self, artdict):
        print("Checking for infobox existence")
        pool = Pool(processes=100)
        revs = []
        for a in artdict:
            rev = artdict[a]["Revision"].split('oldid=')[1].strip()
            revs.append((a, rev))
        texts = dict(pool.map(self.get_text, revs))
        for a in artdict:
            text = texts[a]
            if text is None:
                artdict[a]["MultiInfobox"] = 0
                artdict[a]["Infobox programming language"] = -1
                artdict[a]["Infobox software"] = -1
                artdict[a]["Infobox file format"] = -1
            else:
                if 'infobox programming language' in text.lower():
                    artdict[a]["Infobox programming language"] = text.lower().index('infobox programming language')
                else:
                    artdict[a]["Infobox programming language"] = -1
                if 'infobox software' in text.lower():
                    artdict[a]["Infobox software"] = text.lower().index('infobox software')
                else:
                    artdict[a]["Infobox software"] = -1
                if 'infobox file format' in text.lower():
                    artdict[a]["Infobox file format"] = text.lower().index('infobox file format')
                else:
                    artdict[a]["Infobox file format"] = -1
                artdict[a]["MultiInfobox"] = text.lower().count("{{infobox")
        return artdict


if __name__ == "__main__":
    InfoboxPosition().solo()
