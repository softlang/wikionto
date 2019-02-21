from check.abstract_check import ArtdictCheck
from mine.dbpedia import get_all_templates
from mine.dbpedia import to_uri
from mine.wiki import wiki_request


def chunk(l, n):
    chunks = []
    for i in range(0, len(l), n):
        chunks.append(l[i:i + n])
    return chunks


class IdentifyStubs(ArtdictCheck):

    def check(self, articledict):
        qresult = get_all_templates(root=to_uri("Category:Formal_languages"))
        qresult.update(get_all_templates(root=to_uri("Category:Computer_file_formats")))
        for a in articledict:
            articledict[a]["IsStub"] = 0
        for title, templates in qresult.items():
            if title in articledict and any("-stub" in t.lower() for t in templates):
                articledict[title]["IsStub"] = 1
        return articledict


class IdentifyStubsWikiApi(ArtdictCheck):

    def check(self, articledict):
        for a in articledict:
            articledict[a]["IsStub"] = 0

        titles = list(articledict.keys())
        print(len(titles))
        titlechunks = chunk(titles, 1)
        for titlechunk in titlechunks:
            titlesstring = '|'.join(titlechunk)

            params = {
                "titles": titlesstring,
                "prop": "templates",
                "tllimit": 500,
                "tlnamespace": 10
            }
            response = wiki_request(params)

            if "continue" in response:
                print("continue...")
            normalized = {}
            if "normalized" in response["query"]:
                normalized = {normentry["to"]: normentry["from"] for normentry in response["query"]["normalized"]}

            for pageentry in response["query"]["pages"]:
                title = pageentry["title"]
                if title in normalized:
                    title = normalized[title]
                if "templates" not in pageentry:
                    continue
                for templateentry in pageentry["templates"]:
                    if "-stub" in templateentry["title"].lower():
                        articledict[title]["IsStub"] = 1

        return articledict


if __name__ == '__main__':
    IdentifyStubs().solo()
