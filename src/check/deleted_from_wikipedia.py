from check.abstract_check import ArtdictCheck
from data import DATAP
from json import load
from mine.wiki import wiki_request


def chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class IdentifyDeletedFromWikipedia(ArtdictCheck):

    def check(self, articledict):
        titles = set(articledict.keys())

        with open(DATAP + "/dump/article_ids_reverse.json", "r") as f:
            title_to_id = load(f)

        valid_titles = set(t for t in title_to_id.keys())
        invalid_titles = titles - valid_titles

        for a in articledict:
            articledict[a]["DeletedFromWikipedia"] = int(a in invalid_titles)
        return articledict


class IdentifyDeletedFromWikipedia2(ArtdictCheck):

    def check(self, articledict):
        titles = list(articledict.keys())

        titlechunks = chunk(titles, 50)
        for titlechunk in titlechunks:
            titlesstring = '|'.join(titlechunk)

            params = {
                "titles": titlesstring,
            }
            response = wiki_request(params)

            normalized = {}
            if "normalized" in response["query"]:
                normalized = {normentry["to"]: normentry["from"] for normentry in response["query"]["normalized"]}
            results = response["query"]["pages"]
            for result in results:
                title = result["title"]
                if title in normalized:
                    title = normalized[title]
                articledict[title]["DeletedFromWikipedia2"] = int("missing" in result)

        return articledict


if __name__ == '__main__':
    IdentifyDeletedFromWikipedia2().solo()
