from check.abstract_check import ArtdictCheck


class SeedWordSetSim(ArtdictCheck):

    def check(self, articledict):
        print("Annotating similarity to seed sentences")

        seedwordlists = list(articledict[cl]["words"] for cl in articledict
                             if "words" in articledict[cl] and articledict[cl]["Seed"] == 1)

        i = 0
        for title in articledict:
            i += 1
            if "words" not in articledict[title] or articledict[title]["Seed"] == 1:
                continue
            words = set(articledict[title]["words"])
            if not words:
                continue
            sims = map(lambda wordlist: len(set(wordlist) & set(words)), seedwordlists)
            articledict[title]["WordSetSim"] = max(sims)
            if i % 1000 == 0:
                print(str(i) + "/" + str(len(articledict.items())))
        return articledict


if __name__ == '__main__':
    SeedWordSetSim().solo()
