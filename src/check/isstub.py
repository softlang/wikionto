from check.abstract_check import ArtdictCheck
from mine.dbpedia import get_all_templates
from mine.dbpedia import to_uri


class IdentifyStubs(ArtdictCheck):

    def check(self, articledict):
        qresult = get_all_templates(root=to_uri("Category:Formal_languages"))
        qresult.update(get_all_templates(root=to_uri("Category:Computer_file_formats")))
        for a in articledict:
            articledict[a]["IsStub"] = 0
        for title, templates in qresult.items():
            if title in articledict and any("stub" in t.lower() for t in templates):
                articledict[title]["IsStub"] = 1
        return articledict


class DeleteStubPages(ArtdictCheck):
    def check(self, articledict):
        invalid = [a for a in articledict if articledict[a]["IsStub"]]
        for i in invalid:
            del articledict[i]
        return articledict


if __name__ == '__main__':
    IdentifyStubs().solo()
