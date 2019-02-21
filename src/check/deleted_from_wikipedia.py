from check.abstract_check import ArtdictCheck
from mine.wiki import wiki_request


def chunk(l, n):
    chunks = []
    for i in range(0, len(l), n):
        chunks.append(l[i:i + n])
    return chunks


class IdentifyDeletedFromWikipedia(ArtdictCheck):

    def check(self, articledict):
        print("Checking for deleted articles on Wikipedia")

        for a in articledict:
            articledict[a]["DeletedFromWikipedia"] = 0
            articledict[a]["NotStandalone"] = 0

        titles = list(articledict.keys())
        print(len(titles))
        titlechunks = chunk(titles, 50)
        c = 0
        for titlechunk in titlechunks:
            print("Sending Chunk " + str(c))
            c += 1
            titlesstring = '|'.join(titlechunk)

            params = {
                "titles": titlesstring,
                "redirects": ""
            }
            response = wiki_request(params)

            normalized = {}
            if "normalized" in response["query"]:
                normalized = {normentry["to"]: normentry["from"] for normentry in response["query"]["normalized"]}

            # corner case, where deleted article becomes subsection
            if "redirects" in response["query"]:
                for redirect in response["query"]["redirects"]:
                    if "tofragment" in redirect:
                        title = redirect["from"]
                        if title in normalized:
                            title = normalized[title]
                        articledict[title]["NotStandalone"] = 1

            results = response["query"]["pages"]
            for result in results:
                title = result["title"]
                if title in normalized:
                    title = normalized[title]
                if title in titlechunk:
                    articledict[title]["DeletedFromWikipedia"] = int("missing" in result)

        return articledict


if __name__ == '__main__':
    IdentifyDeletedFromWikipedia().solo()
